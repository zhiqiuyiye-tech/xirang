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


class OpenapiGetPermissionListRequest(CTYunRequest):
    """
    查询权限列表
    """

    def __init__(self, request_param):
        super(OpenapiGetPermissionListRequest, self).__init__("/v1/permission/getPermissionList", "GET", "iam", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.permission_name is not None:
            query_param["permissionName"] = self.parameters.permission_name
        if self.parameters.permission_code is not None:
            query_param["permissionCode"] = self.parameters.permission_code
        if self.parameters.permission_type is not None:
            query_param["permissionType"] = self.parameters.permission_type
        if self.parameters.service_name is not None:
            query_param["serviceName"] = self.parameters.service_name
        if self.parameters.url is not None:
            query_param["url"] = self.parameters.url
        if self.parameters.open_url is not None:
            query_param["openUrl"] = self.parameters.open_url
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenapiGetPermissionListRequestParam(object):

    def __init__(self, page=None, page_size=None, permission_name=None, permission_code=None, permission_type=None, service_name=None, url=None, open_url=None):
        """
        :param page: 页码, 需大于0,缺省时为1
        :param page_size: 页大小,需大于0,缺省时为10
        :param permission_name: 权限名称,模糊匹配
        :param permission_code: 权限编码,模糊匹配
        :param permission_type: 权限类型, 1-读 2-写
        :param service_name: 服务名称,模糊匹配
        :param url: url,模糊匹配
        :param open_url: openUrl,模糊匹配
        """
        self.page = page
        self.page_size = page_size
        self.permission_name = permission_name
        self.permission_code = permission_code
        self.permission_type = permission_type
        self.service_name = service_name
        self.url = url
        self.open_url = open_url

    def set_page(self, page):
        """
        :param page: 页码, 需大于0,缺省时为1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小,需大于0,缺省时为10
        """
        self.page_size = page_size

    def set_permission_name(self, permission_name):
        """
        :param permission_name: 权限名称,模糊匹配
        """
        self.permission_name = permission_name

    def set_permission_code(self, permission_code):
        """
        :param permission_code: 权限编码,模糊匹配
        """
        self.permission_code = permission_code

    def set_permission_type(self, permission_type):
        """
        :param permission_type: 权限类型, 1-读 2-写
        """
        self.permission_type = permission_type

    def set_service_name(self, service_name):
        """
        :param service_name: 服务名称,模糊匹配
        """
        self.service_name = service_name

    def set_url(self, url):
        """
        :param url: url,模糊匹配
        """
        self.url = url

    def set_open_url(self, open_url):
        """
        :param open_url: openUrl,模糊匹配
        """
        self.open_url = open_url

    def check_param(self):
        """
        the param required check
        """
        pass

