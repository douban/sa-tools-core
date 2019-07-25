# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class RunInstancesRequest(Request):

    def __init__(self):
        super(RunInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'RunInstances', 'cvm.api.qcloud.com')

    def get_ClientToken(self):
        return self.get_params().get('ClientToken')

    def set_ClientToken(self, ClientToken):
        self.add_param('ClientToken', ClientToken)

    def get_DataDisks(self):
        return self.get_params().get('DataDisks')

    def set_DataDisks(self, DataDisks):
        self.add_param('DataDisks', DataDisks)

    def get_DryRun(self):
        return self.get_params().get('DryRun')

    def set_DryRun(self, DryRun):
        self.add_param('DryRun', DryRun)

    def get_EnhancedService(self):
        return self.get_params().get('EnhancedService')

    def set_EnhancedService(self, EnhancedService):
        self.add_param('EnhancedService', EnhancedService)

    def get_HostName(self):
        return self.get_params().get('HostName')

    def set_HostName(self, HostName):
        self.add_param('HostName', HostName)

    def get_ImageId(self):
        return self.get_params().get('ImageId')

    def set_ImageId(self, ImageId):
        self.add_param('ImageId', ImageId)

    def get_InstanceChargePrepaid(self):
        return self.get_params().get('InstanceChargePrepaid')

    def set_InstanceChargePrepaid(self, InstanceChargePrepaid):
        self.add_param('InstanceChargePrepaid', InstanceChargePrepaid)

    def get_InstanceChargeType(self):
        return self.get_params().get('InstanceChargeType')

    def set_InstanceChargeType(self, InstanceChargeType):
        self.add_param('InstanceChargeType', InstanceChargeType)

    def get_InstanceCount(self):
        return self.get_params().get('InstanceCount')

    def set_InstanceCount(self, InstanceCount):
        self.add_param('InstanceCount', InstanceCount)

    def get_InstanceName(self):
        return self.get_params().get('InstanceName')

    def set_InstanceName(self, InstanceName):
        self.add_param('InstanceName', InstanceName)

    def get_InstanceType(self):
        return self.get_params().get('InstanceType')

    def set_InstanceType(self, InstanceType):
        self.add_param('InstanceType', InstanceType)

    def get_InternetAccessible(self):
        return self.get_params().get('InternetAccessible')

    def set_InternetAccessible(self, InternetAccessible):
        self.add_param('InternetAccessible', InternetAccessible)

    def get_LoginSettings(self):
        return self.get_params().get('LoginSettings')

    def set_LoginSettings(self, LoginSettings):
        self.add_param('LoginSettings', LoginSettings)

    def get_Placement(self):
        return self.get_params().get('Placement')

    def set_Placement(self, Placement):
        self.add_param('Placement', Placement)

    def get_PurchaseSource(self):
        return self.get_params().get('PurchaseSource')

    def set_PurchaseSource(self, PurchaseSource):
        self.add_param('PurchaseSource', PurchaseSource)

    def get_SecurityGroupIds(self):
        return self.get_params().get('SecurityGroupIds')

    def set_SecurityGroupIds(self, SecurityGroupIds):
        self.add_param('SecurityGroupIds', SecurityGroupIds)

    def get_SystemDisk(self):
        return self.get_params().get('SystemDisk')

    def set_SystemDisk(self, SystemDisk):
        self.add_param('SystemDisk', SystemDisk)

    def get_Uin(self):
        return self.get_params().get('Uin')

    def set_Uin(self, Uin):
        self.add_param('Uin', Uin)

    def get_UserData(self):
        return self.get_params().get('UserData')

    def set_UserData(self, UserData):
        self.add_param('UserData', UserData)

    def get_VirtualPrivateCloud(self):
        return self.get_params().get('VirtualPrivateCloud')

    def set_VirtualPrivateCloud(self, VirtualPrivateCloud):
        self.add_param('VirtualPrivateCloud', VirtualPrivateCloud)
