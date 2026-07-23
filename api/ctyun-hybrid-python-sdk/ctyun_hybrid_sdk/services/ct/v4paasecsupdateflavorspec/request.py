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


class V4PaasEcsUpdateFlavorSpecRequest(CTYunRequest):
    """
    云主机修改规格(工单)
    """

    def __init__(self, request_param):
        super(V4PaasEcsUpdateFlavorSpecRequest, self).__init__("/v4/paas/ecs/update-flavor-spec", "POST", "ct", "application/json")
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
        if self.parameters.channel_info is not None:
            if type(self.parameters.channel_info) is dict:
                channel_info_dict_value = self.parameters.channel_info
            else:
                channel_info_dict_value = self.parameters.channel_info.get_dic()
            body_param["channelInfo"] = channel_info_dict_value
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.flavor_id is not None:
            body_param["flavorID"] = self.parameters.flavor_id
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


class ChannelInfo(object):

    def __init__(self, paas_accout_id, ):
        """
        :param paas_accout_id: 
        """
        self.paas_accout_id = paas_accout_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.paas_accout_id is not None:
            obj_dict["paasAccoutID"] = self.paas_accout_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_accout_id is None:
            raise Exception("paas_accout_id can not None")


class V4PaasEcsUpdateFlavorSpecRequestParam(object):

    def __init__(self, channel_info, region_id, instance_id, flavor_id, client_token=None):
        """
        :param channel_info: ，资源的付费账号，通过上送IT用于内部结算
        :param client_token: 客户端存根，用于保证订单幂等性。
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param flavor_id: 目标规格ID
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.instance_id = instance_id
        self.flavor_id = flavor_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.channel_info is None:
            raise Exception("channel_info can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.flavor_id is None:
            raise Exception("flavor_id can not None")

