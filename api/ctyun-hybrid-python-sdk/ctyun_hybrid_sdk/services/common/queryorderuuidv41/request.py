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


class QueryOrderUuidV41Request(CTYunRequest):
    """
    订单状态：目前仅支持完成-3/施工失败-5/开通中-14   
    资源类型：返回主资源类型。如果多子订单为批开则返回第一个子订单的资源类型，如果多子订单不同主资源类型(VM/EIP退订这种)则以VM为主
    """

    def __init__(self, request_param):
        super(QueryOrderUuidV41Request, self).__init__("/v4/order/query-uuid", "GET", "common", "")
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
        if self.parameters.master_order_id is not None:
            query_param["masterOrderId"] = self.parameters.master_order_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryOrderUuidV41RequestParam(object):

    def __init__(self, master_order_id, ):
        """
        :param master_order_id: 主订单ID(兼容了v1的masterOrderID)
        """
        self.master_order_id = master_order_id

    def check_param(self):
        """
        the param required check
        """
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")

