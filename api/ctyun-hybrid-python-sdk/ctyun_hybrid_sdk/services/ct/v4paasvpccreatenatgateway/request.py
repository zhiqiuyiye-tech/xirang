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


class V4PaasVpcCreateNatGatewayRequest(CTYunRequest):
    """
    用于创建NAT网关：   
    本接口为同步接口，创建成功后同步返回natGatewayID。
    """

    def __init__(self, request_param):
        super(V4PaasVpcCreateNatGatewayRequest, self).__init__("/v4/paas/vpc/create-nat-gateway", "POST", "ct", "application/json")
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
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.spec is not None:
            body_param["spec"] = self.parameters.spec
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.channel_info is not None:
            if type(self.parameters.channel_info) is dict:
                channel_info_dict_value = self.parameters.channel_info
            else:
                channel_info_dict_value = self.parameters.channel_info.get_dic()
            body_param["channelInfo"] = channel_info_dict_value
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

    def __init__(self, paas_resource_id=None, paas_accout_id=None, master_order_id=None, hide=None, tags=None, metas=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        :param hide: hide=true，后端数据库设置资源标记out_display=2（不可见）；hide=false或者不传，out_display=1（可见）
        :param tags: 标签，自定义map结构
        :param metas: 元数据，自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_accout_id = paas_accout_id
        self.master_order_id = master_order_id
        self.hide = hide
        self.tags = tags
        self.metas = metas

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

    def set_hide(self, hide):
        """
        :param hide: hide=true，后端数据库设置资源标记out_display=2（不可见）；hide=false或者不传，out_display=1（可见）
        """
        self.hide = hide

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
        if self.paas_accout_id is not None:
            obj_dict["paasAccoutID"] = self.paas_accout_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.hide is not None:
            obj_dict["hide"] = self.hide
        if self.tags is not None:
            obj_dict["tags"] = self.tags
        if self.metas is not None:
            obj_dict["metas"] = self.metas
        return obj_dict


class V4PaasVpcCreateNatGatewayRequestParam(object):

    def __init__(self, client_token, region_id, vpc_id, name, spec, az_name=None, project_id=None, description=None, channel_info=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池id
        :param az_name: 可用区名称，如果是4.0资源池，必须提供可用区名称
        :param project_id: 企业项目ID
        :param vpc_id: 需要创建NAT网关的VPC的ID
        :param name: NAT网关名称,英文字母、中文、特殊符号_(下划线) -(中划线) /(斜杠) 进行命名 不支持使用特殊符号、数字作为命名开头，不支持特殊符号作为命名结尾 命名长度为2-32位
        :param spec: 规格 1~4, 1表示小型, 2表示中型, 3表示大型, 4表示超大型
        :param description: 描述信息,0-128位
        :param channel_info: 渠道侧信息，暂时空。后续完善
        """
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.vpc_id = vpc_id
        self.name = name
        self.spec = spec
        self.description = description
        self.channel_info = channel_info

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称，如果是4.0资源池，必须提供可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 描述信息,0-128位
        """
        self.description = description

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息，暂时空。后续完善
        """
        self.channel_info = channel_info

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.spec is None:
            raise Exception("spec can not None")

