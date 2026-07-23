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


class PermissionRuleModifyRequest(CTYunRequest):
    """
    1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 默认权限组不支持创建规则   
    * 入参：公有云没有permissionGroupID参数，兼容v1加入permissionGroupID入参，修改为非必填参数，传了permissionGroupID会对该参数校验；   
    * 返参 v1的returnObj是数组类型，公有云是object类型；   
    
    """

    def __init__(self, request_param):
        super(PermissionRuleModifyRequest, self).__init__("/v4/sfs/permission-rule/modify", "POST", "sfs", "application/json")
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
        if self.parameters.permission_group_id is not None:
            body_param["permissionGroupID"] = self.parameters.permission_group_id
        if self.parameters.permission_rule_id is not None:
            body_param["permissionRuleID"] = self.parameters.permission_rule_id
        if self.parameters.rw_permission is not None:
            body_param["rwPermission"] = self.parameters.rw_permission
        if self.parameters.user_permission is not None:
            body_param["userPermission"] = self.parameters.user_permission
        if self.parameters.auth_addr is not None:
            body_param["authAddr"] = self.parameters.auth_addr
        if self.parameters.priority is not None:
            body_param["priority"] = self.parameters.priority
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


class PermissionRuleModifyRequestParam(object):

    def __init__(self, region_id, permission_rule_id, rw_permission, user_permission, auth_addr, priority, permission_group_id=None):
        """
        :param region_id: 资源池ID
        :param permission_group_id: 权限组ID
        :param permission_rule_id: 权限组规则ID
        :param rw_permission: 有效值范围： rw、ro
        :param user_permission: 有效值范围：no_root_squash
        :param auth_addr: 授权地址
        :param priority: 1-400
        """
        self.region_id = region_id
        self.permission_group_id = permission_group_id
        self.permission_rule_id = permission_rule_id
        self.rw_permission = rw_permission
        self.user_permission = user_permission
        self.auth_addr = auth_addr
        self.priority = priority

    def set_permission_group_id(self, permission_group_id):
        """
        :param permission_group_id: 权限组ID
        """
        self.permission_group_id = permission_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.permission_rule_id is None:
            raise Exception("permission_rule_id can not None")
        if self.rw_permission is None:
            raise Exception("rw_permission can not None")
        if self.user_permission is None:
            raise Exception("user_permission can not None")
        if self.auth_addr is None:
            raise Exception("auth_addr can not None")
        if self.priority is None:
            raise Exception("priority can not None")

