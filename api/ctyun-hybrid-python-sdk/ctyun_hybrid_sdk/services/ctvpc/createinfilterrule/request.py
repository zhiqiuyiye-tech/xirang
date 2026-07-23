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


class CreateInFilterRuleRequest(CTYunRequest):
    """
    destPort与srcPort 起始端口必须小于结束端口 当协议为ALL/ICMP时，端口传'-'
    """

    def __init__(self, request_param):
        super(CreateInFilterRuleRequest, self).__init__("/v4/mirrorflow/create-filter-in-rule", "POST", "ctvpc", "application/json")
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
        if self.parameters.mirror_filter_id is not None:
            body_param["mirrorFilterID"] = self.parameters.mirror_filter_id
        if self.parameters.dest_cidr is not None:
            body_param["destCidr"] = self.parameters.dest_cidr
        if self.parameters.src_cidr is not None:
            body_param["srcCidr"] = self.parameters.src_cidr
        if self.parameters.dest_port is not None:
            body_param["destPort"] = self.parameters.dest_port
        if self.parameters.src_port is not None:
            body_param["srcPort"] = self.parameters.src_port
        if self.parameters.protocol is not None:
            body_param["protocol"] = self.parameters.protocol
        if self.parameters.enable_collection is not None:
            body_param["enableCollection"] = self.parameters.enable_collection
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


class CreateInFilterRuleRequestParam(object):

    def __init__(self, region_id, mirror_filter_id, dest_cidr, src_cidr, dest_port, src_port, protocol, enable_collection, ):
        """
        :param region_id: 区域ID
        :param mirror_filter_id: 过滤条件 ID
        :param dest_cidr: 目标 cidr
        :param src_cidr: 源 cidr
        :param dest_port: 目的端口：格式为“起始端口/结束端口”，且起始端口不能大于结束端口。当协议为 ALL 或ICMP，传值"-"(不限端口)
        :param src_port: 源端口：格式为“起始端口/结束端口”，且起始端口不能大于结束端口。当协议为 ALL 或ICMP，传值"-"(不限端口)
        :param protocol: 协议：TCP、UDP、ICMP、ALL 大小写均可
        :param enable_collection: 是否开启采集，true 表示采集，false 表示不采集
        """
        self.region_id = region_id
        self.mirror_filter_id = mirror_filter_id
        self.dest_cidr = dest_cidr
        self.src_cidr = src_cidr
        self.dest_port = dest_port
        self.src_port = src_port
        self.protocol = protocol
        self.enable_collection = enable_collection

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.mirror_filter_id is None:
            raise Exception("mirror_filter_id can not None")
        if self.dest_cidr is None:
            raise Exception("dest_cidr can not None")
        if self.src_cidr is None:
            raise Exception("src_cidr can not None")
        if self.dest_port is None:
            raise Exception("dest_port can not None")
        if self.src_port is None:
            raise Exception("src_port can not None")
        if self.protocol is None:
            raise Exception("protocol can not None")
        if self.enable_collection is None:
            raise Exception("enable_collection can not None")

