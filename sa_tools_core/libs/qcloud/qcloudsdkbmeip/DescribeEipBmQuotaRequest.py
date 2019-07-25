# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeEipBmQuotaRequest(Request):

    def __init__(self):
        super(DescribeEipBmQuotaRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'DescribeEipBmQuota', 'bmeip.api.qcloud.com')
