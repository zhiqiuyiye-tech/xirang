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


class SfsZoneListsfsRequest(CTYunRequest):
    """
    注意：目前底层只有performance和capacity类型，fileSystemType传入hdd_e，列表返回为空。
    """

    def __init__(self, request_param):
        super(SfsZoneListsfsRequest, self).__init__("/v4/sfs/zonelist", "GET", "sfs", "")
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
        if self.parameters.file_system_type is not None:
            query_param["fileSystemType"] = self.parameters.file_system_type
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


class SfsZoneListsfsRequestParam(object):

    def __init__(self, region_id, file_system_type=None, page_size=None, page_no=None):
        """
        :param region_id: 资源池ID
        :param file_system_type: 文件系统类型，取值范围：performance-性能型、capacity-标准型、hdd_e-标准型专属。不传表示查询所有类型
        :param page_size: 分页查询时每页包含的地域数（即可用区个数），默认为10，范围[1-100]，大于100取100，小于1取10
        :param page_no: 页码，默认为1
        """
        self.region_id = region_id
        self.file_system_type = file_system_type
        self.page_size = page_size
        self.page_no = page_no

    def set_file_system_type(self, file_system_type):
        """
        :param file_system_type: 文件系统类型，取值范围：performance-性能型、capacity-标准型、hdd_e-标准型专属。不传表示查询所有类型
        """
        self.file_system_type = file_system_type

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页包含的地域数（即可用区个数），默认为10，范围[1-100]，大于100取100，小于1取10
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，默认为1
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

