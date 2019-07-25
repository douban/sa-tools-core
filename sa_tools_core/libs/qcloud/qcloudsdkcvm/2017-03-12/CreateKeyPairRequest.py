# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class CreateKeyPairRequest(Request):

    def __init__(self):
        super(CreateKeyPairRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'CreateKeyPair', 'cvm.api.qcloud.com')

    def get_KeyName(self):
        return self.get_params().get('KeyName')

    def set_KeyName(self, KeyName):
        self.add_param('KeyName', KeyName)

    def get_ProjectId(self):
        return self.get_params().get('ProjectId')

    def set_ProjectId(self, ProjectId):
        self.add_param('ProjectId', ProjectId)
