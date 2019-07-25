# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipBmApplyRequest(Request):

    def __init__(self):
        super(EipBmApplyRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipBmApply', 'bmeip.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_exclusive(self):
        return self.get_params().get('exclusive')

    def set_exclusive(self, exclusive):
        self.add_param('exclusive', exclusive)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

    def get_ipList(self):
        return self.get_params().get('ipList')

    def set_ipList(self, ipList):
        self.add_param('ipList', ipList)

    def get_payMode(self):
        return self.get_params().get('payMode')

    def set_payMode(self, payMode):
        self.add_param('payMode', payMode)

    def get_setType(self):
        return self.get_params().get('setType')

    def set_setType(self, setType):
        self.add_param('setType', setType)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
