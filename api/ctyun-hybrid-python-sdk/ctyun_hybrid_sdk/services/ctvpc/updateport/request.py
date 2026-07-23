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


class UpdatePortRequest(CTYunRequest):
    """
    修改网卡属性
    """

    def __init__(self, request_param):
        super(UpdatePortRequest, self).__init__("/v4/ports/update", "POST", "ctvpc", "application/json")
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
        if self.parameters.network_interface_id is not None:
            body_param["networkInterfaceID"] = self.parameters.network_interface_id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.security_group_ids is not None:
            body_param["securityGroupIDs"] = self.parameters.security_group_ids
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.mtu is not None:
            body_param["mtu"] = self.parameters.mtu
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


class UpdatePortRequestParam(object):

    def __init__(self, region_id, network_interface_id, description=None, name=None, security_group_ids=None, client_token=None, mtu=None):
        """
        :param region_id: 资源池id
        :param network_interface_id: 网卡id
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&()_-+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param name: 网卡名称，非空的情况下校验，支持拉丁字母、中文、数字，下划线，连字符，中文/英文字母开头，不能以http:/https:开头，长度2-32
        :param security_group_ids: 安全组id 注意:此参数为数组
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        :param mtu: 网卡mtu，1500-8000，仅4.0资源池有效
        """
        self.region_id = region_id
        self.network_interface_id = network_interface_id
        self.description = description
        self.name = name
        self.security_group_ids = security_group_ids
        self.client_token = client_token
        self.mtu = mtu

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&()_-+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_name(self, name):
        """
        :param name: 网卡名称，非空的情况下校验，支持拉丁字母、中文、数字，下划线，连字符，中文/英文字母开头，不能以http:/https:开头，长度2-32
        """
        self.name = name

    def set_security_group_ids(self, security_group_ids):
        """
        :param security_group_ids: 安全组id
        """
        self.security_group_ids = security_group_ids

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_mtu(self, mtu):
        """
        :param mtu: 网卡mtu，1500-8000，仅4.0资源池有效
        """
        self.mtu = mtu

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.network_interface_id is None:
            raise Exception("network_interface_id can not None")

