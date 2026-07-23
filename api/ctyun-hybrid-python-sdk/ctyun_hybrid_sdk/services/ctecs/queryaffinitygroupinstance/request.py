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


class QueryAffinityGroupInstanceRequest(CTYunRequest):
    """
    可以根据用户给定的云主机组，查询云主机组内云主机的详细信息，参考公有云：   
    https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=8320&data=87&isNormal=1&vid=81
    """

    def __init__(self, request_param):
        super(QueryAffinityGroupInstanceRequest, self).__init__("/v4/ecs/affinity-group/list-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.affinity_group_id is not None:
            body_param["affinityGroupID"] = self.parameters.affinity_group_id
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


class QueryAffinityGroupInstanceRequestParam(object):

    def __init__(self, region_id, affinity_group_id, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param affinity_group_id: 云主机组ID
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        :param page_size: 每页记录数目，取值范围：[1, 50]，注：默认值为10
        """
        self.region_id = region_id
        self.affinity_group_id = affinity_group_id
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 页码，取值范围：正整数（≥1），注：默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 每页记录数目，取值范围：[1, 50]，注：默认值为10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.affinity_group_id is None:
            raise Exception("affinity_group_id can not None")

