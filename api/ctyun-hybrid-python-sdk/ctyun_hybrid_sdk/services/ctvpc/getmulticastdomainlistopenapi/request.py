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


class GetMulticastDomainListOpenapiRequest(CTYunRequest):
    """
    查询组播域列表
    """

    def __init__(self, request_param):
        super(GetMulticastDomainListOpenapiRequest, self).__init__("/v4/multicast/list-domain", "GET", "ctvpc", "")
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
        if self.parameters.client_token is not None:
            query_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.ids is not None:
            query_param["ids"] = self.parameters.ids
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


class GetMulticastDomainListOpenapiRequestParam(object):

    def __init__(self, region_id, client_token=None, vpc_id=None, ids=None, page_no=None, page_size=None):
        """
        :param client_token: 仅用于保证操作幂等，无实际含义
        :param region_id: 资源池id
        :param vpc_id: 所属vpc id
        :param ids: 组播域ids，多个ID之间用半角逗号（,）隔开
        :param page_no: 列表的页码，默认值为 1
        :param page_size: 分页查询时每页的行数，最大值为 100，默认值为 10
        """
        self.client_token = client_token
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.ids = ids
        self.page_no = page_no
        self.page_size = page_size

    def set_client_token(self, client_token):
        """
        :param client_token: 仅用于保证操作幂等，无实际含义
        """
        self.client_token = client_token

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: 所属vpc id
        """
        self.vpc_id = vpc_id

    def set_ids(self, ids):
        """
        :param ids: 组播域ids，多个ID之间用半角逗号（,）隔开
        """
        self.ids = ids

    def set_page_no(self, page_no):
        """
        :param page_no: 列表的页码，默认值为 1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时每页的行数，最大值为 100，默认值为 10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

