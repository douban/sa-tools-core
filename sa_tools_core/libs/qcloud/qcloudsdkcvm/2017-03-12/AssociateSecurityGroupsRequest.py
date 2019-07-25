# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class AssociateSecurityGroupsRequest(Request):

    def __init__(self):
        super(AssociateSecurityGroupsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'AssociateSecurityGroups', 'cvm.api.qcloud.com')

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_SecurityGroupIds(self):
        return self.get_params().get('SecurityGroupIds')

    def set_SecurityGroupIds(self, SecurityGroupIds):
        self.add_param('SecurityGroupIds', SecurityGroupIds)
