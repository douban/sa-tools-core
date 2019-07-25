# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmListenerInfoRequest(Request):

    def __init__(self):
        super(DescribeBmListenerInfoRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmListenerInfo', 'bmlb.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_searchKey(self):
        return self.get_params().get('searchKey')

    def set_searchKey(self, searchKey):
        self.add_param('searchKey', searchKey)
