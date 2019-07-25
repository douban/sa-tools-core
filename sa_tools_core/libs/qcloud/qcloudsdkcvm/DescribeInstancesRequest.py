# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescribeInstancesRequest(Request):

    def __init__(self):
        super(DescribeInstancesRequest, self).__init__(
            'cvm', 'qcloudcliV1', 'DescribeInstances', 'cvm.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_lanIps(self):
        return self.get_params().get('lanIps')

    def set_lanIps(self, lanIps):
        self.add_param('lanIps', lanIps)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_searchWord(self):
        return self.get_params().get('searchWord')

    def set_searchWord(self, searchWord):
        self.add_param('searchWord', searchWord)

    def get_simplify(self):
        return self.get_params().get('simplify')

    def set_simplify(self, simplify):
        self.add_param('simplify', simplify)

    def get_status(self):
        return self.get_params().get('status')

    def set_status(self, status):
        self.add_param('status', status)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)
