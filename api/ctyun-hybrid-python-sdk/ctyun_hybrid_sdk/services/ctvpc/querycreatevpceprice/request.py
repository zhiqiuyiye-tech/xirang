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


class QueryCreateVPCEPriceRequest(CTYunRequest):
    """
    创建终端节点服务.当type为反向reverse时，自动创建不指定的中转ip。中转ip列表可产看详情信息。
    """

    def __init__(self, request_param):
        super(QueryCreateVPCEPriceRequest, self).__init__("/v4/vpce/query-create-endpoint-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.endpoint_name is not None:
            body_param["endpointName"] = self.parameters.endpoint_name
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.ip is not None:
            body_param["IP"] = self.parameters.ip
        if self.parameters.whitelist_flag is not None:
            body_param["whitelistFlag"] = self.parameters.whitelist_flag
        if self.parameters.whitelist is not None:
            body_param["whitelist"] = self.parameters.whitelist
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class QueryCreateVPCEPriceRequestParam(object):

    def __init__(self, client_token, region_id, cycle_type, endpoint_service_id, endpoint_name, subnet_id, vpc_id, whitelist_flag, ip=None, whitelist=None, description=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池 ID
        :param cycle_type: 收费类型：只能填写 on_demand	
        :param endpoint_service_id: 终端节点关联的终端节点服务	
        :param endpoint_name: 终端节点名称，只能由数字，字母，-组成不能以数字和-开头，最大长度28	
        :param subnet_id: 子网id	
        :param vpc_id: 所属的专有网络id
        :param ip: vpc address
        :param whitelist_flag: 白名单开关 1.开启 0.关闭，默认1	
        :param whitelist: 白名单 注意:此参数为数组
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.client_token = client_token
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.endpoint_service_id = endpoint_service_id
        self.endpoint_name = endpoint_name
        self.subnet_id = subnet_id
        self.vpc_id = vpc_id
        self.ip = ip
        self.whitelist_flag = whitelist_flag
        self.whitelist = whitelist
        self.description = description

    def set_ip(self, ip):
        """
        :param ip: vpc address
        """
        self.ip = ip

    def set_whitelist(self, whitelist):
        """
        :param whitelist: 白名单
        """
        self.whitelist = whitelist

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.endpoint_name is None:
            raise Exception("endpoint_name can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.whitelist_flag is None:
            raise Exception("whitelist_flag can not None")

