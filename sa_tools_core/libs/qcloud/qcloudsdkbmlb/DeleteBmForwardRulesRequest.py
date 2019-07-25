# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DeleteBmForwardRulesRequest(Request):

    def __init__(self):
        super(DeleteBmForwardRulesRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DeleteBmForwardRules', 'bmlb.api.qcloud.com')

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

    def get_locationIds(self):
        return self.get_params().get('locationIds')

    def set_locationIds(self, locationIds):
        self.add_param('locationIds', locationIds)
