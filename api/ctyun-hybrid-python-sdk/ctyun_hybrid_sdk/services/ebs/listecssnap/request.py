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


class ListEcsSnapRequest(CTYunRequest):
    """
    参数请求方式说明：该GET请求参数通过body传输
    """

    def __init__(self, request_param):
        super(ListEcsSnapRequest, self).__init__("/v4/ebs_snapshot/list", "GET", "ebs", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.volume_id is not None:
            query_param["volumeID"] = self.parameters.volume_id
        if self.parameters.snapshot_id is not None:
            query_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.snapshot_name is not None:
            query_param["snapshotName"] = self.parameters.snapshot_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEcsSnapRequestParam(object):

    def __init__(self, region_id, volume_id=None, snapshot_id=None, snapshot_name=None):
        """
        :param region_id: 资源池ID
        :param volume_id: 云硬盘ID
        :param snapshot_id: 云硬盘快照ID
        :param snapshot_name: 云硬盘快照名称，支持输入名称的一部分做模糊匹配
        """
        self.region_id = region_id
        self.volume_id = volume_id
        self.snapshot_id = snapshot_id
        self.snapshot_name = snapshot_name

    def set_volume_id(self, volume_id):
        """
        :param volume_id: 云硬盘ID
        """
        self.volume_id = volume_id

    def set_snapshot_id(self, snapshot_id):
        """
        :param snapshot_id: 云硬盘快照ID
        """
        self.snapshot_id = snapshot_id

    def set_snapshot_name(self, snapshot_name):
        """
        :param snapshot_name: 云硬盘快照名称，支持输入名称的一部分做模糊匹配
        """
        self.snapshot_name = snapshot_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

