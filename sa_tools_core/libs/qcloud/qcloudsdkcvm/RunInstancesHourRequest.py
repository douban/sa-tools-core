# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class RunInstancesHourRequest(Request):

    def __init__(self):
        super(RunInstancesHourRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'RunInstancesHour', 'cvm.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_bandwidthType(self):
        return self.get_params().get('bandwidthType')

    def set_bandwidthType(self, bandwidthType):
        self.add_param('bandwidthType', bandwidthType)

    def get_clientToken(self):
        return self.get_params().get('clientToken')

    def set_clientToken(self, clientToken):
        self.add_param('clientToken', clientToken)

    def get_cpu(self):
        return self.get_params().get('cpu')

    def set_cpu(self, cpu):
        self.add_param('cpu', cpu)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

    def get_hostName(self):
        return self.get_params().get('hostName')

    def set_hostName(self, hostName):
        self.add_param('hostName', hostName)

    def get_imageId(self):
        return self.get_params().get('imageId')

    def set_imageId(self, imageId):
        self.add_param('imageId', imageId)

    def get_imageType(self):
        return self.get_params().get('imageType')

    def set_imageType(self, imageType):
        self.add_param('imageType', imageType)

    def get_instanceName(self):
        return self.get_params().get('instanceName')

    def set_instanceName(self, instanceName):
        self.add_param('instanceName', instanceName)

    def get_instanceType(self):
        return self.get_params().get('instanceType')

    def set_instanceType(self, instanceType):
        self.add_param('instanceType', instanceType)

    def get_isVpcGateway(self):
        return self.get_params().get('isVpcGateway')

    def set_isVpcGateway(self, isVpcGateway):
        self.add_param('isVpcGateway', isVpcGateway)

    def get_keyId(self):
        return self.get_params().get('keyId')

    def set_keyId(self, keyId):
        self.add_param('keyId', keyId)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

    def get_needMonitorAgent(self):
        return self.get_params().get('needMonitorAgent')

    def set_needMonitorAgent(self, needMonitorAgent):
        self.add_param('needMonitorAgent', needMonitorAgent)

    def get_needSecurityAgent(self):
        return self.get_params().get('needSecurityAgent')

    def set_needSecurityAgent(self, needSecurityAgent):
        self.add_param('needSecurityAgent', needSecurityAgent)

    def get_password(self):
        return self.get_params().get('password')

    def set_password(self, password):
        self.add_param('password', password)

    def get_privateIpAddresses(self):
        return self.get_params().get('privateIpAddresses')

    def set_privateIpAddresses(self, privateIpAddresses):
        self.add_param('privateIpAddresses', privateIpAddresses)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_purchaseSource(self):
        return self.get_params().get('purchaseSource')

    def set_purchaseSource(self, purchaseSource):
        self.add_param('purchaseSource', purchaseSource)

    def get_rootSize(self):
        return self.get_params().get('rootSize')

    def set_rootSize(self, rootSize):
        self.add_param('rootSize', rootSize)

    def get_storageSize(self):
        return self.get_params().get('storageSize')

    def set_storageSize(self, storageSize):
        self.add_param('storageSize', storageSize)

    def get_storageType(self):
        return self.get_params().get('storageType')

    def set_storageType(self, storageType):
        self.add_param('storageType', storageType)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_unlimitZone(self):
        return self.get_params().get('unlimitZone')

    def set_unlimitZone(self, unlimitZone):
        self.add_param('unlimitZone', unlimitZone)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)

    def get_wanIp(self):
        return self.get_params().get('wanIp')

    def set_wanIp(self, wanIp):
        self.add_param('wanIp', wanIp)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
