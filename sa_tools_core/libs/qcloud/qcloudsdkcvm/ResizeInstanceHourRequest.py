# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ResizeInstanceHourRequest(Request):

    def __init__(self):
        super(ResizeInstanceHourRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ResizeInstanceHour', 'cvm.api.qcloud.com')

    def get_cpu(self):
        return self.get_params().get('cpu')

    def set_cpu(self, cpu):
        self.add_param('cpu', cpu)

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

    def get_storageSize(self):
        return self.get_params().get('storageSize')

    def set_storageSize(self, storageSize):
        self.add_param('storageSize', storageSize)
