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


class ShowPrivateZoneRequest(CTYunRequest):
    """
    内网DNS详情
    """

    def __init__(self, request_param):
        super(ShowPrivateZoneRequest, self).__init__("/v4/private-zone/query", "GET", "ctvpc", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowPrivateZoneRequestParam(object):

    def __init__(self, region_id, zone_id, project_id=None, az_name=None):
        """
        :param region_id: 资源池id
        :param zone_id: 内网DNS的id
        :param project_id: 企业项目ID，默认为"0"
        :param az_name: 可用区名称
        """
        self.region_id = region_id
        self.zone_id = zone_id
        self.project_id = project_id
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为"0"
        """
        self.project_id = project_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.zone_id is None:
            raise Exception("zone_id can not None")

