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


class IaasEbsEbsrefundNewRequest(CTYunRequest):
    """
    支持退订一块包周期计费/按需的云硬盘。退订云硬盘后，将退还对应部分云硬盘费用。当云硬盘状态为“未挂载”时，才可以退订。
    """

    def __init__(self, request_param):
        super(IaasEbsEbsrefundNewRequest, self).__init__("/v4/ebs/refund-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
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


class IaasEbsEbsrefundNewRequestParam(object):

    def __init__(self, region_id, resource_id=None, disk_id=None, client_token=None):
        """
        :param resource_id: 参数resourceID或diskID二者必传其一,且不能同时传入
        :param disk_id: 参数resourceID或diskID二者必传其一,且不能同时传入
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云暂不支持，忽略
        :param region_id: 资源池Id
        """
        self.resource_id = resource_id
        self.disk_id = disk_id
        self.client_token = client_token
        self.region_id = region_id

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 参数resourceID或diskID二者必传其一,且不能同时传入
        """
        self.resource_id = resource_id

    def set_disk_id(self, disk_id):
        """
        :param disk_id: 参数resourceID或diskID二者必传其一,且不能同时传入
        """
        self.disk_id = disk_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一。公有云字段，混合云暂不支持，忽略
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

