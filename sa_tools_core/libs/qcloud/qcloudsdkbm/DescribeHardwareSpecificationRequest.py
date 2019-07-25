# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeHardwareSpecificationRequest(Request):

    def __init__(self):
        super(DescribeHardwareSpecificationRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeHardwareSpecification', 'bm.api.qcloud.com')

