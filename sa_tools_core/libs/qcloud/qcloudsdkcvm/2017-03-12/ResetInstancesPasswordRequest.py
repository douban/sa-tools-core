# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ResetInstancesPasswordRequest(Request):

    def __init__(self):
        super(ResetInstancesPasswordRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ResetInstancesPassword', 'cvm.api.qcloud.com')

    def get_ForceStop(self):
        return self.get_params().get('ForceStop')

    def set_ForceStop(self, ForceStop):
        self.add_param('ForceStop', ForceStop)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_Password(self):
        return self.get_params().get('Password')

    def set_Password(self, Password):
        self.add_param('Password', Password)

    def get_UserName(self):
        return self.get_params().get('UserName')

    def set_UserName(self, UserName):
        self.add_param('UserName', UserName)
