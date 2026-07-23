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


class EnableElbIpv6Request(CTYunRequest):
    """
    负载均衡开启IPv6   
    3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的   
    #### 备注   
    * 不支持 3.0，因为 3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的
    """

    def __init__(self, request_param):
        super(EnableElbIpv6Request, self).__init__("/v4/elb/enable-ipv6", "POST", "ctelb", "application/json")
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
        if self.parameters.elb_id is not None:
            body_param["elbID"] = self.parameters.elb_id
        if self.parameters.ip is not None:
            body_param["ip"] = self.parameters.ip
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


class EnableElbIpv6RequestParam(object):

    def __init__(self, region_id, elb_id, ip=None):
        """
        :param region_id: 资源池ID
        :param elb_id: 负载均衡ID
        :param ip: ipv6 地址(1.0版本这个参数是必传，公有云为非必传，目前做成非必传，如果未指定该字段，则由系统从弹性负载均衡所在子网的 IPv6 地址段中分配一个未被分配使用的地址)
        """
        self.region_id = region_id
        self.elb_id = elb_id
        self.ip = ip

    def set_ip(self, ip):
        """
        :param ip: ipv6 地址(1.0版本这个参数是必传，公有云为非必传，目前做成非必传，如果未指定该字段，则由系统从弹性负载均衡所在子网的 IPv6 地址段中分配一个未被分配使用的地址)
        """
        self.ip = ip

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.elb_id is None:
            raise Exception("elb_id can not None")

