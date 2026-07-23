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


class L2GatewayQueryRenewPriceOpenapiRequest(CTYunRequest):
    """
    企业交换机续订询价
    """

    def __init__(self, request_param):
        super(L2GatewayQueryRenewPriceOpenapiRequest, self).__init__("/v4/l2gw/query-renew-price", "POST", "cda", "application/json")
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
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.l2gw_id is not None:
            body_param["l2gwID"] = self.parameters.l2gw_id
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


class L2GatewayQueryRenewPriceOpenapiRequestParam(object):

    def __init__(self, region_id, cycle_type, cycle_count, l2gw_id, ):
        """
        :param region_id: 资源池ID
        :param cycle_type: 订购类型：month（包月） / year（包年）
        :param cycle_count: 订购时长，包月1-11，包年1-3
        :param l2gw_id: l2gwID
        """
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.l2gw_id = l2gw_id

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
        if self.l2gw_id is None:
            raise Exception("l2gw_id can not None")

