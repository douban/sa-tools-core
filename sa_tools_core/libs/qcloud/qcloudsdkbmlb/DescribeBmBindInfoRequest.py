# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeBmBindInfoRequest(Request):

    def __init__(self):
        super(DescribeBmBindInfoRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'DescribeBmBindInfo', 'bmlb.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
