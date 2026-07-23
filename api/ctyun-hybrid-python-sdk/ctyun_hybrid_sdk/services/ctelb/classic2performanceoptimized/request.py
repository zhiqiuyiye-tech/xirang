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


class Classic2PerformanceOptimizedRequest(CTYunRequest):
    """
    经典型负载均衡实例升级为性能保障型；3,0底层性能保障型没有余量，无法升级
    """

    def __init__(self, request_param):
        super(Classic2PerformanceOptimizedRequest, self).__init__("/v4/elb/upgrade-to-pgelb", "POST", "ctelb", "application/json")
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
        if self.parameters.elb_id is not None:
            body_param["elbID"] = self.parameters.elb_id
        if self.parameters.sla_name is not None:
            body_param["slaName"] = self.parameters.sla_name
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
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


class Classic2PerformanceOptimizedRequestParam(object):

    def __init__(self, client_token, region_id, elb_id, sla_name, cycle_type, cycle_count, ):
        """
        :param client_token: 公有云文档必传
        :param region_id: 资源池ID
        :param elb_id: 经典型负载均衡实例 ID
        :param sla_name: lb的规格名称, 支持:elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large
        :param cycle_type: 公有云参数仅对齐必传性，订购类型：month（包月） / year（包年）
        :param cycle_count: 公有云参数仅对齐必传性，实际为无效参数
        """
        self.client_token = client_token
        self.region_id = region_id
        self.elb_id = elb_id
        self.sla_name = sla_name
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.elb_id is None:
            raise Exception("elb_id can not None")
        if self.sla_name is None:
            raise Exception("sla_name can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")

