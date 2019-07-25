# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmVportInfoRequest(Request):

    def __init__(self):
        super(DescribeBmVportInfoRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmVportInfo', 'bmlb.api.qcloud.com')

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)
