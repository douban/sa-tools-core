# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDeviceOperationLogRequest(Request):

    def __init__(self):
        super(DescribeDeviceOperationLogRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDeviceOperationLog', 'bm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_startTime(self):
        return self.get_params().get('startTime')

    def set_startTime(self, startTime):
        self.add_param('startTime', startTime)

    def get_endTime(self):
        return self.get_params().get('endTime')

    def set_endTime(self, endTime):
        self.add_param('endTime', endTime)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

