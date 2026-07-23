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


class JobInfoRequest(CTYunRequest):
    """
    查看job资源操作任务状态，例如开关机，重启。   
    resourceId字段将废弃，暂时保留，兼容旧接口。   
    增加uuid（资源的唯一id）字段   
    注意：该接口不支持paas批量任务查询，paas批量请使用/v4/paas/job/info
    """

    def __init__(self, request_param):
        super(JobInfoRequest, self).__init__("/v4/job/info", "GET", "ctecs", "")
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
        if self.parameters.job_id is not None:
            query_param["jobID"] = self.parameters.job_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class JobInfoRequestParam(object):

    def __init__(self, job_id, ):
        """
        :param job_id: 异步任务id
        """
        self.job_id = job_id

    def check_param(self):
        """
        the param required check
        """
        if self.job_id is None:
            raise Exception("job_id can not None")

