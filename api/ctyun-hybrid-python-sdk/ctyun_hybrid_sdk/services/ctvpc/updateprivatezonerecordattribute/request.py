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


class UpdatePrivateZoneRecordAttributeRequest(CTYunRequest):
    """
    修改内网 DNS 记录（公有云不支持name传参）
    """

    def __init__(self, request_param):
        super(UpdatePrivateZoneRecordAttributeRequest, self).__init__("/v4/private-zone-record/update", "POST", "ctvpc", "application/json")
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
        if self.parameters.zone_record_id is not None:
            body_param["zoneRecordID"] = self.parameters.zone_record_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.value_list is not None:
            body_param["valueList"] = self.parameters.value_list
        if self.parameters.ttl is not None:
            body_param["TTL"] = self.parameters.ttl
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


class UpdatePrivateZoneRecordAttributeRequestParam(object):

    def __init__(self, region_id, zone_record_id, value_list, client_token=None, name=None, description=None, ttl=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池id
        :param zone_record_id: 记录id
        :param name: 名称，不支持进行修改
        :param description: 描述
        :param value_list: 记录集值 注意:此参数为数组
        :param ttl: 单位秒，默认300 取值范围：300~2147483647，默认300
        """
        self.client_token = client_token
        self.region_id = region_id
        self.zone_record_id = zone_record_id
        self.name = name
        self.description = description
        self.value_list = value_list
        self.ttl = ttl

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 名称，不支持进行修改
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_ttl(self, ttl):
        """
        :param ttl: 单位秒，默认300 取值范围：300~2147483647，默认300
        """
        self.ttl = ttl

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.zone_record_id is None:
            raise Exception("zone_record_id can not None")
        if self.value_list is None:
            raise Exception("value_list can not None")

