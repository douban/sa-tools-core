# coding: utf-8

import re
import sys
import logging
import argparse

from sa_tools_core.libs.sentry import report
from sa_tools_core.libs.permission import require_user
from sa_tools_core.libs.notify.email import send_mail
from sa_tools_core.libs.notify.wework import send_message as send_wework
from sa_tools_core.libs.notify.lark import send_message as send_lark
from sa_tools_core.libs.notify.pushbullet import send_message as send_pushbullet
from sa_tools_core.libs.notify.pushover import send_message as send_pushover
from sa_tools_core.libs.notify.telegram import send_message as send_telegram
from sa_tools_core.libs.notify.sms import send_sms
from sa_tools_core.utils import get_os_username
from sa_tools_core.consts import SYSADMIN_EMAIL

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARN)

NOTIFY_TYPES = ("wework", "lark", "email", "sms", "pushbullet", "pushover", "telegram")
DEFAULT_TITLE = "Sent from sa-notify"
DEFAULT_MSG_TYPE = "text"


class Notifier(object):
    def __init__(
        self,
        content=None,
        title=DEFAULT_TITLE,
        from_addr=SYSADMIN_EMAIL,
        msg_type=DEFAULT_MSG_TYPE,
    ):
        self.content = content
        self.title = title
        self.from_addr = from_addr
        self.msg_type = msg_type

    def __getattr__(self, attr):
        if attr in NOTIFY_TYPES:
            f = getattr(self, "_%s" % attr)

            def _func(*a, **kw):
                addrs = kw.get("addrs") or a[0]
                addrs = [addr for addr in addrs if addr]
                if not addrs:
                    logger.warning("notify abort, ignoring empty %s addrs", attr)
                    return
                kw["content"] = kw.get("content") or self.content
                kw["title"] = kw.get("title") or self.title
                if kw["title"]:
                    kw["title"] = kw["title"].strip()
                logger.info("notify %s %s", attr, addrs)
                return f(*a, **kw)

            return _func
        raise AttributeError

    def _wework(self, addrs, content=None, **kw):
        content = content if content is not None else self.content
        send_wework(addrs, content, msg_type=self.msg_type)

    def _lark(self, addrs, content=None, **kw):
        send_lark(addrs, content, **kw)

    def _email(self, addrs, content=None, title=None, from_addr=None, **kw):
        content = content if content is not None else self.content
        send_mail(addrs, content, subject=title, from_addr=from_addr or self.from_addr)

    def _pushbullet(self, addrs, content=None, title=None, **kw):
        content = content if content is not None else self.content
        for addr in addrs:
            send_pushbullet(addr, title, content)

    def _pushover(self, addrs, content=None, **kw):
        content = content if content is not None else self.content
        for addr in addrs:
            send_pushover(addr, content)

    def _telegram(self, addrs, content=None, **kw):
        content = content if content is not None else self.content
        for addr in addrs:
            send_telegram(addr, content, msg_type=self.msg_type)

    def _sms(self, addrs, content=None, **kw):
        content = content if content is not None else self.content
        for addr in addrs:
            send_sms(addr, content)


@require_user
def notify(args):
    msg_type = "markdown" if args.markdown else "text"
    notifier = Notifier(args.content, args.subject, msg_type=msg_type)
    for type_ in NOTIFY_TYPES:
        values = vars(args)[type_]
        if values:
            addrs = [i for v in values for i in re.split(r"[,\s]+", v)]
            try:
                if args.company:
                    getattr(notifier, type_)(addrs, from_addr=args.from_addr, company=args.company)
                else:
                    getattr(notifier, type_)(addrs, from_addr=args.from_addr)
            except Exception as e:
                logger.exception("Notifier.%s(%s) failed: %s", type_, addrs, e)
                report()


def main(args=None):
    """
    e.g.
    $ sa-notify --wework user1 --content 'xxx'
    $ echo 'xxx' | sa-notify --wework user1,user2 --email user1@douban.com user3@douban.com
    """
    parser = argparse.ArgumentParser(
        epilog=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-u", "--user", help="LDAP username, use your OS user name by default.")
    parser.add_argument("-c", "--content", help="content.")
    parser.add_argument(
        "-s", "--subject", help='subject. default="%(default)s"', default=DEFAULT_TITLE
    )
    parser.add_argument("-f", "--from-addr", help="From address, currently only works for email.")
    parser.add_argument("--company", help="Company user in, used when multiple company or tenant is configured.")
    for type_ in NOTIFY_TYPES:
        parser.add_argument(
            "--%s" % type_, nargs="*", help="your enterprise address of %s." % type_
        )
    parser.add_argument(
        "--markdown",
        help="use markdown rendering, only wework & telegram supported",
        action="store_true",
    )

    args = parser.parse_args(args)
    args.user = args.user or get_os_username()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

    if not any(vars(args)[type_] for type_ in NOTIFY_TYPES):
        parser.error("too few arguments")
    if args.content is None:
        args.content = sys.stdin.read()
        if not args.content:
            parser.error("content empty")

    notify(args)
