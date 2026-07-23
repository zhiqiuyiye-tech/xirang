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


class EcsAttachDelegateRequest(CTYunRequest):
    """
    接口功能介绍：该接口提供用户云主机绑定委托能力，委托信息将以用户元数据数据形式存入   
    接口约束：   
    	确保当前请求资源池下，该云主机存在（即instanceID真实存在且与regionID相对应）   
    	确保委托名称（delegateName）对应委托存在   
    	云主机只有在运行（running）或关机（stopped）状态才可执行该操作   
    	目前该功能仅支持多可用区类型资源池
    """

    def __init__(self, request_param):
        super(EcsAttachDelegateRequest, self).__init__("/v4/ecs/delegate/attach", "POST", "ctecs", "application/json")
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
        if self.parameters.delegate_name is not None:
            body_param["delegateName"] = self.parameters.delegate_name
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


class EcsAttachDelegateRequestParam(object):

    def __init__(self, region_id, instance_id, delegate_name, ):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param delegate_name: 委托名称
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.delegate_name = delegate_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.delegate_name is None:
            raise Exception("delegate_name can not None")

