# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ImportKeyPairRequest(Request):

    def __init__(self):
        super(ImportKeyPairRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ImportKeyPair', 'cvm.api.qcloud.com')

    def get_keyName(self):
        return self.get_params().get('keyName')

    def set_keyName(self, keyName):
        self.add_param('keyName', keyName)

    def get_pubKey(self):
        return self.get_params().get('pubKey')

    def set_pubKey(self, pubKey):
        self.add_param('pubKey', pubKey)
