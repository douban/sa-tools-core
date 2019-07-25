# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryBmLBPriceRequest(Request):

    def __init__(self):
        super(InquiryBmLBPriceRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'InquiryBmLBPrice', 'bmlb.api.qcloud.com')

    def get_loadBalancerType(self):
        return self.get_params().get('loadBalancerType')

    def set_loadBalancerType(self, loadBalancerType):
        self.add_param('loadBalancerType', loadBalancerType)
