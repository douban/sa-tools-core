# coding: utf-8

import json
import urllib
import logging

from sa_tools_core.utils import get_config

PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

logger = logging.getLogger(__name__)


def send_message(user_key, message):
    # APP_TOKEN created on pushover.net
    APP_TOKEN = get_config('pushover')

    data = {
        "token": APP_TOKEN,
        "user": user_key,
        "message": message,
    }
    payload = urllib.urlencode(data)

    resp = json.loads(urllib.urlopen(PUSHOVER_URL, payload).read())
    if int(resp['status']) != 1:
        raise Exception('api failed, resp: %s' % resp)
