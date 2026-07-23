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


class OpenapiCreateServiceRequest(CTYunRequest):
    """
    服务管理创建
    """

    def __init__(self, request_param):
        super(OpenapiCreateServiceRequest, self).__init__("/v1/service/createService", "POST", "iam", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.cloud_type is not None:
            body_param["cloudType"] = self.parameters.cloud_type
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.code is not None:
            body_param["code"] = self.parameters.code
        if self.parameters.data_version is not None:
            body_param["dataVersion"] = self.parameters.data_version
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


class OpenapiCreateServiceRequestParam(object):

    def __init__(self, name, cloud_type, type, code, data_version=None):
        """
        :param name: 长度为2-20字符   
         支持中文汉字，大、小写字母和数字，支持特殊符号下划线、中划线、括号
        :param cloud_type: 3- 天翼云自研池子 11-VMWARE 50-ZSTACK
        :param type: 1 资源池级 2 全局级
        :param code: 长度为2-30字符   
         支持大、小写字母、数字，支持特殊符号下划线、中划线、英文括号
        :param data_version: 数据版本
        """
        self.name = name
        self.cloud_type = cloud_type
        self.type = type
        self.code = code
        self.data_version = data_version

    def set_data_version(self, data_version):
        """
        :param data_version: 数据版本
        """
        self.data_version = data_version

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.cloud_type is None:
            raise Exception("cloud_type can not None")
        if self.type is None:
            raise Exception("type can not None")
        if self.code is None:
            raise Exception("code can not None")

