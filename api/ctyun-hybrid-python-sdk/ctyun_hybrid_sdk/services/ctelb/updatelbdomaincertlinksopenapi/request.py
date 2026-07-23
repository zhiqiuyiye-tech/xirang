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


class UpdateLBDomainCertLinksOpenapiRequest(CTYunRequest):
    """
    修改扩展域名证书
    """

    def __init__(self, request_param):
        super(UpdateLBDomainCertLinksOpenapiRequest, self).__init__("/v4/elb/update-domain-cert-links", "POST", "ctelb", "application/json")
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
        if self.parameters.domain_cert_id is not None:
            body_param["domainCertID"] = self.parameters.domain_cert_id
        if self.parameters.certificate_id is not None:
            body_param["certificateID"] = self.parameters.certificate_id
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


class UpdateLBDomainCertLinksOpenapiRequestParam(object):

    def __init__(self, region_id, domain_cert_id, certificate_id=None, description=None):
        """
        :param region_id: 资源池ID
        :param domain_cert_id: 多证书 ID
        :param certificate_id: 证书ID
        :param description: 描述,支持拉丁字母、中文、数字, 特殊字符：~!@#$%^&*()_-+=<>?:"{}！@#￥%……&（） —— -+={}《》？：“”【】、；‘'，。、，不能以 http: / https: 开头，长度 0 - 128
        """
        self.region_id = region_id
        self.domain_cert_id = domain_cert_id
        self.certificate_id = certificate_id
        self.description = description

    def set_certificate_id(self, certificate_id):
        """
        :param certificate_id: 证书ID
        """
        self.certificate_id = certificate_id

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
        if self.domain_cert_id is None:
            raise Exception("domain_cert_id can not None")

