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


class ResubscribeInstanceRequest(CTYunRequest):
    """
    续订一台包周期的云主机
    """

    def __init__(self, request_param):
        super(ResubscribeInstanceRequest, self).__init__("/v4/ecs/resubscribe-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.pay_voucher_price is not None:
            body_param["payVoucherPrice"] = self.parameters.pay_voucher_price
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


class ResubscribeInstanceRequestParam(object):

    def __init__(self, region_id, cycle_type, cycle_count, client_token, instance_id, pay_voucher_price=None):
        """
        :param region_id: 
        :param cycle_type: 订购周期类型，取值范围: MONTH表示按月, YEAR表示按年
        :param cycle_count: 订购时长，包周期计费必传，最长不超过5年
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param instance_id: 云主机ID(资源id也兼容)
        :param pay_voucher_price: （暂不支持，传参不生效）代金券，满足以下规则：两位小数，不足两位自动补0，超过两位小数无效；不可为负数；字段为0时表示不使用代金券
        """
        self.region_id = region_id
        self.cycle_type = cycle_type
        self.cycle_count = cycle_count
        self.client_token = client_token
        self.instance_id = instance_id
        self.pay_voucher_price = pay_voucher_price

    def set_pay_voucher_price(self, pay_voucher_price):
        """
        :param pay_voucher_price: （暂不支持，传参不生效）代金券，满足以下规则：两位小数，不足两位自动补0，超过两位小数无效；不可为负数；字段为0时表示不使用代金券
        """
        self.pay_voucher_price = pay_voucher_price

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
        if self.instance_id is None:
            raise Exception("instance_id can not None")

