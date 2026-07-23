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


class NewSfsRequest(CTYunRequest):
    """
    创建文件系统
    """

    def __init__(self, request_param):
        super(NewSfsRequest, self).__init__("/v4/oceanfs/new-sfs", "POST", "oceanfs", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.sfs_name is not None:
            body_param["sfsName"] = self.parameters.sfs_name
        if self.parameters.sfs_type is not None:
            body_param["sfsType"] = self.parameters.sfs_type
        if self.parameters.sfs_protocol is not None:
            body_param["sfsProtocol"] = self.parameters.sfs_protocol
        if self.parameters.on_demand is not None:
            body_param["onDemand"] = self.parameters.on_demand
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.sfs_size is not None:
            body_param["sfsSize"] = self.parameters.sfs_size
        if self.parameters.vpc is not None:
            body_param["vpc"] = self.parameters.vpc
        if self.parameters.subnet is not None:
            body_param["subnet"] = self.parameters.subnet
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


class NewSfsRequestParam(object):

    def __init__(self, region_id, sfs_name, sfs_type, sfs_protocol, sfs_size, vpc, subnet, client_token=None, az_name=None, project_id=None, on_demand=None, cycle_type=None, cycle_count=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池 ID
        :param az_name: 多可用区资源池下，必须指定可用区。4.0资源池必填
        :param project_id: 资源所属企业项目 ID
        :param sfs_name: 单账户单资源池下，命名需唯一，支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param sfs_type: massive
        :param sfs_protocol: 协议类型
        :param on_demand: true/false，默认为 true
        :param cycle_type: onDemand 为 false 时，必须指定
        :param cycle_count: onDemand 为 false 时必须指定。周期最大长度不能超过 5 年
        :param sfs_size: 单位 GB,最大最小限制由云管页面配置
        :param vpc: 虚拟网 ID
        :param subnet: 子网 ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.sfs_name = sfs_name
        self.sfs_type = sfs_type
        self.sfs_protocol = sfs_protocol
        self.on_demand = on_demand
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.sfs_size = sfs_size
        self.vpc = vpc
        self.subnet = subnet

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 多可用区资源池下，必须指定可用区。4.0资源池必填
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 资源所属企业项目 ID
        """
        self.project_id = project_id

    def set_on_demand(self, on_demand):
        """
        :param on_demand: true/false，默认为 true
        """
        self.on_demand = on_demand

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: onDemand 为 false 时，必须指定
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: onDemand 为 false 时必须指定。周期最大长度不能超过 5 年
        """
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_name is None:
            raise Exception("sfs_name can not None")
        if self.sfs_type is None:
            raise Exception("sfs_type can not None")
        if self.sfs_protocol is None:
            raise Exception("sfs_protocol can not None")
        if self.sfs_size is None:
            raise Exception("sfs_size can not None")
        if self.vpc is None:
            raise Exception("vpc can not None")
        if self.subnet is None:
            raise Exception("subnet can not None")

