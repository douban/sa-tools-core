# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDevicePartitionRequest(Request):

    def __init__(self):
        super(DescribeDevicePartitionRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDevicePartition', 'bm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)
