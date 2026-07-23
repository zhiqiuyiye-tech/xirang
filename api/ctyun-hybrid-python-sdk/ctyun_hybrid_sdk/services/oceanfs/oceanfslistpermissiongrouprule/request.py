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


class OceanfsListPermissionGroupRuleRequest(CTYunRequest):
    """
    海量文件返回权限组规则描述信息
    """

    def __init__(self, request_param):
        super(OceanfsListPermissionGroupRuleRequest, self).__init__("/v4/oceanfs/permission-rule/list-permission-rule", "GET", "oceanfs", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.permission_group_fuid is not None:
            query_param["permissionGroupFuid"] = self.parameters.permission_group_fuid
        if self.parameters.permission_group_id is not None:
            query_param["permissionGroupID"] = self.parameters.permission_group_id
        if self.parameters.permission_rule_fuid is not None:
            query_param["permissionRuleFuid"] = self.parameters.permission_rule_fuid
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OceanfsListPermissionGroupRuleRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, permission_group_fuid=None, permission_group_id=None, permission_rule_fuid=None):
        """
        :param page_no: 页数。默认为1
        :param page_size: 每页的个数。默认为10，范围[1-100]，大于100取100，不传、传0取10
        :param region_id: 资源池id
        :param permission_group_fuid: 权限组fuid(混合云暂不支持，可填入权限组ID值)
        :param permission_group_id: 权限组ID
        :param permission_rule_fuid: 权限组规则的fuid(混合云暂不支持该字段查询)
        """
        self.page_no = page_no
        self.page_size = page_size
        self.region_id = region_id
        self.permission_group_fuid = permission_group_fuid
        self.permission_group_id = permission_group_id
        self.permission_rule_fuid = permission_rule_fuid

    def set_page_no(self, page_no):
        """
        :param page_no: 页数。默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页的个数。默认为10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_permission_group_fuid(self, permission_group_fuid):
        """
        :param permission_group_fuid: 权限组fuid(混合云暂不支持，可填入权限组ID值)
        """
        self.permission_group_fuid = permission_group_fuid

    def set_permission_group_id(self, permission_group_id):
        """
        :param permission_group_id: 权限组ID
        """
        self.permission_group_id = permission_group_id

    def set_permission_rule_fuid(self, permission_rule_fuid):
        """
        :param permission_rule_fuid: 权限组规则的fuid(混合云暂不支持该字段查询)
        """
        self.permission_rule_fuid = permission_rule_fuid

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

