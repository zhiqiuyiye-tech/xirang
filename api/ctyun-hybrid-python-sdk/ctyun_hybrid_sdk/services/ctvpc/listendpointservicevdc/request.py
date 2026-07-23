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


class ListEndpointServiceVdcRequest(CTYunRequest):
    """
    查看终端节点服务列表VDC
    """

    def __init__(self, request_param):
        super(ListEndpointServiceVdcRequest, self).__init__("/v4/vpce/list-endpoint-service-vdc", "GET", "ctvpc", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        if self.parameters.endpoint_service_name is not None:
            query_param["endpointServiceName"] = self.parameters.endpoint_service_name
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEndpointServiceVdcRequestParam(object):

    def __init__(self, region_id, page=None, page_size=None, id=None, endpoint_service_name=None, query_content=None, org_id=None):
        """
        :param region_id: 资源池ID
        :param page: 页码，默认值1。不填/输入0，按照1查询
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        :param id: 节点服务id
        :param endpoint_service_name: 终端节点服务名称，该字段为精确匹配	
        :param query_content: 支持对终端节点服务名称进行模糊匹配	
        :param org_id: 组织id
        """
        self.region_id = region_id
        self.page = page
        self.page_size = page_size
        self.id = id
        self.endpoint_service_name = endpoint_service_name
        self.query_content = query_content
        self.org_id = org_id

    def set_page(self, page):
        """
        :param page: 页码，默认值1。不填/输入0，按照1查询
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页行数，范围1-100，不填/输入0，默认10查询，大于100按照100查询
        """
        self.page_size = page_size

    def set_id(self, id):
        """
        :param id: 节点服务id
        """
        self.id = id

    def set_endpoint_service_name(self, endpoint_service_name):
        """
        :param endpoint_service_name: 终端节点服务名称，该字段为精确匹配	
        """
        self.endpoint_service_name = endpoint_service_name

    def set_query_content(self, query_content):
        """
        :param query_content: 支持对终端节点服务名称进行模糊匹配	
        """
        self.query_content = query_content

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

