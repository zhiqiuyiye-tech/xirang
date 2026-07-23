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


class QueryRaidTypesRequest(CTYunRequest):
    """
    查询物理机本地盘可选择的raid类型
    """

    def __init__(self, request_param):
        super(QueryRaidTypesRequest, self).__init__("/v4/ebm/raid-type-list", "GET", "ebm", "")
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
        if self.parameters.device_type is not None:
            query_param["deviceType"] = self.parameters.device_type
        if self.parameters.volume_type is not None:
            query_param["volumeType"] = self.parameters.volume_type
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryRaidTypesRequestParam(object):

    def __init__(self, region_id, device_type, volume_type, az_name=None):
        """
        :param region_id: 区域ID
        :param device_type: 设备类型
        :param volume_type: 磁盘类型，system、data
        :param az_name: 可用区（4.0必填）
        """
        self.region_id = region_id
        self.device_type = device_type
        self.volume_type = volume_type
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区（4.0必填）
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_type is None:
            raise Exception("device_type can not None")
        if self.volume_type is None:
            raise Exception("volume_type can not None")

