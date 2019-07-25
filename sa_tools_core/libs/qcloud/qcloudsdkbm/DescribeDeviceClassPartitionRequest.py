# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDeviceClassPartitionRequest(Request):

    def __init__(self):
        super(DescribeDeviceClassPartitionRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDeviceClassPartition', 'bm.api.qcloud.com')

    def get_deviceClassCode(self):
        return self.get_params().get('deviceClassCode')

    def set_deviceClassCode(self, deviceClassCode):
        self.add_param('deviceClassCode', deviceClassCode)

    def get_cpuId(self):
        return self.get_params().get('cpuId')

    def set_cpuId(self, cpuId):
        self.add_param('cpuId', cpuId)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

    def get_haveRaidCard(self):
        return self.get_params().get('haveRaidCard')

    def set_haveRaidCard(self, haveRaidCard):
        self.add_param('haveRaidCard', haveRaidCard)

    def get_diskTypeId1(self):
        return self.get_params().get('diskTypeId1')

    def set_diskTypeId1(self, diskTypeId1):
        self.add_param('diskTypeId1', diskTypeId1)

    def get_diskNum1(self):
        return self.get_params().get('diskNum1')

    def set_diskNum1(self, diskNum1):
        self.add_param('diskNum1', diskNum1)

    def get_diskTypeId2(self):
        return self.get_params().get('diskTypeId2')

    def set_diskTypeId2(self, diskTypeId2):
        self.add_param('diskTypeId2', diskTypeId2)

    def get_diskNum2(self):
        return self.get_params().get('diskNum2')

    def set_diskNum2(self, diskNum2):
        self.add_param('diskNum2', diskNum2)

