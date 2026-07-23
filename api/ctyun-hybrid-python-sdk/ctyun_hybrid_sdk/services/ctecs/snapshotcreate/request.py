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


class SnapshotCreateRequest(CTYunRequest):
    """
    创建云主机快照
    """

    def __init__(self, request_param):
        super(SnapshotCreateRequest, self).__init__("/v4/ecs/snapshot/create", "POST", "ctecs", "application/json")
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
        if self.parameters.snapshot_name is not None:
            body_param["snapshotName"] = self.parameters.snapshot_name
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


class SnapshotCreateRequestParam(object):

    def __init__(self, region_id, instance_id, snapshot_name, ):
        """
        :param region_id: 区域ID
        :param instance_id: 云主机id
        :param snapshot_name: 云主机快照名称，不允许与已有的重复。满足以下规则：不能使用中文，且长度为2-63字符
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.snapshot_name = snapshot_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.snapshot_name is None:
            raise Exception("snapshot_name can not None")

