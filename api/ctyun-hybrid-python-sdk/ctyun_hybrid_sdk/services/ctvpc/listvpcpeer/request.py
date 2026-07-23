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


class ListVpcPeerRequest(CTYunRequest):
    """
    获取待处理对等连接请求列表接口查询
    """

    def __init__(self, request_param):
        super(ListVpcPeerRequest, self).__init__("/v4/vpc/vpcpeer/requests", "GET", "ctvpc", "")
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
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListVpcPeerRequestParam(object):

    def __init__(self, region_id, page_size=None, page_no=None, page=None):
        """
        :param region_id: 资源池id
        :param page_size: 当前页数据条数
        :param page_no: 列表的页码，默认值为 1, 推荐使用该字段, page 后续会废弃
        :param page: 当前页，公有云将废弃字段，暂不支持
        """
        self.region_id = region_id
        self.page_size = page_size
        self.page_no = page_no
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 当前页数据条数
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的页码，默认值为 1, 推荐使用该字段, page 后续会废弃
        """
        self.page_no = page_no

    def set_page(self, page):
        """
        :param page: 当前页，公有云将废弃字段，暂不支持
        """
        self.page = page

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

