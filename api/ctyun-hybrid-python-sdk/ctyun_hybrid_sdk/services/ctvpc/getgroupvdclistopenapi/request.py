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


class GetGroupVdcListOpenApiRequest(CTYunRequest):
    """
    查询ip地址组已绑定vdc列表
    """

    def __init__(self, request_param):
        super(GetGroupVdcListOpenApiRequest, self).__init__("/v4/eipPool/vdcList", "GET", "ctvpc", "")
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
        if self.parameters.eip_address_group_id is not None:
            query_param["eipAddressGroupID"] = self.parameters.eip_address_group_id
        if self.parameters.vdc_name is not None:
            query_param["vdcName"] = self.parameters.vdc_name
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


class GetGroupVdcListOpenApiRequestParam(object):

    def __init__(self, eip_address_group_id, vdc_name=None, page=None, page_size=None):
        """
        :param eip_address_group_id: 
        :param vdc_name: 
        :param page: 
        :param page_size: 
        """
        self.eip_address_group_id = eip_address_group_id
        self.vdc_name = vdc_name
        self.page = page
        self.page_size = page_size

    def set_vdc_name(self, vdc_name):
        """
        :param vdc_name: 
        """
        self.vdc_name = vdc_name

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

    def check_param(self):
        """
        the param required check
        """
        if self.eip_address_group_id is None:
            raise Exception("eip_address_group_id can not None")

