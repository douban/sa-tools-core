# coding: utf-8

from __future__ import absolute_import

import json
import logging

import pylark

from sa_tools_core.utils import get_config
from sa_tools_core.consts import DEFAULT_LARK_TENANT

logger = logging.getLogger(__name__)

APP_ID = "aaaaaaaaaaaaaaaaaa"
APP_SECRET = "bbbbbbbbbbbbbbbbbbbbbb"


class LarkApp(object):
    tenants = {}

    @staticmethod
    def load_from_configs(configs: dict):
        app = LarkApp()
        for name, config in configs.items():
            lark = pylark.Lark(
                app_id=config["app_id"],
                app_secret=config["app_secret"]
            )
            app.tenants[name] = lark
        return app

    def get_lark(self, company="douban"):
        lark = self.tenants.get(company)
        if lark:
            return lark
        logger.error(f"no tenant named {company}, please check your code and configs")


def send_message(addrs, content, **kwargs):
    secret = get_config("lark-multi-tenant")
    # config template:
    # {
    #     "your_company": {
    #        "app_id": "1",
    #        "app_secret": "1",
    #        "encrypt_key": "1",
    #        "verification_token": "1"
    #    }
    # }
    lark_bundle = LarkApp.load_from_configs(configs=json.loads(secret))
    company = kwargs.get("company", DEFAULT_LARK_TENANT) or DEFAULT_LARK_TENANT
    lark = lark_bundle.get_lark(company=company)
    for addr in addrs:
        res, response = lark.message.send_raw_message(
            pylark.SendRawMessageReq(
                receive_id_type="email",
                receive_id=addr,
                content=json.dumps({"text": content}),
                msg_type="text",
            )
        )
