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


class PaasEbmCreateInstanceRequest(CTYunRequest):
    """
    批量删除物理机（工单）
    """

    def __init__(self, request_param):
        super(PaasEbmCreateInstanceRequest, self).__init__("/v4/paas/ebm/delete", "POST", "ct", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.instance_uuid_list is not None:
            body_param["instanceUUIDList"] = self.parameters.instance_uuid_list
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

    def __init__(self, paas_resource_id, paas_account_id, master_order_id, ):
        """
        :param paas_resource_id: 
        :param paas_account_id: 
        :param master_order_id: 
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")
        if self.paas_account_id is None:
            raise Exception("paas_account_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")


class PaasEbmCreateInstanceRequestParam(object):

    def __init__(self, channel_info, client_token, region_id, instance_uuid_list, az_name=None):
        """
        :param channel_info: 混合云历史版本可以不填
        :param client_token: 客户端存根
        :param region_id: 资源池ID
        :param az_name: 可用区名称
        :param instance_uuid_list: 物理机实例ID列表 注意:此参数为数组
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.instance_uuid_list = instance_uuid_list

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.channel_info is None:
            raise Exception("channel_info can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid_list is None:
            raise Exception("instance_uuid_list can not None")

