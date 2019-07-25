# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryPriceResetInstanceRequest(Request):

    def __init__(self):
        super(InquiryPriceResetInstanceRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryPriceResetInstance', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_EnhancedService(self):
        return self.get_params().get('EnhancedService')

    def set_EnhancedService(self, EnhancedService):
        self.add_param('EnhancedService', EnhancedService)

    def get_ImageId(self):
        return self.get_params().get('ImageId')

    def set_ImageId(self, ImageId):
        self.add_param('ImageId', ImageId)

    def get_InstanceId(self):
        return self.get_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_param('InstanceId', InstanceId)

    def get_LoginSettings(self):
        return self.get_params().get('LoginSettings')

    def set_LoginSettings(self, LoginSettings):
        self.add_param('LoginSettings', LoginSettings)

    def get_SystemDisk(self):
        return self.get_params().get('SystemDisk')

    def set_SystemDisk(self, SystemDisk):
        self.add_param('SystemDisk', SystemDisk)
