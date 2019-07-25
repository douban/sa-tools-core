# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmInstancesRequest(Request):

    def __init__(self):
        super(DescribeBmInstancesRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeBmInstances', 'bm.api.qcloud.com')
