# coding: utf-8

import json
import base64
import urllib
import urllib2
import logging

from sa_tools_core.utils import get_config

PUSH_KEY = get_config('pushbullet')
# PUSH_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'  # reply@douban.com
PUSH_URL = 'https://api.pushbullet.com/v2/pushes'

logger = logging.getLogger(__name__)


def send_message(email, title, body):
    data = {
        "email": email,
        "type": 'note',
        "title": title,
        "body": body,
    }
    payload = urllib.urlencode(data)
    req = urllib2.Request(PUSH_URL)
    base64string = base64.encodestring('%s:%s' % (PUSH_KEY, ''))[:-1]
    authheader = "Basic %s" % base64string
    req.add_header("Authorization", authheader)

    resp = json.loads(urllib2.urlopen(req, payload).read())
    if not resp['receiver_email'] == email:
        raise Exception('api failed, resp: %s' % resp)
