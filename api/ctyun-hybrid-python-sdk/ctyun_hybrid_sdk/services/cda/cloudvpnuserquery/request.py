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


class CloudvpnUserQueryRequest(CTYunRequest):
    """
    客户信息查询
    """

    def __init__(self, request_param):
        super(CloudvpnUserQueryRequest, self).__init__("/v4/cloudvpn/user/query", "GET", "cda", "")
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
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.customer_name is not None:
            query_param["customerName"] = self.parameters.customer_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CloudvpnUserQueryRequestParam(object):

    def __init__(self, region_id=None, customer_name=None):
        """
        :param region_id: 资源池id（此参数在v2无实际意义）
        :param customer_name: 客户名称（若header里已传用户ID，则以header里的用户ID为准，此传参优先级低）
        """
        self.region_id = region_id
        self.customer_name = customer_name

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池id（此参数在v2无实际意义）
        """
        self.region_id = region_id

    def set_customer_name(self, customer_name):
        """
        :param customer_name: 客户名称（若header里已传用户ID，则以header里的用户ID为准，此传参优先级低）
        """
        self.customer_name = customer_name

    def check_param(self):
        """
        the param required check
        """
        pass

