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


class SfsIopsReadRequest(CTYunRequest):
    """
    查询文件系统历史读IOPS信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
    """

    def __init__(self, request_param):
        super(SfsIopsReadRequest, self).__init__("/v4/sfs/iops-read", "GET", "sfs", "application/json")
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
        if self.parameters.uid is not None:
            body_param["UID"] = self.parameters.uid
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class SfsIopsReadRequestParam(object):

    def __init__(self, region_id, uid, start_time, end_time, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param uid: 文件系统ID
        :param start_time: 开始时间，时间格式yyyy-MM-dd HH:mm:ss
        :param end_time: 结束时间，时间格式yyyy-MM-dd HH:mm:ss
        :param page_no: 查询的页码,大于等于1，传0不分页
        :param page_size: 每页的元素个数 取值范围[1, 1000]，传0不分页
        """
        self.region_id = region_id
        self.uid = uid
        self.start_time = start_time
        self.end_time = end_time
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 查询的页码,大于等于1，传0不分页
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页的元素个数 取值范围[1, 1000]，传0不分页
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.uid is None:
            raise Exception("uid can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

