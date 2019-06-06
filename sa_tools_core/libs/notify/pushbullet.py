# coding: utf-8

import json
import base64
import logging
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen, Request

from sa_tools_core.utils import get_config

PUSH_URL = 'https://api.pushbullet.com/v2/pushes'

logger = logging.getLogger(__name__)


def send_message(email, title, body):
    PUSH_KEY = get_config('pushbullet')

    data = {
        "email": email,
        "type": 'note',
        "title": title,
        "body": body,
    }
    payload = urlencode(data)
    req = Request(PUSH_URL)
    base64string = base64.encodestring('%s:%s' % (PUSH_KEY, ''))[:-1]
    authheader = "Basic %s" % base64string
    req.add_header("Authorization", authheader)

    resp = json.loads(urlopen(req, payload).read())
    if not resp['receiver_email'] == email:
        raise Exception('api failed, resp: %s' % resp)
