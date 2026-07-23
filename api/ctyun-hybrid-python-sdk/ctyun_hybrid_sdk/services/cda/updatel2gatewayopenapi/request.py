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


class UpdateL2GatewayOpenapiRequest(CTYunRequest):
    """
    更新企业交换机
    """

    def __init__(self, request_param):
        super(UpdateL2GatewayOpenapiRequest, self).__init__("/v4/l2gw/update", "POST", "cda", "application/json")
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
        if self.parameters.l2gw_id is not None:
            body_param["l2gwID"] = self.parameters.l2gw_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class UpdateL2GatewayOpenapiRequestParam(object):

    def __init__(self, l2gw_id, region_id, name, description=None):
        """
        :param l2gw_id: 企业交换机ID
        :param region_id: 资源池ID
        :param name: 支持拉丁字母、中文、数字，下划线，连字符，必须以中文 / 英文字母开头，不能以数字、_和-、 http: / https: 开头，长度 2 - 32
        :param description: 支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:"{},./;'[\\]·！@#￥%……&*（） —— -+={}\\《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.l2gw_id = l2gw_id
        self.region_id = region_id
        self.name = name
        self.description = description

    def set_description(self, description):
        """
        :param description: 支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+= <>?:"{},./;'[\\]·！@#￥%……&*（） —— -+={}\\《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.l2gw_id is None:
            raise Exception("l2gw_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")

