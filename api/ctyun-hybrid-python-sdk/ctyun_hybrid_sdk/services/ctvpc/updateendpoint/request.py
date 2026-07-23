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


class UpdateEndpointRequest(CTYunRequest):
    """
    更新终端节点
    """

    def __init__(self, request_param):
        super(UpdateEndpointRequest, self).__init__("/v4/vpce/update-endpoint", "POST", "ctvpc", "application/json")
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
        if self.parameters.endpoint_id is not None:
            body_param["endpointID"] = self.parameters.endpoint_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.endpoint_name is not None:
            body_param["endpointName"] = self.parameters.endpoint_name
        if self.parameters.enable_dns is not None:
            body_param["enableDns"] = self.parameters.enable_dns
        if self.parameters.whitelist is not None:
            body_param["whitelist"] = self.parameters.whitelist
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


class UpdateEndpointRequestParam(object):

    def __init__(self, region_id, endpoint_id, client_token=None, endpoint_name=None, enable_dns=None, whitelist=None, description=None):
        """
        :param region_id: 资源池id
        :param endpoint_id: 终端节点ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param endpoint_name: 终端节点名称，只能由数字，字母，-组成不能以数字和-开头，长度2-28
        :param enable_dns: 是否开启dns, true:开启,false:关闭
        :param whitelist: 白名单 最大20个 注意:此参数为数组
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.region_id = region_id
        self.endpoint_id = endpoint_id
        self.client_token = client_token
        self.endpoint_name = endpoint_name
        self.enable_dns = enable_dns
        self.whitelist = whitelist
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_endpoint_name(self, endpoint_name):
        """
        :param endpoint_name: 终端节点名称，只能由数字，字母，-组成不能以数字和-开头，长度2-28
        """
        self.endpoint_name = endpoint_name

    def set_enable_dns(self, enable_dns):
        """
        :param enable_dns: 是否开启dns, true:开启,false:关闭
        """
        self.enable_dns = enable_dns

    def set_whitelist(self, whitelist):
        """
        :param whitelist: 白名单 最大20个
        """
        self.whitelist = whitelist

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_id is None:
            raise Exception("endpoint_id can not None")

