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


class BatchRollbackEbsSnapRequest(CTYunRequest):
    """
    批量快照回滚（批量重置云硬盘）
    """

    def __init__(self, request_param):
        super(BatchRollbackEbsSnapRequest, self).__init__("/v4/ebs_snapshot/batch-rollback-ebs-snap", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_list is not None:
            body_param["snapshotList"] = self.parameters.snapshot_list
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class BatchRollbackEbsSnapRequestParam(object):

    def __init__(self, snapshot_list, region_id, az_name=None):
        """
        :param snapshot_list: 快照ID列表,以逗号分隔，最多8个；全部快照都存在才可进行批量重置。
        :param region_id: 资源池ID
        :param az_name: 多可用区资源池下，必须指定可用区。
        """
        self.snapshot_list = snapshot_list
        self.region_id = region_id
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 多可用区资源池下，必须指定可用区。
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.snapshot_list is None:
            raise Exception("snapshot_list can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

