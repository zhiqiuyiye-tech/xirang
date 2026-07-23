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


class ListEbsBackupPolicyTasksRequest(CTYunRequest):
    """
    查询备份策略创建的备份任务列表
    """

    def __init__(self, request_param):
        super(ListEbsBackupPolicyTasksRequest, self).__init__("/v4/ebs-backup/policy/list-tasks", "GET", "ebsbackup", "")
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
        if self.parameters.policy_id is not None:
            query_param["policyID"] = self.parameters.policy_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.task_status is not None:
            query_param["taskStatus"] = self.parameters.task_status
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEbsBackupPolicyTasksRequestParam(object):

    def __init__(self, region_id, policy_id, page_no=None, page_size=None, asc=None, sort=None, task_status=None):
        """
        :param region_id: 资源池id
        :param policy_id: 备份策略ID
        :param page_no: 页码，默认值1
        :param page_size: 每页记录数目 ,默认10，范围[1-100]，大于100取100，不传、传0取10
        :param asc: 和sort配合使用，是否升序排列，默认降序  true-升序，false-降序
        :param sort: 和asc配合使用，指定用于排序的字段。可选字段：createdTime/completedTime，默认createdTime
        :param task_status: 备份任务状态，-1-失败，0-执行中，1-成功
        """
        self.region_id = region_id
        self.policy_id = policy_id
        self.page_no = page_no
        self.page_size = page_size
        self.asc = asc
        self.sort = sort
        self.task_status = task_status

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目 ,默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_asc(self, asc):
        """
        :param asc: 和sort配合使用，是否升序排列，默认降序  true-升序，false-降序
        """
        self.asc = asc

    def set_sort(self, sort):
        """
        :param sort: 和asc配合使用，指定用于排序的字段。可选字段：createdTime/completedTime，默认createdTime
        """
        self.sort = sort

    def set_task_status(self, task_status):
        """
        :param task_status: 备份任务状态，-1-失败，0-执行中，1-成功
        """
        self.task_status = task_status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.policy_id is None:
            raise Exception("policy_id can not None")

