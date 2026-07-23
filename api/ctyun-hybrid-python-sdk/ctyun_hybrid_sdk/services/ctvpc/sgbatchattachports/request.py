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


class SgBatchAttachPortsRequest(CTYunRequest):
    """
    安全组批量绑定网卡。clientToken公有云必填字段，字段不影响接口功能，混合云不必填当作对齐。
    """

    def __init__(self, request_param):
        super(SgBatchAttachPortsRequest, self).__init__("/v4/vpc/batch-attach-security-group-ports", "POST", "ctvpc", "application/json")
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
        if self.parameters.security_group_id is not None:
            body_param["securityGroupID"] = self.parameters.security_group_id
        if self.parameters.port_ids is not None:
            body_param["portIDs"] = self.parameters.port_ids
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


class SgBatchAttachPortsRequestParam(object):

    def __init__(self, region_id, security_group_id, port_ids, client_token=None):
        """
        :param region_id: 区域ID
        :param security_group_id: 安全组ID
        :param port_ids: 网卡ID列表 注意:此参数为数组
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.region_id = region_id
        self.security_group_id = security_group_id
        self.port_ids = port_ids
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.security_group_id is None:
            raise Exception("security_group_id can not None")
        if self.port_ids is None:
            raise Exception("port_ids can not None")

