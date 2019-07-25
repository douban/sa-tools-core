# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipAclBmSetRequest(Request):

    def __init__(self):
        super(EipAclBmSetRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipAclBmSet', 'bmeip.api.qcloud.com')

    def get_aclId(self):
        return self.get_params().get('aclId')

    def set_aclId(self, aclId):
        self.add_param('aclId', aclId)

    def get_aclName(self):
        return self.get_params().get('aclName')

    def set_aclName(self, aclName):
        self.add_param('aclName', aclName)

    def get_rule(self):
        return self.get_params().get('rule')

    def set_rule(self, rule):
        self.add_param('rule', rule)

    def get_status(self):
        return self.get_params().get('status')

    def set_status(self, status):
        self.add_param('status', status)

    def get_type(self):
        return self.get_params().get('type')

    def set_type(self, type):
        self.add_param('type', type)
