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


class QueryInstancIDV41Request(CTYunRequest):
    """
    1.订单状态：目前仅支持完成-3/施工失败-5/开通中-14   
    2.资源UUID：仅返回云主机resourceID集合。如果是VM/EIP分多子订单这种退订场景，会仅返回VM的resourceID，但是orderStatus还是会以VM和EIP共同的为准
    """

    def __init__(self, request_param):
        super(QueryInstancIDV41Request, self).__init__("/v4/ecs/order/query-uuid", "GET", "ctecs", "")
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


class QueryInstancIDV41RequestParam(object):

    def __init__(self, master_order_id=None):
        """
        :param master_order_id: 主订单ID
        """
        self.master_order_id = master_order_id

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: 主订单ID
        """
        self.master_order_id = master_order_id

    def check_param(self):
        """
        the param required check
        """
        pass

