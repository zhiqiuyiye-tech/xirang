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


class OceanfsNewPermissionGroupRuleRequest(CTYunRequest):
    """
    海量文件创建权限组规则
    """

    def __init__(self, request_param):
        super(OceanfsNewPermissionGroupRuleRequest, self).__init__("/v4/oceanfs/permission-rule/new-permission-rule", "POST", "oceanfs", "application/json")
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
        if self.parameters.permission_group_id is not None:
            body_param["permissionGroupID"] = self.parameters.permission_group_id
        if self.parameters.auth_addr is not None:
            body_param["authAddr"] = self.parameters.auth_addr
        if self.parameters.rw_permission is not None:
            body_param["rwPermission"] = self.parameters.rw_permission
        if self.parameters.user_permission is not None:
            body_param["userPermission"] = self.parameters.user_permission
        if self.parameters.permission_rule_priority is not None:
            body_param["permissionRulePriority"] = self.parameters.permission_rule_priority
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


class OceanfsNewPermissionGroupRuleRequestParam(object):

    def __init__(self, region_id, auth_addr, rw_permission, user_permission, permission_rule_priority, permission_group_fuid=None, permission_group_id=None):
        """
        :param region_id: 资源池ID
        :param permission_group_fuid: 权限组fuid(混合云暂不支持，可填入权限组ID值)   
         permissionGroupFuid或permissionGroupID必传其中一个
        :param permission_group_id: 权限组ID permissionGroupFuid或permissionGroupID必传其中一个
        :param auth_addr: 授权地址
        :param rw_permission: 读写权限控制。有效值范围：rw、ro
        :param user_permission: nfs 访问用户映射。有效值范围：no_root_squash
        :param permission_rule_priority: 优先级。有效值范围：1-400
        """
        self.region_id = region_id
        self.permission_group_fuid = permission_group_fuid
        self.permission_group_id = permission_group_id
        self.auth_addr = auth_addr
        self.rw_permission = rw_permission
        self.user_permission = user_permission
        self.permission_rule_priority = permission_rule_priority

    def set_permission_group_fuid(self, permission_group_fuid):
        """
        :param permission_group_fuid: 权限组fuid(混合云暂不支持，可填入权限组ID值)   
         permissionGroupFuid或permissionGroupID必传其中一个
        """
        self.permission_group_fuid = permission_group_fuid

    def set_permission_group_id(self, permission_group_id):
        """
        :param permission_group_id: 权限组ID permissionGroupFuid或permissionGroupID必传其中一个
        """
        self.permission_group_id = permission_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.auth_addr is None:
            raise Exception("auth_addr can not None")
        if self.rw_permission is None:
            raise Exception("rw_permission can not None")
        if self.user_permission is None:
            raise Exception("user_permission can not None")
        if self.permission_rule_priority is None:
            raise Exception("permission_rule_priority can not None")

