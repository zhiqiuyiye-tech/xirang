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


class CreateVdcUserGroupRequest(CTYunRequest):
    """
    创建VDC用户组
    """

    def __init__(self, request_param):
        super(CreateVdcUserGroupRequest, self).__init__("/v1/vdc/create-user-group", "POST", "iam", "application/json")
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
        if self.parameters.org_id is not None:
            body_param["orgID"] = self.parameters.org_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class CreateVdcUserGroupRequestParam(object):

    def __init__(self, org_id, name, description=None):
        """
        :param org_id: vdc的id
        :param name: 用户组名称
        :param description: 描述
        """
        self.org_id = org_id
        self.name = name
        self.description = description

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.org_id is None:
            raise Exception("org_id can not None")
        if self.name is None:
            raise Exception("name can not None")

