# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmAgentStatusRequest(Request):

    def __init__(self):
        super(DescribeBmAgentStatusRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeBmAgentStatus', 'bm.api.qcloud.com')
