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


class QueryResourceRequest(CTYunRequest):
    """
    从25.630 v2.2.3版本后支持
    """

    def __init__(self, request_param):
        super(QueryResourceRequest, self).__init__("/v4/resource/list", "POST", "common", "application/json")
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
        if self.parameters.resource_ids is not None:
            body_param["resourceIDs"] = self.parameters.resource_ids
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
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


class QueryResourceRequestParam(object):

    def __init__(self, page, page_size, resource_ids=None):
        """
        :param resource_ids: 资源ID列表 注意:此参数为数组
        :param page: 页码 -1 返回全量数据不分页
        :param page_size: 分页大小 默认10
        """
        self.resource_ids = resource_ids
        self.page = page
        self.page_size = page_size

    def set_resource_ids(self, resource_ids):
        """
        :param resource_ids: 资源ID列表
        """
        self.resource_ids = resource_ids

    def check_param(self):
        """
        the param required check
        """
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

