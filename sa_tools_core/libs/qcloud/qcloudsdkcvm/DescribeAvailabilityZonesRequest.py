# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeAvailabilityZonesRequest(Request):

    def __init__(self):
        super(DescribeAvailabilityZonesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeAvailabilityZones', 'cvm.api.qcloud.com')

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
