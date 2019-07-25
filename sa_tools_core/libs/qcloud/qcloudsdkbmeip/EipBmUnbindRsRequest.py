# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class EipBmUnbindRsRequest(Request):

    def __init__(self):
        super(EipBmUnbindRsRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'EipBmUnbindRs', 'bmeip.api.qcloud.com')

    def get_eipId(self):
        return self.get_params().get('eipId')

    def set_eipId(self, eipId):
        self.add_param('eipId', eipId)

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)
