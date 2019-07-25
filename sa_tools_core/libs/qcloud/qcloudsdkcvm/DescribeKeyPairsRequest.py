# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeKeyPairsRequest(Request):

    def __init__(self):
        super(DescribeKeyPairsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeKeyPairs', 'cvm.api.qcloud.com')

    def get_keyIds(self):
        return self.get_params().get('keyIds')

    def set_keyIds(self, keyIds):
        self.add_param('keyIds', keyIds)

    def get_keyName(self):
        return self.get_params().get('keyName')

    def set_keyName(self, keyName):
        self.add_param('keyName', keyName)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)
