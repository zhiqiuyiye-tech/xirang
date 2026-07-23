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


class ListTargetGroupRequest(CTYunRequest):
    """
    查看后端服务组列表
    """

    def __init__(self, request_param):
        super(ListTargetGroupRequest, self).__init__("/v4/elb/list-target-group", "GET", "ctelb", "")
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
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        if self.parameters.vpc_id is not None:
            query_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.health_check_id is not None:
            query_param["healthCheckID"] = self.parameters.health_check_id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.lb_uuid is not None:
            query_param["lbUuid"] = self.parameters.lb_uuid
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListTargetGroupRequestParam(object):

    def __init__(self, region_id, client_token=None, ids=None, vpc_id=None, health_check_id=None, name=None, lb_uuid=None, project_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性, 长度 1 - 64（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 区域ID
        :param ids: 后端服务组ID列表，以","分隔
        :param vpc_id: vpc ID
        :param health_check_id: 健康检查ID
        :param name: 后端服务组名称
        :param lb_uuid: 负载均衡id
        :param project_id: 企业项目ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.ids = ids
        self.vpc_id = vpc_id
        self.health_check_id = health_check_id
        self.name = name
        self.lb_uuid = lb_uuid
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性, 长度 1 - 64（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_ids(self, ids):
        """
        :param ids: 后端服务组ID列表，以","分隔
        """
        self.ids = ids

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc ID
        """
        self.vpc_id = vpc_id

    def set_health_check_id(self, health_check_id):
        """
        :param health_check_id: 健康检查ID
        """
        self.health_check_id = health_check_id

    def set_name(self, name):
        """
        :param name: 后端服务组名称
        """
        self.name = name

    def set_lb_uuid(self, lb_uuid):
        """
        :param lb_uuid: 负载均衡id
        """
        self.lb_uuid = lb_uuid

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

