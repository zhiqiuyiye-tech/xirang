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


class CreatePrivateZoneRecordRequest(CTYunRequest):
    """
    创建内网 DNS 记录(公有云传参没有azName和projectID字段)
    """

    def __init__(self, request_param):
        super(CreatePrivateZoneRecordRequest, self).__init__("/v4/private-zone-record/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.zone_id is not None:
            body_param["zoneID"] = self.parameters.zone_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.value_list is not None:
            body_param["valueList"] = self.parameters.value_list
        if self.parameters.ttl is not None:
            body_param["TTL"] = self.parameters.ttl
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreatePrivateZoneRecordRequestParam(object):

    def __init__(self, region_id, zone_id, name, type, value_list, client_token=None, description=None, ttl=None, az_name=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池id
        :param zone_id: 域名id
        :param name: 记录集名称
        :param description: 描述
        :param type: 记录集类型，枚举值：A-将域名执行IPv4地址；CNAME-将域名指向另外一个域名； MX-将域名指向邮件服务器地址；AAAA- 将域名指向IPv6地址；TXT-设置文本记录
        :param value_list: 记录集值 注意:此参数为数组
        :param ttl: TTL值，取值范围：【300，2147483647】，默认300
        :param az_name: 可用区名称
        :param project_id: 企业项目ID，默认为"0"
        """
        self.client_token = client_token
        self.region_id = region_id
        self.zone_id = zone_id
        self.name = name
        self.description = description
        self.type = type
        self.value_list = value_list
        self.ttl = ttl
        self.az_name = az_name
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_ttl(self, ttl):
        """
        :param ttl: TTL值，取值范围：【300，2147483647】，默认300
        """
        self.ttl = ttl

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为"0"
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.zone_id is None:
            raise Exception("zone_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.type is None:
            raise Exception("type can not None")
        if self.value_list is None:
            raise Exception("value_list can not None")

