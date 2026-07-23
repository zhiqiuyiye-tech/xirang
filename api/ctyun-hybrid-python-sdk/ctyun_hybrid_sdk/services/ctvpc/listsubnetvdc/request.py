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


class ListSubnetVdcRequest(CTYunRequest):
    """
    查询用户专有网络下子网列表
    """

    def __init__(self, request_param):
        super(ListSubnetVdcRequest, self).__init__("/v4/vpc/list-subnet-vdc", "GET", "ctvpc", "")
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
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.client_token is not None:
            query_param["clientToken"] = self.parameters.client_token
        if self.parameters.org_id is not None:
            query_param["orgID"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListSubnetVdcRequestParam(object):

    def __init__(self, region_id, vpc_id=None, subnet_id=None, az_name=None, page_number=None, page_size=None, client_token=None, org_id=None):
        """
        :param region_id: 
        :param vpc_id: VPC的id，建议填写该参数
        :param subnet_id: 多个 subnet 的 ID 之间用半角逗号（,）隔开。
        :param az_name: 可用区名称(该参数未使用，输入无意义)
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param client_token: 客户端存根
        :param org_id: 组织ID
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.az_name = az_name
        self.page_number = page_number
        self.page_size = page_size
        self.client_token = client_token
        self.org_id = org_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: VPC的id，建议填写该参数
        """
        self.vpc_id = vpc_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 多个 subnet 的 ID 之间用半角逗号（,）隔开。
        """
        self.subnet_id = subnet_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(该参数未使用，输入无意义)
        """
        self.az_name = az_name

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_org_id(self, org_id):
        """
        :param org_id: 组织ID
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

