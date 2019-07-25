# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeInstancesRequest(Request):

    def __init__(self):
        super(DescribeInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeInstances', 'cvm.api.qcloud.com')

    def get_Filters(self):
        return self.get_params().get('Filters')

    def set_Filters(self, Filters):
        self.add_param('Filters', Filters)

    def get_InnerSubnetIds(self):
        return self.get_params().get('InnerSubnetIds')

    def set_InnerSubnetIds(self, InnerSubnetIds):
        self.add_param('InnerSubnetIds', InnerSubnetIds)

    def get_InnerVpcIds(self):
        return self.get_params().get('InnerVpcIds')

    def set_InnerVpcIds(self, InnerVpcIds):
        self.add_param('InnerVpcIds', InnerVpcIds)

    def get_InstanceIds(self):
        return self.get_params().get('InstanceIds')

    def set_InstanceIds(self, InstanceIds):
        self.add_param('InstanceIds', InstanceIds)

    def get_IpAddresses(self):
        return self.get_params().get('IpAddresses')

    def set_IpAddresses(self, IpAddresses):
        self.add_param('IpAddresses', IpAddresses)

    def get_Limit(self):
        return self.get_params().get('Limit')

    def set_Limit(self, Limit):
        self.add_param('Limit', Limit)

    def get_Offset(self):
        return self.get_params().get('Offset')

    def set_Offset(self, Offset):
        self.add_param('Offset', Offset)

    def get_VagueInstanceName(self):
        return self.get_params().get('VagueInstanceName')

    def set_VagueInstanceName(self, VagueInstanceName):
        self.add_param('VagueInstanceName', VagueInstanceName)

    def get_VagueIpAddress(self):
        return self.get_params().get('VagueIpAddress')

    def set_VagueIpAddress(self, VagueIpAddress):
        self.add_param('VagueIpAddress', VagueIpAddress)
