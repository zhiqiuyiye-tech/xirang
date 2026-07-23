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


class CreateVdcHybridHubRequest(CTYunRequest):
    """
    创建VDC组织-hub
    """

    def __init__(self, request_param):
        super(CreateVdcHybridHubRequest, self).__init__("/v4/vdc/hub/create-vdc", "POST", "user", "application/json")
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
        if self.parameters.org_name is not None:
            body_param["orgName"] = self.parameters.org_name
        if self.parameters.parent_org_id is not None:
            body_param["parentOrgID"] = self.parameters.parent_org_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class CreateVdcHybridHubRequestParam(object):

    def __init__(self, org_name, parent_org_id, description=None):
        """
        :param org_name: 组织名称，长度为3-50字符，支持中文汉字，大、小写字母和数字，支持特殊符号下划线、中划线、括号
        :param parent_org_id: 父级组织ID
        :param description: 组织描述，长度不超过100
        """
        self.org_name = org_name
        self.parent_org_id = parent_org_id
        self.description = description

    def set_description(self, description):
        """
        :param description: 组织描述，长度不超过100
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.org_name is None:
            raise Exception("org_name can not None")
        if self.parent_org_id is None:
            raise Exception("parent_org_id can not None")

