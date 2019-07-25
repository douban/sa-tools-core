# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyBmListenerRequest(Request):

    def __init__(self):
        super(ModifyBmListenerRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'ModifyBmListener', 'bmlb.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_customHealthSwitch(self):
        return self.get_params().get('customHealthSwitch')

    def set_customHealthSwitch(self, customHealthSwitch):
        self.add_param('customHealthSwitch', customHealthSwitch)

    def get_healthNum(self):
        return self.get_params().get('healthNum')

    def set_healthNum(self, healthNum):
        self.add_param('healthNum', healthNum)

    def get_healthRequest(self):
        return self.get_params().get('healthRequest')

    def set_healthRequest(self, healthRequest):
        self.add_param('healthRequest', healthRequest)

    def get_healthResponse(self):
        return self.get_params().get('healthResponse')

    def set_healthResponse(self, healthResponse):
        self.add_param('healthResponse', healthResponse)

    def get_healthSwitch(self):
        return self.get_params().get('healthSwitch')

    def set_healthSwitch(self, healthSwitch):
        self.add_param('healthSwitch', healthSwitch)

    def get_inputType(self):
        return self.get_params().get('inputType')

    def set_inputType(self, inputType):
        self.add_param('inputType', inputType)

    def get_intervalTime(self):
        return self.get_params().get('intervalTime')

    def set_intervalTime(self, intervalTime):
        self.add_param('intervalTime', intervalTime)

    def get_lineSeparatorType(self):
        return self.get_params().get('lineSeparatorType')

    def set_lineSeparatorType(self, lineSeparatorType):
        self.add_param('lineSeparatorType', lineSeparatorType)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_listenerName(self):
        return self.get_params().get('listenerName')

    def set_listenerName(self, listenerName):
        self.add_param('listenerName', listenerName)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_sessionExpire(self):
        return self.get_params().get('sessionExpire')

    def set_sessionExpire(self, sessionExpire):
        self.add_param('sessionExpire', sessionExpire)

    def get_timeOut(self):
        return self.get_params().get('timeOut')

    def set_timeOut(self, timeOut):
        self.add_param('timeOut', timeOut)

    def get_toaFlag(self):
        return self.get_params().get('toaFlag')

    def set_toaFlag(self, toaFlag):
        self.add_param('toaFlag', toaFlag)

    def get_unhealthNum(self):
        return self.get_params().get('unhealthNum')

    def set_unhealthNum(self, unhealthNum):
        self.add_param('unhealthNum', unhealthNum)
