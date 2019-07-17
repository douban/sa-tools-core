# coding: utf-8

import re
import sys
import logging
import argparse

from sa_tools_core.libs.permission import require_user
from sa_tools_core.libs.notify.email import send_mail
from sa_tools_core.libs.notify.wechat import send_message as send_wechat
from sa_tools_core.libs.notify.pushbullet import send_message as send_pushbullet
from sa_tools_core.libs.notify.pushover import send_message as send_pushover
from sa_tools_core.libs.notify.telegram import send_message as send_telegram
from sa_tools_core.libs.notify.sms import send_sms
from sa_tools_core.utils import get_os_username
from sa_tools_core.consts import SYSADMIN_EMAIL

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARN)

NOTIFY_TYPES = ('wechat', 'wework', 'email', 'sms', 'pushbullet', 'pushover', 'telegram')
DEFAULT_TITLE = 'Sent from sa-notify'


class Notifier(object):
    def __init__(self, content=None, title=DEFAULT_TITLE, from_addr=SYSADMIN_EMAIL):
        self.content = content
        self.title = title
        self.from_addr = from_addr

    def __getattr__(self, attr):
        if attr in NOTIFY_TYPES:
            f = getattr(self, '_%s' % attr)

            def _func(*a, **kw):
                addrs = kw.get('addrs') or a[0]
                addrs = [addr for addr in addrs if addr]
                if not addrs:
                    logger.warning('notify abort, ignoring empty %s addrs', attr)
                    return
                kw['content'] = kw.get('content') or self.content
                kw['title'] = kw.get('title') or self.title
                if kw['title']:
                    kw['title'] = kw['title'].strip()
                logger.info('notify %s %s', attr, addrs)
                return f(*a, **kw)
            return _func
        raise AttributeError

    def _wechat(self, addrs, content=None, **kw):
        send_wechat('|'.join(addrs), content)

    def _wework(self, addrs, content=None, **kw):
        send_wechat('|'.join(addrs), content, qy=True)

    def _email(self, addrs, content=None, title=None, from_addr=None, **kw):
        send_mail(addrs, content, subject=title, from_addr=from_addr or self.from_addr)

    def _pushbullet(self, addrs, content=None, title=None, **kw):
        for addr in addrs:
            send_pushbullet(addr, title, content)

    def _pushover(self, addrs, content=None, **kw):
        for addr in addrs:
            send_pushover(addr, content)

    def _telegram(self, addrs, content=None, **kw):
        for addr in addrs:
            send_telegram(addr, content)

    def _sms(self, addrs, content=None, **kw):
        for addr in addrs:
            send_sms(addr, content)


@require_user
def notify(args):
    notifier = Notifier(args.content, args.subject)
    for type_ in NOTIFY_TYPES:
        values = vars(args)[type_]
        if values:
            addrs = [i for v in values for i in re.split(r'[,\s]+', v)]
            try:
                getattr(notifier, type_)(addrs, from_addr=args.from_addr)
            except Exception as e:
                logger.exception('Notifier.%s(%s) failed: %s', type_, addrs, e)


def main(args=None):
    """
    e.g.
    $ sa-notify --wechat user1 --content 'xxx'
    $ echo 'xxx' | sa-notify --wechat user1,user2 --email user1@douban.com user3@douban.com
    """
    parser = argparse.ArgumentParser(epilog=main.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('-c', '--content', help='content.')
    parser.add_argument('-s', '--subject', help='subject. default="%(default)s"',
                        default=DEFAULT_TITLE)
    parser.add_argument('-f', '--from-addr', help='From address, currently only works for email.')
    for type_ in NOTIFY_TYPES:
        parser.add_argument('--%s' % type_, nargs='*',
                            help='your enterprise address of %s.' % type_)

    args = parser.parse_args(args)
    args.user = args.user or get_os_username()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    if not any(vars(args)[type_] for type_ in NOTIFY_TYPES):
        parser.error("too few arguments")
    if args.content is None:
        args.content = sys.stdin.read()
        if not args.content:
            parser.error("content empty")

    notify(args)
