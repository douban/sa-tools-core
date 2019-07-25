# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class StopInstancesRequest(Request):

    def __init__(self):
        super(StopInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'StopInstances', 'cvm.api.qcloud.com')

    def get_forceStop(self):
        return self.get_params().get('forceStop')

    def set_forceStop(self, forceStop):
        self.add_param('forceStop', forceStop)

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)
