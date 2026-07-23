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


class OpenapiEcsPortsListV4Request(CTYunRequest):
    """
    查询网卡列表
    """

    def __init__(self, request_param):
        super(OpenapiEcsPortsListV4Request, self).__init__("/v4/ecs/ports/list", "GET", "ctecs", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.device_id is not None:
            query_param["deviceID"] = self.parameters.device_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.order_key is not None:
            query_param["orderKey"] = self.parameters.order_key
        if self.parameters.order_direction is not None:
            query_param["orderDirection"] = self.parameters.order_direction
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class OpenapiEcsPortsListV4RequestParam(object):

    def __init__(self, region_id, project_id=None, vpc_id=None, device_id=None, subnet_id=None, page_number=None, page_size=None, order_key=None, order_direction=None):
        """
        :param project_id: 企业项目ID
        :param region_id: 资源池ID
        :param vpc_id: 所属vpc id 
        :param device_id: 关联设备id （主机id）
        :param subnet_id: 所属子网id
        :param page_number: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询；小于0返回错误
        :param order_key: createdAt, updatedAt -不支持
        :param order_direction: desc, asc   -不支持
        """
        self.project_id = project_id
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.device_id = device_id
        self.subnet_id = subnet_id
        self.page_number = page_number
        self.page_size = page_size
        self.order_key = order_key
        self.order_direction = order_direction

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 所属vpc id 
        """
        self.vpc_id = vpc_id

    def set_device_id(self, device_id):
        """
        :param device_id: 关联设备id （主机id）
        """
        self.device_id = device_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 所属子网id
        """
        self.subnet_id = subnet_id

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询；小于0返回错误
        """
        self.page_size = page_size

    def set_order_key(self, order_key):
        """
        :param order_key: createdAt, updatedAt -不支持
        """
        self.order_key = order_key

    def set_order_direction(self, order_direction):
        """
        :param order_direction: desc, asc   -不支持
        """
        self.order_direction = order_direction

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

