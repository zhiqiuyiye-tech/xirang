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


class UpdateVpcPeerConnectionAttributeRequest(CTYunRequest):
    """
    修改对等连接
    """

    def __init__(self, request_param):
        super(UpdateVpcPeerConnectionAttributeRequest, self).__init__("/v4/vpc/modify-vpc-peer-connection", "POST", "ctvpc", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
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


class UpdateVpcPeerConnectionAttributeRequestParam(object):

    def __init__(self, instance_id, region_id, client_token=None, name=None, description=None):
        """
        :param client_token: 唯一token（非必填，并且此字段在私有云不具有实际意义）
        :param instance_id: 对等连接id
        :param name: 名称（2-32长度，只允许中文、英文、数字和特殊字符-, _，只能以中文和英文开头）
        :param description: 描述 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param region_id: 资源池id
        """
        self.client_token = client_token
        self.instance_id = instance_id
        self.name = name
        self.description = description
        self.region_id = region_id

    def set_client_token(self, client_token):
        """
        :param client_token: 唯一token（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 名称（2-32长度，只允许中文、英文、数字和特殊字符-, _，只能以中文和英文开头）
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

