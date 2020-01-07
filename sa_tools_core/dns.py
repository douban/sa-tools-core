# coding: utf-8

from __future__ import print_function

import json
import logging
import argparse
from six.moves.configparser import ConfigParser

from pydnspod import pydnspod

from sa_tools_core.libs.permission import require_sa
from sa_tools_core.consts import (EXTERNAL_DOMAINS_CONFIG_FILE,
                                  DNS_MONITOR_CALLBACK_URL,
                                  DEFAULT_DNS_DOMAIN)
from sa_tools_core.utils import (get_os_username, get_config,
                                 ipv6_addr_to_tinydns_generic,
                                 output, to_str)

logger = logging.getLogger(__name__)

DOMAIN = DEFAULT_DNS_DOMAIN
DEFAULT_TTL = 300
DEFAULT_MX = 10
DEFAULT_LINE = '默认'
DNSPOD_TO_TINYDNS = {
    'A': ['={domain}:{value}:{ttl}', '+{domain}:{value}:{ttl}'],
    'AAAA': ':{domain}:28:{value}:{ttl}',
    'MX': '@{domain}::{value}:{dist}:{ttl}',
    'NS': '.{domain}::{value}:{ttl}',
    'TXT': '\'{domain}:{value}:{ttl}',
    'CNAME': 'C{domain}:{value}:{ttl}',
}
MAX_RECORDS_COUNT = 3000

DNSPOD_TIMEOUT = 5
DNSPOD_RETRIES = 3

dns_monitor_cb_key_func = lambda: get_config('dns_monitor_callback_key')  # NOQA

external_domains_config = ConfigParser(allow_no_value=True)
external_domains_config.read(EXTERNAL_DOMAINS_CONFIG_FILE)


def get_api_token_by_domain(domain):
    """
    config file example:
    token_id,token,domain
    111,yyy,*
    222,xxx,domain1.com|domain2.com|domain3.co
    """
    result = {}
    for conf in get_config('dnspod').splitlines():
        id_token, domains = conf.rsplit(',', 1)
        for scope in domains.split('|'):
            result[scope] = id_token
    logger.debug("domain config is %s", result)
    return result[domain] if domain in result else result['*']


class DNSPod(object):
    """manipulate the domain served by dnspod"""
    def __init__(self, login_email="", login_password="",
                 api_token_or_func=get_api_token_by_domain,
                 domain=DOMAIN,
                 dry_run=False,
                 verbose=True):
        self.email = login_email
        self.passwd = login_password
        self.api_token = api_token_or_func(domain) if callable(api_token_or_func) else api_token_or_func
        self.dry_run = dry_run
        self.verbose = verbose
        self._dns_monitor_cb_key = None

        self.domain_str = domain
        domain_dict = json.loads(self.domain.info(domain=domain))['domain']
        self.domain_id = domain_dict['id']
        self.domain_grade = domain_dict['grade']
        self.domain_grade_title = domain_dict['grade_title']

    @property
    def user(self):
        return pydnspod.User(self.email, self.passwd, self.api_token,
                             timeout=DNSPOD_TIMEOUT,
                             retries=DNSPOD_RETRIES)

    @property
    def domain(self):
        """
        dnspod 返回码说明 (http://www.dnspod.cn/docs/info.html#common-response)
        :todo 这块放入pydnspod模块做详细处理
        -1 登陆失败
        -2 API使用超出限制
        -3 不是合法代理 (仅用于代理接口)
        -4 不在代理名下 (仅用于代理接口)
        -7 无权使用此接口
        -8 登录失败次数过多，帐号被暂时封禁
        85 帐号异地登录，请求被拒绝
        -99 此功能暂停开放，请稍候重试
        1 操作成功
        2 只允许POST方法
        3 未知错误
        6 用户ID错误 (仅用于代理接口)
        7 用户不在您名下 (仅用于代理接口)
        83 该帐户已经被锁定，无法进行任何操作
        85 该帐户开启了登录区域保护，当前IP不在允许的区域内
        """
        return pydnspod.Domain(self.email, self.passwd, self.api_token,
                               timeout=DNSPOD_TIMEOUT,
                               retries=DNSPOD_RETRIES)

    @property
    def record(self):
        return pydnspod.Record(self.email, self.passwd, self.api_token,
                               timeout=DNSPOD_TIMEOUT,
                               retries=DNSPOD_RETRIES)

    @property
    def monitor(self):
        return pydnspod.Monitor(self.email, self.passwd, self.api_token,
                                timeout=DNSPOD_TIMEOUT,
                                retries=DNSPOD_RETRIES)

    @property
    def dns_monitor_cb_key(self):
        if self._dns_monitor_cb_key is None:
            self._dns_monitor_cb_key = dns_monitor_cb_key_func()
        return self._dns_monitor_cb_key

    def get_user_log(self):
        ret = self.user.log()
        return json.loads(ret).get('log', [])

    def get_record_types(self):
        ret = self.domain.record_type(domain_grade=self.domain_grade)
        return json.loads(ret).get('types', [])

    def get_record_lines(self):
        ret = self.domain.record_line(domain_id=self.domain_id,
                                      domain_grade=self.domain_grade)
        return json.loads(ret).get('lines', [])

    def get_records(self, **kw):
        # FIXME: https://www.dnspod.cn/docs/records.html#record-list, iter to get all
        records = json.loads(self.record.list(domain_id=self.domain_id, length=MAX_RECORDS_COUNT, **kw)).get('records', [])
        return records

    def remove_records(self, sub_domain, type=None, value=None, line=DEFAULT_LINE):
        """remove all records of the sub_domain, type, value"""
        line = line if line else DEFAULT_LINE
        records = self.get_records(sub_domain=sub_domain)
        # NOTE: only deal with default line type records by default
        exist_records = [r for r in records
                         if (to_str(r['line']) == line)
                         and (not type or r['type'] == type)
                         and (not value or r['value'].rstrip('.') == value.rstrip('.'))]

        if self.verbose:
            logger.info('remove_records({sub_domain}, {type}, {value}, {line})'
                        .format(sub_domain=sub_domain,
                                type=type, value=value, line=line))

        if exist_records:
            if self.verbose:
                [logger.info('self.record.remove({domain_id}, {record_id})'
                             .format(domain_id=self.domain_id, record_id=r['id']))
                 for r in exist_records]
            if self.dry_run:
                return [], ''

            results = [json.loads(self.record.remove(domain_id=self.domain_id, record_id=r['id']))
                       for r in exist_records]

            successes = [int(r['status']['code']) == 1 for r in results]
            msg = 'remove records failed: {msgs}'.format(msgs=' || '.join([r['status']['message']
                                                         for r in results]))
        else:
            return [], ''

        return exist_records, '' if all(successes) else msg

    def add_or_modify_record(self, sub_domain, type, value, ttl=DEFAULT_TTL, mx=DEFAULT_MX,
                             line=DEFAULT_LINE,
                             force_enable=None):
        """
        - add or modify 一个 记录
            - 若存在，则 modify
                - 若没差，则直接返回
                - 若有差，
                    - 若 enable，则先把对立的 type 记录都设 disable
                        （若为 CNAME，则把其他 CNAME 都设为 disable），再真正调 modify
                    - 若 disable，真正调 modify
            - 若不存在，则 add
                - 若 enable，则先把对立的 type 记录都设 disable
                    （若为 CNAME，则把其他 CNAME 都设为 disable），再真正调 add
                - 若 disable，真正调 add
        """
        ttl = ttl if ttl else DEFAULT_TTL
        line = line if line else DEFAULT_LINE
        mx = mx if mx else DEFAULT_MX
        mx = "0" if type != 'MX' else mx
        status = 'enable' if force_enable else 'disable'

        # @.example.com.h1.aqb.so. -> example.com.h1.aqb.so.
        value = value.replace('@', '').lstrip('.')

        records = self.get_records(sub_domain=sub_domain)
        # NOTE: only deal with default line type records by default
        exist_records = [r for r in records
                         if to_str(r['line']) == line
                         and r['type'] == type
                         and r['value'].rstrip('.') == value.rstrip('.')]

        if self.verbose:
            logger.info('add_or_modify_record({sub_domain}, {type}, {value}, ttl={ttl}, '
                        'mx={mx}, line={line}, force_enable={force_enable})'
                        .format(sub_domain=sub_domain,
                                type=type, value=value,
                                ttl=ttl, mx=mx, line=line, force_enable=force_enable))

        if exist_records:

            # if no changes
            if all([r['ttl'] == str(ttl)
                    and r['mx'] == str(mx)
                    and ('enabled' if int(r['enabled']) else 'disabled') == status
                    for r in exist_records]):
                return exist_records, ''

            if force_enable:
                if type == 'A':
                    self.set_status(sub_domain, 'CNAME', enable=False)
                elif type == 'CNAME':
                    self.set_status(sub_domain, 'A', enable=False)
                    self.set_status(sub_domain, 'CNAME', enable=False, except_values=[value])

            # if only change status
            only_status_change_exist_records = [r for r in exist_records
                                                if (r['ttl'] == str(ttl)
                                                    and r['mx'] == str(mx)
                                                    and ('enabled' if int(r['enabled'])
                                                         else 'disabled') != status)]
            rest_exist_records = [r for r in exist_records
                                  if not (r['ttl'] == str(ttl)
                                          and r['mx'] == str(mx)
                                          and ('enabled' if int(r['enabled'])
                                               else 'disabled') != status)]
            self.set_status_by_records(only_status_change_exist_records, enable=force_enable)

            if self.verbose:
                [logger.info('record.modify({domain_id}, {record_id}, {sub_domain}, '
                             '{record_type}, {value}, {record_line}, {ttl}, {mx}, {status})'
                             .format(domain_id=self.domain_id, record_id=r['id'],
                                     sub_domain=r['name'],
                                     record_type=type, value=value,
                                     record_line=line,
                                     ttl=ttl, mx=mx, status=status))
                 for r in rest_exist_records]
            if self.dry_run:
                return [], ''

            # NOTE: 一小时超过五次没有任何变动的修改会导致记录被锁定一小时，会报 API usage is limited
            results = [json.loads(self.record.modify(domain_id=self.domain_id, record_id=r['id'],
                                                     sub_domain=r['name'],
                                                     record_type=type, value=value,
                                                     record_line=line,
                                                     ttl=ttl, mx=mx, status=status))
                       for r in rest_exist_records]

            successes = [int(r['status']['code']) == 1 for r in results]
            msg = 'modify records failed: {msgs}'.format(msgs=' || '.join([r['status']['message']
                                                         for r in results]))
            return exist_records, '' if all(successes) else msg
        else:
            if force_enable:
                if type == 'A':
                    self.set_status(sub_domain, 'CNAME', enable=False)
                elif type == 'CNAME':
                    self.set_status(sub_domain, 'A', enable=False)
                    self.set_status(sub_domain, 'CNAME', enable=False)

            if self.verbose:
                logger.info('record.create({domain_id}, {sub_domain}, {record_type}, {value}, '
                            '{record_line}, {ttl}, {mx}, {status})'
                            .format(domain_id=self.domain_id, sub_domain=sub_domain,
                                    record_type=type, value=value, record_line=line,
                                    ttl=ttl, mx=mx, status=status))
            if self.dry_run:
                return [], ''

            result = json.loads(self.record.create(domain_id=self.domain_id, sub_domain=sub_domain,
                                                   record_type=type, value=value, record_line=line,
                                                   ttl=ttl, mx=mx, status=status))
            success = int(result['status']['code']) == 1

            msg = 'add record failed: {msg}'.format(msg=result['status']['message'])
            return [result['record']] if success else [], '' if success else msg

    def set_status(self, sub_domain, type, value=None, enable=True, except_values=[]):
        """set status of records which has same type (and value)"""
        except_values = [v.rstrip('.') for v in except_values]

        records = self.get_records(sub_domain=sub_domain)
        if value:
            exist_records = [r for r in records
                             if r['type'] == type and r['value'].rstrip('.') == value.rstrip('.')]
        else:
            exist_records = [r for r in records
                             if r['type'] == type and r['value'].rstrip('.') not in except_values]

        if exist_records:
            return self.set_status_by_records(exist_records, enable=enable)
        else:
            return False, 'the record not found'

    def set_status_by_records(self, records, enable=True):
        status = 'enable' if enable else 'disable'

        if self.verbose:
            [logger.info('record.modify_status({domain_id}, {record_id}, {status})'
                         '  # {sub_domain}, {record_type}, {value}'
                         .format(domain_id=self.domain_id,
                                 record_id=r['id'],
                                 status=status,
                                 sub_domain=r['name'],
                                 record_type=r.get('type', ''),
                                 value=r.get('value', '')))
             for r in records]
        if self.dry_run:
            return True, ''

        results = [json.loads(self.record.modify_status(domain_id=self.domain_id,
                                                        record_id=r['id'],
                                                        status=status))
                   for r in records]
        successes = [int(r['status']['code']) == 1 for r in results]
        msg = 'set record status failed: {msgs}'.format(msgs=' || '.join([r['status']['message']
                                                        for r in results]))
        return all(successes), '' if all(successes) else msg

    def get_monitors(self, **kwargs):
        return json.loads(self.monitor.list(**kwargs)).get('monitors', [])

    def add_monitors(self, sub_domain, port, monitor_interval, monitor_schema_type, monitor_uri_path, points,
                     bak_ip_mode, send_to_dns_monitor_cb=True):
        records = [r for r in self.get_records(sub_domain=sub_domain) if r['enabled'] == '1' and
                   (r['type'] == 'A' or r['type'] == 'CNAME')]

        if self.verbose:
            for r in records:
                logger.info('add_monitor({sub_domain} {line} {type} {value})'.format(
                            sub_domain=r['name'], line=to_str(r['line']),
                            type=r['type'], value=r['value']))

        if self.dry_run:
            return

        params = {
            'domain_id': self.domain_id,
            'port': port,
            'monitor_interval': monitor_interval,
            'host': '{}.{}'.format(sub_domain, self.domain_str),
            'monitor_type': monitor_schema_type,
            'monitor_path': monitor_uri_path,
            'points': points,
            'bak_ip': bak_ip_mode,
            'email_notice': 'me',
            'less_notice': 'yes'
        }

        if send_to_dns_monitor_cb:
            params.update({'callback_url': DNS_MONITOR_CALLBACK_URL.format(cb_token=self.dns_monitor_cb_key),
                          'callback_key': self.dns_monitor_cb_key})

        for r in records:
            params['record_id'] = r['id']
            self.monitor.create(**params)

    def remove_monitors(self, sub_domain):
        monitors = [m for m in self.get_monitors() if m['domain_id'] == self.domain_id and m['sub_domain'] == sub_domain]

        if self.verbose:
            for m in monitors:
                logger.info('remove_monitors({sub_domain} {line} {ip} {type} {path})'.format(
                            sub_domain=sub_domain, line=to_str(m['record_line']), ip=m['ip'], type=m['monitor_type'],
                            path=m['monitor_path']))

        if self.dry_run:
            return

        for m in monitors:
            self.monitor.remove(monitor_id=m['monitor_id'])


def parse_sub_domains(sub_domains, top_level_domain):
    domain_group_prefix = '' if top_level_domain == DOMAIN else top_level_domain + ':'

    sub_domains = sub_domains.split(',')
    sub_domains = [s.strip() for s in sub_domains if s.strip()]

    sub_domains_extended = [sub_domain
                            for domain_group in sub_domains
                            if external_domains_config.has_section(domain_group_prefix + domain_group)
                            for sub_domain in external_domains_config.options(domain_group_prefix + domain_group)]
    sub_domains = [sub_domain
                   for sub_domain in sub_domains
                   if not external_domains_config.has_section(domain_group_prefix + sub_domain)] + sub_domains_extended
    return sub_domains


@require_sa
def list_monitor(args):
    dnspod = DNSPod(domain=args.domain)

    monitors = dnspod.get_monitors()

    monitors = [m for m in monitors if m['domain'] == args.domain]
    if not args.all:
        monitors = [m for m in monitors if m['monitor_status'] == 'enabled']
    if args.sub_domain:
        monitors = [m for m in monitors if m['sub_domain'] == args.sub_domain]
    output('{:>10} {:<12} {:>15} {:>4} {:>5} {:<20} {:<5}'.format('sub_domain', 'line', 'ip', 'port', 'type', 'path',
                                                                  'status'))
    output('-' * 80)
    for monitor in monitors:
        output('{:>10} {:<12} {:>15} {:>4} {:>5} {:<20} {:<5}'.format(monitor['sub_domain'],
                                                                      to_str(monitor['record_line']),
                                                                      monitor['ip'], monitor['port'], monitor['monitor_type'],
                                                                      monitor['monitor_path'],
                                                                      monitor['monitor_status']))


@require_sa
def add_monitor(args):
    dnspod = DNSPod(dry_run=args.dry_run, domain=args.domain)

    sub_domains = parse_sub_domains(args.sub_domains, args.domain)

    for sub_domain in sub_domains:
        dnspod.add_monitors(sub_domain, args.port, args.monitor_interval, args.monitor_schema_type,
                            args.monitor_uri_path, args.points, args.bak_ip_mode, args.send_to_callback)


@require_sa
def remove_monitor(args):
    dnspod = DNSPod(dry_run=args.dry_run, domain=args.domain)

    sub_domains = parse_sub_domains(args.sub_domains, args.domain)

    for sub_domain in sub_domains:
        dnspod.remove_monitors(sub_domain)


@require_sa
def list_(args):
    dnspod = DNSPod(domain=args.domain)
    params = {}
    if args.search:
        params['keyword'] = args.search
    if args.sub_domain:
        params['sub_domain'] = args.sub_domain

    records = dnspod.get_records(**params)

    output("name", "type", "line", "value", "mx", "ttl", "status")
    output("-" * 50)
    for record in records:
        output(record['name'], record['type'], record['line'], record['value'],
               (record['mx'] if int(record['mx']) else '-'), record['ttl'],
               ('enabled' if int(record['enabled']) else 'disabled'))


@require_sa
def show(args):
    dnspod = DNSPod(domain=args.domain)
    if args.record_line:
        output('>>>', 'supported lines')
        for line in dnspod.get_record_lines():
            output(line)
    if args.record_type:
        output('>>>', 'supported types')
        for type_ in dnspod.get_record_types():
            output(type_)
    if args.user_log:
        output('>>>', 'user log')
        for log_line in dnspod.get_user_log():
            output(log_line)


@require_sa
def dump(args):
    """
    ref: http://cr.yp.to/djbdns/tinydns-data.html
    # record type:
    'A' : =img0.exampleio.com:211.147.4.31:300; +movie.example.com:211.147.4.31:300
    'CNAME' : Cimg1.exampleio.com:img1-exampleio-com.b0.aicdn.com.:86400
    'MX' : @example.com::aspmx.l.google.com.:10:ttl
    'NS' : .example.com::ns1.example.com.:300; &example.com::ns1.example.com.:300
    'TXT' : 'read.example.com:v=spf1 include\072mailgun.org ~all:86400
    'GENERIC' : :fqdn:dns_type:rdata:ttl:timestamp:lo (it starts with a colon)
    'AAAA' : :ipv6.example.com:28:\052\013\103\100\035\000\000\000\200\000\000\000\000\000\276\357:300
    """

    dnspod = DNSPod(domain=args.domain)
    records = dnspod.get_records()
    records.sort(reverse=True, key=lambda x: x['id'])

    for record in records:
        name, type_, value, mx, ttl, enable = record['name'], record['type'], record['value'], \
            record['mx'], record['ttl'], int(record['enabled'])
        domain = args.domain if name == '@' else '.'.join([name, args.domain])

        if type_ == 'A':
            if 'mail' in name:
                line = DNSPOD_TO_TINYDNS[type_][0].format(domain=domain, value=value, ttl=ttl)
            else:
                line = DNSPOD_TO_TINYDNS[type_][1].format(domain=domain, value=value, ttl=ttl)
        elif type_ == 'AAAA':
            line = DNSPOD_TO_TINYDNS[type_].format(domain=domain, value=ipv6_addr_to_tinydns_generic(value), ttl=ttl)
        elif type_ == 'MX':
            line = DNSPOD_TO_TINYDNS[type_].format(domain=domain, value=value, dist=mx, ttl=ttl)
        elif type_ == 'TXT':
            line = DNSPOD_TO_TINYDNS[type_].format(domain=domain, value=value.replace(':', '\\072'), ttl=ttl)
        else:
            line = DNSPOD_TO_TINYDNS[type_].format(domain=domain, value=value, ttl=ttl)

        if not enable:
            line = '#' + line

        output(line)


@require_sa
def ensure(args):
    """sub_domain -> (type, value, ttl, enable)"""
    dnspod = DNSPod(dry_run=args.dry_run, domain=args.domain)
    sub_domains = parse_sub_domains(args.sub_domains, args.domain)

    records = []
    for sub_domain in sub_domains:
        full_domain = sub_domain.rstrip('.') + '.' + DOMAIN
        value = args.value.format(domain=full_domain, sub_domain=sub_domain, type=args.type)
        sub_domain_records, msg = dnspod.add_or_modify_record(sub_domain, args.type, value,
                                                              ttl=args.ttl, mx=args.mx,
                                                              line=args.line,
                                                              force_enable=args.enable)
        if msg:
            logger.error('ensure sub-domain {sub_domain} failed: {msg}'
                         .format(sub_domain=sub_domain, msg=msg))
            exit(2)

        records += sub_domain_records

        if args.excl:
            dnspod.set_status(sub_domain, args.type, enable=False, except_values=[value])

    logger.info('sub-domains {sub_domains} ensured.'.format(sub_domains=sub_domains))


@require_sa
def remove(args):
    dnspod = DNSPod(dry_run=args.dry_run, domain=args.domain)
    sub_domains = parse_sub_domains(args.sub_domains, args.domain)

    records = []
    sub_domains_removed = []
    for sub_domain in sub_domains:
        full_domain = sub_domain.rstrip('.') + '.' + DOMAIN
        value = args.value.format(domain=full_domain, sub_domain=sub_domain, type=args.type)
        sub_domain_records, msg = dnspod.remove_records(sub_domain, args.type, value, args.line)
        if msg:
            logger.error('remove records of sub-domain ({sub_domain}, {type}, {value}) '
                         'failed: {msg}'
                         .format(sub_domain=sub_domain, msg=msg,
                                 type=type,
                                 value=value))
            exit(2)
        if sub_domain_records:
            sub_domains_removed.append(sub_domain)
        else:
            logger.warn('No records matched.')

        records += sub_domain_records

    logger.info('records of sub-domains ({sub_domains}, {type}, {value}) removed.'
                .format(sub_domains=sub_domains_removed,
                        type=args.type,
                        value=args.value))


def main(args=None):
    """
    e.g.
    $ sa-dns ensure sub1.subdomain1 --type CNAME --value {domain}.anotherdomain. --enable
    $ sa-dns remove subdomain1,subdomain2
    $ sa-dns -d example.com dump
    $ sa-dns show -tlu
    """
    parser = argparse.ArgumentParser(epilog=main.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('-d', '--domain', default=DOMAIN,
                        help='Top level domain. (default: %(default)s)')

    # compatible with py2 & 3
    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    dump_parser = subparsers.add_parser('dump', help='Dump dns records.')
    dump_parser.set_defaults(func=dump)
    dump_parser.set_defaults(parser_name='dump')

    list_parser = subparsers.add_parser('list', help='List dns records.')
    list_parser.add_argument('-s', '--search', help='Filter by search keywords.')
    list_parser.add_argument('-S', '--sub-domain', help='Filter by sub domain.')
    list_parser.set_defaults(func=list_)
    list_parser.set_defaults(parser_name='list')

    show_parser = subparsers.add_parser('show', help='Show information.')
    show_parser.add_argument('-t', '--record-type', action='store_true',
                             help='Show record type supported')
    show_parser.add_argument('-l', '--record-line', action='store_true',
                             help='Show record line supported')
    show_parser.add_argument('-u', '--user-log', action='store_true',
                             help='Show user log')
    show_parser.set_defaults(func=show)
    show_parser.set_defaults(parser_name='show')

    ensure_parser = subparsers.add_parser('ensure',
                                          help="Add or modified, "
                                               "ensure the dns records that demanded to present.")
    ensure_parser.add_argument('sub_domains', help='Sub domains, comma-separated.')
    ensure_parser.add_argument('--type', choices=['A', 'CNAME', 'MX', 'TXT'],
                               required=True,
                               help='DNS record type.')
    ensure_parser.add_argument('--value',
                               required=True,
                               help='DNS record value. '
                                    'Support pattern, like `{domain}.h1.aqb.so`. '
                                    'Avaliable variable are domain, sub_domain, type')
    ensure_parser.add_argument('--ttl', default=DEFAULT_TTL, help='DNS record time-to-live.'
                                                                  '(default: %(default)s)')
    ensure_parser.add_argument('--mx', default=DEFAULT_MX,
                               help='MX priority value, required by MX record.'
                                    '(default: %(default)s)')
    ensure_parser.add_argument('--line', default=DEFAULT_LINE, help='DNS record line.'
                                                                    '(default: %(default)s)')
    ensure_status = ensure_parser.add_mutually_exclusive_group(required=True)
    ensure_status.add_argument('--enable', action='store_true', help='Enable the DNS records.')
    ensure_status.add_argument('--disable', action='store_true', help='Disable the DNS records.')
    ensure_parser.add_argument('--excl', '--exclusive', action='store_true',
                               help='Exclusive, disable other records with the same type.')
    ensure_parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    ensure_parser.set_defaults(func=ensure)
    ensure_parser.set_defaults(parser_name='ensure')

    remove_parser = subparsers.add_parser('remove', help='Remove dns records.')
    remove_parser.add_argument('sub_domains', help='Sub domains, comma-separated.')
    remove_parser.add_argument('--type', choices=['', 'A', 'CNAME', 'MX', 'TXT'],
                               default='',
                               help='DNS record type.')
    remove_parser.add_argument('--value',
                               default='',
                               help='DNS record value. '
                                    'Support pattern, like `{domain}.h1.aqb.so`. '
                                    'Avaliable variable are domain, sub_domain, type')
    remove_parser.add_argument('--line', default=DEFAULT_LINE, help='DNS record line.'
                                                                    '(default: %(default)s)')
    remove_parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    remove_parser.set_defaults(func=remove)
    remove_parser.set_defaults(parser_name='remove')

    monitor_parser = subparsers.add_parser('monitor', help='DNSPod Monitor.')
    monitor_subparser = monitor_parser.add_subparsers(help='Monitor Sub Commands.')
    monitor_list_parser = monitor_subparser.add_parser('list', help='List monitors.')
    monitor_list_parser.add_argument('-a', '--all', action='store_true', help='List all monitors.')
    monitor_list_parser.add_argument('-S', '--sub-domain', help='Filter by sub domain.')
    monitor_list_parser.set_defaults(func=list_monitor)
    monitor_add_parser = monitor_subparser.add_parser('add', help='Add monitors.')
    monitor_add_parser.add_argument('sub_domains', help='Sub domains, comma-separated.')
    monitor_add_parser.add_argument('-p', '--port', default=80, help='monitor HTTP(S) port.(default: %(default)s)')
    monitor_add_parser.add_argument('-i', '--monitor-interval', default=60, choices=[60, 180, 360, 600],
                                    help='monitor interval. (default: %(default)s)')
    monitor_add_parser.add_argument('-t', '--monitor-schema-type', default='http', choices=['http', 'https'],
                                    help='monitor schema type. (default: %(default)s)')
    monitor_add_parser.add_argument('-P', '--monitor-uri-path', default='/', help='monitor uri path. (default: %(default)s)')
    monitor_add_parser.add_argument('--points', default='ctc,cuc,cmc,ctc-2,cuc-2,cmc-2,ctc-3,cuc-3,cmc-3',
                                    help='comma-separated monitor points/probes. (default: %(default)s)')
    monitor_add_parser.add_argument('-b', '--bak-ip-mode', default='pass',
                                    help='chose from pass, pause, pause2, auto or comma-separated ip. (default: %(default)s)')
    monitor_add_parser.add_argument('--send-to-callback', action='store_true', help='whether send to dns monitor callback')
    monitor_add_parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    monitor_add_parser.set_defaults(func=add_monitor)
    monitor_remove_parser = monitor_subparser.add_parser('remove', help='Remove monitors.')
    monitor_remove_parser.add_argument('sub_domains', help='Sub domains, comma-separated.')
    monitor_remove_parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    monitor_remove_parser.set_defaults(func=remove_monitor)

    args = parser.parse_args(args)
    args.user = args.user or get_os_username()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    args.func(args)
