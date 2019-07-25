# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class CreateBmLoadBalancerRequest(Request):

    def __init__(self):
        super(CreateBmLoadBalancerRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'CreateBmLoadBalancer', 'bmlb.api.qcloud.com')

    def get_exclusive(self):
        return self.get_params().get('exclusive')

    def set_exclusive(self, exclusive):
        self.add_param('exclusive', exclusive)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

    def get_loadBalancerType(self):
        return self.get_params().get('loadBalancerType')

    def set_loadBalancerType(self, loadBalancerType):
        self.add_param('loadBalancerType', loadBalancerType)

    def get_payMode(self):
        return self.get_params().get('payMode')

    def set_payMode(self, payMode):
        self.add_param('payMode', payMode)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_specifiedVips(self):
        return self.get_params().get('specifiedVips')

    def set_specifiedVips(self, specifiedVips):
        self.add_param('specifiedVips', specifiedVips)

    def get_tgwSetType(self):
        return self.get_params().get('tgwSetType')

    def set_tgwSetType(self, tgwSetType):
        self.add_param('tgwSetType', tgwSetType)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vipIspId(self):
        return self.get_params().get('vipIspId')

    def set_vipIspId(self, vipIspId):
        self.add_param('vipIspId', vipIspId)
