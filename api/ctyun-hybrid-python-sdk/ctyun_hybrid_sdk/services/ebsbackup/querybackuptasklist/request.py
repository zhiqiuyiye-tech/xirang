# coding=utf8

# Copyright 2023 CTYUN.CN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ctyun_hybrid_sdk.core.request import CTYunRequest


class QueryBackupTaskListRequest(CTYunRequest):
    """
    查询云硬盘备份任务列表
    """

    def __init__(self, request_param):
        super(QueryBackupTaskListRequest, self).__init__("/v4/ebs-backup/task/list-task", "GET", "ebsbackup", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.task_id is not None:
            query_param["taskID"] = self.parameters.task_id
        if self.parameters.task_status is not None:
            query_param["taskStatus"] = self.parameters.task_status
        if self.parameters.task_type is not None:
            query_param["taskType"] = self.parameters.task_type
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryBackupTaskListRequestParam(object):

    def __init__(self, region_id, query_content=None, task_id=None, task_status=None, task_type=None):
        """
        :param region_id: 资源池ID
        :param query_content: 模糊过滤：云硬盘ID/云硬盘名称/备份任务ID/备份名称/存储库名称
        :param task_id: 云硬盘备份任务ID
        :param task_status: 任务状态:执行中:running,成功:success,失败:failed,已取消:canceled-暂不支持,取消中:canceling-暂不支持
        :param task_type: 任务类型:1:创建任务;2:删除任务;3:恢复任务；0:不筛选；
        """
        self.region_id = region_id
        self.query_content = query_content
        self.task_id = task_id
        self.task_status = task_status
        self.task_type = task_type

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊过滤：云硬盘ID/云硬盘名称/备份任务ID/备份名称/存储库名称
        """
        self.query_content = query_content

    def set_task_id(self, task_id):
        """
        :param task_id: 云硬盘备份任务ID
        """
        self.task_id = task_id

    def set_task_status(self, task_status):
        """
        :param task_status: 任务状态:执行中:running,成功:success,失败:failed,已取消:canceled-暂不支持,取消中:canceling-暂不支持
        """
        self.task_status = task_status

    def set_task_type(self, task_type):
        """
        :param task_type: 任务类型:1:创建任务;2:删除任务;3:恢复任务；0:不筛选；
        """
        self.task_type = task_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

