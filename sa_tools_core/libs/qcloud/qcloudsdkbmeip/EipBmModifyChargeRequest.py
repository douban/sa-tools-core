# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipBmModifyChargeRequest(Request):

    def __init__(self):
        super(EipBmModifyChargeRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipBmModifyCharge', 'bmeip.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_eipIds(self):
        return self.get_params().get('eipIds')

    def set_eipIds(self, eipIds):
        self.add_param('eipIds', eipIds)

    def get_payMode(self):
        return self.get_params().get('payMode')

    def set_payMode(self, payMode):
        self.add_param('payMode', payMode)
