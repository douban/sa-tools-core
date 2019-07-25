# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryInstancePriceRequest(Request):

    def __init__(self):
        super(InquiryInstancePriceRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryInstancePrice', 'cvm.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_bandwidthType(self):
        return self.get_params().get('bandwidthType')

    def set_bandwidthType(self, bandwidthType):
        self.add_param('bandwidthType', bandwidthType)

    def get_bandwidthUpgradeEndTime(self):
        return self.get_params().get('bandwidthUpgradeEndTime')

    def set_bandwidthUpgradeEndTime(self, bandwidthUpgradeEndTime):
        self.add_param('bandwidthUpgradeEndTime', bandwidthUpgradeEndTime)

    def get_bandwidthUpgradeStartTime(self):
        return self.get_params().get('bandwidthUpgradeStartTime')

    def set_bandwidthUpgradeStartTime(self, bandwidthUpgradeStartTime):
        self.add_param('bandwidthUpgradeStartTime', bandwidthUpgradeStartTime)

    def get_cpu(self):
        return self.get_params().get('cpu')

    def set_cpu(self, cpu):
        self.add_param('cpu', cpu)

    def get_endTime(self):
        return self.get_params().get('endTime')

    def set_endTime(self, endTime):
        self.add_param('endTime', endTime)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

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

    def get_instanceModel(self):
        return self.get_params().get('instanceModel')

    def set_instanceModel(self, instanceModel):
        self.add_param('instanceModel', instanceModel)

    def get_instanceType(self):
        return self.get_params().get('instanceType')

    def set_instanceType(self, instanceType):
        self.add_param('instanceType', instanceType)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

    def get_period(self):
        return self.get_params().get('period')

    def set_period(self, period):
        self.add_param('period', period)

    def get_purchaseSource(self):
        return self.get_params().get('purchaseSource')

    def set_purchaseSource(self, purchaseSource):
        self.add_param('purchaseSource', purchaseSource)

    def get_rootSize(self):
        return self.get_params().get('rootSize')

    def set_rootSize(self, rootSize):
        self.add_param('rootSize', rootSize)

    def get_startTime(self):
        return self.get_params().get('startTime')

    def set_startTime(self, startTime):
        self.add_param('startTime', startTime)

    def get_storageSize(self):
        return self.get_params().get('storageSize')

    def set_storageSize(self, storageSize):
        self.add_param('storageSize', storageSize)

    def get_storageType(self):
        return self.get_params().get('storageType')

    def set_storageType(self, storageType):
        self.add_param('storageType', storageType)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
