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


class CreateLBDomainCertLinksOpenapiRequest(CTYunRequest):
    """
    创建多证书
    """

    def __init__(self, request_param):
        super(CreateLBDomainCertLinksOpenapiRequest, self).__init__("/v4/elb/create-domain-cert-links", "POST", "ctelb", "application/json")
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
        if self.parameters.listener_id is not None:
            body_param["listenerID"] = self.parameters.listener_id
        if self.parameters.certificate_id is not None:
            body_param["certificateID"] = self.parameters.certificate_id
        if self.parameters.domain_name is not None:
            body_param["domainName"] = self.parameters.domain_name
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


class CreateLBDomainCertLinksOpenapiRequestParam(object):

    def __init__(self, region_id, listener_id, certificate_id, domain_name, description=None):
        """
        :param region_id: 区域ID
        :param listener_id: 监听器ID 需使用https类型监听器
        :param certificate_id: 证书ID 需使用服务器类型证书
        :param domain_name: 域名，同步底层校验规则^([a-zA-Z0-9][a-zA-Z0-9\\-]{0,62})(\\.[a-zA-Z0-9][a-zA-Z0-9\\-]{0,62})+$，长度不超过128，支持字母数字，不支持特殊字符
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.region_id = region_id
        self.listener_id = listener_id
        self.certificate_id = certificate_id
        self.domain_name = domain_name
        self.description = description

    def set_description(self, description):
        """
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.listener_id is None:
            raise Exception("listener_id can not None")
        if self.certificate_id is None:
            raise Exception("certificate_id can not None")
        if self.domain_name is None:
            raise Exception("domain_name can not None")

