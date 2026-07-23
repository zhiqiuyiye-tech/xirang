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


class CheckIpAvailableRequest(CTYunRequest):
    """
    检查子网IP是否可用
    """

    def __init__(self, request_param):
        super(CheckIpAvailableRequest, self).__init__("/v4/vpc/check-ip-avaliable", "GET", "ctvpc", "")
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
        if self.parameters.subnet_id is not None:
            query_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.fixed_ip is not None:
            query_param["fixedIP"] = self.parameters.fixed_ip
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class CheckIpAvailableRequestParam(object):

    def __init__(self, region_id, subnet_id, fixed_ip, ):
        """
        :param region_id: 资源池ID
        :param subnet_id: 子网ID
        :param fixed_ip: IP地址，支持ipv4和ipv6地址
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.fixed_ip = fixed_ip

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.fixed_ip is None:
            raise Exception("fixed_ip can not None")

