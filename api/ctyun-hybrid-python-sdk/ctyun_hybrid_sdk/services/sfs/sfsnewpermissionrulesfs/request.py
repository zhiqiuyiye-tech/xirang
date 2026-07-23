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


class SfsNewPermissionRuleSfsRequest(CTYunRequest):
    """
    1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 支持ipv4，ipv6。同一权限组，创建权限组规则的时候下面的authAddr不能重复   
    4. 当前接口使用前请使用资源池概况信息查询接口查询对应的资源池信息，如资源池信息"regionVersion": "v4.0",即可使用；如资源池信息"regionVersion": "v3.0", 则不可使用。   
    5. V2云管侧userPermission暂只支持no_root_squash权限
    """

    def __init__(self, request_param):
        super(SfsNewPermissionRuleSfsRequest, self).__init__("/v4/sfs/permission-rule/new-permission-rule", "POST", "sfs", "application/json")
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
        if self.parameters.permission_group_fuid is not None:
            body_param["permissionGroupFuid"] = self.parameters.permission_group_fuid
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
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


class SfsNewPermissionRuleSfsRequestParam(object):

    def __init__(self, permission_group_fuid, region_id, auth_addr, rw_permission, user_permission, permission_rule_priority, ):
        """
        :param permission_group_fuid: 权限组ID
        :param region_id: 资源池ID
        :param auth_addr: 允许单个IP或网段，如：10.10.1.123或192.168.3.0/24，格式: ipv4/ipv6
        :param rw_permission: 枚举：rw/ro
        :param user_permission: 枚举: no_root_squash,root_squash,all_squash
        :param permission_rule_priority: 最大值: 400、最小值: 1
        """
        self.permission_group_fuid = permission_group_fuid
        self.region_id = region_id
        self.auth_addr = auth_addr
        self.rw_permission = rw_permission
        self.user_permission = user_permission
        self.permission_rule_priority = permission_rule_priority

    def check_param(self):
        """
        the param required check
        """
        if self.permission_group_fuid is None:
            raise Exception("permission_group_fuid can not None")
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

