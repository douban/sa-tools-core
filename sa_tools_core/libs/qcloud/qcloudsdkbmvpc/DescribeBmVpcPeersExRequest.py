# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmVpcPeersExRequest(Request):

    def __init__(self):
        super(DescribeBmVpcPeersExRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'DescribeBmVpcPeersEx', 'bmvpc.api.qcloud.com')

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_orderDirection(self):
        return self.get_params().get('orderDirection')

    def set_orderDirection(self, orderDirection):
        self.add_param('orderDirection', orderDirection)

    def get_orderField(self):
        return self.get_params().get('orderField')

    def set_orderField(self, orderField):
        self.add_param('orderField', orderField)

    def get_peeringConnectionIds(self):
        return self.get_params().get('peeringConnectionIds')

    def set_peeringConnectionIds(self, peeringConnectionIds):
        self.add_param('peeringConnectionIds', peeringConnectionIds)

    def get_state(self):
        return self.get_params().get('state')

    def set_state(self, state):
        self.add_param('state', state)
