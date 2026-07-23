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


class ListVmRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容4.0资源池
    """

    def __init__(self, request_param):
        super(ListVmRequest, self).__init__("/v4/elb/list-vm", "GET", "ctelb", "")
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
        if self.parameters.target_group_id is not None:
            query_param["targetGroupID"] = self.parameters.target_group_id
        if self.parameters.load_balance_id is not None:
            query_param["loadBalanceID"] = self.parameters.load_balance_id
        if self.parameters.query_content is not None:
            query_param["queryContent"] = self.parameters.query_content
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListVmRequestParam(object):

    def __init__(self, region_id, target_group_id, load_balance_id, query_content=None):
        """
        :param region_id: 资源池id
        :param target_group_id: 主机组id
        :param load_balance_id: 负载均衡id
        :param query_content: 模糊搜索，目前支持模糊搜索id
        """
        self.region_id = region_id
        self.target_group_id = target_group_id
        self.load_balance_id = load_balance_id
        self.query_content = query_content

    def set_query_content(self, query_content):
        """
        :param query_content: 模糊搜索，目前支持模糊搜索id
        """
        self.query_content = query_content

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.target_group_id is None:
            raise Exception("target_group_id can not None")
        if self.load_balance_id is None:
            raise Exception("load_balance_id can not None")

