# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class CreateBmNatGatewayRequest(Request):

    def __init__(self):
        super(CreateBmNatGatewayRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'CreateBmNatGateway', 'bmvpc.api.qcloud.com')

    def get_assignedEipSet(self):
        return self.get_params().get('assignedEipSet')

    def set_assignedEipSet(self, assignedEipSet):
        self.add_param('assignedEipSet', assignedEipSet)

    def get_autoAllocEipNum(self):
        return self.get_params().get('autoAllocEipNum')

    def set_autoAllocEipNum(self, autoAllocEipNum):
        self.add_param('autoAllocEipNum', autoAllocEipNum)

    def get_exclusive(self):
        return self.get_params().get('exclusive')

    def set_exclusive(self, exclusive):
        self.add_param('exclusive', exclusive)

    def get_forwardMode(self):
        return self.get_params().get('forwardMode')

    def set_forwardMode(self, forwardMode):
        self.add_param('forwardMode', forwardMode)

    def get_ips(self):
        return self.get_params().get('ips')

    def set_ips(self, ips):
        self.add_param('ips', ips)

    def get_isBackup(self):
        return self.get_params().get('isBackup')

    def set_isBackup(self, isBackup):
        self.add_param('isBackup', isBackup)

    def get_maxConcurrent(self):
        return self.get_params().get('maxConcurrent')

    def set_maxConcurrent(self, maxConcurrent):
        self.add_param('maxConcurrent', maxConcurrent)

    def get_natName(self):
        return self.get_params().get('natName')

    def set_natName(self, natName):
        self.add_param('natName', natName)

    def get_subnetIds(self):
        return self.get_params().get('subnetIds')

    def set_subnetIds(self, subnetIds):
        self.add_param('subnetIds', subnetIds)

    def get_unSubnetIds(self):
        return self.get_params().get('unSubnetIds')

    def set_unSubnetIds(self, unSubnetIds):
        self.add_param('unSubnetIds', unSubnetIds)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
