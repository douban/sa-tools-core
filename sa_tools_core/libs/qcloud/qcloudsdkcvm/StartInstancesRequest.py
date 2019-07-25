# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class StartInstancesRequest(Request):

    def __init__(self):
        super(StartInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'StartInstances', 'cvm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)
