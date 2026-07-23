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


class RenewEbmRequest(CTYunRequest):
    """
    续订物理机
    """

    def __init__(self, request_param):
        super(RenewEbmRequest, self).__init__("/v4/ebm/renew", "POST", "ebm", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
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


class RenewEbmRequestParam(object):

    def __init__(self, region_id, az_name, instance_uuid, cycle_type, cycle_count, client_token=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区
        :param instance_uuid: 裸金属实例ID
        :param cycle_type: 订购周期类型，值为"MONTH"表示cycleCount的值单位为月，值为"YEAR"表示cycleCount的值单位为年
        :param cycle_count: 订购周期，值的单位由cycleType决定，最长订购周期为60个月（5年）
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，未对齐 不支持（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid = instance_uuid
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，未对齐 不支持（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.cycle_type is None:
            raise Exception("cycle_type can not None")
        if self.cycle_count is None:
            raise Exception("cycle_count can not None")

