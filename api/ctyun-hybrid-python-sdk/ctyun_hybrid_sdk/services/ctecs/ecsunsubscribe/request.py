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


class EcsUnsubscribeRequest(CTYunRequest):
    """
    支持退订或者销毁云主机，默认直接销毁，要求：   
     1.云主机必须存在   
     2.释放云主机前请先检查云主机是否绑定虚拟IP，如果有请先解绑虚拟IP   
     3.请检查云主机是否存在快照，如果存在快照不允许释放云主机   
     4.云主机处于关机状态下才可释放
    """

    def __init__(self, request_param):
        super(EcsUnsubscribeRequest, self).__init__("/v4/ecs/unsubscribe", "POST", "ctecs", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.unsubscribe_only is not None:
            body_param["unsubscribeOnly"] = self.parameters.unsubscribe_only
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


class EcsUnsubscribeRequestParam(object):

    def __init__(self, id, client_token, region_id, az_name=None, unsubscribe_only=None):
        """
        :param id: 云主机ID(资源id也兼容)
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param az_name: 可用区名称，没有可用区时填default
        :param region_id: 资源池ID
        :param unsubscribe_only: true - 仅退订到回收站，可恢复   
         false - 直接销毁，不可恢复
        """
        self.id = id
        self.client_token = client_token
        self.az_name = az_name
        self.region_id = region_id
        self.unsubscribe_only = unsubscribe_only

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，没有可用区时填default
        """
        self.az_name = az_name

    def set_unsubscribe_only(self, unsubscribe_only):
        """
        :param unsubscribe_only: true - 仅退订到回收站，可恢复   
         false - 直接销毁，不可恢复
        """
        self.unsubscribe_only = unsubscribe_only

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

