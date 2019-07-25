# coding: utf-8

from __future__ import print_function

import sys
import json
import logging
import argparse
import importlib
import subprocess
from functools import partial
from collections import defaultdict

from sa_tools_core.utils import get_os_username, jprint
from sa_tools_core.consts import (BS_API_REQUESTS_MODULE_PREFIX,
                                  BS_CMD_PATTERN,
                                  BS_DEFAULT_ATTRS,
                                  BS_DEFAULT_PARAMS,
                                  BS_DEFAULT_PARAMS_BM,
                                  BS_PLURAL_SUFFIX)

logger = logging.getLogger(__name__)

"""
参数输入处理规则
instanceId -> alias
subnetId -> subnetName -> cidrBlock
vpcId -> vpcName -> cidrBlock
eipId -> eipName -> eip
vpcIp == ip

复杂结构 params:
  list、dict
list params input, don't use json
  ip -> ipList, ips
  instanceId -> instanceIds
若 list 跟 dict 嵌套，将 list 抹掉: subnetSet
"""

# TODO: support Chinese help message (但 qcloudcli 跟这个文档并不完全对应)
# https://cloud.tencent.com/document/api/386/6632

action_mapping = defaultdict(dict)

# TODO: add PARAM_MAPPING for cvm
PARAM_MAPPING = {
    'instanceId': (['alias'], ['get_data_for_reduce', 'bm', 'list'],
                   lambda x: [i['instanceId'] for i in x[0].get('deviceList', []) if i['alias'] == x[1]['alias']][0],
                   ),
    'subnetId': (['subnetName'], ['get_data_for_reduce', 'bmvpc', 'subnet'],
                 lambda x: [i['subnetId'] for i in x[0] if i['subnetName'] == x[1]['subnetName']][0],
                 ),
    'unSubnetId': (['subnetName'], ['get_data_for_reduce', 'bmvpc', 'subnet'],
                   lambda x: [i['unSubnetId'] for i in x[0] if i['subnetName'] == x[1]['subnetName']][0],
                   ),
    'vpcId': (['vpcName'], ['get_data_for_reduce', 'bmvpc', 'list'],
              lambda x: [i['vpcId'] for i in x[0] if i['vpcName'] == x[1]['vpcName']][0],
              ),
    # NOTE: eips -> eipIds; --eip is not valid, will get all eips, but result will be fine if there're not many eips.
    #   we hack this in get_data_for_reduce.
    'eipId': (['eip'], ['get_data_for_reduce', 'bmeip', 'list'],
              lambda x: [i['eipId'] for i in x[0].get('eipSet', []) if i['eip'] == x[1]['eip']][0],
              ),

    'ipList': (['ip'], ['list2json']),
    'ips': (['ip'], ['list2json']),
    'instanceIds': (['instanceId'], ['list2json']),
    'eipIds': (['eipId'], ['list2json']),
    'eips': (['eip'], ['list2json']),
    'aliases': (['alias'], ['list2json']),

    'subnetSet': (['subnetName', 'cidrBlock'], ['list2json']),
}


def translate_param(args, param_key, new_params=None):
    logger.debug('translate_param(args=%s, param_key=%s, new_params=%s)', args, param_key, new_params)
    param_translate_rule = PARAM_MAPPING[param_key]

    # e.g. instanceIds -> instanceId -> alias
    if len(param_translate_rule[0]) == 1:
        intermediate_param_key = param_translate_rule[0][0]
        if intermediate_param_key in PARAM_MAPPING and getattr(args, intermediate_param_key) is None:
            _param_key = PARAM_MAPPING[intermediate_param_key][0][0]
            if isinstance(getattr(args, _param_key), list):
                rets = [translate_param(args, intermediate_param_key, {_param_key: i})
                        for i in getattr(args, _param_key)]
                new_params = {intermediate_param_key: rets}
                if all((v is None or isinstance(v, list) and all(i is None for i in v)) for v in new_params.values()):
                    new_params = None

    if new_params is None:
        new_params = {k: getattr(args, k) for k in param_translate_rule[0]}
    if all(v is None for v in new_params.values()):
        return

    def _func(r, f):
        if not isinstance(f, list):
            f = [f]
        _f = f[0]
        if not callable(_f):
            _f = globals()[_f]
        return partial(_f, *f[1:])(r)

    try:
        ret = reduce(_func, param_translate_rule[1:], new_params)
    except IndexError:
        return
    return ret


def list2json(params):
    logger.debug('list2json(params=%s)', params)
    if len(params) == 1:
        obj = params.values()[0]
    else:
        n = len(params.values()[0])
        assert all(len(v) == n for v in params.values())
        obj = [{k: v[i] for k, v in params.items() if v[i] is not None} for i in range(n)]
    if not obj:
        return
    return json.dumps(obj).replace('"', '\\"')


def action_simplify(action, mod_suffix=''):
    mod_suffix = mod_suffix.lstrip('bm')
    if mod_suffix:
        mod_suffix = mod_suffix[0].upper() + mod_suffix[1:]
    action = (action.replace('Get', '')
                    .replace('Describe', '')
                    .replace('Description', '')
                    .replace('UnBind', 'Unbind')
                    .replace('LoadBalancer', 'Lb')
                    .replace('Ex', '')
                    .replace(mod_suffix, '')
                    .replace('Bm', '')
                    .replace('Query', ''))
    action = ''.join(['_%s' % c.lower() if c.isupper() else c for c in action])[1:]
    return action


def populate_subparser(parser, mod_suffix=''):
    mod_suffix = mod_suffix.lower()
    parser.set_defaults(mod_suffix=mod_suffix)

    module_path = BS_API_REQUESTS_MODULE_PREFIX + mod_suffix
    mod = importlib.import_module(module_path)
    mod_suffix = mod_suffix if mod_suffix.lstrip('bm') else 'device'
    mapping = action_mapping[mod_suffix]
    for action in dir(mod):
        if action.endswith('Request'):
            orig_action = action[:-len('Request')]
            simple_action = action_simplify(orig_action, mod_suffix=mod_suffix)
            mapping[simple_action or 'list'] = orig_action

    subparsers = parser.add_subparsers(help='Sub commands')
    for simple_action, orig_action in mapping.items():
        action_parser = subparsers.add_parser(simple_action, help='')
        action_parser.add_argument('-r', '--raw', action='store_true', help='raw output.')
        action_parser.add_argument('-j', '--json', action='store_true', help='json format output.')
        action_parser.add_argument('-a', '--attrs', nargs='*', default=list(BS_DEFAULT_ATTRS),
                                   help='the attrs that should be output. (default: %(default)s)')
        action_parser.add_argument('-e', '--extra-attrs', nargs='*',
                                   help='the extra-attrs that should be output.')
        action_parser.add_argument('-s', '--sep', default=', ', help='separator, (default: %(default)s)')

        action_parser.set_defaults(orig_action=orig_action)
        action_mod = getattr(mod, orig_action + 'Request')
        action_cls = getattr(action_mod, orig_action + 'Request')
        param_keys = {param[len('set_'):] for param in action_cls.__dict__ if param.startswith('set_')}
        action_parser.set_defaults(param_keys=param_keys)
        translate_param_keys = set()
        translate_added_param_keys = set()
        extra_new_param_keys = defaultdict(list)
        logger.debug('mod: %s, action: %s, param_keys: %s', mod_suffix, simple_action, param_keys)
        for param_key in param_keys:
            # original params
            kw = {}
            if mod_suffix.startswith('bm') and param_key in BS_DEFAULT_PARAMS_BM:
                kw['default'] = BS_DEFAULT_PARAMS_BM[param_key]
                kw['help'] = '(default: %(default)s)'
            elif param_key in BS_DEFAULT_PARAMS:
                kw['default'] = BS_DEFAULT_PARAMS[param_key]
                kw['help'] = '(default: %(default)s)'
            action_parser.add_argument('--%s' % param_key, **kw)

            # translated params
            if param_key in PARAM_MAPPING:
                new_param_keys = PARAM_MAPPING[param_key][0]

                if len(new_param_keys) == 1 and new_param_keys[0] in PARAM_MAPPING:
                    extra_new_param_keys[param_key] += PARAM_MAPPING[new_param_keys[0]][0]

                if all(new_param_key not in param_keys for new_param_key in new_param_keys):
                    translate_param_keys.add(param_key)
                    kw = {}
                    kw['help'] = 'translated param -> %s' % param_key
                    if any(param_key.endswith(suffix) for suffix in BS_PLURAL_SUFFIX):
                        kw['nargs'] = '*'
                    for new_param_key in new_param_keys:
                        if new_param_key in translate_added_param_keys:
                            continue
                        try:
                            action_parser.add_argument('--%s' % new_param_key, **kw)
                            logger.debug('add new_param_key: %s', new_param_key)
                            translate_added_param_keys.add(new_param_key)
                        except Exception:
                            logger.error('param_keys: %s, translate_added_param_keys: %s, new_param_key: %s',
                                         param_keys, translate_added_param_keys, new_param_key)
                            raise
                else:
                    logger.debug('some new_param_keys(%s) already be added in param_keys(%s).',
                                 new_param_keys, param_keys)

        # extra translated params
        for param_key, extra_new_param_keys in extra_new_param_keys.items():
            kw = {}
            kw['help'] = 'translated param -> %s' % param_key
            if any(param_key.endswith(suffix) for suffix in BS_PLURAL_SUFFIX):
                kw['nargs'] = '*'
            for extra_new_param_key in extra_new_param_keys:
                if extra_new_param_key not in (param_keys | translate_added_param_keys):
                    try:
                        action_parser.add_argument('--%s' % extra_new_param_key, **kw)
                        logger.debug('add extra_new_param_key: %s', extra_new_param_key)
                    except Exception:
                        logger.error('param_keys: %s, translate_added_param_keys: %s, extra_new_param_key: %s',
                                     param_keys, translate_added_param_keys, extra_new_param_key)
                        raise

        action_parser.set_defaults(translate_param_keys=translate_param_keys)


def _str(i):
    s = None
    try:
        s = str(i)
    except UnicodeEncodeError:
        s = str(i.encode('utf-8'))
    return s


def output_simplify(args, output):
    try:
        ret = json.loads(output)
    except ValueError:
        logger.error('output: %s', output)
        raise
    code = ret.get('code')
    if code != 0:
        logger.warn('response code non-zero')
        return False, ret

    data = ret.get('data')
    # FIXME: some api output no "data" dict key
    if not data:
        _ret = {k: v for k, v in ret.items() if k.endswith('Set')}
        if _ret:
            data = _ret
    attrs = set(args.attrs + (args.extra_attrs or []))

    def _simplify(data):
        if isinstance(data, list):
            data = [_simplify(i) for i in data]
            if not args.json:
                data = '\n'.join(sorted(_str(i) for i in data))
        elif isinstance(data, dict):
            is_leaf = False
            # NOTE: rough leaf determination
            if not any(isinstance(v, (dict,)) for k, v in data.items()):
                is_leaf = True
            if any(isinstance(i, (dict,)) for k, v in data.items() if isinstance(v, list) for i in v):
                is_leaf = False
            data = {k: _simplify(v) for k, v in data.items() if not is_leaf or k in attrs} or data
            if not args.json:
                if is_leaf:
                    data = args.sep.join([_str(v) for k, v in data.items()])
                else:
                    data = '\n'.join([('%s' if idx % 2 else '>> %s') % _str(i) for p in data.items() for idx, i in enumerate(p)])
        return data

    return True, _simplify(data)


# TODO: support direct API call
def _execute(mod_suffix, action, params):
    logger.debug('call _execute(%s, %s, %s)', mod_suffix, action, params)

    mapping = action_mapping[mod_suffix if mod_suffix.lstrip('bm') else 'device']
    if action in mapping:
        action = mapping[action]

    if isinstance(params, dict):
        params = params.items()
    params = ' '.join(['--"%s" "%s"' % (k, v) for k, v in params if v is not None])
    cmd = BS_CMD_PATTERN.format(module=mod_suffix,
                                action=action,
                                params=params)
    logger.info('CMD: %s', cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0 or stderr:
        logger.error('CMD ERROR: %s', stderr)
    return stdout


def get_data_for_reduce(mod_suffix, action, params):
    # HACK: eip list need eips, but we got eip, so we translate it here
    if (mod_suffix, action) == ('bmeip', 'list'):
        if PARAM_MAPPING['eips'][0][0] in params.keys():
            params.update({'eips': list2json(
                {'eips': [params['eip']]}
                )})

    output = _execute(mod_suffix, action, params)
    data = json.loads(output).get('data', {})
    logger.debug('get_data_for_reduce: data: %s, params: %s', data, params)
    return data, params


def execute(args):
    params = [(k, getattr(args, k)) for k in args.param_keys if getattr(args, k) is not None]
    for k in args.param_keys:
        if k in PARAM_MAPPING and k in args.translate_param_keys and getattr(args, k) is None:
            logger.debug('%s should be translated to %s', k, PARAM_MAPPING[k][0])
            translated_param = translate_param(args, k)
            if translated_param is not None:
                params.append((k, translated_param))
                logger.debug('translated success: %s -> %s=%s', PARAM_MAPPING[k][0], k, translated_param)

    output = _execute(args.mod_suffix, action=args.orig_action, params=params)
    if args.raw:
        return True, output
    return output_simplify(args, output)


def device(args):
    """ bm device """
    ret, output = execute(args)
    if output:
        if args.json or ret is False:
            jprint(output)
        else:
            print(output)


cvm = bmeip = bmlb = bmvpc = device


def main():
    """
    e.g.

    API DOC: https://cloud.tencent.com/document/api/386/6632

    $ sa-bs device list -j
    $ sa-bs device list -a alias
    $ sa-bs device list --alias host
    $ sa-bs vpc list -e createTime vpcId
    $ sa-bs vpc subnet
    $ sa-bs vpc subnet_ips --vpcId 1001 --subnetId 6555 -j
    $ sa-bs vpc subnet_ips --subnetName SA
    $ sa-bs vpc subnet_by_cpm_id --alias host22
    $ sa-bs eip list -a eip
    $ sa-bs lb list
    $ sa-bs -vvvv eip list --eipIds '[\\"eip-xxxxxxxx\\"]' -r
    $ sa-bs eip list --eip 1.1.1.1
    $ sa-bs vpc register_batch_ip --subnetName SA --ip 10.0.0.1
    $ sa-bs eip apply
    $ sa-bs eip bind_vpc_ip --eip 1.1.1.1 --vpcIp 10.0.0.1
    $ sa-bs vpc create_interface --alias host11 host22 --subnetName DBA-dummy
    $ sa-bs device reload_os --passwd XXXXXX --subnetName OfflineComputation --alias host88
    $ sa-bs device modify_alias --alias host33 --instanceId cpm-xxxxxxxx
    $ sa-bs -vvvv vpc create_subnet --subnetName Isolation-dummy --cidrBlock 10.0.1.0/24 --vlanId 2222

    ## 机型组合
    $ sa-bs device list -e deviceClassCode
    $ sa-bs device os --deviceClassCode Y0-BS09v2 -a osNameDisplay osTypeId
    $ sa-bs device class_partition --cpuId 4 --diskNum1 2 --diskNum2 12 --diskTypeId1 1 --diskTypeId2 6 --haveRaidCard 0 --mem 64 --deviceClassCode "Y0-BS09v2"
    $ sa-bs device class_partition --cpuId 4 --diskNum1 2 --diskNum2 12 --diskTypeId1 1 --diskTypeId2 6 --haveRaidCard 0 --mem 64
    $ sa-bs device elastic_price --cpuId 4 --diskNum1 2 --diskNum2 12 --diskTypeId1 1 --diskTypeId2 6 --haveRaidCard 0 --mem 64
    $ sa-bs device inventory --cpuId 4 --diskNum1 2 --diskNum2 12 --diskTypeId1 1 --diskTypeId2 6 --haveRaidCard 0 --mem 64 --deviceClassCode "Y0-BS09v2" --subnetName OfflineComputation
    $ sa-bs device hardware_info --alias host11
    $ sa-bs device hardware_specification

    ### 购买机器 ( see https://cloud.tencent.com/document/api/386/6638 )
    $ sa-bs device buy --goodsNum 2 --timeSpan 1 --timeUnit m --alias new_host \
        --subnetName SA --ip 10.0.0.2 10.0.0.3 \
        --cpuId 4 --diskNum1 2 --diskNum2 12 --diskTypeId1 1 --diskTypeId2 6 --haveRaidCard 0 --mem 64 \
        --raidId 25 \
        --deviceClassCode "Y0-BS09v2" --needSecurityAgent 0 --needMonitorAgent 0 --autoRenewFlag 1
    $ sa-bs device deploy_process --instanceId cpm-xxxxxxxx
    $ sa-bs device deploy_process --alias host11
    $ sa-bs device operation_log --alias host22

    ## CVM

    $ sa-bs cvm instances

    """  # NOQA
    parser = argparse.ArgumentParser(epilog=main.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose.')

    # compatible with py2 & 3
    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    # level = logging.DEBUG
    # logging.basicConfig(level=level,
    #                     format='%(asctime)s %(name)s %(levelname)s %(message)s')

    device_parser = subparsers.add_parser('device', help='')
    populate_subparser(device_parser, mod_suffix='bm')
    device_parser.set_defaults(func=device)

    eip_parser = subparsers.add_parser('eip', help='')
    populate_subparser(eip_parser, mod_suffix='bmEip')
    eip_parser.set_defaults(func=bmeip)

    lb_parser = subparsers.add_parser('lb', help='')
    populate_subparser(lb_parser, mod_suffix='bmLb')
    lb_parser.set_defaults(func=bmlb)

    vpc_parser = subparsers.add_parser('vpc', help='')
    populate_subparser(vpc_parser, mod_suffix='bmVpc')
    vpc_parser.set_defaults(func=bmvpc)

    cvm_parser = subparsers.add_parser('cvm', help='')
    populate_subparser(cvm_parser, mod_suffix='Cvm')
    cvm_parser.set_defaults(func=cvm)

    args = parser.parse_args()
    args.user = args.user or get_os_username()

    level = logging.WARNING - args.verbose * 10
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    sys.exit(args.func(args))
