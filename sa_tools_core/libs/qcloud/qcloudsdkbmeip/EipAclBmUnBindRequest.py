# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipAclBmUnBindRequest(Request):

    def __init__(self):
        super(EipAclBmUnBindRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipAclBmUnBind', 'bmeip.api.qcloud.com')

    def get_eipAcl(self):
        return self.get_params().get('eipAcl')

    def set_eipAcl(self, eipAcl):
        self.add_param('eipAcl', eipAcl)
