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


class ListSecurityGroupsRequest(CTYunRequest):
    """
    查询用户安全组列表
    """

    def __init__(self, request_param):
        super(ListSecurityGroupsRequest, self).__init__("/v4/vpc/query-security-groups", "GET", "ctvpc", "")
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
        if self.parameters.page_number is not None:
            query_param["pageNumber"] = self.parameters.page_number
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.instance_id is not None:
            query_param["instanceID"] = self.parameters.instance_id
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListSecurityGroupsRequestParam(object):

    def __init__(self, region_id, vpc_id=None, page_number=None, page_size=None, query_content=None, instance_id=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param vpc_id: 安全组所在的专有网络ID。 3.0此参数无用
        :param page_number: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param query_content: 【模糊查询】  安全组ID或名称
        :param instance_id: 实例 ID
        :param project_id: 企业项目id
        """
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.page_number = page_number
        self.page_size = page_size
        self.query_content = query_content
        self.instance_id = instance_id
        self.project_id = project_id

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 安全组所在的专有网络ID。 3.0此参数无用
        """
        self.vpc_id = vpc_id

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

    def set_query_content(self, query_content):
        """
        :param query_content: 【模糊查询】  安全组ID或名称
        """
        self.query_content = query_content

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 实例 ID
        """
        self.instance_id = instance_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

