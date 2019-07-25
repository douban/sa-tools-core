# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmForwardListenersRequest(Request):

    def __init__(self):
        super(DescribeBmForwardListenersRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmForwardListeners', 'bmlb.api.qcloud.com')

    def get_listenerIds(self):
        return self.get_params().get('listenerIds')

    def set_listenerIds(self, listenerIds):
        self.add_param('listenerIds', listenerIds)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)
