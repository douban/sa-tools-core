# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeRegionsRequest(Request):

    def __init__(self):
        super(DescribeRegionsRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeRegions', 'bm.api.qcloud.com')

    def get_regionId(self):
        return self.get_params().get('regionId')

    def set_regionId(self, regionId):
        self.add_param('regionId', regionId)
