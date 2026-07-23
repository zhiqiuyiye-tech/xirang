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


class CtvpnUserGatewayAddRequest(CTYunRequest):
    """
    用户网关创建
    """

    def __init__(self, request_param):
        super(CtvpnUserGatewayAddRequest, self).__init__("/v4/vpn/user-gateway/add", "POST", "ctvpn", "application/json")
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
        if self.parameters.customer_id is not None:
            body_param["customerID"] = self.parameters.customer_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.ip_address is not None:
            body_param["ipAddress"] = self.parameters.ip_address
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


class CtvpnUserGatewayAddRequestParam(object):

    def __init__(self, region_id, customer_id, name, ip_address, project_id=None):
        """
        :param region_id: 资源池id
        :param customer_id: 用户id
        :param name: 用户网关名称,长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param ip_address: ip地址
        :param project_id: 企业项目id，若传了此参数，则资源归属于该企业项目
        """
        self.region_id = region_id
        self.customer_id = customer_id
        self.name = name
        self.ip_address = ip_address
        self.project_id = project_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id，若传了此参数，则资源归属于该企业项目
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.customer_id is None:
            raise Exception("customer_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.ip_address is None:
            raise Exception("ip_address can not None")

