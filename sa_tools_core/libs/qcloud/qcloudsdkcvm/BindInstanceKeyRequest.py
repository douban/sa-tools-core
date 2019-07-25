# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class BindInstanceKeyRequest(Request):

    def __init__(self):
        super(BindInstanceKeyRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'BindInstanceKey', 'cvm.api.qcloud.com')

    def get_hardPowerOffFlag(self):
        return self.get_params().get('hardPowerOffFlag')

    def set_hardPowerOffFlag(self, hardPowerOffFlag):
        self.add_param('hardPowerOffFlag', hardPowerOffFlag)

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_keyId(self):
        return self.get_params().get('keyId')

    def set_keyId(self, keyId):
        self.add_param('keyId', keyId)
