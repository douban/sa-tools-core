# coding: utf-8

from __future__ import absolute_import

import logging
from functools import wraps

import sentry_sdk
from sentry_sdk.client import Client
from sentry_sdk.hub import Hub
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.dedupe import DedupeIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.modules import ModulesIntegration
from sentry_sdk.integrations.argv import ArgvIntegration

from sa_tools_core.consts import SENTRY_DSN

logger = logging.getLogger(__name__)

try:
    _client = Client(
        dsn=SENTRY_DSN,
        default_integrations=False,
        integrations=[
            ExcepthookIntegration(),
            DedupeIntegration(),
            StdlibIntegration(),
            ModulesIntegration(),
            ArgvIntegration(),
        ],
        max_breadcrumbs=5,
        attach_stacktrace=True,
    )
    _hub = Hub(_client)
except:
    logger.exception('failed to load sentry: ')


def report(msg=None, **kw):
    try:
        extra = kw.pop('extra', {})

        with sentry_sdk.push_scope() as scope:
            for k, v in extra.items():
                scope.set_extra(k, v)
            scope.level = kw.pop('level', logging.ERROR)

            if 'user' in kw:
                scope.user = kw.get('user')

            if msg:
                _hub.capture_message(msg, level=scope.level)
            else:
                _hub.capture_exception()
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
