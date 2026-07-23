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


class OpenapiCreatePermissionRequest(CTYunRequest):
    """
    权限新增
    """

    def __init__(self, request_param):
        super(OpenapiCreatePermissionRequest, self).__init__("/v1/permission/createPermission", "POST", "iam", "application/json")
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
        if self.parameters.permission_name is not None:
            body_param["permissionName"] = self.parameters.permission_name
        if self.parameters.service_code is not None:
            body_param["serviceCode"] = self.parameters.service_code
        if self.parameters.permission_code is not None:
            body_param["permissionCode"] = self.parameters.permission_code
        if self.parameters.permission_urls is not None:
            body_param["permissionUrls"] = self.parameters.permission_urls
        if self.parameters.openapi_urls is not None:
            body_param["openapiUrls"] = self.parameters.openapi_urls
        if self.parameters.permission_type is not None:
            body_param["permissionType"] = self.parameters.permission_type
        if self.parameters.data_version is not None:
            body_param["dataVersion"] = self.parameters.data_version
        if self.parameters.permission_description is not None:
            body_param["permissionDescription"] = self.parameters.permission_description
        if self.parameters.service_name is not None:
            body_param["serviceName"] = self.parameters.service_name
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


class OpenapiCreatePermissionRequestParam(object):

    def __init__(self, permission_name, service_code, permission_code, permission_type, data_version, service_name, permission_urls=None, openapi_urls=None, permission_description=None):
        """
        :param permission_name: 长度为3-20字符   
         支持中文汉字，大、小写字母和数字，支持特殊符号下划线、中划线、括号
        :param service_code: 服务编码
        :param permission_code: 权限编码
        :param permission_urls: 权限对应的后端URL列表
        :param openapi_urls: 关联的openapiurl
        :param permission_type: 1：读权限，2：写权
        :param data_version: 数据的版本
        :param permission_description: 权限描述
        :param service_name: 服务名称
        """
        self.permission_name = permission_name
        self.service_code = service_code
        self.permission_code = permission_code
        self.permission_urls = permission_urls
        self.openapi_urls = openapi_urls
        self.permission_type = permission_type
        self.data_version = data_version
        self.permission_description = permission_description
        self.service_name = service_name

    def set_permission_urls(self, permission_urls):
        """
        :param permission_urls: 权限对应的后端URL列表
        """
        self.permission_urls = permission_urls

    def set_openapi_urls(self, openapi_urls):
        """
        :param openapi_urls: 关联的openapiurl
        """
        self.openapi_urls = openapi_urls

    def set_permission_description(self, permission_description):
        """
        :param permission_description: 权限描述
        """
        self.permission_description = permission_description

    def check_param(self):
        """
        the param required check
        """
        if self.permission_name is None:
            raise Exception("permission_name can not None")
        if self.service_code is None:
            raise Exception("service_code can not None")
        if self.permission_code is None:
            raise Exception("permission_code can not None")
        if self.permission_type is None:
            raise Exception("permission_type can not None")
        if self.data_version is None:
            raise Exception("data_version can not None")
        if self.service_name is None:
            raise Exception("service_name can not None")

