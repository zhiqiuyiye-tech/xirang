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


class GetEipAddressGroupsOpenApiRequest(CTYunRequest):
    """
    查询ip地址组列表
    """

    def __init__(self, request_param):
        super(GetEipAddressGroupsOpenApiRequest, self).__init__("/v4/eipPool", "GET", "ctvpc", "")
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
        if self.parameters.provider is not None:
            query_param["provider"] = self.parameters.provider
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.eip is not None:
            query_param["eip"] = self.parameters.eip
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.vdc_id is not None:
            query_param["vdcID"] = self.parameters.vdc_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetEipAddressGroupsOpenApiRequestParam(object):

    def __init__(self, region_id, provider=None, name=None, eip=None, page=None, page_size=None, vdc_id=None):
        """
        :param provider: 
        :param name: 
        :param eip: 
        :param page: 
        :param page_size: 
        :param region_id: 
        :param vdc_id: 
        """
        self.provider = provider
        self.name = name
        self.eip = eip
        self.page = page
        self.page_size = page_size
        self.region_id = region_id
        self.vdc_id = vdc_id

    def set_provider(self, provider):
        """
        :param provider: 
        """
        self.provider = provider

    def set_name(self, name):
        """
        :param name: 
        """
        self.name = name

    def set_eip(self, eip):
        """
        :param eip: 
        """
        self.eip = eip

    def set_page(self, page):
        """
        :param page: 
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 
        """
        self.page_size = page_size

    def set_vdc_id(self, vdc_id):
        """
        :param vdc_id: 
        """
        self.vdc_id = vdc_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

