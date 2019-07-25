# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDeviceClassRequest(Request):

    def __init__(self):
        super(DescribeDeviceClassRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDeviceClass', 'bm.api.qcloud.com')
