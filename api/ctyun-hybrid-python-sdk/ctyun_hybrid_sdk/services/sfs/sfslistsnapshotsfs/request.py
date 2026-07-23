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


class SfsListSnapshotSfsRequest(CTYunRequest):
    """
    弹性文件查询快照
    """

    def __init__(self, request_param):
        super(SfsListSnapshotSfsRequest, self).__init__("/v4/sfs/snapshot/list", "GET", "sfs", "")
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
        if self.parameters.uid is not None:
            query_param["UID"] = self.parameters.uid
        if self.parameters.snapshot_id is not None:
            query_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class SfsListSnapshotSfsRequestParam(object):

    def __init__(self, region_id, uid=None, snapshot_id=None, page_size=None, page_no=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param uid: 弹性文件ID
        :param snapshot_id: 快照ID
        :param page_size: 每页包含的元素个数，默认10，可选范围1-100，不传、传0取10，大于100取100
        :param page_no: 列表的分页页码
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.uid = uid
        self.snapshot_id = snapshot_id
        self.page_size = page_size
        self.page_no = page_no
        self.project_id = project_id

    def set_uid(self, uid):
        """
        :param uid: 弹性文件ID
        """
        self.uid = uid

    def set_snapshot_id(self, snapshot_id):
        """
        :param snapshot_id: 快照ID
        """
        self.snapshot_id = snapshot_id

    def set_page_size(self, page_size):
        """
        :param page_size: 每页包含的元素个数，默认10，可选范围1-100，不传、传0取10，大于100取100
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的分页页码
        """
        self.page_no = page_no

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

