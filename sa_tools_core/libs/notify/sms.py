# coding: utf-8

import logging

logger = logging.getLogger(__name__)


def send_sms(num, content):
    # implement this yourself
    # TODO: use plugin mode
    logger.info('Success send sms to %s', num)
