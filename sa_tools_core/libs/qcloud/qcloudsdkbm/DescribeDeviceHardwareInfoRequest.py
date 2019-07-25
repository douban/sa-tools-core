# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDeviceHardwareInfoRequest(Request):

    def __init__(self):
        super(DescribeDeviceHardwareInfoRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDeviceHardwareInfo', 'bm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

