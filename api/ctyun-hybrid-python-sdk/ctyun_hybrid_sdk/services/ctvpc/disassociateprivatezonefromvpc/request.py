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


class DisassociatePrivateZoneFromVpcRequest(CTYunRequest):
    """
    内网取消 DNS 关联 VPC
    """

    def __init__(self, request_param):
        super(DisassociatePrivateZoneFromVpcRequest, self).__init__("/v4/private-zone/disassociate-vpc", "POST", "ctvpc", "application/json")
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
        if self.parameters.vpc_id_list is not None:
            body_param["vpcIDList"] = self.parameters.vpc_id_list
        if self.parameters.zone_id is not None:
            body_param["zoneID"] = self.parameters.zone_id
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


class DisassociatePrivateZoneFromVpcRequestParam(object):

    def __init__(self, region_id, vpc_id_list, zone_id, client_token=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param vpc_id_list: 关联的vpc,多个vpc用逗号隔开
        :param zone_id: 内网DNS的id
        :param project_id: 企业项目ID，默认为"0"
        """
        self.client_token = client_token
        self.region_id = region_id
        self.vpc_id_list = vpc_id_list
        self.zone_id = zone_id
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为"0"
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id_list is None:
            raise Exception("vpc_id_list can not None")
        if self.zone_id is None:
            raise Exception("zone_id can not None")

