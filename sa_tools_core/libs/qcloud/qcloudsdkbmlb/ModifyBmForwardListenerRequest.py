# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class ModifyBmForwardListenerRequest(Request):

    def __init__(self):
        super(ModifyBmForwardListenerRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'ModifyBmForwardListener', 'bmlb.api.qcloud.com')

    def get_bandwidth(self):
        return self.get_params().get('bandwidth')

    def set_bandwidth(self, bandwidth):
        self.add_param('bandwidth', bandwidth)

    def get_certCaContent(self):
        return self.get_params().get('certCaContent')

    def set_certCaContent(self, certCaContent):
        self.add_param('certCaContent', certCaContent)

    def get_certCaId(self):
        return self.get_params().get('certCaId')

    def set_certCaId(self, certCaId):
        self.add_param('certCaId', certCaId)

    def get_certCaName(self):
        return self.get_params().get('certCaName')

    def set_certCaName(self, certCaName):
        self.add_param('certCaName', certCaName)

    def get_certContent(self):
        return self.get_params().get('certContent')

    def set_certContent(self, certContent):
        self.add_param('certContent', certContent)

    def get_certId(self):
        return self.get_params().get('certId')

    def set_certId(self, certId):
        self.add_param('certId', certId)

    def get_certKey(self):
        return self.get_params().get('certKey')

    def set_certKey(self, certKey):
        self.add_param('certKey', certKey)

    def get_certName(self):
        return self.get_params().get('certName')

    def set_certName(self, certName):
        self.add_param('certName', certName)

    def get_forwardProtocol(self):
        return self.get_params().get('forwardProtocol')

    def set_forwardProtocol(self, forwardProtocol):
        self.add_param('forwardProtocol', forwardProtocol)

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

    def get_sslMode(self):
        return self.get_params().get('sslMode')

    def set_sslMode(self, sslMode):
        self.add_param('sslMode', sslMode)
