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


class ListPrivateZoneVdcRequest(CTYunRequest):
    """
    内网DNS列表
    """

    def __init__(self, request_param):
        super(ListPrivateZoneVdcRequest, self).__init__("/v4/private-zone/list-vdc", "GET", "ctvpc", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.client_token is not None:
            query_param["clientToken"] = self.parameters.client_token
        if self.parameters.zone_id is not None:
            query_param["zoneID"] = self.parameters.zone_id
        if self.parameters.zone_name is not None:
            query_param["zoneName"] = self.parameters.zone_name
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListPrivateZoneVdcRequestParam(object):

    def __init__(self, region_id, client_token=None, zone_id=None, zone_name=None, page_number=None, page_size=None, org_id=None):
        """
        :param region_id: 资源池id
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param zone_id: 内网DNS的id
        :param zone_name: 名称
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param org_id: 组织id
        """
        self.region_id = region_id
        self.client_token = client_token
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.page_number = page_number
        self.page_size = page_size
        self.org_id = org_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_zone_id(self, zone_id):
        """
        :param zone_id: 内网DNS的id
        """
        self.zone_id = zone_id

    def set_zone_name(self, zone_name):
        """
        :param zone_name: 名称
        """
        self.zone_name = zone_name

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

