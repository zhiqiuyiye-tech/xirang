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


class QryCycleBillDetailProdCycleIdRequest(CTYunRequest):
    """
    49. 账单明细产品+账期（包周期）
    """

    def __init__(self, request_param):
        super(QryCycleBillDetailProdCycleIdRequest, self).__init__("/qryCycleBillDetailProdCycleId", "POST", "billing", "application/json")
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
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.billing_cycle_id is not None:
            body_param["billingCycleId"] = self.parameters.billing_cycle_id
        if self.parameters.resource_id is not None:
            body_param["resourceId"] = self.parameters.resource_id
        if self.parameters.product_code is not None:
            body_param["productCode"] = self.parameters.product_code
        if self.parameters.contract_id is not None:
            body_param["contractId"] = self.parameters.contract_id
        if self.parameters.bill_type is not None:
            body_param["billType"] = self.parameters.bill_type
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


class QryCycleBillDetailProdCycleIdRequestParam(object):

    def __init__(self, billing_cycle_id, page_no=None, page_size=None, resource_id=None, product_code=None, contract_id=None, bill_type=None):
        """
        :param page_no: 页码
        :param page_size: 页数
        :param billing_cycle_id: 200101
        :param resource_id: 资源id
        :param product_code: 产品编码
        :param contract_id: (混合云暂未接入)
        :param bill_type: 1-收入 2-支出
        """
        self.page_no = page_no
        self.page_size = page_size
        self.billing_cycle_id = billing_cycle_id
        self.resource_id = resource_id
        self.product_code = product_code
        self.contract_id = contract_id
        self.bill_type = bill_type

    def set_page_no(self, page_no):
        """
        :param page_no: 页码
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页数
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id
        """
        self.resource_id = resource_id

    def set_product_code(self, product_code):
        """
        :param product_code: 产品编码
        """
        self.product_code = product_code

    def set_contract_id(self, contract_id):
        """
        :param contract_id: (混合云暂未接入)
        """
        self.contract_id = contract_id

    def set_bill_type(self, bill_type):
        """
        :param bill_type: 1-收入 2-支出
        """
        self.bill_type = bill_type

    def check_param(self):
        """
        the param required check
        """
        if self.billing_cycle_id is None:
            raise Exception("billing_cycle_id can not None")

