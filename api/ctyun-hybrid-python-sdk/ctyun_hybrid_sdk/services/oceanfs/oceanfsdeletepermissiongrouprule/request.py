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


class OceanfsDeletePermissionGroupRuleRequest(CTYunRequest):
    """
    海量文件删除权限组规则
    """

    def __init__(self, request_param):
        super(OceanfsDeletePermissionGroupRuleRequest, self).__init__("/v4/oceanfs/permission-rule/delete-permission-rule", "POST", "oceanfs", "application/json")
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
        if self.parameters.permission_rule_fuid is not None:
            body_param["permissionRuleFuid"] = self.parameters.permission_rule_fuid
        if self.parameters.permission_rule_id is not None:
            body_param["permissionRuleID"] = self.parameters.permission_rule_id
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


class OceanfsDeletePermissionGroupRuleRequestParam(object):

    def __init__(self, region_id, permission_rule_fuid=None, permission_rule_id=None):
        """
        :param region_id: 资源池ID
        :param permission_rule_fuid: 权限组规则的fuid(混合云暂不支持，可填入权限组规则ID值)   
         permissionRuleFuid或permissionRuleID必传其中一个
        :param permission_rule_id: 权限组规则ID permissionRuleFuid或permissionRuleID必传其中一个
        """
        self.region_id = region_id
        self.permission_rule_fuid = permission_rule_fuid
        self.permission_rule_id = permission_rule_id

    def set_permission_rule_fuid(self, permission_rule_fuid):
        """
        :param permission_rule_fuid: 权限组规则的fuid(混合云暂不支持，可填入权限组规则ID值)   
         permissionRuleFuid或permissionRuleID必传其中一个
        """
        self.permission_rule_fuid = permission_rule_fuid

    def set_permission_rule_id(self, permission_rule_id):
        """
        :param permission_rule_id: 权限组规则ID permissionRuleFuid或permissionRuleID必传其中一个
        """
        self.permission_rule_id = permission_rule_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

