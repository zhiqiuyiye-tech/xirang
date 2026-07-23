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


class ListPrivateZoneRecordRequest(CTYunRequest):
    """
    内网dns记录列表
    """

    def __init__(self, request_param):
        super(ListPrivateZoneRecordRequest, self).__init__("/v4/private-zone-record/list", "GET", "ctvpc", "")
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
        if self.parameters.zone_id is not None:
            query_param["zoneID"] = self.parameters.zone_id
        if self.parameters.zone_record_id is not None:
            query_param["zoneRecordID"] = self.parameters.zone_record_id
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListPrivateZoneRecordRequestParam(object):

    def __init__(self, region_id, zone_id=None, zone_record_id=None, page_number=None, page_size=None, page_no=None):
        """
        :param region_id: 资源池id
        :param zone_id: 内网dns的id
        :param zone_record_id: 记录id
        :param page_number: 页码，默认值1。不填/输入0，按照1查询（以pageNo为主，后期pageNumber废弃）
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param page_no: 页码，默认值1。不填/输入0，按照1查询（以pageNo为主，后期pageNumber废弃）
        """
        self.region_id = region_id
        self.zone_id = zone_id
        self.zone_record_id = zone_record_id
        self.page_number = page_number
        self.page_size = page_size
        self.page_no = page_no

    def set_zone_id(self, zone_id):
        """
        :param zone_id: 内网dns的id
        """
        self.zone_id = zone_id

    def set_zone_record_id(self, zone_record_id):
        """
        :param zone_record_id: 记录id
        """
        self.zone_record_id = zone_record_id

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询（以pageNo为主，后期pageNumber废弃）
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1。不填/输入0，按照1查询（以pageNo为主，后期pageNumber废弃）
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

