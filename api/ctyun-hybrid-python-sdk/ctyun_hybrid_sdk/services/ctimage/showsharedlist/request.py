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


class ShowSharedListRequest(CTYunRequest):
    """
    在您将一份私有镜像共享给其他项目之后，此接口可用于查询该私有镜像的共享列表
    """

    def __init__(self, request_param):
        super(ShowSharedListRequest, self).__init__("/v4/image/show-shared-list", "GET", "ctimage", "")
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
        if self.parameters.image_id is not None:
            query_param["imageID"] = self.parameters.image_id
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowSharedListRequestParam(object):

    def __init__(self, region_id, image_id, page_no=None, page_size=None):
        """
        :param region_id: 区域ID
        :param image_id: 镜像ID
        :param page_no: 页码，取值范围：最小 1（默认值）。
        :param page_size: 每页记录数目，取值范围：最小 1，最大 50，默认值 10。
        """
        self.region_id = region_id
        self.image_id = image_id
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：最小 1（默认值）。
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：最小 1，最大 50，默认值 10。
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.image_id is None:
            raise Exception("image_id can not None")

