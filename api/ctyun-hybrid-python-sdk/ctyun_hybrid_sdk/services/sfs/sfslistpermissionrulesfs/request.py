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


class SfsListPermissionRuleSfsRequest(CTYunRequest):
    """
    注意：   
    1. permissionGroupFuid和permissionRuleFuid至少存在一个   
    2. pageNo默认为1，pageSize默认为10，取值[1, 100]，超过上限时默认取上限值   
    3. 当前接口使用前请使用资源池概况信息查询接口查询对应的资源池信息，如资源池信息"regionVersion": "v4.0",即可使用；如资源池信息"regionVersion": "v3.0", 则不可使用。
    """

    def __init__(self, request_param):
        super(SfsListPermissionRuleSfsRequest, self).__init__("/v4/sfs/permission-rule/list-permission-rule", "GET", "sfs", "")
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
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.permission_group_fuid is not None:
            query_param["permissionGroupFuid"] = self.parameters.permission_group_fuid
        if self.parameters.permission_rule_fuid is not None:
            query_param["permissionRuleFuid"] = self.parameters.permission_rule_fuid
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class SfsListPermissionRuleSfsRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, permission_group_fuid=None, permission_rule_fuid=None):
        """
        :param region_id: 资源池ID
        :param page_no: 页数，默认为1
        :param page_size: 每页个数，取值范围[1, 100]，默认为10，超过上限为默认最大值，不传、传0取10
        :param permission_group_fuid: 权限组ID；permissionGroupFuid和permissionRuleFuid至少存在一个
        :param permission_rule_fuid: 权限组规则ID；permissionGroupFuid和permissionRuleFuid至少存在一个
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.permission_group_fuid = permission_group_fuid
        self.permission_rule_fuid = permission_rule_fuid

    def set_page_no(self, page_no):
        """
        :param page_no: 页数，默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页个数，取值范围[1, 100]，默认为10，超过上限为默认最大值，不传、传0取10
        """
        self.page_size = page_size

    def set_permission_group_fuid(self, permission_group_fuid):
        """
        :param permission_group_fuid: 权限组ID；permissionGroupFuid和permissionRuleFuid至少存在一个
        """
        self.permission_group_fuid = permission_group_fuid

    def set_permission_rule_fuid(self, permission_rule_fuid):
        """
        :param permission_rule_fuid: 权限组规则ID；permissionGroupFuid和permissionRuleFuid至少存在一个
        """
        self.permission_rule_fuid = permission_rule_fuid

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

