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


class UpdateBandwidthAttributeRequest(CTYunRequest):
    """
    修改共享带宽的名称描述
    """

    def __init__(self, request_param):
        super(UpdateBandwidthAttributeRequest, self).__init__("/v4/bandwidth/modify-attribute", "POST", "ctvpc", "application/json")
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
        if self.parameters.bandwidth_id is not None:
            body_param["bandwidthID"] = self.parameters.bandwidth_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class UpdateBandwidthAttributeRequestParam(object):

    def __init__(self, region_id, bandwidth_id, name=None, description=None, client_token=None):
        """
        :param region_id: 资源池id
        :param bandwidth_id: 共享带宽id
        :param name: 名称。字符长度2-32位字符,支持拉丁字母、中文、数字、下划线(_)，连字符(-），中文英文字母开头。不可重名
        :param description: 描述 支持拉丁字母、中文、数字, 特殊字符：·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128，不支持换行符
        :param client_token: （非必填，并且此字段在私有云不具有实际意义,，不会校验合理性）保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符。
        """
        self.region_id = region_id
        self.bandwidth_id = bandwidth_id
        self.name = name
        self.description = description
        self.client_token = client_token

    def set_name(self, name):
        """
        :param name: 名称。字符长度2-32位字符,支持拉丁字母、中文、数字、下划线(_)，连字符(-），中文英文字母开头。不可重名
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述 支持拉丁字母、中文、数字, 特殊字符：·~！@#￥%……&*（） —— -+={}|《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128，不支持换行符
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: （非必填，并且此字段在私有云不具有实际意义,，不会校验合理性）保证请求幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken只支持ASCII字符。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bandwidth_id is None:
            raise Exception("bandwidth_id can not None")

