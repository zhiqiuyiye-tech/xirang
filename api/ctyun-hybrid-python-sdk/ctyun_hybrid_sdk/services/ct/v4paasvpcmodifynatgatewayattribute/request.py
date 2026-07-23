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


class V4PaasVpcModifyNatGatewayAttributeRequest(CTYunRequest):
    """
    变配接口只支持资源升级操作
    """

    def __init__(self, request_param):
        super(V4PaasVpcModifyNatGatewayAttributeRequest, self).__init__("/v4/paas/vpc/modify-nat-gateway-attribute", "POST", "ct", "application/json")
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
        if self.parameters.nat_gateway_id is not None:
            body_param["natGatewayID"] = self.parameters.nat_gateway_id
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
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

    def __init__(self, paas_resource_id=None, paas_account_id=None, master_order_id=None, tags=None, metas=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_account_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        :param tags: 标签，自定义map结构
        :param metas: 元数据，自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas

    def set_paas_resource_id(self, paas_resource_id):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        """
        self.paas_resource_id = paas_resource_id

    def set_paas_account_id(self, paas_account_id):
        """
        :param paas_account_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        """
        self.paas_account_id = paas_account_id

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        """
        self.master_order_id = master_order_id

    def set_tags(self, tags):
        """
        :param tags: 标签，自定义map结构
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 元数据，自定义map结构
        """
        self.metas = metas

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.tags is not None:
            obj_dict["tags"] = self.tags
        if self.metas is not None:
            obj_dict["metas"] = self.metas
        return obj_dict


class V4PaasVpcModifyNatGatewayAttributeRequestParam(object):

    def __init__(self, region_id, nat_gateway_id, spec, channel_info=None, client_token=None):
        """
        :param channel_info: 渠道侧信息，暂时允许空，后续完善
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param nat_gateway_id: 要修改的NAT网关的ID
        :param spec: 规格 1~4, 1表示小型, 2表示中型, 3表示大型, 4表示超大型,只支持资源升级操作
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.nat_gateway_id = nat_gateway_id
        self.spec = spec

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息，暂时允许空，后续完善
        """
        self.channel_info = channel_info

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.nat_gateway_id is None:
            raise Exception("nat_gateway_id can not None")
        if self.spec is None:
            raise Exception("spec can not None")

