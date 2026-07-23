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


class V4PaasEbsRefundEbsRequest(CTYunRequest):
    """
    删除云硬盘(工单)
    """

    def __init__(self, request_param):
        super(V4PaasEbsRefundEbsRequest, self).__init__("/v4/paas/ebs/refund-ebs", "POST", "ct", "application/json")
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
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
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

    def __init__(self, paas_resource_id=None, paas_accout_id=None, master_order_id=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        """
        self.paas_resource_id = paas_resource_id
        self.paas_accout_id = paas_accout_id
        self.master_order_id = master_order_id

    def set_paas_resource_id(self, paas_resource_id):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        """
        self.paas_resource_id = paas_resource_id

    def set_paas_accout_id(self, paas_accout_id):
        """
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        """
        self.paas_accout_id = paas_accout_id

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        """
        self.master_order_id = master_order_id

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_accout_id is not None:
            obj_dict["paasAccoutID"] = self.paas_accout_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        return obj_dict


class V4PaasEbsRefundEbsRequestParam(object):

    def __init__(self, client_token, disk_id, channel_info=None, region_id=None):
        """
        :param channel_info: 渠道侧信息
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID，如本地语境支持保存regionID，那么建议传递
        :param disk_id: 云硬盘ID
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.disk_id = disk_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息
        """
        self.channel_info = channel_info

    def set_region_id(self, region_id):
        """
        :param region_id: 资源池ID，如本地语境支持保存regionID，那么建议传递
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

