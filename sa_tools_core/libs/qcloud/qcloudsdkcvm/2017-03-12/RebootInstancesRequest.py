# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class RebootInstancesRequest(Request):

    def __init__(self):
        super(RebootInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'RebootInstances', 'cvm.api.qcloud.com')

    def get_ForceReboot(self):
        return self.get_params().get('ForceReboot')

    def set_ForceReboot(self, ForceReboot):
        self.add_param('ForceReboot', ForceReboot)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_StopType(self):
        return self.get_params().get('StopType')

    def set_StopType(self, StopType):
        self.add_param('StopType', StopType)
