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


class QueryProductCatalogDetailRequest(CTYunRequest):
    """
    产品目录详情
    """

    def __init__(self, request_param):
        super(QueryProductCatalogDetailRequest, self).__init__("/v1/billing/queryProductCatalogDetail", "GET", "billing", "")
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
        if self.parameters.id is not None:
            query_param["id"] = self.parameters.id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryProductCatalogDetailRequestParam(object):

    def __init__(self, id, ):
        """
        :param id: 目录ID
        """
        self.id = id

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")

