# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ReturnIpsRequest(Request):

    def __init__(self):
        super(ReturnIpsRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'ReturnIps', 'bmvpc.api.qcloud.com')

    def get_ips(self):
        return self.get_params().get('ips')

    def set_ips(self, ips):
        self.add_param('ips', ips)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
