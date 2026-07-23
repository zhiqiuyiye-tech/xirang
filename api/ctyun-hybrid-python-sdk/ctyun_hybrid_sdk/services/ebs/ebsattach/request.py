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


class EbsAttachRequest(CTYunRequest):
    """
    支持云硬盘挂载至某一云主机。   
    注意：   
    1. V1版本regionID是必传项，公有云官网regionID为选填项，V2对齐公有云；规则为：regionID可不传，如果传了regionID，该字段会被校验；   
    2. 云主机下限制挂载云硬盘个数上限为20
    """

    def __init__(self, request_param):
        super(EbsAttachRequest, self).__init__("/v4/ebs/attach", "POST", "ebs", "application/json")
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
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.resource_id is not None:
            body_param["resourceID"] = self.parameters.resource_id
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


class EbsAttachRequestParam(object):

    def __init__(self, instance_uuid, resource_id, region_id=None, disk_bus=None):
        """
        :param region_id: 区域ID；如本地语境支持保存regionID，那么建议传递
        :param instance_uuid: 云管平台虚机ID
        :param resource_id: 资源ID
        :param disk_bus: 挂载总线协议类型，2.2.6版本新增
        """
        self.region_id = region_id
        self.instance_uuid = instance_uuid
        self.resource_id = resource_id
        self.disk_bus = disk_bus

    def set_region_id(self, region_id):
        """
        :param region_id: 区域ID；如本地语境支持保存regionID，那么建议传递
        """
        self.region_id = region_id

    def set_disk_bus(self, disk_bus):
        """
        :param disk_bus: 挂载总线协议类型，2.2.6版本新增
        """
        self.disk_bus = disk_bus

    def check_param(self):
        """
        the param required check
        """
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.resource_id is None:
            raise Exception("resource_id can not None")

