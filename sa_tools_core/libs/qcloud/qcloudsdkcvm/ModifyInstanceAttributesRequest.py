# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyInstanceAttributesRequest(Request):

    def __init__(self):
        super(ModifyInstanceAttributesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ModifyInstanceAttributes', 'cvm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_instanceName(self):
        return self.get_params().get('instanceName')

    def set_instanceName(self, instanceName):
        self.add_param('instanceName', instanceName)
