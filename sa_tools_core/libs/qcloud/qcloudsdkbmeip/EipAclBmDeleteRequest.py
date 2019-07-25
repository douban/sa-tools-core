# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipAclBmDeleteRequest(Request):

    def __init__(self):
        super(EipAclBmDeleteRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipAclBmDelete', 'bmeip.api.qcloud.com')

    def get_aclId(self):
        return self.get_params().get('aclId')

    def set_aclId(self, aclId):
        self.add_param('aclId', aclId)
