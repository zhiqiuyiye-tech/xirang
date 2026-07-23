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


class CreatePrivateNatPriceRequest(CTYunRequest):
    """
    创建私网NAT网关的询价，传参与创建一致。不涉及价格的参数只校验是否必传（不为空），不校验实际内容的有效性，直接透传。
    """

    def __init__(self, request_param):
        super(CreatePrivateNatPriceRequest, self).__init__("/v4/privatenat/query_create_price", "POST", "ctnat", "application/json")
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
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.bill_mode is not None:
            body_param["billMode"] = self.parameters.bill_mode
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class CreatePrivateNatPriceRequestParam(object):

    def __init__(self, region_id, vpc_id, subnet_id, spec, name, bill_mode, az_name, description=None, cycle_type=None, cycle_count=None):
        """
        :param region_id: 资源池id
        :param vpc_id: 非询价参数，不做校验（虚拟私有云ID
        :param subnet_id: 非询价参数，不做校验（子网ID
        :param spec: 规格, small 表示小型, medium 表示中型, large 表示大型, xlarge 表示超大型
        :param name: 非询价参数，不做校验（NAT网关名称
        :param description: 非询价参数，不做校验（描述信息
        :param bill_mode: 付费模式：2 - 按需，1 - 包周期；   
         包周期的时候，cycleType和cycleCount必填
        :param cycle_type: 订购类型：month / year 按月/按年;   
         只有 billMode=1的时候有意义，否则不校验
        :param cycle_count: 订购时长，billMode=1 此参数必填；订购时长为1-11月，或1-5年   
         只有 billMode=1的时候有意义，否则不校验
        :param az_name: 可用区名称
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.spec = spec
        self.name = name
        self.description = description
        self.bill_mode = bill_mode
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.az_name = az_name

    def set_description(self, description):
        """
        :param description: 非询价参数，不做校验（描述信息
        """
        self.description = description

    def set_cycle_type(self, cycle_type):
        """
        :param cycle_type: 订购类型：month / year 按月/按年;   
         只有 billMode=1的时候有意义，否则不校验
        """
        self.cycle_type = cycle_type

    def set_cycle_count(self, cycle_count):
        """
        :param cycle_count: 订购时长，billMode=1 此参数必填；订购时长为1-11月，或1-5年   
         只有 billMode=1的时候有意义，否则不校验
        """
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.spec is None:
            raise Exception("spec can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.bill_mode is None:
            raise Exception("bill_mode can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")

