# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyInstanceProjectRequest(Request):

    def __init__(self):
        super(ModifyInstanceProjectRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyInstanceProject', 'cvm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)
