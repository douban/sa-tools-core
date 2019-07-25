# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryPriceResizeInstanceDisksRequest(Request):

    def __init__(self):
        super(InquiryPriceResizeInstanceDisksRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryPriceResizeInstanceDisks', 'cvm.api.qcloud.com')

    def get_DataDisks(self):
        return self.get_params().get('DataDisks')

    def set_DataDisks(self, DataDisks):
        self.add_param('DataDisks', DataDisks)

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_ForceStop(self):
        return self.get_params().get('ForceStop')

    def set_ForceStop(self, ForceStop):
        self.add_param('ForceStop', ForceStop)

    def get_InstanceId(self):
        return self.get_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_param('InstanceId', InstanceId)

    def get_Uin(self):
        return self.get_params().get('Uin')

    def set_Uin(self, Uin):
        self.add_param('Uin', Uin)
