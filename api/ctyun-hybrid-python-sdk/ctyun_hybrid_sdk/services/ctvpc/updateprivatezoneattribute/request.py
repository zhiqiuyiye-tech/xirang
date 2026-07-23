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


class UpdatePrivateZoneAttributeRequest(CTYunRequest):
    """
    修改内网DNS
    """

    def __init__(self, request_param):
        super(UpdatePrivateZoneAttributeRequest, self).__init__("/v4/private-zone/update", "POST", "ctvpc", "application/json")
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
        if self.parameters.vpc_id_list is not None:
            body_param["vpcIDList"] = self.parameters.vpc_id_list
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.zone_id is not None:
            body_param["zoneID"] = self.parameters.zone_id
        if self.parameters.proxy_pattern is not None:
            body_param["proxyPattern"] = self.parameters.proxy_pattern
        if self.parameters.ttl is not None:
            body_param["TTL"] = self.parameters.ttl
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


class UpdatePrivateZoneAttributeRequestParam(object):

    def __init__(self, region_id, zone_id, client_token=None, vpc_id_list=None, description=None, proxy_pattern=None, ttl=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param vpc_id_list: 关联的vpc,多个ID之间用半角逗号（,）隔开。   
         注：修改时，该字段是增量挂载，即不能挂载已经绑定过的vpc。   
         1、创建接口(/v4/private-zone/create)绑定的vpc不能再传，会导致再次绑定出错；   
         2、尽量不使用该接口进行绑定vpc，即该字段最好不传值。若需要绑定vpc请使用/v4/private-zone/disassociate-vpc
        :param description: 描述
        :param zone_id: 内网DNS的id
        :param proxy_pattern: zone, record ，默认zone
        :param ttl: zone ttl, 单位秒。默认300
        :param project_id: 企业项目ID，默认为"0"	
        """
        self.client_token = client_token
        self.region_id = region_id
        self.vpc_id_list = vpc_id_list
        self.description = description
        self.zone_id = zone_id
        self.proxy_pattern = proxy_pattern
        self.ttl = ttl
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_vpc_id_list(self, vpc_id_list):
        """
        :param vpc_id_list: 关联的vpc,多个ID之间用半角逗号（,）隔开。   
         注：修改时，该字段是增量挂载，即不能挂载已经绑定过的vpc。   
         1、创建接口(/v4/private-zone/create)绑定的vpc不能再传，会导致再次绑定出错；   
         2、尽量不使用该接口进行绑定vpc，即该字段最好不传值。若需要绑定vpc请使用/v4/private-zone/disassociate-vpc
        """
        self.vpc_id_list = vpc_id_list

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_proxy_pattern(self, proxy_pattern):
        """
        :param proxy_pattern: zone, record ，默认zone
        """
        self.proxy_pattern = proxy_pattern

    def set_ttl(self, ttl):
        """
        :param ttl: zone ttl, 单位秒。默认300
        """
        self.ttl = ttl

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为"0"	
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.zone_id is None:
            raise Exception("zone_id can not None")

