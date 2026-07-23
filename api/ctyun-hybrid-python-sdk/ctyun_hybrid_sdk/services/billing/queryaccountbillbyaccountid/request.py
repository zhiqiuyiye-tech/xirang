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


class QueryAccountBillByAccountIdRequest(CTYunRequest):
    """
    47. 账户账单查询
    """

    def __init__(self, request_param):
        super(QueryAccountBillByAccountIdRequest, self).__init__("/queryAccountBillByAccountId", "POST", "billing", "application/json")
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
        if self.parameters.account is not None:
            account = []
            if isinstance(self.parameters.account, list):
                for item in self.parameters.account:
                    if type(item) is dict:
                        account.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        account.append(item_dict_value)
            else:
                account.append(self.parameters.account.get_dic())
            body_param["account"] = account
        if self.parameters.billing_cycle_id is not None:
            body_param["billingCycleId"] = self.parameters.billing_cycle_id
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


class Account(object):

    def __init__(self, account_id=None):
        """
        :param account_id: 账号
        """
        self.account_id = account_id

    def set_account_id(self, account_id):
        """
        :param account_id: 账号
        """
        self.account_id = account_id

    def get_dic(self):
        obj_dict = dict()
        if self.account_id is not None:
            obj_dict["accountId"] = self.account_id
        return obj_dict


class QueryAccountBillByAccountIdRequestParam(object):

    def __init__(self, account, billing_cycle_id, ):
        """
        :param account:  注意:此参数为数组
        :param billing_cycle_id: 202401
        """
        self.account = account
        self.billing_cycle_id = billing_cycle_id

    def check_param(self):
        """
        the param required check
        """
        if self.account is None:
            raise Exception("account can not None")
        if self.billing_cycle_id is None:
            raise Exception("billing_cycle_id can not None")

