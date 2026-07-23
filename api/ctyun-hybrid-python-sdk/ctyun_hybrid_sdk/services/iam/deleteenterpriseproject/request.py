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


class DeleteEnterpriseProjectRequest(CTYunRequest):
    """
    删除企业项目
    """

    def __init__(self, request_param):
        super(DeleteEnterpriseProjectRequest, self).__init__("/v1/project/deleteEnterpriseProject", "POST", "iam", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.enterprise_project_id is not None:
            body_param["enterpriseProjectID"] = self.parameters.enterprise_project_id
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DeleteEnterpriseProjectRequestParam(object):

    def __init__(self, enterprise_project_id, ):
        """
        :param enterprise_project_id: 企业项目id
        """
        self.enterprise_project_id = enterprise_project_id

    def check_param(self):
        """
        the param required check
        """
        if self.enterprise_project_id is None:
            raise Exception("enterprise_project_id can not None")

