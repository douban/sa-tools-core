# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ImportKeyPairRequest(Request):

    def __init__(self):
        super(ImportKeyPairRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ImportKeyPair', 'cvm.api.qcloud.com')

    def get_KeyName(self):
        return self.get_params().get('KeyName')

    def set_KeyName(self, KeyName):
        self.add_param('KeyName', KeyName)

    def get_ProjectId(self):
        return self.get_params().get('ProjectId')

    def set_ProjectId(self, ProjectId):
        self.add_param('ProjectId', ProjectId)

    def get_PublicKey(self):
        return self.get_params().get('PublicKey')

    def set_PublicKey(self, PublicKey):
        self.add_param('PublicKey', PublicKey)
