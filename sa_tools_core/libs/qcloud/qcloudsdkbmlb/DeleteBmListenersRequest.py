# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DeleteBmListenersRequest(Request):

    def __init__(self):
        super(DeleteBmListenersRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DeleteBmListeners', 'bmlb.api.qcloud.com')

    def get_listenerIds(self):
        return self.get_params().get('listenerIds')

    def set_listenerIds(self, listenerIds):
        self.add_param('listenerIds', listenerIds)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)
