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


class NewVpcListRequest(CTYunRequest):
    """
    查询用户专有网络列表   
    具体详细信息，查看解绑HaVip接口（/v4/vpc/list）。
    """

    def __init__(self, request_param):
        super(NewVpcListRequest, self).__init__("/v4/vpc/new-list", "GET", "ctvpc", "")
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
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.ipv4_cidrs is not None:
            query_param["ipv4Cidrs"] = self.parameters.ipv4_cidrs
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class NewVpcListRequestParam(object):

    def __init__(self, region_id, page_number=None, page_size=None, vpc_id=None, ipv4_cidrs=None, project_id=None):
        """
        :param region_id: 
        :param page_number: 列表的页码，默认值为 1。
        :param page_size: 分页查询时每页的行数，最大值为 50，默认值为 10。
        :param vpc_id: 多个 VPC 的 ID 之间用半角逗号（,）隔开
        :param ipv4_cidrs: 扩展网段，支持模糊查询
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.vpc_id = vpc_id
        self.ipv4_cidrs = ipv4_cidrs
        self.project_id = project_id

    def set_page_number(self, page_number):
        """
        :param page_number: 列表的页码，默认值为 1。
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页的行数，最大值为 50，默认值为 10。
        """
        self.page_size = page_size

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 多个 VPC 的 ID 之间用半角逗号（,）隔开
        """
        self.vpc_id = vpc_id

    def set_ipv4_cidrs(self, ipv4_cidrs):
        """
        :param ipv4_cidrs: 扩展网段，支持模糊查询
        """
        self.ipv4_cidrs = ipv4_cidrs

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

