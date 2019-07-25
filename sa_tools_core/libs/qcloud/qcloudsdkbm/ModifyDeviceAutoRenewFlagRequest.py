# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyDeviceAutoRenewFlagRequest(Request):

    def __init__(self):
        super(ModifyDeviceAutoRenewFlagRequest, self).__init__(
            'bm', 'qcloudcliV1', 'ModifyDeviceAutoRenewFlag', 'bm.api.qcloud.com')

    def get_autoRenewFlag(self):
        return self.get_params().get('autoRenewFlag')

    def set_autoRenewFlag(self, autoRenewFlag):
        self.add_param('autoRenewFlag', autoRenewFlag)

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)
