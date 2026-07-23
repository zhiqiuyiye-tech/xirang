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


class NewIPv6ListRequest(CTYunRequest):
    """
    新查询ipv6列表
    """

    def __init__(self, request_param):
        super(NewIPv6ListRequest, self).__init__("/v4/ipv6/new-ipv6-list", "GET", "ctvpc", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.ip_address is not None:
            query_param["ipAddress"] = self.parameters.ip_address
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class NewIPv6ListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, vpc_id=None, subnet_id=None, ip_address=None):
        """
        :param region_id: 资源池 ID
        :param page_no: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param vpc_id: 专有网络id
        :param subnet_id: 子网id
        :param ip_address: ipv6地址
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.ip_address = ip_address

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 专有网络id
        """
        self.vpc_id = vpc_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网id
        """
        self.subnet_id = subnet_id

    def set_ip_address(self, ip_address):
        """
        :param ip_address: ipv6地址
        """
        self.ip_address = ip_address

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

