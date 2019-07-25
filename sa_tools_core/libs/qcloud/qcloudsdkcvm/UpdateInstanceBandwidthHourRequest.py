# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class UpdateInstanceBandwidthHourRequest(Request):

    def __init__(self):
        super(UpdateInstanceBandwidthHourRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'UpdateInstanceBandwidthHour', 'cvm.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)
