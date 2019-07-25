# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeDeviceInventoryRequest(Request):

    def __init__(self):
        super(DescribeDeviceInventoryRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescribeDeviceInventory', 'bm.api.qcloud.com')

    def get_cpuId(self):
        return self.get_params().get('cpuId')

    def set_cpuId(self, cpuId):
        self.add_param('cpuId', cpuId)

    def get_deviceClassCode(self):
        return self.get_params().get('deviceClassCode')

    def set_deviceClassCode(self, deviceClassCode):
        self.add_param('deviceClassCode', deviceClassCode)

    def get_haveRaidCard(self, haveRaidCard):
        return self.get_params().get('haveRaidCard')

    def set_haveRaidCard(self, haveRaidCard):
        self.add_param('haveRaidCard', haveRaidCard)

    def get_diskNum1(self):
        return self.get_params().get('diskNum1')

    def set_diskNum1(self, diskNum1):
        self.add_param('diskNum1', diskNum1)

    def get_diskNum2(self):
        return self.get_params().get('diskNum2')

    def set_diskNum2(self, diskNum2):
        self.add_param('diskNum2', diskNum2)

    def get_diskTypeId1(self):
        return self.get_params().get('diskTypeId1')

    def set_diskTypeId1(self, diskTypeId1):
        self.add_param('diskTypeId1', diskTypeId1)

    def get_diskTypeId2(self):
        return self.get_params().get('diskTypeId2')

    def set_diskTypeId2(self, diskTypeId2):
        self.add_param('diskTypeId2', diskTypeId2)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
