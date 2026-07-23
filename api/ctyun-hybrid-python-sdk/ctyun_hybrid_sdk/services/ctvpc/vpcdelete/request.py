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


class VpcDeleteRequest(CTYunRequest):
    """
    删除专有网络   
    删除专有网络之前，需要先删除所有子网，且需要删除子网内所有的云资源，包括ECS、弹性裸金属服务器、弹性负载均衡、NAT网关、高可用虚拟 IP 等，需要将子网内的占用IP的资源全部释放。
    """

    def __init__(self, request_param):
        super(VpcDeleteRequest, self).__init__("/v4/vpc/delete", "POST", "ctvpc", "application/json")
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
            body_param["regionId"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
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


class VpcDeleteRequestParam(object):

    def __init__(self, region_id, vpc_id, ):
        """
        :param region_id: 资源池 ID（差异点说明：公有云文档为regionID，2.0适配了regionID和regionId，传哪个字段都行）
        :param vpc_id: 虚拟网络ID
        """
        self.region_id = region_id
        self.vpc_id = vpc_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")

