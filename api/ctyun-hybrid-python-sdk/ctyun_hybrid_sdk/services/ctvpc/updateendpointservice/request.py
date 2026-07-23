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


class UpdateEndpointServiceRequest(CTYunRequest):
    """
    修改终端节点服务
    """

    def __init__(self, request_param):
        super(UpdateEndpointServiceRequest, self).__init__("/v4/vpce/modify-endpoint-service", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.auto_connection is not None:
            body_param["autoConnection"] = self.parameters.auto_connection
        if self.parameters.dns_name is not None:
            body_param["dnsName"] = self.parameters.dns_name
        if self.parameters.shared is not None:
            body_param["shared"] = self.parameters.shared
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


class UpdateEndpointServiceRequestParam(object):

    def __init__(self, endpoint_service_id, region_id, client_token=None, name=None, description=None, auto_connection=None, dns_name=None, shared=None):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param endpoint_service_id: 终端节点服务ID
        :param region_id: 资源池 ID
        :param name: 终端节点服务名称，长度为2-32字符，支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param auto_connection: 是否自动连接，true 表示自动链接，false 表示非自动链接
        :param dns_name: dns名字，支持*   点 .   中划线-  大小写字母，数字，最长253。*只能是开头，中划线不能是开头结尾，每段最长63。总长度最大253
        :param shared: 可以终端节点服务修改为共享公共服务，paas接口使用  1-共享云服务 0-普通服务
        """
        self.client_token = client_token
        self.endpoint_service_id = endpoint_service_id
        self.region_id = region_id
        self.name = name
        self.description = description
        self.auto_connection = auto_connection
        self.dns_name = dns_name
        self.shared = shared

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 终端节点服务名称，长度为2-32字符，支持使用中文、字母、数字、-、_，只能以中文或字母开头
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_auto_connection(self, auto_connection):
        """
        :param auto_connection: 是否自动连接，true 表示自动链接，false 表示非自动链接
        """
        self.auto_connection = auto_connection

    def set_dns_name(self, dns_name):
        """
        :param dns_name: dns名字，支持*   点 .   中划线-  大小写字母，数字，最长253。*只能是开头，中划线不能是开头结尾，每段最长63。总长度最大253
        """
        self.dns_name = dns_name

    def set_shared(self, shared):
        """
        :param shared: 可以终端节点服务修改为共享公共服务，paas接口使用  1-共享云服务 0-普通服务
        """
        self.shared = shared

    def check_param(self):
        """
        the param required check
        """
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

