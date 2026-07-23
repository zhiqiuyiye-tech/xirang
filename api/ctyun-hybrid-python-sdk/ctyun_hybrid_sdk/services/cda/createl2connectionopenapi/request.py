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


class CreateL2ConnectionOpenapiRequest(CTYunRequest):
    """
    创建二层连接
    """

    def __init__(self, request_param):
        super(CreateL2ConnectionOpenapiRequest, self).__init__("/v4/l2gw_connection/create", "POST", "cda", "application/json")
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
        if self.parameters.l2gw_id is not None:
            body_param["l2gwID"] = self.parameters.l2gw_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.l2con_ip is not None:
            body_param["l2conIp"] = self.parameters.l2con_ip
        if self.parameters.tunnel_id is not None:
            body_param["tunnelID"] = self.parameters.tunnel_id
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.tunnel_ip is not None:
            body_param["tunnelIp"] = self.parameters.tunnel_ip
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


class CreateL2ConnectionOpenapiRequestParam(object):

    def __init__(self, region_id, l2gw_id, name, l2con_ip, tunnel_id, subnet_id, tunnel_ip, description=None):
        """
        :param region_id: 资源池ID
        :param l2gw_id: 二层网关id,
        :param name: 二层网关名称，二层网关名称，支持拉丁字母、中文、数字，下划线，连字符，必须以中文 / 英文字母开头，不能以数字、_和-、 http: / https: 开头，长度 2 - 32
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^& ***\\*()_-+= <>?:"{},./;'[\\****\\]***\\*·！@#￥%……&\\****（） —— -+={}\\《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param l2con_ip: 接口ip，必须是子网可用ip
        :param tunnel_id: 隧道号，1-16777215
        :param subnet_id: 二层连接子网,子网和l2gw必须属于同一个vpc，一个子网只能创建1个l2gw_connection
        :param tunnel_ip: 隧道ip
        """
        self.region_id = region_id
        self.l2gw_id = l2gw_id
        self.name = name
        self.description = description
        self.l2con_ip = l2con_ip
        self.tunnel_id = tunnel_id
        self.subnet_id = subnet_id
        self.tunnel_ip = tunnel_ip

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^& ***\\*()_-+= <>?:"{},./;'[\\****\\]***\\*·！@#￥%……&\\****（） —— -+={}\\《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.l2gw_id is None:
            raise Exception("l2gw_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.l2con_ip is None:
            raise Exception("l2con_ip can not None")
        if self.tunnel_id is None:
            raise Exception("tunnel_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.tunnel_ip is None:
            raise Exception("tunnel_ip can not None")

