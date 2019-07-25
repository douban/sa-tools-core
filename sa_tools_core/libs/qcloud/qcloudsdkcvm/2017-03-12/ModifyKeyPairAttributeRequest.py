# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyKeyPairAttributeRequest(Request):

    def __init__(self):
        super(ModifyKeyPairAttributeRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyKeyPairAttribute', 'cvm.api.qcloud.com')

    def get_Description(self):
        return self.get_params().get('Description')

    def set_Description(self, Description):
        self.add_param('Description', Description)

    def get_KeyId(self):
        return self.get_params().get('KeyId')

    def set_KeyId(self, KeyId):
        self.add_param('KeyId', KeyId)

    def get_KeyName(self):
        return self.get_params().get('KeyName')

    def set_KeyName(self, KeyName):
        self.add_param('KeyName', KeyName)
