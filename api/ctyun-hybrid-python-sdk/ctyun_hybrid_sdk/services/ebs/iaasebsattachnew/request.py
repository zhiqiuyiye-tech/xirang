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


class IaasEbsAttachNewRequest(CTYunRequest):
    """
    支持云硬盘挂载至某一云主机。   
    云主机下限制挂载云硬盘个数上限为20
    """

    def __init__(self, request_param):
        super(IaasEbsAttachNewRequest, self).__init__("/v4/ebs/attach-ebs", "POST", "ebs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.disk_bus is not None:
            body_param["diskBus"] = self.parameters.disk_bus
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


class IaasEbsAttachNewRequestParam(object):

    def __init__(self, instance_id, disk_id, region_id=None, client_token=None, disk_bus=None):
        """
        :param region_id: 区域ID	
        :param instance_id: 云主机ID
        :param disk_id: 磁盘ID
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        :param disk_bus: 挂载总线协议类型，2.2.6版本新增
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.disk_id = disk_id
        self.client_token = client_token
        self.disk_bus = disk_bus

    def set_region_id(self, region_id):
        """
        :param region_id: 区域ID	
        """
        self.region_id = region_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def set_disk_bus(self, disk_bus):
        """
        :param disk_bus: 挂载总线协议类型，2.2.6版本新增
        """
        self.disk_bus = disk_bus

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

