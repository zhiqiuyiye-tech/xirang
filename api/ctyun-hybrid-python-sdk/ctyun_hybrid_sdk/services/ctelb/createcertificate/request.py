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


class CreateCertificateRequest(CTYunRequest):
    """
    创建证书   
       
    #### 备注   
    * 不支持3.0，因为3.0 是异步逻辑，4.0 是同步逻辑
    """

    def __init__(self, request_param):
        super(CreateCertificateRequest, self).__init__("/v4/elb/create-certificate", "POST", "ctelb", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.private_key is not None:
            body_param["privateKey"] = self.parameters.private_key
        if self.parameters.certificate is not None:
            body_param["certificate"] = self.parameters.certificate
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
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


class CreateCertificateRequestParam(object):

    def __init__(self, region_id, name, certificate, type, description=None, private_key=None, az_name=None, client_token=None, project_id=None):
        """
        :param region_id: 区域ID
        :param name: 监听器证书名称
        :param description: 描述
        :param private_key: 服务器证书私钥，服务器证书此字段必填
        :param certificate: type为Server该字段表示服务器证书公钥Pem内容;type为Ca该字段表示Ca证书Pem内容
        :param type: 证书类型。取值范围：Server（服务器证书）、Ca（Ca证书）
        :param az_name: 私有云不需要，不做校验，可以忽略。
        :param client_token: 客户端Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 暂无实际功能
        """
        self.region_id = region_id
        self.name = name
        self.description = description
        self.private_key = private_key
        self.certificate = certificate
        self.type = type
        self.az_name = az_name
        self.client_token = client_token
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_private_key(self, private_key):
        """
        :param private_key: 服务器证书私钥，服务器证书此字段必填
        """
        self.private_key = private_key

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
        if self.name is None:
            raise Exception("name can not None")
        if self.certificate is None:
            raise Exception("certificate can not None")
        if self.type is None:
            raise Exception("type can not None")

