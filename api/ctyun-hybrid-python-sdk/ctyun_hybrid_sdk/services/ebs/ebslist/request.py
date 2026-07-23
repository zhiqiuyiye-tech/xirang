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


class EbsListRequest(CTYunRequest):
    """
    云硬盘信息列表   
    1. 冗余返回results，兼容V1字段   
    2.2.6版本: 新增diskBus挂载协议字段返回。
    """

    def __init__(self, request_param):
        super(EbsListRequest, self).__init__("/v4/ebs/list", "GET", "ebs", "")
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
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.resource_id is not None:
            query_param["resourceId"] = self.parameters.resource_id
        if self.parameters.cluster_id is not None:
            query_param["clusterID"] = self.parameters.cluster_id
        if self.parameters.disk_mode is not None:
            query_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.disk_ids is not None:
            query_param["diskIDs"] = self.parameters.disk_ids
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EbsListRequestParam(object):

    def __init__(self, region_id, page_no=None, page_size=None, resource_id=None, cluster_id=None, disk_mode=None, disk_ids=None):
        """
        :param region_id: 资源池id
        :param page_no: 页码，默认1
        :param page_size: 页大小，默认10，范围[1-100]，大于100取100，不传、传0取10
        :param resource_id: 资源id
        :param cluster_id: 云盘所属集群ID
        :param disk_mode: 磁盘模式,可选值:VBD/ISCSI/FCSAN,多个用逗号分隔
        :param disk_ids: 云硬盘ID列表，2.2.6版本支持 注意:此参数为数组
        """
        self.region_id = region_id
        self.page_no = page_no
        self.page_size = page_size
        self.resource_id = resource_id
        self.cluster_id = cluster_id
        self.disk_mode = disk_mode
        self.disk_ids = disk_ids

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 页大小，默认10，范围[1-100]，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id
        """
        self.resource_id = resource_id

    def set_cluster_id(self, cluster_id):
        """
        :param cluster_id: 云盘所属集群ID
        """
        self.cluster_id = cluster_id

    def set_disk_mode(self, disk_mode):
        """
        :param disk_mode: 磁盘模式,可选值:VBD/ISCSI/FCSAN,多个用逗号分隔
        """
        self.disk_mode = disk_mode

    def set_disk_ids(self, disk_ids):
        """
        :param disk_ids: 云硬盘ID列表，2.2.6版本支持
        """
        self.disk_ids = disk_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

