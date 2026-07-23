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


class UpdateLoadBalancerRequest(CTYunRequest):
    """
    更新负载均衡实例
    """

    def __init__(self, request_param):
        super(UpdateLoadBalancerRequest, self).__init__("/v4/elb/update-loadbalancer", "POST", "ctelb", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.sla_name is not None:
            body_param["slaName"] = self.parameters.sla_name
        if self.parameters.delete_protection is not None:
            body_param["deleteProtection"] = self.parameters.delete_protection
        if self.parameters.gw_enabled is not None:
            body_param["gwEnabled"] = self.parameters.gw_enabled
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


class UpdateLoadBalancerRequestParam(object):

    def __init__(self, region_id, id, name=None, description=None, client_token=None, sla_name=None, delete_protection=None, gw_enabled=None):
        """
        :param region_id: 资源池ID
        :param id: 负载均衡ID
        :param name: 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param sla_name: lb的规格名称:   
         4.0资源池：支持：elb.s1.small，elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large   
         3.0资源池：支持：CLASSICAL，STANDARD_1，EHANCED_1，ADVANCED_1，HIGH_1，EXTREME_1
        :param delete_protection: 删除保护。false（不开启）、true（开启）
        :param gw_enabled: 是否开启防火墙引流，2.2.6版本支持
        """
        self.region_id = region_id
        self.id = id
        self.name = name
        self.description = description
        self.client_token = client_token
        self.sla_name = sla_name
        self.delete_protection = delete_protection
        self.gw_enabled = gw_enabled

    def set_name(self, name):
        """
        :param name: 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_sla_name(self, sla_name):
        """
        :param sla_name: lb的规格名称:   
         4.0资源池：支持：elb.s1.small，elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large   
         3.0资源池：支持：CLASSICAL，STANDARD_1，EHANCED_1，ADVANCED_1，HIGH_1，EXTREME_1
        """
        self.sla_name = sla_name

    def set_delete_protection(self, delete_protection):
        """
        :param delete_protection: 删除保护。false（不开启）、true（开启）
        """
        self.delete_protection = delete_protection

    def set_gw_enabled(self, gw_enabled):
        """
        :param gw_enabled: 是否开启防火墙引流，2.2.6版本支持
        """
        self.gw_enabled = gw_enabled

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

