# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class UnbindBmL4ListenerVmIpRequest(Request):

    def __init__(self):
        super(UnbindBmL4ListenerVmIpRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'UnbindBmL4ListenerVmIp', 'bmlb.api.qcloud.com')

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_vmList(self):
        return self.get_params().get('vmList')

    def set_vmList(self, vmList):
        self.add_param('vmList', vmList)
