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


class GetFreeIpHybridRequest(CTYunRequest):
    """
    查询资源池所有可用eip地址
    """

    def __init__(self, request_param):
        super(GetFreeIpHybridRequest, self).__init__("/v4/eip/get-free-ip", "POST", "ctvpc", "application/json")
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
        if self.parameters.provider is not None:
            body_param["provider"] = self.parameters.provider
        if self.parameters.floating_ip_cidrs is not None:
            body_param["floatingIpCidrs"] = self.parameters.floating_ip_cidrs
        if self.parameters.is_segment is not None:
            body_param["isSegment"] = self.parameters.is_segment
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


class GetFreeIpHybridRequestParam(object):

    def __init__(self, region_id, provider=None, floating_ip_cidrs=None, is_segment=None):
        """
        :param region_id: 资源池ID
        :param provider: 不传默认是internet，可通过/v4/eip/EIPGateway/listEIPName查询
        :param floating_ip_cidrs: 查询该网段内可用弹性IP，格式：起始IP-终止IP，多个网段用逗号隔开
        :param is_segment: 不传或传0、false等--返回格式是弹性ip地址列表，例如：['192.168.1.250', '192.168.1.251' ]。传true--返回是可用弹性IP网段列表，如['192.168.1.250-192.168.1.254', '192.168.2.1-192.168.2.5']
        """
        self.region_id = region_id
        self.provider = provider
        self.floating_ip_cidrs = floating_ip_cidrs
        self.is_segment = is_segment

    def set_provider(self, provider):
        """
        :param provider: 不传默认是internet，可通过/v4/eip/EIPGateway/listEIPName查询
        """
        self.provider = provider

    def set_floating_ip_cidrs(self, floating_ip_cidrs):
        """
        :param floating_ip_cidrs: 查询该网段内可用弹性IP，格式：起始IP-终止IP，多个网段用逗号隔开
        """
        self.floating_ip_cidrs = floating_ip_cidrs

    def set_is_segment(self, is_segment):
        """
        :param is_segment: 不传或传0、false等--返回格式是弹性ip地址列表，例如：['192.168.1.250', '192.168.1.251' ]。传true--返回是可用弹性IP网段列表，如['192.168.1.250-192.168.1.254', '192.168.2.1-192.168.2.5']
        """
        self.is_segment = is_segment

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

