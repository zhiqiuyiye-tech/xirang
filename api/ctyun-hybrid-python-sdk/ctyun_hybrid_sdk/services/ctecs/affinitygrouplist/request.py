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


class AffinityGroupListRequest(CTYunRequest):
    """
    查询云主机组列表或者详情
    """

    def __init__(self, request_param):
        super(AffinityGroupListRequest, self).__init__("/v4/ecs/affinity-group/list", "POST", "ctecs", "application/json")
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
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.affinity_group_id is not None:
            body_param["affinityGroupID"] = self.parameters.affinity_group_id
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.asc is not None:
            body_param["asc"] = self.parameters.asc
        if self.parameters.sort is not None:
            body_param["sort"] = self.parameters.sort
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


class AffinityGroupListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, affinity_group_id=None, query_content=None, asc=None, sort=None):
        """
        :param region_id: 资源池ID
        :param page_no: 页码，默认值：1
        :param page_size: 每页记录数目，取值范围：[1, 100]
        :param affinity_group_id: 云主机主机组ID
        :param query_content: 查询内容（可是id或者name）、模糊匹配
        :param asc: 排序方向，默认false 升序，true降序
        :param sort: 默认排序字段created_time，支持排序的字段created_time, updated_time, ecs_count
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.affinity_group_id = affinity_group_id
        self.query_content = query_content
        self.asc = asc
        self.sort = sort

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值：1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 100]
        """
        self.page_size = page_size

    def set_affinity_group_id(self, affinity_group_id):
        """
        :param affinity_group_id: 云主机主机组ID
        """
        self.affinity_group_id = affinity_group_id

    def set_query_content(self, query_content):
        """
        :param query_content: 查询内容（可是id或者name）、模糊匹配
        """
        self.query_content = query_content

    def set_asc(self, asc):
        """
        :param asc: 排序方向，默认false 升序，true降序
        """
        self.asc = asc

    def set_sort(self, sort):
        """
        :param sort: 默认排序字段created_time，支持排序的字段created_time, updated_time, ecs_count
        """
        self.sort = sort

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

