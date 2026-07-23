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


class EcsSnapshotRestoreRequest(CTYunRequest):
    """
    恢复云主机快照   
       
    ### 接口约束   
       
    1. 至少存在一个快照   
    2. 快照的状态为可用   
    3. 云主机存在且状态为关机
    """

    def __init__(self, request_param):
        super(EcsSnapshotRestoreRequest, self).__init__("/v4/ecs/snapshot-restore", "POST", "ctecs", "application/json")
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
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
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


class EcsSnapshotRestoreRequestParam(object):

    def __init__(self, region_id, snapshot_id, ):
        """
        :param region_id: 资源池ID
        :param snapshot_id: 云主机快照实例ID
        """
        self.region_id = region_id
        self.snapshot_id = snapshot_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")

