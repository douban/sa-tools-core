# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class RenewInstanceRequest(Request):

    def __init__(self):
        super(RenewInstanceRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'RenewInstance', 'cvm.api.qcloud.com')

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_period(self):
        return self.get_params().get('period')

    def set_period(self, period):
        self.add_param('period', period)

    def get_purchaseSource(self):
        return self.get_params().get('purchaseSource')

    def set_purchaseSource(self, purchaseSource):
        self.add_param('purchaseSource', purchaseSource)
