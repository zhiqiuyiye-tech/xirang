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


class UpdateSubnetRequest(CTYunRequest):
    """
    修改子网的属性：名称、描述。
    """

    def __init__(self, request_param):
        super(UpdateSubnetRequest, self).__init__("/v4/vpc/update-subnet", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.dns_list is not None:
            body_param["dnsList"] = self.parameters.dns_list
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


class UpdateSubnetRequestParam(object):

    def __init__(self, region_id, subnet_id, client_token=None, name=None, description=None, az_name=None, project_id=None, dns_list=None):
        """
        :param region_id: 资源池 ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param subnet_id: 子网 的 ID
        :param name: 只能由数字，字母，中文，下划线，连字符组成，中文 / 英文字母开头，不能以 http: / https: 开头，长度 2 - 32
        :param description: 子网 描述。内容限制：参考创建子网接口
        :param az_name: 可用区名称   
         （差异点说明：2.0此参数实际无意义）
        :param project_id: 企业项目 ID，默认为"0"（非必填，并且此字段在私有云不具有实际意义）
        :param dns_list: 子网 dns 列表, 最多同时支持 4 个 dns 地址（差异点：V1无此参数，V2对齐公有云文档，支持该功能） 注意:此参数为数组
        """
        self.region_id = region_id
        self.client_token = client_token
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.az_name = az_name
        self.project_id = project_id
        self.dns_list = dns_list

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 只能由数字，字母，中文，下划线，连字符组成，中文 / 英文字母开头，不能以 http: / https: 开头，长度 2 - 32
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 子网 描述。内容限制：参考创建子网接口
        """
        self.description = description

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称   
         （差异点说明：2.0此参数实际无意义）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为"0"（非必填，并且此字段在私有云不具有实际意义）
        """
        self.project_id = project_id

    def set_dns_list(self, dns_list):
        """
        :param dns_list: 子网 dns 列表, 最多同时支持 4 个 dns 地址（差异点：V1无此参数，V2对齐公有云文档，支持该功能）
        """
        self.dns_list = dns_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

