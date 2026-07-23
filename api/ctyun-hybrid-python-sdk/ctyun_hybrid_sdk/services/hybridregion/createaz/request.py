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


class CreateAzRequest(CTYunRequest):
    """
    创建可用区
    """

    def __init__(self, request_param):
        super(CreateAzRequest, self).__init__("/v1/azs/create", "POST", "hybridregion", "application/json")
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
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.code is not None:
            body_param["code"] = self.parameters.code
        if self.parameters.vnc_bm is not None:
            body_param["vncBm"] = self.parameters.vnc_bm
        if self.parameters.vnc_ecs is not None:
            body_param["vncEcs"] = self.parameters.vnc_ecs
        if self.parameters.proxy_url is not None:
            body_param["proxyUrl"] = self.parameters.proxy_url
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class CreateAzRequestParam(object):

    def __init__(self, region_id, name, code, proxy_url, vnc_bm=None, vnc_ecs=None, description=None):
        """
        :param region_id: 资源池ID
        :param name: 可用区名称
        :param code: 可用区编码
        :param vnc_bm: VNC转发地址(裸金属)
        :param vnc_ecs: VNC转发地址(云主机)
        :param proxy_url: AZ_Proxy
        :param description: 备注，最大255字符
        """
        self.region_id = region_id
        self.name = name
        self.code = code
        self.vnc_bm = vnc_bm
        self.vnc_ecs = vnc_ecs
        self.proxy_url = proxy_url
        self.description = description

    def set_vnc_bm(self, vnc_bm):
        """
        :param vnc_bm: VNC转发地址(裸金属)
        """
        self.vnc_bm = vnc_bm

    def set_vnc_ecs(self, vnc_ecs):
        """
        :param vnc_ecs: VNC转发地址(云主机)
        """
        self.vnc_ecs = vnc_ecs

    def set_description(self, description):
        """
        :param description: 备注，最大255字符
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.code is None:
            raise Exception("code can not None")
        if self.proxy_url is None:
            raise Exception("proxy_url can not None")

