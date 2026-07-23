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


class SnapshotListVdcRequest(CTYunRequest):
    """
    查询云主机快照列表，该接口1.16.06及以上云管版本支持。
    """

    def __init__(self, request_param):
        super(SnapshotListVdcRequest, self).__init__("/v4/ecs/snapshot/list-vdc", "POST", "ctecs", "application/json")
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
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.snapshot_status is not None:
            body_param["snapshotStatus"] = self.parameters.snapshot_status
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.query_content is not None:
            body_param["queryContent"] = self.parameters.query_content
        if self.parameters.snapshot_name is not None:
            body_param["snapshotName"] = self.parameters.snapshot_name
        if self.parameters.org_id is not None:
            body_param["orgId"] = self.parameters.org_id
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


class SnapshotListVdcRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, instance_id=None, snapshot_status=None, snapshot_id=None, query_content=None, snapshot_name=None, org_id=None):
        """
        :param region_id: 区域ID
        :param page_no: 页码，默认值:1
        :param page_size: 每页记录数目
        :param instance_id: 云主机实例ID
        :param snapshot_status: 快照状态  公有云字段，混合云暂不支持，忽略
        :param snapshot_id: 云主机快照实例ID
        :param query_content: 模糊查找，根据快照名称、快照uuid、创建快照的云主机名称或创建快照的云主机uuid是否包含或等于该参数值进行筛选
        :param snapshot_name: 快照名称
        :param org_id: 组织id
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.instance_id = instance_id
        self.snapshot_status = snapshot_status
        self.snapshot_id = snapshot_id
        self.query_content = query_content
        self.snapshot_name = snapshot_name
        self.org_id = org_id

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认值:1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目
        """
        self.page_size = page_size

    def set_instance_id(self, instance_id):
        """
        :param instance_id: 云主机实例ID
        """
        self.instance_id = instance_id

    def set_snapshot_status(self, snapshot_status):
        """
        :param snapshot_status: 快照状态  公有云字段，混合云暂不支持，忽略
        """
        self.snapshot_status = snapshot_status

    def set_snapshot_id(self, snapshot_id):
        """
        :param snapshot_id: 云主机快照实例ID
        """
        self.snapshot_id = snapshot_id

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查找，根据快照名称、快照uuid、创建快照的云主机名称或创建快照的云主机uuid是否包含或等于该参数值进行筛选
        """
        self.query_content = query_content

    def set_snapshot_name(self, snapshot_name):
        """
        :param snapshot_name: 快照名称
        """
        self.snapshot_name = snapshot_name

    def set_org_id(self, org_id):
        """
        :param org_id: 组织id
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

