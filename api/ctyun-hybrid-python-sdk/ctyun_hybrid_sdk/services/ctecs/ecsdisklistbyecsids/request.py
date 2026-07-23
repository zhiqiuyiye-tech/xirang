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


class EcsDiskListByEcsIDsRequest(CTYunRequest):
    """
    查询云硬盘列表。**注意**：请求asc，sort 字段不支持，返回字段diskMode未对齐，encrypted字段不支持,暂为默认值
    """

    def __init__(self, request_param):
        super(EcsDiskListByEcsIDsRequest, self).__init__("/v4/ecs/disk/list-by-ecs-ids", "POST", "ctecs", "application/json")
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
        if self.parameters.ecs_id_list is not None:
            body_param["ecsIDList"] = self.parameters.ecs_id_list
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class EcsDiskListByEcsIDsRequestParam(object):

    def __init__(self, region_id, ecs_id_list, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param ecs_id_list: 云主机id列表，英文逗号分割，最多50个，支持分页查询
        :param page_no: 页码，默认1
        :param page_size: 页数，默认50
        """
        self.region_id = region_id
        self.ecs_id_list = ecs_id_list
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页数，默认50
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ecs_id_list is None:
            raise Exception("ecs_id_list can not None")

