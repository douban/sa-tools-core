# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyPayModePre2PostRequest(Request):

    def __init__(self):
        super(ModifyPayModePre2PostRequest, self).__init__(
            'bm', 'qcloudcliV1', 'ModifyPayModePre2Post', 'bm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_opUin(self):
        return self.get_params().get('opUin')

    def set_opUin(self, opUin):
        self.add_param('opUin', opUin)

