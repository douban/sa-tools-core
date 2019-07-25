# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmSubnetExRequest(Request):

    def __init__(self):
        super(DescribeBmSubnetExRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'DescribeBmSubnetEx', 'bmvpc.api.qcloud.com')

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

    def get_orderFeild(self):
        return self.get_params().get('orderFeild')

    def set_orderFeild(self, orderFeild):
        self.add_param('orderFeild', orderFeild)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_subnetName(self):
        return self.get_params().get('subnetName')

    def set_subnetName(self, subnetName):
        self.add_param('subnetName', subnetName)

    def get_type(self):
        return self.get_params().get('type')

    def set_type(self, type):
        self.add_param('type', type)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vlanId(self):
        return self.get_params().get('vlanId')

    def set_vlanId(self, vlanId):
        self.add_param('vlanId', vlanId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)

    def get_zoneIds(self):
        return self.get_params().get('zoneIds')

    def set_zoneIds(self, zoneIds):
        self.add_param('zoneIds', zoneIds)
