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


class ShowLoadBalancerRequest(CTYunRequest):
    """
    查询负载均衡实例
    """

    def __init__(self, request_param):
        super(ShowLoadBalancerRequest, self).__init__("/v4/elb/show-loadbalancer", "GET", "ctelb", "")
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
        if self.parameters.id is not None:
            query_param["ID"] = self.parameters.id
        if self.parameters.elb_id is not None:
            query_param["elbID"] = self.parameters.elb_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowLoadBalancerRequestParam(object):

    def __init__(self, region_id, id=None, elb_id=None):
        """
        :param region_id: 资源id
        :param id: 负载均衡ID，公有云标注后续将废弃
        :param elb_id: 优先推荐使用该参数，ID和elbID必填其一
        """
        self.region_id = region_id
        self.id = id
        self.elb_id = elb_id

    def set_id(self, id):
        """
        :param id: 负载均衡ID，公有云标注后续将废弃
        """
        self.id = id

    def set_elb_id(self, elb_id):
        """
        :param elb_id: 优先推荐使用该参数，ID和elbID必填其一
        """
        self.elb_id = elb_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

