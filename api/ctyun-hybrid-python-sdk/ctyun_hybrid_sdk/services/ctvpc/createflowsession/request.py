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


class CreateFlowSessionRequest(CTYunRequest):
    """
    创建镜像会话
    """

    def __init__(self, request_param):
        super(CreateFlowSessionRequest, self).__init__("/v4/flowsession/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.mirror_filter_id is not None:
            body_param["mirrorFilterID"] = self.parameters.mirror_filter_id
        if self.parameters.src_port is not None:
            body_param["srcPort"] = self.parameters.src_port
        if self.parameters.dst_port is not None:
            body_param["dstPort"] = self.parameters.dst_port
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.vni is not None:
            body_param["vni"] = self.parameters.vni
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


class CreateFlowSessionRequestParam(object):

    def __init__(self, region_id, name, mirror_filter_id, src_port, dst_port, subnet_id, vni, description=None):
        """
        :param region_id: 区域ID
        :param name: 英文字母、中文、特殊符号_(下划线) -(中划线) /(斜杠) 进行命名，不支持使用特殊符号、数字作为命名开头，不支持特殊符号作为命名结尾，命名长度为2-32位
        :param description: 长度为0～50字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，
        :param mirror_filter_id: 过滤条件 ID
        :param src_port: 需要为云主机或裸金属的网卡
        :param dst_port: 需要为云主机或裸金属的网卡
        :param subnet_id: 子网 ID
        :param vni: 0 - 1677215
        """
        self.region_id = region_id
        self.name = name
        self.description = description
        self.mirror_filter_id = mirror_filter_id
        self.src_port = src_port
        self.dst_port = dst_port
        self.subnet_id = subnet_id
        self.vni = vni

    def set_description(self, description):
        """
        :param description: 长度为0～50字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，
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
        if self.mirror_filter_id is None:
            raise Exception("mirror_filter_id can not None")
        if self.src_port is None:
            raise Exception("src_port can not None")
        if self.dst_port is None:
            raise Exception("dst_port can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.vni is None:
            raise Exception("vni can not None")

