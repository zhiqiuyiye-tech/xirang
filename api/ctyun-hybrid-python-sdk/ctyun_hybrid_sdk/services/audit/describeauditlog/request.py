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


class DescribeAuditLogRequest(CTYunRequest):
    """
    查询审计日志详情，包含请求返回值和校验信息
    """

    def __init__(self, request_param):
        super(DescribeAuditLogRequest, self).__init__("/v1/audit/logDetail", "GET", "audit", "")
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
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeAuditLogRequestParam(object):

    def __init__(self, id=None):
        """
        :param id: 审计日志id
        """
        self.id = id

    def set_id(self, id):
        """
        :param id: 审计日志id
        """
        self.id = id

    def check_param(self):
        """
        the param required check
        """
        pass

