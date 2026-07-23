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


class QueryProductDetailRequest(CTYunRequest):
    """
    根据serviceTag和resourceType获取产品信息   
    2.2.6.3 接口注册发布
    """

    def __init__(self, request_param):
        super(QueryProductDetailRequest, self).__init__("/v1/billing/queryProductDetail", "GET", "billing", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.resource_type is not None:
            query_param["resourceType"] = self.parameters.resource_type
        if self.parameters.service_tag is not None:
            query_param["serviceTag"] = self.parameters.service_tag
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryProductDetailRequestParam(object):

    def __init__(self, resource_type, service_tag, ):
        """
        :param resource_type: 
        :param service_tag: 
        """
        self.resource_type = resource_type
        self.service_tag = service_tag

    def check_param(self):
        """
        the param required check
        """
        if self.resource_type is None:
            raise Exception("resource_type can not None")
        if self.service_tag is None:
            raise Exception("service_tag can not None")

