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


class SfsModifyPermissionSfsRequest(CTYunRequest):
    """
    不支持修改默认权限组
    """

    def __init__(self, request_param):
        super(SfsModifyPermissionSfsRequest, self).__init__("/v4/sfs/permission-group/modify-permission-group", "POST", "sfs", "application/json")
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
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.permission_group_fuid is not None:
            body_param["permissionGroupFuid"] = self.parameters.permission_group_fuid
        if self.parameters.permission_group_name is not None:
            body_param["permissionGroupName"] = self.parameters.permission_group_name
        if self.parameters.permission_group_description is not None:
            body_param["permissionGroupDescription"] = self.parameters.permission_group_description
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


class SfsModifyPermissionSfsRequestParam(object):

    def __init__(self, region_id, permission_group_fuid, permission_group_name=None, permission_group_description=None):
        """
        :param region_id: 资源池ID
        :param permission_group_fuid: 权限组ID
        :param permission_group_name: 限组名字。permissionGroupName和permissionGroupDescription至少输入一个。permissionGroupName不允许重复，长度为2～63字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param permission_group_description: 权限组描述信息。permissionGroupName和permissionGroupDescription至少输入一个，最大长度为128字符
        """
        self.region_id = region_id
        self.permission_group_fuid = permission_group_fuid
        self.permission_group_name = permission_group_name
        self.permission_group_description = permission_group_description

    def set_permission_group_name(self, permission_group_name):
        """
        :param permission_group_name: 限组名字。permissionGroupName和permissionGroupDescription至少输入一个。permissionGroupName不允许重复，长度为2～63字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        """
        self.permission_group_name = permission_group_name

    def set_permission_group_description(self, permission_group_description):
        """
        :param permission_group_description: 权限组描述信息。permissionGroupName和permissionGroupDescription至少输入一个，最大长度为128字符
        """
        self.permission_group_description = permission_group_description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.permission_group_fuid is None:
            raise Exception("permission_group_fuid can not None")

