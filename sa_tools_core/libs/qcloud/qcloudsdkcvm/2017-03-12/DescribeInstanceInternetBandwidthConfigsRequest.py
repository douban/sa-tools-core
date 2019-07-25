# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeInstanceInternetBandwidthConfigsRequest(Request):

    def __init__(self):
        super(DescribeInstanceInternetBandwidthConfigsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeInstanceInternetBandwidthConfigs', 'cvm.api.qcloud.com')

    def get_InstanceId(self):
        return self.get_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_param('InstanceId', InstanceId)
