# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ReturnInstanceRequest(Request):

    def __init__(self):
        super(ReturnInstanceRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ReturnInstance', 'cvm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)
