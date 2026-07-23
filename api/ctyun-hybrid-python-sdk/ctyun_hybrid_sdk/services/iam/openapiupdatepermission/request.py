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


class OpenapiUpdatePermissionRequest(CTYunRequest):
    """
    权限修改
    """

    def __init__(self, request_param):
        super(OpenapiUpdatePermissionRequest, self).__init__("/v1/permission/updatePermission", "POST", "iam", "application/json")
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
        if self.parameters.permission_id is not None:
            body_param["permissionID"] = self.parameters.permission_id
        if self.parameters.permission_name is not None:
            body_param["permissionName"] = self.parameters.permission_name
        if self.parameters.permission_description is not None:
            body_param["permissionDescription"] = self.parameters.permission_description
        if self.parameters.permission_urls is not None:
            body_param["permissionUrls"] = self.parameters.permission_urls
        if self.parameters.data_version is not None:
            body_param["dataVersion"] = self.parameters.data_version
        if self.parameters.openapi_urls is not None:
            body_param["openapiUrls"] = self.parameters.openapi_urls
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


class OpenapiUpdatePermissionRequestParam(object):

    def __init__(self, permission_id, permission_name, permission_description=None, permission_urls=None, data_version=None, openapi_urls=None):
        """
        :param permission_id: 权限ID
        :param permission_name: 长度为3-20字符   
         支持中文汉字，大、小写字母和数字，支持特殊符号下划线、中划线、括号
        :param permission_description: 权限描述
        :param permission_urls: 权限对应的后端URL列表
        :param data_version: 数据的版本
        :param openapi_urls: 关联的openapiurl
        """
        self.permission_id = permission_id
        self.permission_name = permission_name
        self.permission_description = permission_description
        self.permission_urls = permission_urls
        self.data_version = data_version
        self.openapi_urls = openapi_urls

    def set_permission_description(self, permission_description):
        """
        :param permission_description: 权限描述
        """
        self.permission_description = permission_description

    def set_permission_urls(self, permission_urls):
        """
        :param permission_urls: 权限对应的后端URL列表
        """
        self.permission_urls = permission_urls

    def set_data_version(self, data_version):
        """
        :param data_version: 数据的版本
        """
        self.data_version = data_version

    def set_openapi_urls(self, openapi_urls):
        """
        :param openapi_urls: 关联的openapiurl
        """
        self.openapi_urls = openapi_urls

    def check_param(self):
        """
        the param required check
        """
        if self.permission_id is None:
            raise Exception("permission_id can not None")
        if self.permission_name is None:
            raise Exception("permission_name can not None")

