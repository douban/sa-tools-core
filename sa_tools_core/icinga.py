# coding: utf-8

from __future__ import print_function

import os
import re
import sys
import six
import logging
import argparse
from pprint import pprint

import inflect

from sa_tools_core.libs.permission import require_user
from sa_tools_core.libs.sentry import report, send_sentry
from sa_tools_core.libs.template import render_notification
from sa_tools_core.libs.icinga import get_icinga_api
from sa_tools_core.libs.notification_gateway import add_notification
from sa_tools_core.notify import NOTIFY_TYPES, Notifier
from sa_tools_core.utils import get_os_username, AttrDict, import_string
from sa_tools_core.consts import ICINGA_EMAIL, ICINGA_CLUSTER_CONFIG_CLASS, ALERT_WIKI_BASE_URL

requests_logger = logging.getLogger('requests')

logger = logging.getLogger(__name__)

icinga_cluster_config = import_string(ICINGA_CLUSTER_CONFIG_CLASS)

inflect_engine = inflect.engine()


@require_user
def show(args):
    icinga_api = get_icinga_api(icinga_cluster_config)
    params = {}
    if args.attrs:
        params['attrs'] = args.attrs
    if args.filter:
        params['filter'] = args.filter
    res = (icinga_api.api.objects.url(inflect_engine.plural(args.type)).get(**params))
    if args.raw:
        print(res)
    else:
        pprint(res)


@require_user
def ack(args):
    icinga_api = get_icinga_api(icinga_cluster_config)
    ret, msg = icinga_api.acknowledge(
        args.host, service=args.service, author=args.user, comment=args.comment, remove=args.remove, notify=args.notify)
    if ret:
        logger.info('icinga acknowledge %s/%s success: %s', args.host, args.service or '', msg)
    else:
        logger.error('icinga acknowledge %s/%s failed: %s', args.host, args.service or '', msg)


@send_sentry
@require_user
def notify(args):
    notifier = Notifier(from_addr=ICINGA_EMAIL)
    env = (
        dict(
            TARGET_TYPE='service',
            NAGIOS_LONGDATETIME='2016-05-11 16:30:50 +8000',
            NAGIOS_NOTIFICATIONTYPE='PROBLEM',
            NAGIOS_HOSTALIAS='sa',
            NAGIOS_SERVICEDESC='fakeservice',
            NAGIOS_SERVICEOUTPUT="整个中文试试",
            NAGIOS_SERVICESTATE='CRITICAL',
            NOTIFICATIONAUTHORNAME='sysadmin',
            NOTIFICATIONCOMMENT='没病走两步~',
            NOTIFICATION_IS_ARCHIVE=False,
            NAGIOS_CONTACTNAME='shuaisa',
            SERVICE_DURATION_SEC='5.001102',
            NAGIOS_CUSTOM_WIKI=''
        ) if args.test else os.environ)

    unicode_env = {}
    for name, value in env.items():
        if isinstance(value, six.string_types):
            unicode_env[six.ensure_text(name)] = six.ensure_text(value)
        else:
            unicode_env[six.ensure_text(name)] = value

    env = AttrDict(unicode_env, _default_value=six.u(''))

    short_env = dict(
        type=env.NAGIOS_NOTIFICATIONTYPE[:3].upper(),
        host=env.NAGIOS_HOSTALIAS,
        hoststate=env.HOSTSTATE,
        service=env.NAGIOS_SERVICEDESC,
        time=' '.join(env.NAGIOS_LONGDATETIME.split()[:2]),
        extra=(env.NAGIOS_HOSTOUTPUT if env.TARGET_TYPE == 'host' else env.NAGIOS_SERVICEOUTPUT),
        link='',
        custom_wiki_url=env.NAGIOS_CUSTOM_WIKI,
        wiki_base_url=ALERT_WIKI_BASE_URL.rstrip(' /')
        )
    duration = env.SERVICE_DURATION_SEC if env.TARGET_TYPE == 'service' \
        else env.HOST_DURATION_SEC

    short_env = AttrDict(short_env, _default_value='')
    ack_link = icinga_cluster_config.get_ack_link(env)
    reboot_host_link = icinga_cluster_config.get_reboot_host_link(env)
    icinga_link = icinga_cluster_config.get_icinga_link(env)
    for type_ in NOTIFY_TYPES:
        values = vars(args)[type_]
        if values:
            addrs = [i for v in values for i in re.split(r'[,\s]+', v)]
            addrs = [a for a in addrs if a]
            if not addrs:
                logger.warning('ignore empty %s addrs' % type_)
                continue
            title, content = render_notification(
                env=env,
                short_env=short_env,
                notify_type=type_,
                ack_link=ack_link,
                reboot_host_link=reboot_host_link,
                icinga_link=icinga_link)
            try:
                ok = add_notification(
                    env.NAGIOS_NOTIFICATIONTYPE, short_env.host, short_env.hoststate, short_env.service, content, type_,
                    ', '.join(addrs), duration)
                logger.info('notification gateway permit: %s', ok)
            except Exception:
                # we catch the exception and send it to sentry, but let the program continue to run
                report()
                logger.exception('add notification to gateway failed: ')
                ok = True
            if ok:
                try:
                    getattr(notifier, type_)(addrs, title=title, content=content)
                except Exception as e:
                    report()
                    logger.error('Notifier.%s(%s) failed: %s', type_, addrs, e)


def main():
    """
    e.g.
    # try test
    $ sa-icinga notify --wechat lihan --email lihan@douban.com --test

    # need icinga pass os environment vars
    $ sa-icinga notify --wechat lihan --email lihan@douban.com

    # icinga2 doc: http://docs.icinga.org/icinga2/latest/doc/module/icinga2/toc

    $ sa-icinga ack --host sa --service check-puppet --comment 'hehe'
    $ sa-icinga ack --host 'sa*' --service 'check-puppet'
    $ sa-icinga ack --host 'sa*' --service 'check-puppet' --remove
    $ sa-icinga show --filter 'host.name == "sa" && service.name == "check-puppet"'
    $ sa-icinga show --type host --filter 'match("sa*", host.name)' | less
    $ sa-icinga show --type service --filter 'regex("check_[a-z]*", service.name)' | less
    $ sa-icinga show --type notification --filter 'notification.host_name == "sa"' | less
    $ sa-icinga show --type user | grep lihan
    $ sa-icinga show --filter 'service.name == "check-puppet"' --attrs acknowledgement
    """
    parser = argparse.ArgumentParser(epilog=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('-v', '--verbose', help='Show more infomation.', action='store_true')

    # compatible with py2 & 3
    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    notify_parser = subparsers.add_parser('notify', help='Notify.')
    notify_parser.add_argument('--test', action='store_true', help='test')
    for type_ in NOTIFY_TYPES:
        notify_parser.add_argument('--%s' % type_, nargs='*', help='your enterprise address of %s.' % type_)
    notify_parser.set_defaults(func=notify)
    notify_parser.set_defaults(parser_name='notify')

    ack_parser = subparsers.add_parser('ack', help='Acknowledge service or host problem.')
    ack_parser.add_argument('--host', '-H', help='host', required=True)
    ack_parser.add_argument('--service', '-s', help='service')
    ack_parser.add_argument('--comment', '-c', help='comment', default='ack by sa-icinga')
    ack_parser.add_argument('--notify', help='whether notify', default=False, action='store_true')
    ack_parser.add_argument('--remove', help='remove ack', action='store_true')
    ack_parser.set_defaults(func=ack)
    ack_parser.set_defaults(parser_name='ack')

    show_parser = subparsers.add_parser('show', help='Show objects.')
    show_parser.add_argument('--type', '-t', help='type of objects', default='service')
    show_parser.add_argument('--filter', '-f', help='filter')
    show_parser.add_argument('--attrs', '-a', help='attrs of the objects to show', nargs='*')
    show_parser.add_argument('--raw', '-r', help='ouput raw json data', action='store_true')
    show_parser.set_defaults(func=show)
    show_parser.set_defaults(parser_name='show')

    args = parser.parse_args()
    args.user = args.user or get_os_username()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')

    if not args.verbose:
        requests_logger.setLevel(logging.ERROR)

    if args.parser_name == 'notify':
        if not any(vars(args)[type_] for type_ in NOTIFY_TYPES):
            sys.exit(0)

    args.func(args)
