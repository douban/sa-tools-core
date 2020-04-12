# coding: utf-8

import re
import sys
import json
import pkgutil
import logging
import argparse
import importlib
from collections import defaultdict, namedtuple

from sa_tools_core.consts import (
    # BS_CMD_PATTERN,
    # BS_DEFAULT_ATTRS,
    # BS_DEFAULT_PARAMS,
    # BS_DEFAULT_PARAMS_BM,
    # BS_PLURAL_SUFFIX,
    TENCENT_DEFAULT_REGIN,)
from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)

tencent_config_func = lambda: get_config('tencent')  # NOQA

ServiceClient = namedtuple('ServiceClient', ['service', 'version', 'cls'])

RE_PARAM = re.compile(r'^:(param|type)\ (\w+):\ (.*)$')
PARAM_TYPES = {
    'str': str,
    'int': int,
    'bool': bool,
}
SPECIAL_PARAM_TYPES = [
    'Filter',
    'Tag',
]


def simplify_action(action):
    action = action.replace('Get', '') \
        .replace('Describe', '') \
        .replace('Description', '') \
        .replace('UnBind', 'Unbind') \
        .replace('LoadBalancer', 'Lb') \
        .replace('Ex', '') \
        .replace('Query', '')

    action = ''.join(['_%s' % c.lower() if c.isupper() else c for c in action])[1:]
    return action


def simplify_param(param):
    return ''.join(['_%s' % c.lower() if c.isupper() else c for c in param])[1:]


def add_common_args(parser):
    parser.add_argument('-r', '--raw', action='store_true', help='raw output.')
    parser.add_argument('-j', '--json', action='store_true', help='json format output.')
    # parser.add_argument(
    #     '-a',
    #     '--attrs',
    #     nargs='*',
    #     default=list(BS_DEFAULT_ATTRS),
    #     help='the attrs that should be output. (default: %(default)s)')
    # parser.add_argument('-e', '--extra-attrs', nargs='*', help='the extra-attrs that should be output.')
    parser.add_argument('-s', '--sep', default=', ', help='separator, (default: %(default)s)')


def extract_params(doc_str, models):
    '''
    extract params from doc string
    '''
    params = defaultdict(dict)
    last_pname = ''
    for line in doc_str.splitlines():
        # NOTE:(everpcpc) for multiline doc
        if (not line.startswith(" ")) and last_pname:
            params[last_pname]['desc'] += line

        m = RE_PARAM.match(line.strip())
        if not m:
            continue
        pname = simplify_param(m.group(2))
        last_pname = pname
        params[pname]['name'] = m.group(2)
        if m.group(1) == 'param':
            params[pname]['desc'] = m.group(3)
        elif m.group(1) == 'type':
            t = m.group(3)
            if t.startswith('list of '):
                params[pname]['multi'] = True
                t = t[len('list of '):]
            if t in SPECIAL_PARAM_TYPES:
                params[pname]['type'] = getattr(models, t)
            else:
                _t = PARAM_TYPES.get(t, None)
                if _t:
                    params[pname]['type'] = _t
                else:
                    raise Exception(f'unkown param type {t} => {line.strip()}')
    return params


def translate_param(parser, param, info):
    '''
    translate param into parser
    '''
    param_name = param.replace('_', '-')
    kw = {'help': info['desc']}
    if info.get('multi', False):
        kw['nargs'] = '*'
    if info['type'] in PARAM_TYPES.values():
        if info['type'] == bool:
            kw['action'] = 'store_true'
        elif info['type'] == int:
            kw['type'] = int
        parser.add_argument(f'--{param_name}', **kw)
        return
    # param type in sdk
    if info['name'] in SPECIAL_PARAM_TYPES:
        pass
    else:
        # TODO:(everpcpc)
        raise Exception(f'param: {info["name"]} => {info["type"]} not supported now')
    parser.add_argument(f'--{param_name}', **kw)


def _execute(req_cls, cli_cls, action, params):
    from tencentcloud.common import credential
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.profile.client_profile import ClientProfile

    _id, _key = tencent_config_func().split(':')
    cred = credential.Credential(_id, _key)
    profile = ClientProfile(httpProfile=HttpProfile())
    client = cli_cls(cred, TENCENT_DEFAULT_REGIN, profile)

    req = req_cls()
    req.from_json_string(json.dumps(params))
    return getattr(client, action)(req)


def execute_action(client, action, argv):
    models = importlib.import_module(f'tencentcloud.{client.service}.{client.version}.models')
    request_cls = getattr(models, f'{action}Request')
    # NOTE:(everpcpc) extract params with action request document
    params = extract_params(request_cls.__init__.__doc__, models)

    parser = argparse.ArgumentParser()
    add_common_args(parser)

    for param, info in params.items():
        translate_param(parser, param, info)

    args = parser.parse_args(argv)

    req_params = dict()
    for param, info in params.items():
        a = getattr(args, param, None)
        if a is not None:
            req_params[info['name']] = a

    ret = _execute(request_cls, client.cls, action, req_params)
    print(ret)


def find_service_version(service):
    service_mod = importlib.import_module(f'tencentcloud.{service}')
    for m in pkgutil.iter_modules(service_mod.__path__):
        if m.ispkg:
            return m.name


def execute_service(service, argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Subcommands', dest='action')
    subparsers.required = True

    version = find_service_version(service)
    if not version:
        raise Exception(f"module not found for {service}")

    mapping = dict()
    client_mod = importlib.import_module(f'tencentcloud.{service}.{version}.{service}_client')
    client_cls = getattr(client_mod, f'{service.capitalize()}Client')

    for method in dir(client_cls):
        if not method[0].isupper():
            continue
        simple_action = simplify_action(method)
        mapping[simple_action] = method
        desc = getattr(client_cls, method).__doc__.split("\n\n")[0].strip()
        subparsers.add_parser(simple_action, help=desc)

    args = parser.parse_args(argv[:1])

    return execute_action(ServiceClient(service, version, client_cls), mapping[args.action], argv[1:])


def main():
    """
    e.g.

    """

    parser = argparse.ArgumentParser(epilog=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose.')

    subparsers = parser.add_subparsers(help='Services', dest='service')
    subparsers.required = True

    import tencentcloud
    for service in pkgutil.iter_modules(tencentcloud.__path__):
        if service.ispkg:
            subparsers.add_parser(service.name, help=f'service => {service.name}')

    args = parser.parse_args(sys.argv[1:2])

    level = logging.WARNING - args.verbose * 10
    logging.basicConfig(level=level, format='%(asctime)s %(name)s %(levelname)s %(message)s')

    sys.exit(execute_service(args.service, sys.argv[2:]))
