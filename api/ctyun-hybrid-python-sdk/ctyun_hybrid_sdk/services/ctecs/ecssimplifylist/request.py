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


class EcsSimplifyListRequest(CTYunRequest):
    """
    查询云主机列表
    """

    def __init__(self, request_param):
        super(EcsSimplifyListRequest, self).__init__("/v4/ecs/simplify-list", "POST", "ctecs", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.project_name is not None:
            query_param["projectName"] = self.parameters.project_name
        if self.parameters.ecs_ids is not None:
            query_param["ecsIDs"] = self.parameters.ecs_ids
        if self.parameters.freezed is not None:
            query_param["freezed"] = self.parameters.freezed
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.ecs_uuids is not None:
            query_param["ecsUuids"] = self.parameters.ecs_uuids
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.ecs_uuid is not None:
            query_param["ecsUUID"] = self.parameters.ecs_uuid
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.cty_nfs_mount is not None:
            query_param["ctyNfsMount"] = self.parameters.cty_nfs_mount
        if self.parameters.vpc_ids is not None:
            query_param["vpcIDs"] = self.parameters.vpc_ids
        if self.parameters.os_type is not None:
            query_param["osType"] = self.parameters.os_type
        if self.parameters.az_id is not None:
            query_param["azID"] = self.parameters.az_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EcsSimplifyListRequestParam(object):

    def __init__(self, region_id, project_id=None, project_name=None, ecs_ids=None, freezed=None, name=None, status=None, sort=None, asc=None, ecs_uuids=None, vpc_id=None, ecs_uuid=None, query_content=None, cty_nfs_mount=None, vpc_ids=None, os_type=None, az_id=None):
        """
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        :param project_name: 企业项目名称
        :param ecs_ids: 支持输入 多个云主机ID  以逗号分隔
        :param freezed: 1 回收站 2 非回收站 3 全部
        :param name: 展示名称，过滤
        :param status: 云主机状态
        :param sort: 需排序字段
        :param asc: asc 表示按升序排序，desc 表示按降序排序
        :param ecs_uuids: 支持输入 多个云主机uuid  以逗号分隔
        :param vpc_id: 0603新增
        :param ecs_uuid: 云主机UUID
        :param query_content: 模糊查询字段
        :param cty_nfs_mount: 云主机镜像是否支持挂载，1-是，2-否
        :param vpc_ids: vpcID数组，英文逗号分割
        :param os_type: 云主机操作系统类型筛选，linux和windows，多个英文逗号分割
        :param az_id: 可用区id,多个英文逗号分割
        """
        self.region_id = region_id
        self.project_id = project_id
        self.project_name = project_name
        self.ecs_ids = ecs_ids
        self.freezed = freezed
        self.name = name
        self.status = status
        self.sort = sort
        self.asc = asc
        self.ecs_uuids = ecs_uuids
        self.vpc_id = vpc_id
        self.ecs_uuid = ecs_uuid
        self.query_content = query_content
        self.cty_nfs_mount = cty_nfs_mount
        self.vpc_ids = vpc_ids
        self.os_type = os_type
        self.az_id = az_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_project_name(self, project_name):
        """
        :param project_name: 企业项目名称
        """
        self.project_name = project_name

    def set_ecs_ids(self, ecs_ids):
        """
        :param ecs_ids: 支持输入 多个云主机ID  以逗号分隔
        """
        self.ecs_ids = ecs_ids

    def set_freezed(self, freezed):
        """
        :param freezed: 1 回收站 2 非回收站 3 全部
        """
        self.freezed = freezed

    def set_name(self, name):
        """
        :param name: 展示名称，过滤
        """
        self.name = name

    def set_status(self, status):
        """
        :param status: 云主机状态
        """
        self.status = status

    def set_sort(self, sort):
        """
        :param sort: 需排序字段
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: asc 表示按升序排序，desc 表示按降序排序
        """
        self.asc = asc

    def set_ecs_uuids(self, ecs_uuids):
        """
        :param ecs_uuids: 支持输入 多个云主机uuid  以逗号分隔
        """
        self.ecs_uuids = ecs_uuids

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 0603新增
        """
        self.vpc_id = vpc_id

    def set_ecs_uuid(self, ecs_uuid):
        """
        :param ecs_uuid: 云主机UUID
        """
        self.ecs_uuid = ecs_uuid

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查询字段
        """
        self.query_content = query_content

    def set_cty_nfs_mount(self, cty_nfs_mount):
        """
        :param cty_nfs_mount: 云主机镜像是否支持挂载，1-是，2-否
        """
        self.cty_nfs_mount = cty_nfs_mount

    def set_vpc_ids(self, vpc_ids):
        """
        :param vpc_ids: vpcID数组，英文逗号分割
        """
        self.vpc_ids = vpc_ids

    def set_os_type(self, os_type):
        """
        :param os_type: 云主机操作系统类型筛选，linux和windows，多个英文逗号分割
        """
        self.os_type = os_type

    def set_az_id(self, az_id):
        """
        :param az_id: 可用区id,多个英文逗号分割
        """
        self.az_id = az_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

