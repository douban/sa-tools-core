# coding: utf-8

import logging
import requests

from sa_tools_core.consts import NOTIFICATION_GATEWAY_API, NOTIFICATION_GATEWAY_TIMEOUT

logger = logging.getLogger(__name__)


def add_notification(type_, host, hoststate, service,
                     content, method, addrs, duration):
    payload = dict(type=type_,
                   host=host, hoststate=hoststate,
                   service=service,
                   content=content,
                   method=method, addrs=addrs, duration=duration)
    resp = requests.post(NOTIFICATION_GATEWAY_API,
                         data=payload,
                         timeout=NOTIFICATION_GATEWAY_TIMEOUT)
    resp.raise_for_status()
    resp_json = resp.json()
    logger.info(resp_json)
    return resp_json['ok']
