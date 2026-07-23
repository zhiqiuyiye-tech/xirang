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


class UpdateIAMUserGroupRequest(CTYunRequest):
    """
    IAM认证-用户组编辑
    """

    def __init__(self, request_param):
        super(UpdateIAMUserGroupRequest, self).__init__("/v1/userGroup/iam/update", "POST", "iam", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
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


class UpdateIAMUserGroupRequestParam(object):

    def __init__(self, name, group_id, description=None):
        """
        :param name: 长度为3-20字符,支持使用中文、英文字母、数字、下划线（_）、中划线（-）、括号、空格
        :param description: 最长长度为100字符
        :param group_id: 用户组id
        """
        self.name = name
        self.description = description
        self.group_id = group_id

    def set_description(self, description):
        """
        :param description: 最长长度为100字符
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

