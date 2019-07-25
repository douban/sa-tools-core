# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryPriceResetInstancesTypeRequest(Request):

    def __init__(self):
        super(InquiryPriceResetInstancesTypeRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryPriceResetInstancesType', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_ForceStop(self):
        return self.get_params().get('ForceStop')

    def set_ForceStop(self, ForceStop):
        self.add_param('ForceStop', ForceStop)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_InstanceType(self):
        return self.get_params().get('InstanceType')

    def set_InstanceType(self, InstanceType):
        self.add_param('InstanceType', InstanceType)

    def get_Uin(self):
        return self.get_params().get('Uin')

    def set_Uin(self, Uin):
        self.add_param('Uin', Uin)
