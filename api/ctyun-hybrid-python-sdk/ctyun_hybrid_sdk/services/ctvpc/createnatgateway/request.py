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


class CreateNatGatewayRequest(CTYunRequest):
    """
    创建NAT网关
    """

    def __init__(self, request_param):
        super(CreateNatGatewayRequest, self).__init__("/v4/vpc/create-nat-gateway", "POST", "ctvpc", "application/json")
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
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
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


class CreateNatGatewayRequestParam(object):

    def __init__(self, region_id, vpc_id, name, spec, cycle_type, cycle_count=None, az_name=None, description=None, client_token=None, subnet_id=None, project_id=None):
        """
        :param region_id: 资源池id
        :param vpc_id: 虚拟私有云id
        :param name: NAT网关名称（2-32长度，只允许中文、英文、数字和特殊字符-, _，只能以中文和英文开头）
        :param spec: 规格，目前只支持1-小型、2-中型、3-大型、4-超大型
        :param cycle_type: 订购类型：month / year，为按需计费类型时传on_demand
        :param cycle_count: 订购时长，订购类型包年/包月时 此参数必填；订购时长为1-11月，或1-3年
        :param az_name: 可用区名称(4.0必填，3.0不用填）
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        :param client_token: 客户端 Token，用于保证请求的幂等性
        :param subnet_id: 子网ID，只有部分4.0资源池支持配置子网
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.name = name
        self.spec = spec
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.az_name = az_name
        self.description = description
        self.client_token = client_token
        self.subnet_id = subnet_id
        self.project_id = project_id

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，订购类型包年/包月时 此参数必填；订购时长为1-11月，或1-3年
        """
        self.cycle_count = cycle_count

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(4.0必填，3.0不用填）
        """
        self.az_name = az_name

    def set_description(self, description):
        """
        :param description: 描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端 Token，用于保证请求的幂等性
        """
        self.client_token = client_token

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网ID，只有部分4.0资源池支持配置子网
        """
        self.subnet_id = subnet_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.spec is None:
            raise Exception("spec can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")

