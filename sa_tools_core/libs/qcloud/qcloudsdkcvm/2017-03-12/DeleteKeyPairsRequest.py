# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DeleteKeyPairsRequest(Request):

    def __init__(self):
        super(DeleteKeyPairsRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DeleteKeyPairs', 'cvm.api.qcloud.com')

    def get_KeyIds(self):
        return self.get_params().get('KeyIds')

    def set_KeyIds(self, KeyIds):
        self.add_param('KeyIds', KeyIds)
