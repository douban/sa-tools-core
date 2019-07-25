# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeEipBmRequest(Request):

    def __init__(self):
        super(DescribeEipBmRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'DescribeEipBm', 'bmeip.api.qcloud.com')

    def get_aclId(self):
        return self.get_params().get('aclId')

    def set_aclId(self, aclId):
        self.add_param('aclId', aclId)

    def get_bindAcl(self):
        return self.get_params().get('bindAcl')

    def set_bindAcl(self, bindAcl):
        self.add_param('bindAcl', bindAcl)

    def get_bindTypes(self):
        return self.get_params().get('bindTypes')

    def set_bindTypes(self, bindTypes):
        self.add_param('bindTypes', bindTypes)

    def get_eipIds(self):
        return self.get_params().get('eipIds')

    def set_eipIds(self, eipIds):
        self.add_param('eipIds', eipIds)

    def get_eips(self):
        return self.get_params().get('eips')

    def set_eips(self, eips):
        self.add_param('eips', eips)

    def get_exclusiveTag(self):
        return self.get_params().get('exclusiveTag')

    def set_exclusiveTag(self, exclusiveTag):
        self.add_param('exclusiveTag', exclusiveTag)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_orderBy(self):
        return self.get_params().get('orderBy')

    def set_orderBy(self, orderBy):
        self.add_param('orderBy', orderBy)

    def get_orderType(self):
        return self.get_params().get('orderType')

    def set_orderType(self, orderType):
        self.add_param('orderType', orderType)

    def get_payMode(self):
        return self.get_params().get('payMode')

    def set_payMode(self, payMode):
        self.add_param('payMode', payMode)

    def get_searchKey(self):
        return self.get_params().get('searchKey')

    def set_searchKey(self, searchKey):
        self.add_param('searchKey', searchKey)

    def get_status(self):
        return self.get_params().get('status')

    def set_status(self, status):
        self.add_param('status', status)

    def get_unInstanceIds(self):
        return self.get_params().get('unInstanceIds')

    def set_unInstanceIds(self, unInstanceIds):
        self.add_param('unInstanceIds', unInstanceIds)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
