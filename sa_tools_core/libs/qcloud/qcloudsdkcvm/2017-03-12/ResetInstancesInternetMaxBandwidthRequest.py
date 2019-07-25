# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ResetInstancesInternetMaxBandwidthRequest(Request):

    def __init__(self):
        super(ResetInstancesInternetMaxBandwidthRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ResetInstancesInternetMaxBandwidth', 'cvm.api.qcloud.com')

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_EndTime(self):
        return self.get_params().get('EndTime')

    def set_EndTime(self, EndTime):
        self.add_param('EndTime', EndTime)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_InternetAccessible(self):
        return self.get_params().get('InternetAccessible')

    def set_InternetAccessible(self, InternetAccessible):
        self.add_param('InternetAccessible', InternetAccessible)

    def get_StartTime(self):
        return self.get_params().get('StartTime')

    def set_StartTime(self, StartTime):
        self.add_param('StartTime', StartTime)
