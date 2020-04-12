# coding: utf-8
'''
An ansible wrapper which makes ansible 2.x be compatible with ansible 1.9

refs:
    - https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
    - https://github.com/ansible/ansible/blob/1da5e21289d7407925190139165a9cd7a3f69960/examples/scripts/uptime.py
'''

from __future__ import absolute_import, print_function

import logging
import ansible

ansible_version = ansible.__version__.split('.')  # NOQA

# if ansible_version < (2, 0, 0):
#     import ansible.utils.template  # NOQA
#     from ansible import errors  # NOQA
#     from ansible.callbacks import DefaultRunnerCallbacks  # NOQA
#     from ansible.inventory import Inventory  # NOQA
#     from ansible.runner import Runner  # NOQA
# else:

from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.host import Host
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C  # NOQA

from sa_tools_core.consts import ANSIBLE_INVENTORY_CONFIG_PATH, ANSIBLE_MODULE_PATH

logger = logging.getLogger(__name__)

loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources=ANSIBLE_INVENTORY_CONFIG_PATH)

Inventory = lambda: inventory  # NOQA

# variable manager takes care of merging all the different sources
# to give you a unified view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)


class DefaultRunnerCallbacks(CallbackBase):
    '''
    make ansible 2.x Callback be compatible with ansible 1.9
    '''
    def __init__(self):
        self.results = {'contacted': {}, 'dark': {}}
        super(DefaultRunnerCallbacks, self).__init__()

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(DefaultRunnerCallbacks, self).v2_runner_on_failed(result, ignore_errors)
        host = result._host.get_name()
        self.results['contacted'][host] = result._result
        self.on_failed(host, result._result, ignore_errors)

    def v2_runner_on_ok(self, result):
        super(DefaultRunnerCallbacks, self).v2_runner_on_ok(result)
        host = result._host.get_name()
        self.results['contacted'][host] = result._result
        self.on_ok(host, result._result)

    def v2_runner_on_skipped(self, result):
        super(DefaultRunnerCallbacks, self).v2_runner_on_skipped(result)
        host = result._host.get_name()
        self.results['dark'][host] = result._result
        self.on_skipped(host, self._get_item_label(getattr(result._result, 'results', {})))

    def v2_runner_on_unreachable(self, result):
        super(DefaultRunnerCallbacks, self).v2_runner_on_unreachable(result)
        host = result._host.get_name()
        self.results['dark'][host] = result._result
        self.on_unreachable(host, result._result)

    def v2_playbook_on_no_hosts_matched(self):
        super(DefaultRunnerCallbacks, self).v2_playbook_on_no_hosts_matched()
        self.on_no_hosts()

    def on_failed(self, host, res, ignore_errors=False):
        pass

    def on_ok(self, host, res):
        pass

    def on_skipped(self, host, item=None):
        pass

    def on_unreachable(self, host, res):
        pass

    def on_no_hosts(self):
        pass


class Runner(object):
    def __init__(
        self,
        connection='ssh',
        module_path=None,  # ex: /usr/share/ansible
        module_name='shell',
        module_args=None,
        forks=C.DEFAULT_FORKS,  # parallelism level
        pattern=None,  # which hosts?  ex: 'all', 'acme.example.org'
        remote_user=C.DEFAULT_REMOTE_USER,  # ex: 'username'
        callbacks=None,  # used for output
        run_hosts=None,  # an optional list of pre-calculated hosts to run on, or host pattern
        become=False,  # whether to run privelege escalation or not
        become_method=C.DEFAULT_BECOME_METHOD,
    ):

        self.callback = callbacks

        # find hosts that match the pattern
        if not run_hosts:
            run_hosts = pattern

        if isinstance(run_hosts, list):
            run_hosts = [h.name if isinstance(h, Host) else h for h in run_hosts]

        # since the API is constructed for CLI it expects certain options to always be set in the context object
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            module_path=module_path or ANSIBLE_MODULE_PATH,
            forks=forks,
            become=become,
            become_method=become_method or 'sudo',
            check=False,
            diff=False,
            verbosity=0)
        self.forks = forks
        self.play = self._create_play(module_name, module_args, run_hosts)

    @classmethod
    def _create_play(cls, module_name, module_args, hosts):
        # create data structure that represents our play,
        # including tasks, this is basically what our YAML loader does internally.
        play_source = dict(
            name="Ansible Play",
            hosts=hosts,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=module_name, args=module_args)),
            ])

        # Create play object, playbook objects use .load instead of init or new methods,
        # this will also automatically create the task objects from the info provided in play_source
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        return play

    def run(self):
        # Run it - instantiate task queue manager,
        # which takes care of forking and setting up all objects to iterate over host list and tasks
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                passwords=dict(),
                stdout_callback=self.
                callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                forks=self.forks,
            )
            # most interesting data for a play is actually sent to the callback's methods
            _ = tqm.run(self.play)
        except Exception:
            raise
        finally:
            # we always need to cleanup child procs and the structures we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
            if loader:
                loader.cleanup_all_tmp_files()

        return self.callback.results
