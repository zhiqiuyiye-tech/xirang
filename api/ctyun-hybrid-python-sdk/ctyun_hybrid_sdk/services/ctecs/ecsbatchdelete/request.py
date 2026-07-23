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


class EcsBatchDeleteRequest(CTYunRequest):
    """
    批量退订或者销毁云主机，默认直接销毁，要求：   
     1.云主机必须存在   
     2.批量释放资源一次不能超过10个   
     3.释放云主机前请先检查云主机是否绑定虚拟IP，如果有请先解绑虚拟IP   
     4.请检查云主机是否存在快照，如果存在快照不允许释放云主机   
     5.云主机处于关机状态下才可释放   
       
    未对齐：   
    1. 混合云v2订单侧批量退订接口不支持包周期和按需同时退订，所以只能退订时只能单个去循环退订，返回最后一个资源的订单id
    """

    def __init__(self, request_param):
        super(EcsBatchDeleteRequest, self).__init__("/v4/ecs/batch-delete", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class EcsBatchDeleteRequestParam(object):

    def __init__(self, instance_id_list, client_token, region_id, unsubscribe_only=None):
        """
        :param instance_id_list: 公有云为主机id，我们暂为resourceId 注意:此参数为数组
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一，使用同一个ClientToken值，其他请求参数相同时，则代表为同一个请求。保留时间为24小时
        :param region_id: 资源池ID
        :param unsubscribe_only: true - 仅退订到回收站，可恢复   
         false - 直接销毁，不可恢复
        """
        self.instance_id_list = instance_id_list
        self.client_token = client_token
        self.region_id = region_id
        self.unsubscribe_only = unsubscribe_only

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
        if self.instance_id_list is None:
            raise Exception("instance_id_list can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

