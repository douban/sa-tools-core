# coding: utf-8

from __future__ import absolute_import

import sys
import logging
from functools import wraps

import sentry_sdk

from sa_tools_core.consts import SENTRY_DSN

logger = logging.getLogger(__name__)

sentry_sdk.init(SENTRY_DSN)
hub = sentry_sdk.Hub.current


def report(msg=None, **kw):
    try:
        extra = kw.pop('extra', {})
        extra['str(sys.argv)'] = str(sys.argv)

        with sentry_sdk.push_scope() as scope:
            for k, v in extra.items():
                scope.set_extra(k, v)
            scope.level = kw.pop('level', logging.ERROR)

            if 'user' in kw:
                scope.user = kw.get('user')

            if msg:
                # stack = kw.pop('stack', None)
                # if stack is None or stack is True:
                #     kw['stack'] = _gen_stack()

                hub.capture_message(msg, level=scope.level, **kw)
            else:
                exc_info = sys.exc_info()
                hub.capture_exception(error=exc_info, **kw)
    except Exception:
        logger.exception('report to sentry failed: ')


def send_sentry(func):
    @wraps(func)
    def _(*a, **kw):
        try:
            return func(*a, **kw)
        except Exception:
            report()
            raise
    return _


def _gen_stack(limit=30):
    try:
        raise Exception
    except Exception:
        f = sys.exc_info()[2].tb_frame.f_back
    stack = []
    n = 0
    while f and n < limit:
        stack.append(f)
        f = f.f_back
        n += 1
    stack.reverse()
    return stack
