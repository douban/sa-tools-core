# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeZoneAbilityRequest(Request):

    def __init__(self):
        super(DescribeZoneAbilityRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeZoneAbility', 'cvm.api.qcloud.com')

    def get_capacity(self):
        return self.get_params().get('capacity')

    def set_capacity(self, capacity):
        self.add_param('capacity', capacity)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
