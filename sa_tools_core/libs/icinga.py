# coding: utf-8

import logging

from icinga2_api.api import Api

from sa_tools_core.consts import ICINGA_CACERT
from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)

icinga_api = None


class IcingaClusterConfig(object):
    """you need to inhert IcingaClusterConfig and impl your own config class
    and specify your class path in sa_tools_core.consts.ICINGA_CLUSTER_CONFIG_CLASS
    """
    @classmethod
    def get_ack_link(cls, env):
        return ''

    @classmethod
    def get_reboot_host_link(cls, env):
        return ''

    @classmethod
    def get_icinga_link(cls, env):
        return ''

    @classmethod
    def get_icinga_hosts(cls):
        return []


class IcingaApi(object):
    def __init__(self, icinga_hosts, icinga_auth, icinga_cacert):
        self.api = Api(icinga_hosts,
                       icinga_auth,
                       icinga_cacert)
        self._filters = []

    def _filter(self, name, value, regex=False, wildcard=False, negation=False, operator='=='):
        if not value:
            return
        value = '"%s"' % value
        filter_ = ''
        if regex:
            filter_ = 'regex(%s, %s)' % (value, name)
        elif wildcard:
            filter_ = 'match(%s, %s)' % (value, name)
        else:
            filter_ = '%s %s %s' % (name, operator, value)
        if negation:
            filter_ = '! (%s)' % filter_
        self._filters.append(filter_)
        return filter_

    @property
    def filter(self):
        return ' && '.join(self._filters)

    def clear_filters(self):
        self._filters = []

    def acknowledge(self, host, service=None, author='anonymous', comment='ack by sa-icinga',
                    remove=False, notify=False):
        type_ = 'Service' if service else 'Host'
        self.clear_filters()
        if host and '*' in host:
            self._filter('host.name', host, wildcard=True)
        else:
            self._filter('host.name', host)
        if service and '*' in service:
            self._filter('service.name', service, wildcard=True)
        else:
            self._filter('service.name', service)

        params = dict(filter=self.filter,
                      type=type_)
        if not remove:
            action = 'acknowledge-problem'
            params['author'] = author
            params['comment'] = comment
        else:
            action = 'remove-acknowledgement'
        if notify:
            params['notify'] = notify

        res = (self.api
               .actions.url(action)
               .post(**params))
        results = res.get('results')
        if results and int(results[0].get('code')) == 200:
            return True, res
        else:
            return False, res


def get_icinga_api(icinga_cluster_config):
    global icinga_api
    if icinga_api is None:
        api_user, passwd = get_config('icinga').split(':')
        ICINGA_AUTH = (api_user, passwd)
        icinga_api = IcingaApi(icinga_cluster_config.get_icinga_hosts(),
                               ICINGA_AUTH,
                               ICINGA_CACERT)
    return icinga_api
