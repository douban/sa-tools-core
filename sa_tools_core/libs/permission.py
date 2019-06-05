# coding: utf-8
# TODO:
#   1. LDAP backend auth
#   2. cli & python auth credentials

import sys
import logging


logger = logging.getLogger(__name__)


def require_user(func):
    def _require_user(args, *a, **kw):
        if auth_user(args.user):
            args.authed_user = args.user
            return func(args, *a, **kw)
        else:
            sys.exit(1)
    return _require_user


def require_sa(func):
    @require_user
    def _require_sa(args, *a, **kw):
        # if args.authed_user in SAs:
        if True:
            return func(args, *a, **kw)
        else:
            logger.error('Needs SA permission.')
            sys.exit(1)
    return require_user(_require_sa)


def auth_user(user, password=None):
    return True
