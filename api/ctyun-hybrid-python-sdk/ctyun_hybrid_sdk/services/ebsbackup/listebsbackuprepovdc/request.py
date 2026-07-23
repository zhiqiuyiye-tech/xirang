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


class ListEbsBackupRepoVdcRequest(CTYunRequest):
    """
    查询云硬盘备份库列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。   
    2.2.6版本新增支持返回容量告警阈值capacityAlertThreshold
    """

    def __init__(self, request_param):
        super(ListEbsBackupRepoVdcRequest, self).__init__("/v4/ebs-backup/repo/list-vdc", "GET", "ebsbackup", "")
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
        if self.parameters.repository_id is not None:
            query_param["repositoryID"] = self.parameters.repository_id
        if self.parameters.repository_name is not None:
            query_param["repositoryName"] = self.parameters.repository_name
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        if self.parameters.hide_expire is not None:
            query_param["hideExpire"] = self.parameters.hide_expire
        if self.parameters.asc is not None:
            query_param["asc"] = self.parameters.asc
        if self.parameters.sort is not None:
            query_param["sort"] = self.parameters.sort
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEbsBackupRepoVdcRequestParam(object):

    def __init__(self, region_id, repository_id=None, repository_name=None, status=None, query_content=None, hide_expire=None, asc=None, sort=None, resource_id=None, org_id=None):
        """
        :param region_id: 资源池id
        :param repository_id: 云硬盘备份存储库ID，支持模糊匹配
        :param repository_name: 云硬盘备份存储库名称，支持模糊匹配
        :param status: 云硬盘备份存储库状态:available-可用;unavailable-不可用
        :param query_content: 模糊查询，筛选存储库名称或id等于此参数值的存储库
        :param hide_expire: 是否隐藏过期的云硬盘备份库，true-隐藏，false-不隐藏
        :param asc: 和sort配合使用，是否升序排列 true-升序，false-降序，默认为false
        :param sort: 和asc配合使用，指定用于排序的字段。可选字段：createdDate/expiredDate/size/freeSize/name
        :param resource_id: 该参数和repositoryID二选一,同时存在时以repositoryID优先
        :param org_id: 组织ID
        """
        self.region_id = region_id
        self.repository_id = repository_id
        self.repository_name = repository_name
        self.status = status
        self.query_content = query_content
        self.hide_expire = hide_expire
        self.asc = asc
        self.sort = sort
        self.resource_id = resource_id
        self.org_id = org_id

    def set_repository_id(self, repository_id):
        """
        :param repository_id: 云硬盘备份存储库ID，支持模糊匹配
        """
        self.repository_id = repository_id

    def set_repository_name(self, repository_name):
        """
        :param repository_name: 云硬盘备份存储库名称，支持模糊匹配
        """
        self.repository_name = repository_name

    def set_status(self, status):
        """
        :param status: 云硬盘备份存储库状态:available-可用;unavailable-不可用
        """
        self.status = status

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊查询，筛选存储库名称或id等于此参数值的存储库
        """
        self.query_content = query_content

    def set_hide_expire(self, hide_expire):
        """
        :param hide_expire: 是否隐藏过期的云硬盘备份库，true-隐藏，false-不隐藏
        """
        self.hide_expire = hide_expire

    def set_asc(self, asc):
        """
        :param asc: 和sort配合使用，是否升序排列 true-升序，false-降序，默认为false
        """
        self.asc = asc

    def set_sort(self, sort):
        """
        :param sort: 和asc配合使用，指定用于排序的字段。可选字段：createdDate/expiredDate/size/freeSize/name
        """
        self.sort = sort

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 该参数和repositoryID二选一,同时存在时以repositoryID优先
        """
        self.resource_id = resource_id

    def set_org_id(self, org_id):
        """
        :param org_id: 组织ID
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

