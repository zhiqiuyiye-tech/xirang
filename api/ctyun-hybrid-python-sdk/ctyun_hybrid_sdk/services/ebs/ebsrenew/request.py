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


class EbsRenewRequest(CTYunRequest):
    """
    云硬盘续订（旧）
    """

    def __init__(self, request_param):
        super(EbsRenewRequest, self).__init__("/v4/ebs/renew", "POST", "ebs", "application/json")
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
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.cycle_type is not None:
            body_param["cycleType"] = self.parameters.cycle_type
        if self.parameters.cycle_count is not None:
            body_param["cycleCount"] = self.parameters.cycle_count
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class EbsRenewRequestParam(object):

    def __init__(self, resource_id, cycle_type, cycle_count, region_id=None, client_token=None):
        """
        :param resource_id: 资源ID，订单创建后的返回值。参考云硬盘开通[表resources](#表resources)。
        :param region_id: 如本地语境支持保存regionID，那么建议传递。
        :param cycle_type: 包周期类型，year/month。
        :param cycle_count: 包周期数。最多续订5年。
        :param client_token: 客户端存根，用于保证订单幂等性。<br/>要求单个云平台账户内唯一。
        """
        self.resource_id = resource_id
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.client_token = client_token

    def set_region_id(self, region_id):
        """
        :param region_id: 如本地语境支持保存regionID，那么建议传递。
        """
        self.region_id = region_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。<br/>要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.resource_id is None:
            raise Exception("resource_id can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")

