# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class InquiryInstancePriceHourRequest(Request):

    def __init__(self):
        super(InquiryInstancePriceHourRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'InquiryInstancePriceHour', 'cvm.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_bandwidthType(self):
        return self.get_params().get('bandwidthType')

    def set_bandwidthType(self, bandwidthType):
        self.add_param('bandwidthType', bandwidthType)

    def get_cpu(self):
        return self.get_params().get('cpu')

    def set_cpu(self, cpu):
        self.add_param('cpu', cpu)

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

    def get_instanceModel(self):
        return self.get_params().get('instanceModel')

    def set_instanceModel(self, instanceModel):
        self.add_param('instanceModel', instanceModel)

    def get_mem(self):
        return self.get_params().get('mem')

    def set_mem(self, mem):
        self.add_param('mem', mem)

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

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
