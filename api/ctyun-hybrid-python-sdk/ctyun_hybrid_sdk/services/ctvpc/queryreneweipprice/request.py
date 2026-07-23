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


class QueryRenewEipPriceRequest(CTYunRequest):
    """
    调用此接口可查询续订弹性公网IP的价格
    """

    def __init__(self, request_param):
        super(QueryRenewEipPriceRequest, self).__init__("/v4/eip/query-renew-price", "POST", "ctvpc", "application/json")
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
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
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


class QueryRenewEipPriceRequestParam(object):

    def __init__(self, region_id, cycle_type, cycle_count, eip_id, client_token=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        :param region_id: 资源池 ID
        :param cycle_type: 订购类型：month / year 
        :param cycle_count: 订购时长，订购类型为month / year时询价支持1以上
        :param project_id: 企业项目ID，默认为用户所在的默认企业项目
        :param eip_id: eipID，只允许查询归属本用户的EIP，其他用户的无法查询
        """
        self.client_token = client_token
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.project_id = project_id
        self.eip_id = eip_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为用户所在的默认企业项目
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")
        if self.eip_id is None:
            raise Exception("eip_id can not None")

