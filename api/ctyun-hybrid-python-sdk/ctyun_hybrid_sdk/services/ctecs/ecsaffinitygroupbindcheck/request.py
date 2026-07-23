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


class EcsAffinityGroupBindCheckRequest(CTYunRequest):
    """
    接口功能介绍   
    可以根据用户给定的云主机与云主机组，校验当前情况下是否可以将云主机加入主机组。如果可以则返回值中needMigrate字段为0，反之则需要将云主机迁移。   
       
    接口约束   
    当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用新版本接口，新版本接口更加规范，覆盖场景更全。   
    云主机需处于运行中（running）或关机（stopped）状态
    """

    def __init__(self, request_param):
        super(EcsAffinityGroupBindCheckRequest, self).__init__("/v4/ecs/affinity-group/bind-check", "POST", "ctecs", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.affinity_group_id is not None:
            body_param["affinityGroupID"] = self.parameters.affinity_group_id
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


class EcsAffinityGroupBindCheckRequestParam(object):

    def __init__(self, region_id, id, affinity_group_id, az_name=None):
        """
        :param region_id: 资源id
        :param az_name: 可用区名称 --暂无提供 可不传
        :param id: 云主机id
        :param affinity_group_id: 云主机组id
        """
        self.region_id = region_id
        self.az_name = az_name
        self.id = id
        self.affinity_group_id = affinity_group_id

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称 --暂无提供 可不传
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.affinity_group_id is None:
            raise Exception("affinity_group_id can not None")

