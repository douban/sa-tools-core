# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyBmL4ListenerBackendWeightRequest(Request):

    def __init__(self):
        super(ModifyBmL4ListenerBackendWeightRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'ModifyBmL4ListenerBackendWeight', 'bmlb.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_port(self):
        return self.get_params().get('port')

    def set_port(self, port):
        self.add_param('port', port)

    def get_weight(self):
        return self.get_params().get('weight')

    def set_weight(self, weight):
        self.add_param('weight', weight)
