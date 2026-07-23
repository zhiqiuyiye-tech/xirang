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


class AttachPortBmRequest(CTYunRequest):
    """
    EIP绑定裸金属网卡
    """

    def __init__(self, request_param):
        super(AttachPortBmRequest, self).__init__("/v4/eip/attach-port-bm", "POST", "ctvpc", "application/json")
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
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.port_id is not None:
            body_param["portID"] = self.parameters.port_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.source_id is not None:
            body_param["sourceID"] = self.parameters.source_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class AttachPortBmRequestParam(object):

    def __init__(self, region_id, port_id, eip_id, source_id, client_token=None):
        """
        :param region_id: 资源池 ID
        :param port_id: 裸金属网卡的云管ID
        :param eip_id: 绑定云产品实例的 EIP 的 ID
        :param source_id: 裸金属的id
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.port_id = port_id
        self.eip_id = eip_id
        self.source_id = source_id
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.port_id is None:
            raise Exception("port_id can not None")
        if self.eip_id is None:
            raise Exception("eip_id can not None")
        if self.source_id is None:
            raise Exception("source_id can not None")

