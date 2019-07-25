# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmLoadBalancersRequest(Request):

    def __init__(self):
        super(DescribeBmLoadBalancersRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmLoadBalancers', 'bmlb.api.qcloud.com')

    def get_domain(self):
        return self.get_params().get('domain')

    def set_domain(self, domain):
        self.add_param('domain', domain)

    def get_exclusive(self):
        return self.get_params().get('exclusive')

    def set_exclusive(self, exclusive):
        self.add_param('exclusive', exclusive)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_loadBalancerIds(self):
        return self.get_params().get('loadBalancerIds')

    def set_loadBalancerIds(self, loadBalancerIds):
        self.add_param('loadBalancerIds', loadBalancerIds)

    def get_loadBalancerName(self):
        return self.get_params().get('loadBalancerName')

    def set_loadBalancerName(self, loadBalancerName):
        self.add_param('loadBalancerName', loadBalancerName)

    def get_loadBalancerType(self):
        return self.get_params().get('loadBalancerType')

    def set_loadBalancerType(self, loadBalancerType):
        self.add_param('loadBalancerType', loadBalancerType)

    def get_loadBalancerVips(self):
        return self.get_params().get('loadBalancerVips')

    def set_loadBalancerVips(self, loadBalancerVips):
        self.add_param('loadBalancerVips', loadBalancerVips)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_orderBy(self):
        return self.get_params().get('orderBy')

    def set_orderBy(self, orderBy):
        self.add_param('orderBy', orderBy)

    def get_orderType(self):
        return self.get_params().get('orderType')

    def set_orderType(self, orderType):
        self.add_param('orderType', orderType)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_searchKey(self):
        return self.get_params().get('searchKey')

    def set_searchKey(self, searchKey):
        self.add_param('searchKey', searchKey)

    def get_tgwSetType(self):
        return self.get_params().get('tgwSetType')

    def set_tgwSetType(self, tgwSetType):
        self.add_param('tgwSetType', tgwSetType)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)
