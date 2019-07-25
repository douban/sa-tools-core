# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipAclBmApplyRequest(Request):

    def __init__(self):
        super(EipAclBmApplyRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipAclBmApply', 'bmeip.api.qcloud.com')

    def get_aclName(self):
        return self.get_params().get('aclName')

    def set_aclName(self, aclName):
        self.add_param('aclName', aclName)

    def get_status(self):
        return self.get_params().get('status')

    def set_status(self, status):
        self.add_param('status', status)
