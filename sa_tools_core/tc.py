# coding: utf-8

import os
import re
import sys
import json
import pkgutil
import logging
import argparse
import importlib
from html.parser import HTMLParser

import yaml
import inflection

from sa_tools_core.consts import TENCENT_DEFAULT_PARAMS, TENCENT_DEFAULT_REGIN

from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)

tencent_config_func = lambda: get_config('tencent')  # NOQA

RE_PARAM = re.compile(r'^:(param|type)\ (\w+):\ (.*)$')
COMMON_PARAM_TYPES = {
    'str': str,
    'int': int,
    'bool': bool,
}


class KVParamType:
    def __init__(self, kname, vname, multi_value=False):
        self.kname = kname
        self.vname = vname
        self.multi_value = multi_value

    def parse_value(self, arg):
        k, v = arg.split('=')
        return {self.kname: k, self.vname: v.split(',') if self.multi_value else v}

    @property
    def help_message(self):
        if self.multi_value:
            return f'\npattern: {self.kname}={self.vname},{self.vname}...'
        else:
            return f'\npattern: {self.kname}={self.vname}'


SPECIAL_PARAM_TYPES = {
    'Filter': KVParamType('Name', 'Values', True),
    'Tag': KVParamType('TagKey', 'TagValues', True),
    'DeviceAlias': KVParamType('InstanceId', 'Alias', False),
}

# TODO: deal with list of internal type
IGNORE_PARAM_TYPES = [
    'DataDisk',
    'TagSpecification',
]


def simplify_action(action):
    action = action.replace('Get', '') \
        .replace('Describe', '') \
        .replace('Description', '') \
        .replace('UnBind', 'Unbind') \
        .replace('LoadBalancer', 'Lb') \
        .replace('Ex', '') \
        .replace('Query', '')
    return inflection.underscore(action)


class HTMLFilter(HTMLParser):
    text = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.text += '\n-> '
        elif tag == 'br':
            self.text += '\n'
        elif tag == 'p':
            self.text += '\n'

    def handle_data(self, data):
        self.text += data


def cleanup_help_message(msg):
    f = HTMLFilter()
    f.feed(msg)
    return f.text.replace(r"%", r"%%").replace('\n\n', '\n')


class ServiceClient:
    def __init__(self, service, version, cls_):
        self.service = service
        self.version = version
        self.cls = cls_


class ParamInfo:
    def __init__(self, name):
        self.name = name
        self.type = None
        self.desc = None
        self.multi = False


def add_output_format_args(parser):
    parser.add_argument(
        '-f',
        '--format',
        default='plain',
        choices=('plain', 'json', 'yaml', 'raw'),
        help='output format, (default: %(default)s)',
    )
    parser.add_argument(
        '-s',
        '--sep',
        default=', ',
        help='separator, only apply in plain output format (default: %(default)s)',
    )
    parser.add_argument('-a', '--attrs', nargs='*', help='the attrs should only output')
    parser.add_argument('-e', '--excludes', nargs='*', help='the extra-attrs that should not output.')


def extract_params(doc_str, models):
    '''
    extract params from doc string
    '''
    params = dict()
    last_pname = ''
    for line in doc_str.splitlines():
        # NOTE:(everpcpc) for multiline doc
        if (not line.startswith(" ")) and last_pname:
            params[last_pname].desc += '\n' + line

        m = RE_PARAM.match(line.strip())
        if not m:
            continue
        last_pname = pname = inflection.underscore(m.group(2))
        pinfo = params.pop(pname, None) or ParamInfo(m.group(2))
        if m.group(1) == 'param':
            pinfo.desc = m.group(3)
        elif m.group(1) == 'type':
            t = m.group(3)
            if t.startswith('list of '):
                pinfo.multi = True
                t = t[len('list of '):]

            if t in COMMON_PARAM_TYPES:
                pinfo.type = COMMON_PARAM_TYPES[t]
            elif t in SPECIAL_PARAM_TYPES.keys():
                pinfo.type = getattr(models, t)
            # NOTE: deal with internal class
            elif t in IGNORE_PARAM_TYPES:
                continue
            elif t.startswith(':class:'):
                _mod, _t = t[len(':class:'):].strip('`').rsplit('.', 1)
                if _mod != models.__name__:
                    raise Exception(f'param type in other models: {line.strip()}')
                subparams = extract_params(getattr(models, _t).__init__.__doc__, models)
                pinfo.type = subparams
            else:
                raise Exception(f'unkown param type {t} => {line.strip()}')
        if pinfo:
            params[pname] = pinfo

    return params


def param2parser(parser, param, info):
    '''
    translate param into parser
    '''
    if isinstance(info.type, dict):
        for sp, si in info.type.items():
            param2parser(parser, f'{param}_{sp}', si)
        return

    kw = {'help': cleanup_help_message(info.desc)}
    tname = info.type.__name__
    if info.multi:
        kw['nargs'] = '*'
    if tname in COMMON_PARAM_TYPES.keys():
        if tname == 'bool':
            default_value = False
            if param in TENCENT_DEFAULT_PARAMS.keys():
                default_value = TENCENT_DEFAULT_PARAMS[param]
            elif '默认取值：TRUE' in info.desc:
                default_value = True

            if default_value:
                kw['action'] = 'store_false'
            else:
                kw['action'] = 'store_true'
            kw['help'] += ' (default: %(default)s)'

        else:
            if tname == 'int':
                kw['type'] = int

            if param in TENCENT_DEFAULT_PARAMS.keys():
                kw['default'] = TENCENT_DEFAULT_PARAMS[param]
                kw['help'] += ' (default: %(default)s)'
    # param type in sdk
    elif tname in SPECIAL_PARAM_TYPES.keys():
        kw['help'] += SPECIAL_PARAM_TYPES[tname].help_message
    else:
        # NOTE:(everpcpc) if raised, add support for it
        raise Exception(f'param: {info.name} => {info.type} not yet supported')
    parser.add_argument(f'--{inflection.dasherize(param)}', **kw)


def arg2param(arg, param, info):
    tname = info.type.__name__
    if tname in COMMON_PARAM_TYPES.keys():
        return arg
    elif tname in SPECIAL_PARAM_TYPES.keys():
        if info.multi:
            return [SPECIAL_PARAM_TYPES[tname].parse_value(a) for a in arg]
        return SPECIAL_PARAM_TYPES[tname].parse_value(arg)
    else:
        raise Exception(f'param {param} not supported: {info}')


def args2params(args, params, prefix=''):
    '''
    translate argument into request param
    '''
    req_params = dict()
    for param, info in params.items():
        if isinstance(info.type, dict):
            req_params[info.name] = args2params(args, info.type, prefix=f'{prefix}{param}_')
            continue

        arg = getattr(args, f'{prefix}{param}', None)
        if arg is not None:
            req_params[info.name] = arg2param(arg, param, info)

    return req_params


def simplify_output(output, oformat, sep=', ', attrs=(), excludes=()):
    data = json.loads(output)

    def _simplify(data):
        if isinstance(data, list):
            data = [_simplify(i) for i in data]
            if oformat == 'plain':
                data = '\n'.join(sorted(i for i in data))
        elif isinstance(data, dict):
            is_leaf = False
            # NOTE: rough leaf determination
            if not any(isinstance(v, (dict,)) for k, v in data.items()):
                is_leaf = True
            if any(isinstance(i, (dict,)) for k, v in data.items() if isinstance(v, list) for i in v):
                is_leaf = False

            if is_leaf:
                if attrs:
                    data = {k: v for k, v in data.items() if k in attrs}
                else:
                    data = {k: v for k, v in data.items() if k not in excludes}
                if oformat == 'plain':
                    data = sep.join([str(v) for k, v in data.items()])
            else:
                data = {k: _simplify(v) for k, v in data.items()} or data
                if oformat == 'plain':
                    data = '\n'.join([
                        ('%s' if idx % 2 else '>> %s') % i for p in data.items() for idx, i in enumerate(p)
                    ])
        return data

    return _simplify(data)


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

    parser = argparse.ArgumentParser(
        f'{os.path.basename(sys.argv[0])} {client.service} {action}',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_output_format_args(parser)

    for param, info in params.items():
        param2parser(parser, param, info)

    args = parser.parse_args(argv)

    req_params = args2params(args, params)

    ret = _execute(request_cls, client.cls, action, req_params)

    if args.format == 'raw':
        print(ret)
        return

    simplified = simplify_output(
        ret.to_json_string(),
        args.format,
        args.sep,
        args.attrs or (),
        args.excludes or (),
    )
    if args.format == 'plain':
        print(simplified)
    elif args.format == 'json':
        print(json.dumps(simplified, ensure_ascii=False, indent=2))
    elif args.format == 'yaml':
        print(yaml.dump(simplified, allow_unicode=True, indent=2))


def find_service_version(service):
    service_mod = importlib.import_module(f'tencentcloud.{service}')
    for m in pkgutil.iter_modules(service_mod.__path__):
        if m.ispkg:
            return m.name


def execute_service(service, argv):
    parser = argparse.ArgumentParser(
        f'{os.path.basename(sys.argv[0])} {service}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        subparsers.add_parser(simple_action, help=cleanup_help_message(desc))

    args = parser.parse_args(argv[:1])

    return execute_action(ServiceClient(service, version, client_cls), mapping[args.action], argv[1:])


def main():
    """
    e.g.

    sa-tc bm devices
    sa-tc bm devices -f yaml
    sa-tc bm devices --alias host
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

    # NOTE:(everpcpc) return code not parsed now
    sys.exit(execute_service(args.service, sys.argv[2:]))
