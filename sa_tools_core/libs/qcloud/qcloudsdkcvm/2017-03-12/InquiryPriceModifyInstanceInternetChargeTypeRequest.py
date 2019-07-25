# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryPriceModifyInstanceInternetChargeTypeRequest(Request):

    def __init__(self):
        super(InquiryPriceModifyInstanceInternetChargeTypeRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryPriceModifyInstanceInternetChargeType', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_InstanceId(self):
        return self.get_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_param('InstanceId', InstanceId)

    def get_InternetAccessible(self):
        return self.get_params().get('InternetAccessible')

    def set_InternetAccessible(self, InternetAccessible):
        self.add_param('InternetAccessible', InternetAccessible)
