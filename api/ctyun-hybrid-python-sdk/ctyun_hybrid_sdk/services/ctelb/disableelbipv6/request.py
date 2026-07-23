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


class DisableElbIpv6Request(CTYunRequest):
    """
    负载均衡关闭IPv6   
    3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的   
    #### 备注   
    * 不支持 3.0，因为 3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的
    """

    def __init__(self, request_param):
        super(DisableElbIpv6Request, self).__init__("/v4/elb/disable-ipv6", "POST", "ctelb", "application/json")
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


class DisableElbIpv6RequestParam(object):

    def __init__(self, region_id, elb_id, ):
        """
        :param region_id: 资源池ID
        :param elb_id: 弹性负载均衡 ID
        """
        self.region_id = region_id
        self.elb_id = elb_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.elb_id is None:
            raise Exception("elb_id can not None")

