# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeInstancesStatusRequest(Request):

    def __init__(self):
        super(DescribeInstancesStatusRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeInstancesStatus', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_Limit(self):
        return self.get_params().get('Limit')

    def set_Limit(self, Limit):
        self.add_param('Limit', Limit)

    def get_Offset(self):
        return self.get_params().get('Offset')

    def set_Offset(self, Offset):
        self.add_param('Offset', Offset)
