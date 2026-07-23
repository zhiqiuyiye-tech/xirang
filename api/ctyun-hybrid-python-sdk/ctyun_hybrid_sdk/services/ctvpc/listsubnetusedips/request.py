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


class ListSubnetUsedIPsRequest(CTYunRequest):
    """
    查看某个子网已使用IP
    """

    def __init__(self, request_param):
        super(ListSubnetUsedIPsRequest, self).__init__("/v4/vpc/list-used-ips", "GET", "ctvpc", "")
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
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.ip is not None:
            query_param["ip"] = self.parameters.ip
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListSubnetUsedIPsRequestParam(object):

    def __init__(self, region_id, subnet_id, page_no=None, page_size=None, ip=None):
        """
        :param region_id: 资源池 ID
        :param subnet_id: 子网ID
        :param page_no: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param ip: 子网内的 IP 地址，2.0该字段为模糊搜索   
         （差异点说明：混合云无此参数，2.0对齐公有云文档补齐该参数）
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.page_no = page_no
        self.page_size = page_size
        self.ip = ip

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

    def set_ip(self, ip):
        """
        :param ip: 子网内的 IP 地址，2.0该字段为模糊搜索   
         （差异点说明：混合云无此参数，2.0对齐公有云文档补齐该参数）
        """
        self.ip = ip

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

