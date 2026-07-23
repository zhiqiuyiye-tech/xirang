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


class QueryCreateNatPriceRequest(CTYunRequest):
    """
    非询价必需字段不做校验，只透传
    """

    def __init__(self, request_param):
        super(QueryCreateNatPriceRequest, self).__init__("/v4/nat/query-create-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
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


class QueryCreateNatPriceRequestParam(object):

    def __init__(self, region_id, spec, cycle_type, cycle_count=None, client_token=None, az_name=None, description=None, name=None, vpc_id=None):
        """
        :param region_id: 资源池id
        :param spec: 规格，规格 1~4, 1表示小型, 2表示中型, 3表示大型, 4表示超大型
        :param cycle_type: 订购类型：month / year，为按需计费类型时传on_demand
        :param cycle_count: 订购时长，为按需计费类型时该值不予处理，即不校验不引用传参内容；包年包月订购时长大于等于1
        :param client_token: 客户端 Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        :param az_name: 非询价必需字段 可用区名称
        :param description: 非询价必需字段 描述信息
        :param name: 非询价必需字段 NAT网关名称
        :param vpc_id: 非询价必需字段 虚拟私有云id
        """
        self.region_id = region_id
        self.spec = spec
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.client_token = client_token
        self.az_name = az_name
        self.description = description
        self.name = name
        self.vpc_id = vpc_id

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，为按需计费类型时该值不予处理，即不校验不引用传参内容；包年包月订购时长大于等于1
        """
        self.cycle_count = cycle_count

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端 Token，用于保证请求的幂等性（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 非询价必需字段 可用区名称
        """
        self.az_name = az_name

    def set_description(self, description):
        """
        :param description: 非询价必需字段 描述信息
        """
        self.description = description

    def set_name(self, name):
        """
        :param name: 非询价必需字段 NAT网关名称
        """
        self.name = name

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 非询价必需字段 虚拟私有云id
        """
        self.vpc_id = vpc_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.spec is None:
            raise Exception("spec can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

