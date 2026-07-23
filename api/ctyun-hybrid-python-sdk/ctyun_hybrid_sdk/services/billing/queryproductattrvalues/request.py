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


class QueryProductAttrValuesRequest(CTYunRequest):
    """
    获取产品属性值列表
    """

    def __init__(self, request_param):
        super(QueryProductAttrValuesRequest, self).__init__("/v1/billing/queryProductAttrValues", "GET", "billing", "")
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
        if self.parameters.product_id is not None:
            query_param["productID"] = self.parameters.product_id
        if self.parameters.attr_id is not None:
            query_param["attrID"] = self.parameters.attr_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryProductAttrValuesRequestParam(object):

    def __init__(self, product_id, attr_id=None):
        """
        :param product_id: 产品ID
        :param attr_id: 产品属性ID
        """
        self.product_id = product_id
        self.attr_id = attr_id

    def set_attr_id(self, attr_id):
        """
        :param attr_id: 产品属性ID
        """
        self.attr_id = attr_id

    def check_param(self):
        """
        the param required check
        """
        if self.product_id is None:
            raise Exception("product_id can not None")

