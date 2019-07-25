# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class TerminateInstancesRequest(Request):

    def __init__(self):
        super(TerminateInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'TerminateInstances', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_ReleaseAddress(self):
        return self.get_params().get('ReleaseAddress')

    def set_ReleaseAddress(self, ReleaseAddress):
        self.add_param('ReleaseAddress', ReleaseAddress)
