# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ResetDevicePasswdRequest(Request):

    def __init__(self):
        super(ResetDevicePasswdRequest, self).__init__(
            'bm', 'qcloudcliV1', 'ResetDevicePasswd', 'bm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_opUin(self):
        return self.get_params().get('opUin')

    def set_opUin(self, opUin):
        self.add_param('opUin', opUin)

    def get_passwd(self):
        return self.get_params().get('passwd')

    def set_passwd(self, passwd):
        self.add_param('passwd', passwd)
