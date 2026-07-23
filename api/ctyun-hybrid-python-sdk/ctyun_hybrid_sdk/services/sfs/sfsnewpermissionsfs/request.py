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


class SfsNewPermissionSfsRequest(CTYunRequest):
    """
    租户在某个资源池下的权限组个数上限目前为20个   
    
    """

    def __init__(self, request_param):
        super(SfsNewPermissionSfsRequest, self).__init__("/v4/sfs/permission-group/new-permission-group", "POST", "sfs", "application/json")
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
        if self.parameters.permission_group_name is not None:
            body_param["permissionGroupName"] = self.parameters.permission_group_name
        if self.parameters.network_type is not None:
            body_param["networkType"] = self.parameters.network_type
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


class SfsNewPermissionSfsRequestParam(object):

    def __init__(self, region_id, permission_group_name, network_type, permission_group_description=None):
        """
        :param region_id: 资源池ID
        :param permission_group_name: 权限组名字。名字不能重复，长度为2-63字符，只能由数字、字母、-组成，不能以数字和-开头、且不能以-结尾。
        :param network_type: 有效值范围：private_network
        :param permission_group_description: 长度为0-128字符
        """
        self.region_id = region_id
        self.permission_group_name = permission_group_name
        self.network_type = network_type
        self.permission_group_description = permission_group_description

    def set_permission_group_description(self, permission_group_description):
        """
        :param permission_group_description: 长度为0-128字符
        """
        self.permission_group_description = permission_group_description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.permission_group_name is None:
            raise Exception("permission_group_name can not None")
        if self.network_type is None:
            raise Exception("network_type can not None")

