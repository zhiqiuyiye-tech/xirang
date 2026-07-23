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


class UpdateIpv6BandwidthOpenapiRequest(CTYunRequest):
    """
    修改ipv6带宽名称
    """

    def __init__(self, request_param):
        super(UpdateIpv6BandwidthOpenapiRequest, self).__init__("/v4/ipv6_bandwidth/update", "POST", "ctvpc", "application/json")
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
        if self.parameters.bandwidth_id is not None:
            body_param["bandwidthID"] = self.parameters.bandwidth_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class UpdateIpv6BandwidthOpenapiRequestParam(object):

    def __init__(self, region_id, bandwidth_id, name, ):
        """
        :param region_id: 资源池ID
        :param bandwidth_id: ipv6带宽ID
        :param name: ipv6带宽名称 长度为2～32字符 支持使用字母、数字、中划线（-）下划线(_)，只能以字母开头
        """
        self.region_id = region_id
        self.bandwidth_id = bandwidth_id
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bandwidth_id is None:
            raise Exception("bandwidth_id can not None")
        if self.name is None:
            raise Exception("name can not None")

