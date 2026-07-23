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


class CreateProductAttrValueRequest(CTYunRequest):
    """
    创建产品属性值
    """

    def __init__(self, request_param):
        super(CreateProductAttrValueRequest, self).__init__("/v1/billing/createProductAttrValue", "POST", "billing", "application/json")
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
        if self.parameters.product_id is not None:
            body_param["productID"] = self.parameters.product_id
        if self.parameters.attr_id is not None:
            body_param["attrID"] = self.parameters.attr_id
        if self.parameters.value is not None:
            body_param["value"] = self.parameters.value
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


class CreateProductAttrValueRequestParam(object):

    def __init__(self, product_id, attr_id, value, description=None):
        """
        :param product_id: 产品ID
        :param attr_id: 属性ID
        :param value: 属性值
        :param description: 描述
        """
        self.product_id = product_id
        self.attr_id = attr_id
        self.value = value
        self.description = description

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.product_id is None:
            raise Exception("product_id can not None")
        if self.attr_id is None:
            raise Exception("attr_id can not None")
        if self.value is None:
            raise Exception("value can not None")

