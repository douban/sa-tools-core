# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class QueryBmTaskResultRequest(Request):

    def __init__(self):
        super(QueryBmTaskResultRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'QueryBmTaskResult', 'bmvpc.api.qcloud.com')

    def get_taskId(self):
        return self.get_params().get('taskId')

    def set_taskId(self, taskId):
        self.add_param('taskId', taskId)
