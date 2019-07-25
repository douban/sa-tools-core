# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeOsRequest(Request):

    def __init__(self):
        super(DescribeOsRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeOs', 'bm.api.qcloud.com')

    def get_deviceClassCode(self):
        return self.get_params().get('deviceClassCode')

    def set_deviceClassCode(self, deviceClassCode):
        self.add_param('deviceClassCode', deviceClassCode)

