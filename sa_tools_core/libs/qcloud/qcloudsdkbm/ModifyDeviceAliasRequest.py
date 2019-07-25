# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyDeviceAliasRequest(Request):

    def __init__(self):
        super(ModifyDeviceAliasRequest, self).__init__(
            'bm', 'qcloudcliV1', 'ModifyDeviceAlias', 'bm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_aliases(self):
        return self.get_params().get('aliases')

    def set_aliases(self, aliases):
        self.add_param('aliases', aliases)

    def get_opUin(self):
        return self.get_params().get('opUin')

    def set_opUin(self, opUin):
        self.add_param('opUin', opUin)

