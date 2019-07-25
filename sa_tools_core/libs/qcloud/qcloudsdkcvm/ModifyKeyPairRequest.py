# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyKeyPairRequest(Request):

    def __init__(self):
        super(ModifyKeyPairRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyKeyPair', 'cvm.api.qcloud.com')

    def get_keyId(self):
        return self.get_params().get('keyId')

    def set_keyId(self, keyId):
        self.add_param('keyId', keyId)

    def get_keyName(self):
        return self.get_params().get('keyName')

    def set_keyName(self, keyName):
        self.add_param('keyName', keyName)
