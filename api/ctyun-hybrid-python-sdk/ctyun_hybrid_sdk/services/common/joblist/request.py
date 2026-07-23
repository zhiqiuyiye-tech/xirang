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


class JobListRequest(CTYunRequest):
    """
    查询job列表
    """

    def __init__(self, request_param):
        super(JobListRequest, self).__init__("/v4/job/list", "GET", "common", "")
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
        if self.parameters.job_id is not None:
            query_param["jobID"] = self.parameters.job_id
        if self.parameters.job_name is not None:
            query_param["jobName"] = self.parameters.job_name
        if self.parameters.job_status is not None:
            query_param["jobStatus"] = self.parameters.job_status
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class JobListRequestParam(object):

    def __init__(self, region_id, job_id=None, job_name=None, job_status=None, query_content=None):
        """
        :param region_id: 资源池id
        :param job_id: 异步任务id
        :param job_name: 异步任务名称
        :param job_status: 任务状态,running/success/failed
        :param query_content: 模糊查询，支持字段有jobID和jobName
        """
        self.region_id = region_id
        self.job_id = job_id
        self.job_name = job_name
        self.job_status = job_status
        self.query_content = query_content

    def set_job_id(self, job_id):
        """
        :param job_id: 异步任务id
        """
        self.job_id = job_id

    def set_job_name(self, job_name):
        """
        :param job_name: 异步任务名称
        """
        self.job_name = job_name

    def set_job_status(self, job_status):
        """
        :param job_status: 任务状态,running/success/failed
        """
        self.job_status = job_status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查询，支持字段有jobID和jobName
        """
        self.query_content = query_content

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

