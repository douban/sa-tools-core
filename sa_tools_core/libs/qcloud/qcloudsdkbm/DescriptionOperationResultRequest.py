# -*- coding: utf-8 -*-

from ..qcloudsdkcore.request import Request

class DescriptionOperationResultRequest(Request):

    def __init__(self):
        super(DescriptionOperationResultRequest, self).__init__(
            'bm', 'qcloudcliV1', 'DescriptionOperationResult', 'bm.api.qcloud.com')

    def get_taskId(self):
        return self.get_params().get('taskId')

    def set_taskId(self, taskId):
        self.add_param('taskId', taskId)

