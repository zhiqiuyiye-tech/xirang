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


class DnsBindLabelOpenapiRequest(CTYunRequest):
    """
    DNS绑定标签
    """

    def __init__(self, request_param):
        super(DnsBindLabelOpenapiRequest, self).__init__("/v4/private-zone/bind-label", "POST", "ctvpc", "application/json")
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
        if self.parameters.zone_id is not None:
            body_param["zoneID"] = self.parameters.zone_id
        if self.parameters.label_key is not None:
            body_param["labelKey"] = self.parameters.label_key
        if self.parameters.label_value is not None:
            body_param["labelValue"] = self.parameters.label_value
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


class DnsBindLabelOpenapiRequestParam(object):

    def __init__(self, region_id, zone_id, label_key, label_value, ):
        """
        :param region_id: 资源id
        :param zone_id: dns的id
        :param label_key: 标签的key
        :param label_value: 标签的value
        """
        self.region_id = region_id
        self.zone_id = zone_id
        self.label_key = label_key
        self.label_value = label_value

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.zone_id is None:
            raise Exception("zone_id can not None")
        if self.label_key is None:
            raise Exception("label_key can not None")
        if self.label_value is None:
            raise Exception("label_value can not None")

