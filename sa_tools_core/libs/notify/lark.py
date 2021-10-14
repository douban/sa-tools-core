# coding: utf-8

from __future__ import absolute_import

import json
import logging

import pylark

from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)

APP_ID = "aaaaaaaaaaaaaaaaaa"
APP_SECRET = "bbbbbbbbbbbbbbbbbbbbbb"


def send_message(addrs, content, **kwargs):
    secret = get_config("lark").split(":")
    APP_ID = secret[0]
    APP_SECRET = secret[1]
    cli = pylark.Lark(app_id=APP_ID, app_secret=APP_SECRET)
    for addr in addrs:
        res, response = cli.message.send_raw_message(
            pylark.SendRawMessageReq(
                receive_id_type="email",
                receive_id=addr,
                content=json.dumps({"text": content}),
                msg_type="text",
            )
        )
