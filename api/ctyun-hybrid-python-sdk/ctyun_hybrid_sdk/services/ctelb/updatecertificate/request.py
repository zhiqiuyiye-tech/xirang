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


class UpdateCertificateRequest(CTYunRequest):
    """
    更新证书
    """

    def __init__(self, request_param):
        super(UpdateCertificateRequest, self).__init__("/v4/elb/update-certificate", "POST", "ctelb", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class UpdateCertificateRequestParam(object):

    def __init__(self, region_id, id, name=None, description=None, az_name=None, client_token=None, project_id=None):
        """
        :param region_id: 区域ID
        :param id: 证书id
        :param name: 证书名称,支持字母、中文、数字，下划线，连字符，中文 / 英文字母开头，长度 2 - 32
        :param description: 证书描述
        :param az_name: 私有云不需要，不做校验，可以忽略。
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 暂无实际功能
        """
        self.region_id = region_id
        self.id = id
        self.name = name
        self.description = description
        self.az_name = az_name
        self.client_token = client_token
        self.project_id = project_id

    def set_name(self, name):
        """
        :param name: 证书名称,支持字母、中文、数字，下划线，连字符，中文 / 英文字母开头，长度 2 - 32
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 证书描述
        """
        self.description = description

    def set_az_name(self, az_name):
        """
        :param az_name: 私有云不需要，不做校验，可以忽略。
        """
        self.az_name = az_name

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 暂无实际功能
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

