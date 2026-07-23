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


class ListListenerRequest(CTYunRequest):
    """
    查看监听器列表   
    
    """

    def __init__(self, request_param):
        super(ListListenerRequest, self).__init__("/v4/elb/list-listener", "GET", "ctelb", "")
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
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.ids is not None:
            query_param["IDs"] = self.parameters.ids
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.load_balancer_id is not None:
            query_param["loadBalancerID"] = self.parameters.load_balancer_id
        if self.parameters.access_control_id is not None:
            query_param["accessControlID"] = self.parameters.access_control_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListListenerRequestParam(object):

    def __init__(self, region_id, client_token=None, az_name=None, project_id=None, ids=None, name=None, load_balancer_id=None, access_control_id=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param region_id: 区域ID
        :param az_name: 可用区名称（底层如未返回，api测返回null）
        :param project_id: 企业项目ID，默认为"0"
        :param ids: 监听器ID列表，以","分隔
        :param name: 监听器名称
        :param load_balancer_id: 负载均衡实例ID
        :param access_control_id: 访问控制ID
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.ids = ids
        self.name = name
        self.load_balancer_id = load_balancer_id
        self.access_control_id = access_control_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称（底层如未返回，api测返回null）
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为"0"
        """
        self.project_id = project_id

    def set_ids(self, ids):
        """
        :param ids: 监听器ID列表，以","分隔
        """
        self.ids = ids

    def set_name(self, name):
        """
        :param name: 监听器名称
        """
        self.name = name

    def set_load_balancer_id(self, load_balancer_id):
        """
        :param load_balancer_id: 负载均衡实例ID
        """
        self.load_balancer_id = load_balancer_id

    def set_access_control_id(self, access_control_id):
        """
        :param access_control_id: 访问控制ID
        """
        self.access_control_id = access_control_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

