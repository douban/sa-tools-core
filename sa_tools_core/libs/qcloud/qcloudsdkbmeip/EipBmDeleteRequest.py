# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipBmDeleteRequest(Request):

    def __init__(self):
        super(EipBmDeleteRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipBmDelete', 'bmeip.api.qcloud.com')

    def get_eipIds(self):
        return self.get_params().get('eipIds')

    def set_eipIds(self, eipIds):
        self.add_param('eipIds', eipIds)
