# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DeleteBmForwardDomainsRequest(Request):

    def __init__(self):
        super(DeleteBmForwardDomainsRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DeleteBmForwardDomains', 'bmlb.api.qcloud.com')

    def get_domainIds(self):
        return self.get_params().get('domainIds')

    def set_domainIds(self, domainIds):
        self.add_param('domainIds', domainIds)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)
