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


class GetEbsSpecListRequest(CTYunRequest):
    """
    2.2.5版本支持
    """

    def __init__(self, request_param):
        super(GetEbsSpecListRequest, self).__init__("/v4/ebs/list-spec", "GET", "ebs", "")
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
        if self.parameters.az_id is not None:
            query_param["azID"] = self.parameters.az_id
        if self.parameters.from_bms is not None:
            query_param["fromBms"] = self.parameters.from_bms
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetEbsSpecListRequestParam(object):

    def __init__(self, region_id, az_id=None, from_bms=None):
        """
        :param region_id: 资源池ID
        :param az_id: 可用区ID，等价于azName
        :param from_bms: true-从裸金属查询， false-全量查询
        """
        self.region_id = region_id
        self.az_id = az_id
        self.from_bms = from_bms

    def set_az_id(self, az_id):
        """
        :param az_id: 可用区ID，等价于azName
        """
        self.az_id = az_id

    def set_from_bms(self, from_bms):
        """
        :param from_bms: true-从裸金属查询， false-全量查询
        """
        self.from_bms = from_bms

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

