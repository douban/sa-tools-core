# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class UnbindBmLocationInstancesRequest(Request):

    def __init__(self):
        super(UnbindBmLocationInstancesRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'UnbindBmLocationInstances', 'bmlb.api.qcloud.com')

    def get_backends(self):
        return self.get_params().get('backends')

    def set_backends(self, backends):
        self.add_param('backends', backends)

    def get_domainId(self):
        return self.get_params().get('domainId')

    def set_domainId(self, domainId):
        self.add_param('domainId', domainId)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_locationId(self):
        return self.get_params().get('locationId')

    def set_locationId(self, locationId):
        self.add_param('locationId', locationId)
