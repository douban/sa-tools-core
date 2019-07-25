# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class SubnetBindBmNatGatewayRequest(Request):

    def __init__(self):
        super(SubnetBindBmNatGatewayRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'SubnetBindBmNatGateway', 'bmvpc.api.qcloud.com')

    def get_natId(self):
        return self.get_params().get('natId')

    def set_natId(self, natId):
        self.add_param('natId', natId)

    def get_subnetIds(self):
        return self.get_params().get('subnetIds')

    def set_subnetIds(self, subnetIds):
        self.add_param('subnetIds', subnetIds)

    def get_unSubnetIds(self):
        return self.get_params().get('unSubnetIds')

    def set_unSubnetIds(self, unSubnetIds):
        self.add_param('unSubnetIds', unSubnetIds)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
