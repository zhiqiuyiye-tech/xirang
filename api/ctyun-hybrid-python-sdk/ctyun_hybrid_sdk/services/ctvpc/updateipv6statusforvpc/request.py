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


class UpdateIPv6StatusForVpcRequest(CTYunRequest):
    """
    修改VPC的 IPv6 状态
    """

    def __init__(self, request_param):
        super(UpdateIPv6StatusForVpcRequest, self).__init__("/v4/vpc/update-ipv6-status", "POST", "ctvpc", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.enable_ipv6 is not None:
            body_param["enableIpv6"] = self.parameters.enable_ipv6
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class UpdateIPv6StatusForVpcRequestParam(object):

    def __init__(self, region_id, vpc_id, enable_ipv6, client_token=None, project_id=None):
        """
        :param region_id: 资源池 ID
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param vpc_id: VPC 的ID
        :param enable_ipv6: 是否开启 IPv6 网段。取值：false（默认值）:不开启，true: 开启
        :param project_id: 企业项目 ID，默认为"0"，公有云参数，暂无意义
        """
        self.region_id = region_id
        self.client_token = client_token
        self.vpc_id = vpc_id
        self.enable_ipv6 = enable_ipv6
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认为"0"，公有云参数，暂无意义
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.enable_ipv6 is None:
            raise Exception("enable_ipv6 can not None")

