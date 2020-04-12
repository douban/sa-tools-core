# coding: utf-8

from __future__ import print_function

import re
import cmd
import sys
import shlex
import string
import logging
import subprocess
from fnmatch import fnmatch
from argparse import ArgumentParser, FileType
from subprocess import Popen, PIPE
from multiprocessing import Value
from textwrap import TextWrapper
from operator import itemgetter

from progressbar import ProgressBar, Percentage, Timer, Bar
from terminaltables import AsciiTable

from sa_tools_core.libs.editor import Editor
from sa_tools_core.utils import reverse_func

from sa_tools_core.libs.ansible import DefaultRunnerCallbacks, Inventory, Runner

logger = logging.getLogger(__name__)

DEFAULT_FORKS = 20
RESULT_FIELDS = ('host', 'rc', 'stdout', 'stderr')
FIELDS_ORDER = ('host', 'stdout', 'stderr', 'rc')


def get_wrap():
    t_width = int(subprocess.check_output(['tput', 'cols']).strip())
    wrap_width = int(t_width / 3)
    return TextWrapper(width=wrap_width).wrap


class ScriptCLI(cmd.Cmd, object):
    PROMPT_TMPL = '(sa-script) {filters} $ '

    parser = ArgumentParser()

    parser.add_argument('host_pattern', metavar='<host-pattern>', nargs='?', help='host pattern that ansible takes')
    parser.add_argument('-f', '--file', type=FileType('r'), dest='script', default=sys.stdin, help='script file name')
    parser.add_argument('-u', '--user', metavar='REMOTE_USER', help='connect as this user')
    parser.add_argument(
        '-c', '--connection', metavar='CONNECTION', default='ssh', help='connection type to use (default=%(default)s)')
    parser.add_argument('-s', '--sudo', action='store_true', help='run operations with sudo')
    parser.add_argument('-F', '--forks', metavar='NUM', type=int, default=DEFAULT_FORKS, help='Level of parallelism')
    parser.add_argument(
        '-C',
        '--compatible',
        action='store_true',
        help='run in compatible mode, use ansible.runner instead of doa.runner as runner class')
    parser.add_argument('-r', '--retry', metavar='NUM', type=int, default=0, help='Retry NUM times(dark only)')
    parser.add_argument('-R', '--retry-failed', action='store_true', help='Also retry contacted_failed')
    parser.add_argument('--host', help='filter results match the host pattern')
    parser.add_argument('--rc', help='filter results match the rc pattern')
    parser.add_argument('--stdout', help='filter results match the stdout pattern')
    parser.add_argument('--stderr', help='filter results match the stderr pattern')
    parser.add_argument('-q', '--quit', action='store_true', help='quit after script execute')

    def __init__(self):
        super(ScriptCLI, self).__init__()
        self.filter_args = []
        self.mark = {}

        self.parser.usage = """
sa-script [-h] [-s] [-f NUM] [-r NUM] [-R] [--host HOST] [--rc RC]
                 [--stdout STDOUT] [--stderr STDERR] [-q]
                 <host-pattern> [script]"""

        args = self.parser.parse_args()
        if not args.host_pattern:
            self.parser.error('too few arguments')

        self.parser.usage = None

        try:
            self._run(args)
        except KeyboardInterrupt:
            sys.exit(2)
        except (ScriptEmptyError, NoHostsError) as e:
            print(e, file=sys.stderr)
            sys.exit(2)

        if args.script == sys.stdin and not args.script.isatty():
            args.quit = True

        if not args.quit:
            while True:
                try:
                    self.cmdloop()
                except KeyboardInterrupt:
                    self.onecmd('reset')
                    print()

    def postloop(self):
        sys.exit(0)

    def _run(self, args):
        self.runner = ScriptRunner(
            args.host_pattern,
            args.script,
            args.user,
            args.connection,
            args.sudo,
            args.retry,
            args.retry_failed,
            args.forks,
            args.compatible,
        )

        self.runner.run()

        if args.host:
            self.onecmd('host ' + args.host)
        if args.rc:
            self.onecmd('rc ' + args.rc)
        if args.stdout:
            self.onecmd('stdout ' + args.stdout)
        if args.host:
            self.onecmd('stderr ' + args.stderr)

        self.onecmd('reset')  # init prompt and mark
        self.onecmd('print')

    def do_run(self, line):
        try:
            args = self.parser.parse_args(shlex.split(line))
        except SystemExit:
            pass  # ArgumentParser will print error message
        else:
            args.host_pattern = args.host_pattern or ':'.join(self.mark)
            try:
                self._run(args)
            except KeyboardInterrupt:
                print('\nabort...')
            except (ScriptEmptyError, NoHostsError) as e:
                print(e, file=sys.stderr)

    def help_run(self):
        print(
            """
run new script and print result
================================
(sa-script) $ run [host-pattern] [script filename] [args]

    empty host-pattern will use last host-pattern

e.g.:
    (sa-script) $ run
    (sa-script) $ run all
    (sa-script) $ run all xxx.sh
              """)

    def do_host(self, line):
        self.marker('host', line)

    def help_host(self):
        print(self.get_filter_help('host'))

    def do_rc(self, line):
        self.marker('rc', line)

    def help_rc(self):
        print(self.get_filter_help('rc'))

    def do_stdout(self, line):
        self.marker('stdout', line)

    def help_stdout(self):
        print(self.get_filter_help('stdout'))

    def do_stderr(self, line):
        self.marker('stderr', line)

    def help_stderr(self):
        print(self.get_filter_help('stderr'))

    def do_reset(self, line):
        self.filter_args = []
        self.reset_mark()

    def help_reset(self):
        print('reset filter')

    def _output(self, data, cmd=None):
        if cmd:
            pipe = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            out, err = pipe.communicate(input=data)

            if out:
                print(out)
            if err:
                print(err, file=sys.stderr)
        else:
            print(data)

    def do_print(self, line):
        if '|' in line:
            fields, cmd = line.split('|', 1)
        else:
            fields = line
            cmd = None

        fields = fields.split()
        fields = fields or ['host', 'rc', 'stdout', 'stderr']

        if not all(field in RESULT_FIELDS for field in fields):
            print('no such fields, check your input', file=sys.stderr)
            return

        data = self.list_fields(*fields)

        if len(fields) > 1:
            header = [fields]
            table = AsciiTable(header + data)

            if not table.ok:
                # the table not fits within the terminal width
                wrap = get_wrap()
                data = [['\n'.join(wrap(i)) for i in item] for item in data]
                table = AsciiTable(header + data)

            data = table.table
        else:
            data = '\n'.join([item[0] for item in data])
            if not data.endswith('\n'):
                data += '\n'

        self._output(data, cmd)

    do_p = do_print

    def help_print(self):
        print(
            """
print marked results (and pipe to shell commands)
==================================================
(sa-script) $ print [filed] [| shell commands]

e.g.:
    (sa-script) $ print
    (sa-script) $ print stderr
    (sa-script) $ print | cat > dump
    (sa-script) $ print stdout | grep xxx | sed xxx | cat > dump
              """)

    help_p = help_print

    def do_exit(self, line):
        return True

    def help_exit(self):
        print('exit')

    def do_EOF(self, line):
        print()
        return True

    help_EOF = help_exit

    def emptyline(self):
        pass

    def reset_mark(self):
        self.mark = dict.fromkeys(self.runner.results.keys(), True)

    def marker(self, key, pattern):
        reverse = False
        if pattern.startswith('!'):
            reverse = True
            pattern = pattern[1:]

        if pattern.startswith(('~', '=')):
            op = pattern[0]
            pattern = pattern[1:]
        elif pattern:
            op = '~'
        else:
            op = ''

        pattern = pattern.strip()

        if op == '=':
            pred_func = lambda result: fnmatch(result.get(key), pattern)  # NOQA
        elif op == '~':
            pred_func = lambda result: re.search(pattern, result.get(key))  # NOQA
        else:
            # pattern is None or empty string
            pred_func = lambda result: result.get(key)  # NOQA

        if reverse:
            pred_func = reverse_func(pred_func)

        self.filter_args.append(
            '{key}{r}{op}{pattern}'.format(key=key, r='!' if reverse else '', op=op, pattern=pattern))

        try:
            self.mark = {
                host: True for host, result in self.runner.results.items() if self.mark.get(host) and pred_func(result)
            }
        except re.error as e:
            self.onecmd('reset')
            print(e, file=sys.stderr)

    def list_fields(self, *fields):
        marked_results = [self.runner.results.get(k) for k, v in self.mark.items() if v]

        rtn = [[result.get(field, '') for field in fields] for result in marked_results]

        for field in FIELDS_ORDER:
            if field in fields:
                rtn.sort(key=itemgetter(fields.index(field)))

        return rtn

    def get_filter_help(self, field):
        return """
filter {field} field
======================================
(sa-script) $ {field} [pattern]
    =<pattern> for wildcard filter.
    [~]<pattern> for regex filter.
    empty pattern for non empty filter""".format(field=field)

    @property
    def prompt(self):
        return self.PROMPT_TMPL.format(filters=' '.join(self.filter_args))


class ScriptRunnerCallbacks(DefaultRunnerCallbacks):
    def __init__(self, pbar):
        self.pbar = pbar
        self.counter = Value('i', 0)
        super(ScriptRunnerCallbacks, self).__init__()

    def on_failed(self, host, res, ignore_errors=False):
        self.update_pbar()

    def on_ok(self, host, res):
        self.update_pbar()

    def on_skipped(self, host, item=None):
        logger.warning('{host} skipped'.format(host=host))

    def on_unreachable(self, host, res):
        self.update_pbar()

    def on_no_hosts(self):
        print('no hosts matched\n', file=sys.stderr)

    def update_pbar(self):
        with self.counter.get_lock():
            self.counter.value += 1
            self.pbar.update(self.counter.value)


class ScriptEmptyError(Exception):
    def __str__(self):
        return 'the script you provide is empty'


class NoHostsError(Exception):
    def __str__(self):
        return 'no hosts matched'


class ScriptRunner(object):
    inventory = Inventory()
    editor = Editor(extension='.sh')

    def __init__(
        self,
        host_pattern,
        script=sys.stdin,
        user=None,
        connection='ssh',
        sudo=False,
        retry=0,
        retry_failed=False,
        forks=DEFAULT_FORKS,
        compatible=False,
    ):

        self.host_pattern = host_pattern

        if script == sys.stdin and script.isatty():
            self.script = self.editor.edit()
            print(self.script)
        else:
            self.script = script.read()

        self.script = ''.join([c for c in self.script if c in string.printable]) if self.script else ''

        if not self.script:
            raise ScriptEmptyError

        self.user = user
        self.connection = connection
        self.sudo = sudo
        self.max_retries = retry
        self.retry_failed = retry_failed
        self.forks = forks
        self.compatible = compatible

        self._results = None
        self.results_is_processed = False

    def _run(self, host_pattern):
        run_hosts = self.inventory.list_hosts(host_pattern)

        if not run_hosts:
            raise NoHostsError

        widgets = [Percentage(), Bar(), Timer()]
        pbar = ProgressBar(widgets=widgets, max_value=len(run_hosts))

        pbar.start()
        params = dict(
            module_name='shell',
            module_args=self.script,
            remote_user=self.user,
            connection=self.connection,
            become=self.sudo,
            callbacks=ScriptRunnerCallbacks(pbar),
            run_hosts=host_pattern,
            forks=self.forks)
        results = Runner(**params).run()
        pbar.finish()
        print()

        _results = results.get('contacted', {})
        _results.update(results.get('dark', {}))
        return _results

    def run(self):
        print('Executing...')

        self._results = self._run(self.host_pattern)

        self.retry()

    def retry(self):

        pred_failed = lambda result: result.get('rc', None) != 0  # NOQA
        pred_dark = lambda result: result.get('rc', None) is None  # NOQA

        pred_func = pred_failed if self.retry_failed else pred_dark

        for i in range(self.max_retries):
            need_retry = [host for host, result in self._results.items() if pred_func(result)]

            print('Retrying {}...'.format(i + 1))

            results = self._run(':'.join(need_retry))

            _results = results.get('contacted', {})
            _results.update(results.get('dark', {}))
            self._results.update(_results)

    @property
    def results(self):
        if not self.results_is_processed:
            for host, result in self._results.items():
                result.update({'host': host})
                result['rc'] = str(result.get('rc', ''))
                result['stdout'] = result.get('stdout', '')
                result['stderr'] = result.get('stderr', result.get('msg', '') + result.get('exception', ''))

            self.results_is_processed = True

        return self._results


def main():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(ch)

    ScriptCLI()
