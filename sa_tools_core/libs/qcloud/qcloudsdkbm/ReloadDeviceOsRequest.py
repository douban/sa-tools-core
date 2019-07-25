# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ReloadDeviceOsRequest(Request):

    def __init__(self):
        super(ReloadDeviceOsRequest, self).__init__(
            'bm', 'qcloudcliV1', 'ReloadDeviceOs', 'bm.api.qcloud.com')

    def get_agentIds(self):
        return self.get_params().get('agentIds')

    def set_agentIds(self, agentIds):
        self.add_param('agentIds', agentIds)

    def get_hyperThreading(self):
        return self.get_params().get('hyperThreading')

    def set_hyperThreading(self, hyperThreading):
        self.add_param('hyperThreading', hyperThreading)

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

    def get_isZoning(self):
        return self.get_params().get('isZoning')

    def set_isZoning(self, isZoning):
        self.add_param('isZoning', isZoning)

    def get_lanIp(self):
        return self.get_params().get('lanIp')

    def set_lanIp(self, lanIp):
        self.add_param('lanIp', lanIp)

    def get_osTypeId(self):
        return self.get_params().get('osTypeId')

    def set_osTypeId(self, osTypeId):
        self.add_param('osTypeId', osTypeId)

    def get_passwd(self):
        return self.get_params().get('passwd')

    def set_passwd(self, passwd):
        self.add_param('passwd', passwd)

    def get_raidId(self):
        return self.get_params().get('raidId')

    def set_raidId(self, raidId):
        self.add_param('raidId', raidId)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_sysDataSpace(self):
        return self.get_params().get('sysDataSpace')

    def set_sysDataSpace(self, sysDataSpace):
        self.add_param('sysDataSpace', sysDataSpace)

    def get_sysRootSpace(self):
        return self.get_params().get('sysRootSpace')

    def set_sysRootSpace(self, sysRootSpace):
        self.add_param('sysRootSpace', sysRootSpace)

    def get_sysSwaporuefiSpace(self):
        return self.get_params().get('sysSwaporuefiSpace')

    def set_sysSwaporuefiSpace(self, sysSwaporuefiSpace):
        self.add_param('sysSwaporuefiSpace', sysSwaporuefiSpace)

    def get_sysUsrlocalSpace(self):
        return self.get_params().get('sysUsrlocalSpace')

    def set_sysUsrlocalSpace(self, sysUsrlocalSpace):
        self.add_param('sysUsrlocalSpace', sysUsrlocalSpace)

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
