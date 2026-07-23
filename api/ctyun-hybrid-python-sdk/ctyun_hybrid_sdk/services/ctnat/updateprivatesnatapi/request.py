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


class UpdatePrivateSnatApiRequest(CTYunRequest):
    """
    修改私网SNAT规则，子网和自定义网段可二选其一，都填以子网ID为主。
    """

    def __init__(self, request_param):
        super(UpdatePrivateSnatApiRequest, self).__init__("/v4/privatenat/modify-snat", "POST", "ctnat", "application/json")
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
        if self.parameters.snat_id is not None:
            body_param["snatID"] = self.parameters.snat_id
        if self.parameters.source_subnet_id is not None:
            body_param["sourceSubnetID"] = self.parameters.source_subnet_id
        if self.parameters.source_cidr is not None:
            body_param["sourceCIDR"] = self.parameters.source_cidr
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.snat_ips is not None:
            body_param["snatIps"] = self.parameters.snat_ips
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


class UpdatePrivateSnatApiRequestParam(object):

    def __init__(self, region_id, snat_id, source_subnet_id=None, source_cidr=None, description=None, snat_ips=None):
        """
        :param region_id: 资源池id
        :param snat_id: SNAT条目id
        :param source_subnet_id: 子网ID，子网ID和自定义cidr只能二选其一，子网ID的优先级最高
        :param source_cidr: 自定义cidr，子网ID和自定义cidr只能二选其一，子网ID的优先级最高
        :param description: SNAT的描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        :param snat_ips: 中转IP列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.snat_id = snat_id
        self.source_subnet_id = source_subnet_id
        self.source_cidr = source_cidr
        self.description = description
        self.snat_ips = snat_ips

    def set_source_subnet_id(self, source_subnet_id):
        """
        :param source_subnet_id: 子网ID，子网ID和自定义cidr只能二选其一，子网ID的优先级最高
        """
        self.source_subnet_id = source_subnet_id

    def set_source_cidr(self, source_cidr):
        """
        :param source_cidr: 自定义cidr，子网ID和自定义cidr只能二选其一，子网ID的优先级最高
        """
        self.source_cidr = source_cidr

    def set_description(self, description):
        """
        :param description: SNAT的描述信息 支持拉丁字母、中文、数字, 特殊字符：!@#$%^&*()+= <>?:"{},./;'[]·！@#￥%……&*（） —— -+_-={}|《》？：“”【】、；‘'，。、，长度 0 - 128。不支持换行符
        """
        self.description = description

    def set_snat_ips(self, snat_ips):
        """
        :param snat_ips: 中转IP列表
        """
        self.snat_ips = snat_ips

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snat_id is None:
            raise Exception("snat_id can not None")

