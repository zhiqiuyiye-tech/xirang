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


class VolumeListByVMRequest(CTYunRequest):
    """
    查询云主机挂载的云硬盘
    """

    def __init__(self, request_param):
        super(VolumeListByVMRequest, self).__init__("/v4/volume/list-by-vm", "GET", "ctecs", "")
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
        if self.parameters.vm_id is not None:
            query_param["vmID"] = self.parameters.vm_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class VolumeListByVMRequestParam(object):

    def __init__(self, region_id, vm_id, page=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param vm_id: 云主机ID
        :param page: 页码
        :param page_size: 每页数量
        """
        self.region_id = region_id
        self.vm_id = vm_id
        self.page = page
        self.page_size = page_size

    def set_page(self, page):
        """
        :param page: 页码
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页数量
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vm_id is None:
            raise Exception("vm_id can not None")

