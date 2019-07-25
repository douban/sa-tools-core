# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyInstancesProjectRequest(Request):

    def __init__(self):
        super(ModifyInstancesProjectRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyInstancesProject', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_ProjectId(self):
        return self.get_params().get('ProjectId')

    def set_ProjectId(self, ProjectId):
        self.add_param('ProjectId', ProjectId)
