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


class AddNicRequest(CTYunRequest):
    """
    添加物理机网卡   
    1.普通版不支持添加安全组   
    2.添加网卡需要关机状态   
    3.普通版本不支持添加网卡
    """

    def __init__(self, request_param):
        super(AddNicRequest, self).__init__("/v4/ebm/add-nic", "POST", "ebm", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.subnet_uuid is not None:
            body_param["subnetUUID"] = self.parameters.subnet_uuid
        if self.parameters.security_groups is not None:
            body_param["securityGroups"] = self.parameters.security_groups
        if self.parameters.ipv4 is not None:
            body_param["ipv4"] = self.parameters.ipv4
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


class AddNicRequestParam(object):

    def __init__(self, region_id, instance_uuid, subnet_uuid, az_name=None, security_groups=None, ipv4=None):
        """
        :param region_id: 资源池id
        :param az_name: 可用区
        :param instance_uuid: 实例UUID
        :param subnet_uuid: 子网UUID
        :param security_groups: 安全组id，多个逗号分隔
        :param ipv4: IPV4地址
        """
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid = instance_uuid
        self.subnet_uuid = subnet_uuid
        self.security_groups = security_groups
        self.ipv4 = ipv4

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_security_groups(self, security_groups):
        """
        :param security_groups: 安全组id，多个逗号分隔
        """
        self.security_groups = security_groups

    def set_ipv4(self, ipv4):
        """
        :param ipv4: IPV4地址
        """
        self.ipv4 = ipv4

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.subnet_uuid is None:
            raise Exception("subnet_uuid can not None")

