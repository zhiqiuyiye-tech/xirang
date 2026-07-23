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


class QueryBillFinancialStatementRequest(CTYunRequest):
    """
    该接口为查询财务统计接口， 对应页面运营中心/财务统计，与前端数据一致
    """

    def __init__(self, request_param):
        super(QueryBillFinancialStatementRequest, self).__init__("/queryBillFinancialStatement", "POST", "billing", "application/json")
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
        if self.parameters.start_date is not None:
            body_param["startDate"] = self.parameters.start_date
        if self.parameters.end_date is not None:
            body_param["endDate"] = self.parameters.end_date
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


class QueryBillFinancialStatementRequestParam(object):

    def __init__(self, start_date, end_date, ):
        """
        :param start_date: 开始时间
        :param end_date: 结束时间
        """
        self.start_date = start_date
        self.end_date = end_date

    def check_param(self):
        """
        the param required check
        """
        if self.start_date is None:
            raise Exception("start_date can not None")
        if self.end_date is None:
            raise Exception("end_date can not None")

