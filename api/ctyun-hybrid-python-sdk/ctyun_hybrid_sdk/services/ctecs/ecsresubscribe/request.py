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


class EcsResubscribeRequest(CTYunRequest):
    """
    续订一台包周期的云主机
    """

    def __init__(self, request_param):
        super(EcsResubscribeRequest, self).__init__("/v4/ecs/resubscribe", "POST", "ctecs", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
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


class EcsResubscribeRequestParam(object):

    def __init__(self, region_id, cycle_type, cycle_count, client_token, id, az_name=None):
        """
        :param region_id: 资源池ID
        :param cycle_type: 订购周期类型，取值范围: MONTH表示按月, YEAR表示按年
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年
        :param az_name: 可用区名称,您可以调用获取资源池信息，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param id: 云主机ID(资源id也兼容)
        """
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.az_name = az_name
        self.client_token = client_token
        self.id = id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称,您可以调用获取资源池信息，查询结果中zoneList内返回存在可用区名称(即多可用区，本字段填写实际可用区名称)，若查询结果中zoneList为空(即为单可用区，本字段填写default)。
        """
        self.az_name = az_name

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
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.id is None:
            raise Exception("id can not None")

