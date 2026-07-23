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


class SfsListReadWriteSfsRequest(CTYunRequest):
    """
    查看文件系统只读/读写信息
    """

    def __init__(self, request_param):
        super(SfsListReadWriteSfsRequest, self).__init__("/v4/sfs/list-rw", "GET", "sfs", "application/json")
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


class SfsListReadWriteSfsRequestParam(object):

    def __init__(self, region_id, uid=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param uid: 文件系统ID
        :param page_no: 查询的页码，默认为1
        :param page_size: 每页的元素个数 取值范围[1, 100]，默认为10，大于100取100，不传、传0取10
        """
        self.region_id = region_id
        self.uid = uid
        self.page_no = page_no
        self.page_size = page_size

    def set_uid(self, uid):
        """
        :param uid: 文件系统ID
        """
        self.uid = uid

    def set_page_no(self, page_no):
        """
        :param page_no: 查询的页码，默认为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页的元素个数 取值范围[1, 100]，默认为10，大于100取100，不传、传0取10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

