# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class StopInstancesRequest(Request):

    def __init__(self):
        super(StopInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'StopInstances', 'cvm.api.qcloud.com')

    def get_ForceStop(self):
        return self.get_params().get('ForceStop')

    def set_ForceStop(self, ForceStop):
        self.add_param('ForceStop', ForceStop)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_StopType(self):
        return self.get_params().get('StopType')

    def set_StopType(self, StopType):
        self.add_param('StopType', StopType)
