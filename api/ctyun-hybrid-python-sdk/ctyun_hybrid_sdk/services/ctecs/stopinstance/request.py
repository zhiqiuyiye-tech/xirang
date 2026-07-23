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


class StopInstanceRequest(CTYunRequest):
    """
    该接口提供用户关闭一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
    """

    def __init__(self, request_param):
        super(StopInstanceRequest, self).__init__("/v4/ecs/stop-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class StopInstanceRequestParam(object):

    def __init__(self, region_id, instance_id, client_token=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 实例ID
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.client_token = client_token

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证操作幂等性。要求单个云平台账户内唯一。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")

