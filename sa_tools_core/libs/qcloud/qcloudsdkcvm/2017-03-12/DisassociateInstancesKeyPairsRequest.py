# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DisassociateInstancesKeyPairsRequest(Request):

    def __init__(self):
        super(DisassociateInstancesKeyPairsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DisassociateInstancesKeyPairs', 'cvm.api.qcloud.com')

    def get_ForceStop(self):
        return self.get_params().get('ForceStop')

    def set_ForceStop(self, ForceStop):
        self.add_param('ForceStop', ForceStop)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_KeyIds(self):
        return self.get_params().get('KeyIds')

    def set_KeyIds(self, KeyIds):
        self.add_param('KeyIds', KeyIds)
