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


class ListIAMUserGroupsRequest(CTYunRequest):
    """
    IAM认证-用户组列表查询
    """

    def __init__(self, request_param):
        super(ListIAMUserGroupsRequest, self).__init__("/v1/userGroup/iam/list", "GET", "iam", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.role_type is not None:
            query_param["roleType"] = self.parameters.role_type
        if self.parameters.hmac_verify_status is not None:
            query_param["hmacVerifyStatus"] = self.parameters.hmac_verify_status
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListIAMUserGroupsRequestParam(object):

    def __init__(self, page, page_size, name=None, role_type=None, hmac_verify_status=None):
        """
        :param name: 用户组名称，支持模糊查询
        :param role_type: 用户组类型，1:系统默认,6:用户自定义，系统默认类型的用户组其中包括1:运营管理员,2:代维管理员,3:vdc管理员,4:vdc业务员5:vdc只读管理员
        :param hmac_verify_status: 完整性校验状态，1-未验证 3-验证成功 4-验证失败 2-验证中
        :param page: 页数
        :param page_size: 每页显示条数，最大为100
        """
        self.name = name
        self.role_type = role_type
        self.hmac_verify_status = hmac_verify_status
        self.page = page
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 用户组名称，支持模糊查询
        """
        self.name = name

    def set_role_type(self, role_type):
        """
        :param role_type: 用户组类型，1:系统默认,6:用户自定义，系统默认类型的用户组其中包括1:运营管理员,2:代维管理员,3:vdc管理员,4:vdc业务员5:vdc只读管理员
        """
        self.role_type = role_type

    def set_hmac_verify_status(self, hmac_verify_status):
        """
        :param hmac_verify_status: 完整性校验状态，1-未验证 3-验证成功 4-验证失败 2-验证中
        """
        self.hmac_verify_status = hmac_verify_status

    def check_param(self):
        """
        the param required check
        """
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

