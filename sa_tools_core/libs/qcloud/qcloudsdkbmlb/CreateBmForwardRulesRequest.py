# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class CreateBmForwardRulesRequest(Request):

    def __init__(self):
        super(CreateBmForwardRulesRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'CreateBmForwardRules', 'bmlb.api.qcloud.com')

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_rules(self):
        return self.get_params().get('rules')

    def set_rules(self, rules):
        self.add_param('rules', rules)
