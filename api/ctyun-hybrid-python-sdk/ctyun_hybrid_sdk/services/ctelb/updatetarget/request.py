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


class UpdateTargetRequest(CTYunRequest):
    """
    更新后端服务
    """

    def __init__(self, request_param):
        super(UpdateTargetRequest, self).__init__("/v4/elb/update-target", "POST", "ctelb", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.protocol_port is not None:
            body_param["protocolPort"] = self.parameters.protocol_port
        if self.parameters.weight is not None:
            body_param["weight"] = self.parameters.weight
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


class UpdateTargetRequestParam(object):

    def __init__(self, region_id, id, description=None, protocol_port=None, weight=None):
        """
        :param region_id: 资源池ID
        :param id: 后端服务ID(可查询后端服务列表获取后端服务ID)
        :param description: 描述，支持字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:'{},./;'[,]·！@#￥%……&*（） —— -+={},《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        :param protocol_port: 端口
        :param weight: 权重
        """
        self.region_id = region_id
        self.id = id
        self.description = description
        self.protocol_port = protocol_port
        self.weight = weight

    def set_description(self, description):
        """
        :param description: 描述，支持字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:'{},./;'[,]·！@#￥%……&*（） —— -+={},《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_protocol_port(self, protocol_port):
        """
        :param protocol_port: 端口
        """
        self.protocol_port = protocol_port

    def set_weight(self, weight):
        """
        :param weight: 权重
        """
        self.weight = weight

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

