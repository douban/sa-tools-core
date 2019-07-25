# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDevicePositionRequest(Request):

    def __init__(self):
        super(DescribeDevicePositionRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDevicePosition', 'bm.api.qcloud.com')

    def get_alias(self):
        return self.get_params().get('alias')

    def set_alias(self, alias):
        self.add_param('alias', alias)

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
