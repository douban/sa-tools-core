# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryPriceRenewInstancesRequest(Request):

    def __init__(self):
        super(InquiryPriceRenewInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryPriceRenewInstances', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_InstanceChargePrepaid(self):
        return self.get_params().get('InstanceChargePrepaid')

    def set_InstanceChargePrepaid(self, InstanceChargePrepaid):
        self.add_param('InstanceChargePrepaid', InstanceChargePrepaid)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_InternetAccessible(self):
        return self.get_params().get('InternetAccessible')

    def set_InternetAccessible(self, InternetAccessible):
        self.add_param('InternetAccessible', InternetAccessible)

    def get_Uin(self):
        return self.get_params().get('Uin')

    def set_Uin(self, Uin):
        self.add_param('Uin', Uin)
