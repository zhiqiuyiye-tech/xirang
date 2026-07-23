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


class SfsListMountpointRequest(CTYunRequest):
    """
    对齐公有云，v1文档未有该接口定义
    """

    def __init__(self, request_param):
        super(SfsListMountpointRequest, self).__init__("/v4/sfs/list-mountpoint-sfs", "GET", "sfs", "")
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
        if self.parameters.sfs_uid is not None:
            query_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class SfsListMountpointRequestParam(object):

    def __init__(self, region_id, sfs_uid, page_size=None, page_no=None):
        """
        :param region_id: 资源池ID
        :param sfs_uid: 弹性文件系统ID
        :param page_size: 每页包含的数量，默认值10，范围[1, 100]，超过100按100查询，不传、传0取10
        :param page_no: 当前页码，默认值1
        """
        self.region_id = region_id
        self.sfs_uid = sfs_uid
        self.page_size = page_size
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页包含的数量，默认值10，范围[1, 100]，超过100按100查询，不传、传0取10
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 当前页码，默认值1
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")

