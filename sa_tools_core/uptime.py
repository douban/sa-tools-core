# coding: utf-8

import logging
from argparse import ArgumentParser

from sa_tools_core.libs.permission import require_sa
from sa_tools_core.libs.process import process
from sa_tools_core.utils import get_os_username


logger = logging.getLogger(__name__)


@require_sa
def uptime(args):
    logger.info('getting uptime info.')
    print(process.uptime()['stdout'])


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('-u', '--user', help='LDAP username')

    args = parser.parse_args(args)

    args.user = args.user or get_os_username()

    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    uptime(args)
