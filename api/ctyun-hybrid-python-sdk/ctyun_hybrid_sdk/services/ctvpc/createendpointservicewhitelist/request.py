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


class CreateEndpointServiceWhitelistRequest(CTYunRequest):
    """
    添加终端节点服务白名单
    """

    def __init__(self, request_param):
        super(CreateEndpointServiceWhitelistRequest, self).__init__("/v4/vpce/create-endpoint-service-whitelist", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.email is not None:
            body_param["email"] = self.parameters.email
        if self.parameters.bss_account_id is not None:
            body_param["bssAccountID"] = self.parameters.bss_account_id
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


class CreateEndpointServiceWhitelistRequestParam(object):

    def __init__(self, region_id, endpoint_service_id, client_token=None, email=None, bss_account_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 资源池ID
        :param endpoint_service_id: 终端节点服务ID
        :param email: 账户邮箱，邮箱和账户至少填一个
        :param bss_account_id: 账户,邮箱和账户至少填一个
        """
        self.client_token = client_token
        self.region_id = region_id
        self.endpoint_service_id = endpoint_service_id
        self.email = email
        self.bss_account_id = bss_account_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_email(self, email):
        """
        :param email: 账户邮箱，邮箱和账户至少填一个
        """
        self.email = email

    def set_bss_account_id(self, bss_account_id):
        """
        :param bss_account_id: 账户,邮箱和账户至少填一个
        """
        self.bss_account_id = bss_account_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")

