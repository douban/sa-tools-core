# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class BuyDeviceRequest(Request):

    def __init__(self):
        super(BuyDeviceRequest, self).__init__(
            'bm', 'qcloudcliV1', 'BuyDevice', 'bm.api.qcloud.com')

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

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

    def get_osTypeId(self):
        return self.get_params().get('osTypeId')

    def set_osTypeId(self, osTypeId):
        self.add_param('osTypeId', osTypeId)

    def get_raidId(self):
        return self.get_params().get('raidId')

    def set_raidId(self, raidId):
        self.add_param('raidId', raidId)

    def get_timeUnit(self):
        return self.get_params().get('timeUnit')

    def set_timeUnit(self, timeUnit):
        self.add_param('timeUnit', timeUnit)

    def get_timeSpan(self):
        return self.get_params().get('timeSpan')

    def set_timeSpan(self, timeSpan):
        self.add_param('timeSpan', timeSpan)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

    def get_hasWanIp(self):
        return self.get_params().get('hasWanIp')

    def set_hasWanIp(self, hasWanIp):
        self.add_param('hasWanIp', hasWanIp)

    def get_needSecurityAgent(self):
        return self.get_params().get('needSecurityAgent')

    def set_needSecurityAgent(self, needSecurityAgent):
        self.add_param('needSecurityAgent', needSecurityAgent)

    def get_needMonitorAgent(self):
        return self.get_params().get('needMonitorAgent')

    def set_needMonitorAgent(self, needMonitorAgent):
        self.add_param('needMonitorAgent', needMonitorAgent)

    def get_alias(self):
        return self.get_params().get('alias')

    def set_alias(self, alias):
        self.add_param('alias', alias)

    def get_sysRootSpace(self):
        return self.get_params().get('sysRootSpace')

    def set_sysRootSpace(self, sysRootSpace):
        self.add_param('sysRootSpace', sysRootSpace)

    def get_sysSwaporuefiSpace(self):
        return self.get_params().get('sysSwaporuefiSpace')

    def set_sysSwaporuefiSpace(self, sysSwaporuefiSpace):
        self.add_param('sysSwaporuefiSpace', sysSwaporuefiSpace)

    def get_sysDataSpace(self):
        return self.get_params().get('sysDataSpace')

    def set_sysDataSpace(self, sysDataSpace):
        self.add_param('sysDataSpace', sysDataSpace)

    def get_hyperThreading(self):
        return self.get_params().get('hyperThreading')

    def set_hyperThreading(self, hyperThreading):
        self.add_param('hyperThreading', hyperThreading)

    def get_autoRenewFlag(self):
        return self.get_params().get('autoRenewFlag')

    def set_autoRenewFlag(self, autoRenewFlag):
        self.add_param('autoRenewFlag', autoRenewFlag)

    def get_ipList(self):
        return self.get_params().get('ipList')

    def set_ipList(self, ipList):
        self.add_param('ipList', ipList)

    def get_fileSystem(self):
        return self.get_params().get('fileSystem')

    def set_fileSystem(self, fileSystem):
        self.add_param('fileSystem', fileSystem)

    def get_tagDetail(self):
        return self.get_params().get('tagDetail')

    def set_tagDetail(self, tagDetail):
        self.add_param('tagDetail', tagDetail)

