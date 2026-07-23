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


class QueryBillDetailRequest(CTYunRequest):
    """
    该接口为查询账单详情接口， 对应页面运营中心/账单明细， 返回数据一致
    """

    def __init__(self, request_param):
        super(QueryBillDetailRequest, self).__init__("/queryBillDetail", "POST", "billing", "application/json")
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
        if self.parameters.billing_cycle_id is not None:
            body_param["billingCycleId"] = self.parameters.billing_cycle_id
        if self.parameters.product_code is not None:
            body_param["productCode"] = self.parameters.product_code
        if self.parameters.master_order_id is not None:
            body_param["masterOrderId"] = self.parameters.master_order_id
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.bill_mode is not None:
            body_param["billMode"] = self.parameters.bill_mode
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


class QueryBillDetailRequestParam(object):

    def __init__(self, billing_cycle_id, page_no, page_size, product_code=None, master_order_id=None, bill_mode=None):
        """
        :param billing_cycle_id: 202404
        :param product_code: 产品编码
        :param master_order_id: 订单 id
        :param page_no: 范围 > 0
        :param page_size: 范围 1~100
        :param bill_mode: 1 - 包周期 2 -按需
        """
        self.billing_cycle_id = billing_cycle_id
        self.product_code = product_code
        self.master_order_id = master_order_id
        self.page_no = page_no
        self.page_size = page_size
        self.bill_mode = bill_mode

    def set_product_code(self, product_code):
        """
        :param product_code: 产品编码
        """
        self.product_code = product_code

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: 订单 id
        """
        self.master_order_id = master_order_id

    def set_bill_mode(self, bill_mode):
        """
        :param bill_mode: 1 - 包周期 2 -按需
        """
        self.bill_mode = bill_mode

    def check_param(self):
        """
        the param required check
        """
        if self.billing_cycle_id is None:
            raise Exception("billing_cycle_id can not None")
        if self.page_no is None:
            raise Exception("page_no can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

