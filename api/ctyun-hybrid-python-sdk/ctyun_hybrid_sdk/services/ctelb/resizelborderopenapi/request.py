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


class ResizeLbOrderOpenapiRequest(CTYunRequest):
    """
    性能保障型负载均衡变配；3,0底层性能保障型没有余量
    """

    def __init__(self, request_param):
        super(ResizeLbOrderOpenapiRequest, self).__init__("/v4/elb/modify-pgelb-spec", "POST", "ctelb", "application/json")
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


class ResizeLbOrderOpenapiRequestParam(object):

    def __init__(self, client_token, region_id, elb_id, sla_name, ):
        """
        :param client_token: 公有云文档必传
        :param region_id: 区域ID
        :param elb_id: 负载均衡 ID
        :param sla_name: lb的规格名称, 支持:elb.s2.small(标准型I)，elb.s3.small(标准型II)，elb.s4.small(增强型I)，elb.s5.small(增强型II)，elb.s2.large(高阶型I)，elb.s3.large(高阶型II)，elb.s4.large(超强型I)，elb.s5.large(超强型II)
        """
        self.client_token = client_token
        self.region_id = region_id
        self.elb_id = elb_id
        self.sla_name = sla_name

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

