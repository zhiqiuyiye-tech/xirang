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


class CdaPhysicalLineBindRequest(CTYunRequest):
    """
    专线网关绑定物理专线
    """

    def __init__(self, request_param):
        super(CdaPhysicalLineBindRequest, self).__init__("/v4/cda/physical-line/bind", "POST", "cda", "application/json")
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
        if self.parameters.gateway_name is not None:
            body_param["gatewayName"] = self.parameters.gateway_name
        if self.parameters.line_id is not None:
            body_param["lineID"] = self.parameters.line_id
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


class CdaPhysicalLineBindRequestParam(object):

    def __init__(self, gateway_name, line_id, region_id=None):
        """
        :param region_id: 此接口中无实际意义
        :param gateway_name: 专线网关名称
        :param line_id: 物理专线id
        """
        self.region_id = region_id
        self.gateway_name = gateway_name
        self.line_id = line_id

    def set_region_id(self, region_id):
        """
        :param region_id: 此接口中无实际意义
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.gateway_name is None:
            raise Exception("gateway_name can not None")
        if self.line_id is None:
            raise Exception("line_id can not None")

