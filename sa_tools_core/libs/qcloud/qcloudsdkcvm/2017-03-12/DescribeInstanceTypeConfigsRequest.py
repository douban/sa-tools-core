# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeInstanceTypeConfigsRequest(Request):

    def __init__(self):
        super(DescribeInstanceTypeConfigsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeInstanceTypeConfigs', 'cvm.api.qcloud.com')

    def get_Filters(self):
        return self.get_params().get('Filters')

    def set_Filters(self, Filters):
        self.add_param('Filters', Filters)
