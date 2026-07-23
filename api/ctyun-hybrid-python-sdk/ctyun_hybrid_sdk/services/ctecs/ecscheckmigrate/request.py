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


class EcsCheckMigrateRequest(CTYunRequest):
    """
    云主机热迁移校验
    """

    def __init__(self, request_param):
        super(EcsCheckMigrateRequest, self).__init__("/v4/ecs/check-ecs-migrate", "POST", "ctecs", "application/json")
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
        if self.parameters.ecs_ids is not None:
            body_param["ecsIDs"] = self.parameters.ecs_ids
        if self.parameters.host_id is not None:
            body_param["hostID"] = self.parameters.host_id
        if self.parameters.is_live is not None:
            body_param["isLive"] = self.parameters.is_live
        if self.parameters.source_host_name is not None:
            body_param["sourceHostName"] = self.parameters.source_host_name
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


class EcsCheckMigrateRequestParam(object):

    def __init__(self, region_id, ecs_ids, host_id=None, is_live=None, source_host_name=None):
        """
        :param region_id: 资源池id
        :param ecs_ids: 虚机列表 注意:此参数为数组
        :param host_id: 目标宿主机id或uuid
        :param is_live: 是否热迁移，默认否-即冷迁移（ecsIDs同时需要传关机状态的虚机列表），热迁移（ecsIDs需要传开启状态的虚机列表）
        :param source_host_name: 源宿主机名称
        """
        self.region_id = region_id
        self.ecs_ids = ecs_ids
        self.host_id = host_id
        self.is_live = is_live
        self.source_host_name = source_host_name

    def set_host_id(self, host_id):
        """
        :param host_id: 目标宿主机id或uuid
        """
        self.host_id = host_id

    def set_is_live(self, is_live):
        """
        :param is_live: 是否热迁移，默认否-即冷迁移（ecsIDs同时需要传关机状态的虚机列表），热迁移（ecsIDs需要传开启状态的虚机列表）
        """
        self.is_live = is_live

    def set_source_host_name(self, source_host_name):
        """
        :param source_host_name: 源宿主机名称
        """
        self.source_host_name = source_host_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.ecs_ids is None:
            raise Exception("ecs_ids can not None")

