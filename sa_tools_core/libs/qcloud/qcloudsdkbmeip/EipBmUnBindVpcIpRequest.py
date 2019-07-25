# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipBmUnBindVpcIpRequest(Request):

    def __init__(self):
        super(EipBmUnBindVpcIpRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipBmUnBindVpcIp', 'bmeip.api.qcloud.com')

    def get_eipId(self):
        return self.get_params().get('eipId')

    def set_eipId(self, eipId):
        self.add_param('eipId', eipId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)

    def get_vpcIp(self):
        return self.get_params().get('vpcIp')

    def set_vpcIp(self, vpcIp):
        self.add_param('vpcIp', vpcIp)
