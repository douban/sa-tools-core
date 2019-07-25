# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeKeyPairsRequest(Request):

    def __init__(self):
        super(DescribeKeyPairsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeKeyPairs', 'cvm.api.qcloud.com')

    def get_Filters(self):
        return self.get_params().get('Filters')

    def set_Filters(self, Filters):
        self.add_param('Filters', Filters)

    def get_KeyIds(self):
        return self.get_params().get('KeyIds')

    def set_KeyIds(self, KeyIds):
        self.add_param('KeyIds', KeyIds)

    def get_Limit(self):
        return self.get_params().get('Limit')

    def set_Limit(self, Limit):
        self.add_param('Limit', Limit)

    def get_Offset(self):
        return self.get_params().get('Offset')

    def set_Offset(self, Offset):
        self.add_param('Offset', Offset)
