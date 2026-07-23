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


class EditAzRequest(CTYunRequest):
    """
    编辑可用区
    """

    def __init__(self, request_param):
        super(EditAzRequest, self).__init__("/v1/azs/edit-az", "PUT", "hybridregion", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.vnc_ecs is not None:
            body_param["vncEcs"] = self.parameters.vnc_ecs
        if self.parameters.vnc_bm is not None:
            body_param["vncBm"] = self.parameters.vnc_bm
        if self.parameters.proxy_url is not None:
            body_param["proxyUrl"] = self.parameters.proxy_url
        if self.parameters.az_id is not None:
            body_param["azID"] = self.parameters.az_id
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EditAzRequestParam(object):

    def __init__(self, name, proxy_url, az_id, description=None, vnc_ecs=None, vnc_bm=None):
        """
        :param name: 
        :param description: 
        :param vnc_ecs: 
        :param vnc_bm: 
        :param proxy_url: 与列表返回的AzProxy字段对应
        :param az_id: 
        """
        self.name = name
        self.description = description
        self.vnc_ecs = vnc_ecs
        self.vnc_bm = vnc_bm
        self.proxy_url = proxy_url
        self.az_id = az_id

    def set_description(self, description):
        """
        :param description: 
        """
        self.description = description

    def set_vnc_ecs(self, vnc_ecs):
        """
        :param vnc_ecs: 
        """
        self.vnc_ecs = vnc_ecs

    def set_vnc_bm(self, vnc_bm):
        """
        :param vnc_bm: 
        """
        self.vnc_bm = vnc_bm

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.proxy_url is None:
            raise Exception("proxy_url can not None")
        if self.az_id is None:
            raise Exception("az_id can not None")

