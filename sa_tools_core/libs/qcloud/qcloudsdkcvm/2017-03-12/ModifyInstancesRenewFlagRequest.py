# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyInstancesRenewFlagRequest(Request):

    def __init__(self):
        super(ModifyInstancesRenewFlagRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyInstancesRenewFlag', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_RenewFlag(self):
        return self.get_params().get('RenewFlag')

    def set_RenewFlag(self, RenewFlag):
        self.add_param('RenewFlag', RenewFlag)
