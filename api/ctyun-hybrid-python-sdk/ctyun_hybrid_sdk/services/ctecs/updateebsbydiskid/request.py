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


class UpdateEbsByDiskIDRequest(CTYunRequest):
    """
    修改云硬盘
    """

    def __init__(self, request_param):
        super(UpdateEbsByDiskIDRequest, self).__init__("/v4/ecs/volume/update", "POST", "ctecs", "application/json")
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
        if self.parameters.disk_name is not None:
            body_param["diskName"] = self.parameters.disk_name
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
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


class UpdateEbsByDiskIDRequestParam(object):

    def __init__(self, disk_name, disk_id, region_id=None):
        """
        :param region_id: 资源池ID
        :param disk_name: 云盘名称
        :param disk_id: 云硬盘id
        """
        self.region_id = region_id
        self.disk_name = disk_name
        self.disk_id = disk_id

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.disk_name is None:
            raise Exception("disk_name can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

