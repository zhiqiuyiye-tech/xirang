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


class ListPortRequest(CTYunRequest):
    """
    查询网卡列表
    """

    def __init__(self, request_param):
        super(ListPortRequest, self).__init__("/v4/ports/list", "GET", "ctvpc", "")
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
        if self.parameters.device_id is not None:
            query_param["deviceID"] = self.parameters.device_id
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListPortRequestParam(object):

    def __init__(self, region_id, vpc_id=None, device_id=None, subnet_id=None, page_number=None, page_size=None, page_no=None, project_id=None):
        """
        :param region_id: 资源池id
        :param vpc_id: vpc id
        :param device_id: 关联设备id
        :param subnet_id: 子网id
        :param page_number: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误；建议优先使用pageNo
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询；小于0返回错误
        :param page_no: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误;对齐公有云，优先使用;V2.2.4开始支持
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.device_id = device_id
        self.subnet_id = subnet_id
        self.page_number = page_number
        self.page_size = page_size
        self.page_no = page_no
        self.project_id = project_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc id
        """
        self.vpc_id = vpc_id

    def set_device_id(self, device_id):
        """
        :param device_id: 关联设备id
        """
        self.device_id = device_id

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 子网id
        """
        self.subnet_id = subnet_id

    def set_page_number(self, page_number):
        """
        :param page_number: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误；建议优先使用pageNo
        """
        self.page_number = page_number

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询；小于0返回错误
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值1。不填/输入0，按照1查询；小于0返回错误;对齐公有云，优先使用;V2.2.4开始支持
        """
        self.page_no = page_no

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

