# coding: utf-8

from __future__ import absolute_import

import logging

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from wechat.enterprise import WxApi

from sa_tools_core.utils import get_config


logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# CORPID = 'aaaaaaaaaaaaaaaaaa'
# CORPSECRET = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
# APPID = 100002 or 2


def send_message(touser=None, content=None, safe="0", msg_type='text',
                 toparty=None, totag=None, qy=False, **kwargs):
    if qy:
        secret = get_config('wework')
        safe = None
    else:
        secret = get_config('wechat')
    CORPID, CORPSECRET, APPID = secret.split(':')
    agentid = int(APPID)
    api = WxApi(CORPID, CORPSECRET)

    ret, api_error = api.send_message(msg_type=msg_type,
                                      content=content,
                                      agentid=agentid,  # APP ID
                                      safe=safe,
                                      # 成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
                                      touser=touser,
                                      # 部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
                                      toparty=toparty,
                                      # 标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
                                      totag=totag,
                                      )
    if api_error:
        logger.error((
            'send_message({touser}, {content}) get {err_code}, {err_msg}'
            .format(touser=touser,
                    content=content,
                    err_code=api_error.code,
                    err_msg=api_error.message)))
    return ret, api_error
