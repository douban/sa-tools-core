# coding: utf-8

from __future__ import absolute_import

import logging

from wechatpy.enterprise import WeChatClient

from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)

# CORPID = 'aaaaaaaaaaaaaaaaaa'
# CORPSECRET = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
# APPID = 100002 or 2


def send_message(
    touser=None,
    content=None,
    msg_type="text",
    toparty=None,
    totag=None,
    **kwargs,
):
    secret = get_config("wework")
    CORPID, CORPSECRET, APPID = secret.split(":")
    agentid = int(APPID)
    api = WeChatClient(CORPID, CORPSECRET)
    message = dict(
        agent_id=agentid,
        user_ids=touser,
        content=content,
        party_ids=toparty,
        tag_ids=totag,
    )

    if msg_type == "text":
        ret = api.message.send_text(**message)
    elif msg_type == "markdown":
        ret = api.message.send_markdown(**message)
    else:
        raise Exception("unsupported message type")
    return ret
