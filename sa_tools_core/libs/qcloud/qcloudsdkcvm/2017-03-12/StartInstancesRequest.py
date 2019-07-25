# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class StartInstancesRequest(Request):

    def __init__(self):
        super(StartInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'StartInstances', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)
