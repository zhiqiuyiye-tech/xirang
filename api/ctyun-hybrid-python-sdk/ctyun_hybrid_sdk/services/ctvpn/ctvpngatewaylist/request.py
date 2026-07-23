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


class CtvpnGatewayListRequest(CTYunRequest):
    """
    GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
    """

    def __init__(self, request_param):
        super(CtvpnGatewayListRequest, self).__init__("/v4/vpn/gateway/list", "GET", "ctvpn", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.id is not None:
            query_param["ID"] = self.parameters.id
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        if self.parameters.customer_id is not None:
            query_param["customerID"] = self.parameters.customer_id
        if self.parameters.ct_user_id is not None:
            query_param["ctUserId"] = self.parameters.ct_user_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CtvpnGatewayListRequestParam(object):

    def __init__(self, region_id, name=None, query_content=None, id=None, resource_id=None, customer_id=None, ct_user_id=None, page=None, page_size=None):
        """
        :param region_id: 资源池id
        :param name: 名称
        :param query_content: 模糊搜索，支持名称和id
        :param id: vpn网关id
        :param resource_id: vpn网关id
        :param customer_id: 1.0参数，2.0无实际意义
        :param ct_user_id: 1.0参数，2.0无实际意义
        :param page: 当前页面 默认1
        :param page_size: 页面大小 默认10
        """
        self.region_id = region_id
        self.name = name
        self.query_content = query_content
        self.id = id
        self.resource_id = resource_id
        self.customer_id = customer_id
        self.ct_user_id = ct_user_id
        self.page = page
        self.page_size = page_size

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索，支持名称和id
        """
        self.query_content = query_content

    def set_id(self, id):
        """
        :param id: vpn网关id
        """
        self.id = id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: vpn网关id
        """
        self.resource_id = resource_id

    def set_customer_id(self, customer_id):
        """
        :param customer_id: 1.0参数，2.0无实际意义
        """
        self.customer_id = customer_id

    def set_ct_user_id(self, ct_user_id):
        """
        :param ct_user_id: 1.0参数，2.0无实际意义
        """
        self.ct_user_id = ct_user_id

    def set_page(self, page):
        """
        :param page: 当前页面 默认1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 页面大小 默认10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

