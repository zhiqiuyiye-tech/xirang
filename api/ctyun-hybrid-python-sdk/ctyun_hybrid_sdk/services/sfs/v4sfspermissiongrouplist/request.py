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


class V4SfsPermissionGroupListRequest(CTYunRequest):
    """
    弹性文件返回权限组描述信息
    """

    def __init__(self, request_param):
        super(V4SfsPermissionGroupListRequest, self).__init__("/v4/sfs/permission-group/list", "GET", "sfs", "")
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
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.permission_group_id is not None:
            query_param["permissionGroupID"] = self.parameters.permission_group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class V4SfsPermissionGroupListRequestParam(object):

    def __init__(self, region_id, page_size=None, page_no=None, permission_group_id=None):
        """
        :param region_id: 资源池id
        :param page_size: 每页元素数量，默认值10，范围[1-100]，大于100取100，不传、传0取10
        :param page_no: 页码，默认值1
        :param permission_group_id: 权限组的 fuid	
        """
        self.region_id = region_id
        self.page_size = page_size
        self.page_no = page_no
        self.permission_group_id = permission_group_id

    def set_page_size(self, page_size):
        """
        :param page_size: 每页元素数量，默认值10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1
        """
        self.page_no = page_no

    def set_permission_group_id(self, permission_group_id):
        """
        :param permission_group_id: 权限组的 fuid	
        """
        self.permission_group_id = permission_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

