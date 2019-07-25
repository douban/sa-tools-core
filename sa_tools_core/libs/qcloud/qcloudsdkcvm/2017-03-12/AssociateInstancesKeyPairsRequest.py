# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class AssociateInstancesKeyPairsRequest(Request):

    def __init__(self):
        super(AssociateInstancesKeyPairsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'AssociateInstancesKeyPairs', 'cvm.api.qcloud.com')

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
