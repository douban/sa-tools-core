# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmLocationBackendsRequest(Request):

    def __init__(self):
        super(DescribeBmLocationBackendsRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmLocationBackends', 'bmlb.api.qcloud.com')

    def get_domainId(self):
        return self.get_params().get('domainId')

    def set_domainId(self, domainId):
        self.add_param('domainId', domainId)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

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

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_queryType(self):
        return self.get_params().get('queryType')

    def set_queryType(self, queryType):
        self.add_param('queryType', queryType)
