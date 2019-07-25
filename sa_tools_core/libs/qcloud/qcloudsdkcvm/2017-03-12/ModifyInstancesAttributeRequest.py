# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyInstancesAttributeRequest(Request):

    def __init__(self):
        super(ModifyInstancesAttributeRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyInstancesAttribute', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_InstanceName(self):
        return self.get_params().get('InstanceName')

    def set_InstanceName(self, InstanceName):
        self.add_param('InstanceName', InstanceName)

    def get_ResetNewCreationIdentify(self):
        return self.get_params().get('ResetNewCreationIdentify')

    def set_ResetNewCreationIdentify(self, ResetNewCreationIdentify):
        self.add_param('ResetNewCreationIdentify', ResetNewCreationIdentify)

    def get_SecurityGroups(self):
        return self.get_params().get('SecurityGroups')

    def set_SecurityGroups(self, SecurityGroups):
        self.add_param('SecurityGroups', SecurityGroups)

    def get_UserData(self):
        return self.get_params().get('UserData')

    def set_UserData(self, UserData):
        self.add_param('UserData', UserData)
