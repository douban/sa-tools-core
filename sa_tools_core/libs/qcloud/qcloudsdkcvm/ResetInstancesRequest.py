# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ResetInstancesRequest(Request):

    def __init__(self):
        super(ResetInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'ResetInstances', 'cvm.api.qcloud.com')

    def get_hardPowerOffFlag(self):
        return self.get_params().get('hardPowerOffFlag')

    def set_hardPowerOffFlag(self, hardPowerOffFlag):
        self.add_param('hardPowerOffFlag', hardPowerOffFlag)

    def get_imageId(self):
        return self.get_params().get('imageId')

    def set_imageId(self, imageId):
        self.add_param('imageId', imageId)

    def get_imageType(self):
        return self.get_params().get('imageType')

    def set_imageType(self, imageType):
        self.add_param('imageType', imageType)

    def get_instanceId(self):
        return self.get_params().get('instanceId')

    def set_instanceId(self, instanceId):
        self.add_param('instanceId', instanceId)

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

    def get_purchaseSource(self):
        return self.get_params().get('purchaseSource')

    def set_purchaseSource(self, purchaseSource):
        self.add_param('purchaseSource', purchaseSource)

    def get_rootSize(self):
        return self.get_params().get('rootSize')

    def set_rootSize(self, rootSize):
        self.add_param('rootSize', rootSize)
