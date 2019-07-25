# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DeleteKeyPairRequest(Request):

    def __init__(self):
        super(DeleteKeyPairRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DeleteKeyPair', 'cvm.api.qcloud.com')

    def get_keyIds(self):
        return self.get_params().get('keyIds')

    def set_keyIds(self, keyIds):
        self.add_param('keyIds', keyIds)
