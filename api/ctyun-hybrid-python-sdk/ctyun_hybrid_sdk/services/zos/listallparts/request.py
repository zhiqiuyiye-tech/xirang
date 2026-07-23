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


class ListAllPartsRequest(CTYunRequest):
    """
    v2.1.4.x版本修改对象储存调用链后，该接口功能无法实现，暂不提供
    """

    def __init__(self, request_param):
        super(ListAllPartsRequest, self).__init__("/v4/oss/list-all-parts", "GET", "zos", "")
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
        if self.parameters.bucket is not None:
            query_param["bucket"] = self.parameters.bucket
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
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


class ListAllPartsRequestParam(object):

    def __init__(self, bucket, region_id, page=None, page_size=None, page_no=None):
        """
        :param bucket: 桶名	
        :param region_id: 区域 ID	
        :param page: 页码。默认1
        :param page_size: 每页展示的最大分段数量。取值范围 1~50，默认值为 10	
        :param page_no: 页码，若与参数 page 同时存在，以 pageNo 为准。默认值 1
        """
        self.bucket = bucket
        self.region_id = region_id
        self.page = page
        self.page_size = page_size
        self.page_no = page_no

    def set_page(self, page):
        """
        :param page: 页码。默认1
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页展示的最大分段数量。取值范围 1~50，默认值为 10	
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，若与参数 page 同时存在，以 pageNo 为准。默认值 1
        """
        self.page_no = page_no

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

