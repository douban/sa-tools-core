# coding: utf-8

import logging
import requests

from sa_tools_core.utils import get_config
from sa_tools_core.consts import PROXIES

logger = logging.getLogger(__name__)


def send_message(chatid, content):
    PUSH_KEY = get_config('telegram')
    PUSH_URL = 'https://api.telegram.org/bot%s/sendMessage' % PUSH_KEY

    message = {
        "chat_id": chatid,
        "text": content
    }

    req = requests.post(PUSH_URL, json=message, proxies=PROXIES)
    resp = req.json()
    if not resp['ok']:
        raise Exception('api failed, resp: %s' % resp)
