# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class GetDeviceDeployProcessRequest(Request):

    def __init__(self):
        super(GetDeviceDeployProcessRequest, self).__init__(
            'bm', 'qcloudcliV1', 'GetDeviceDeployProcess', 'bm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_isElastic(self):
        return self.get_params().get('isElastic')

    def set_isElastic(self, isElastic):
        self.add_param('isElastic', isElastic)
