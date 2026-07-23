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


class V4PaasElbCreateLoadbalancerRequest(CTYunRequest):
    """
    本接口用于创建负载均衡实例：   
    本接口为同步接口，调用成功后会同步返回底层创建的实例ID。   
    
    """

    def __init__(self, request_param):
        super(V4PaasElbCreateLoadbalancerRequest, self).__init__("/v4/paas/elb/create-loadbalancer", "POST", "ct", "application/json")
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
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.private_ip_address is not None:
            body_param["privateIpAddress"] = self.parameters.private_ip_address
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
        if self.parameters.resource_type is not None:
            body_param["resourceType"] = self.parameters.resource_type
        if self.parameters.delete_protection is not None:
            body_param["deleteProtection"] = self.parameters.delete_protection
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.sla_name is not None:
            body_param["slaName"] = self.parameters.sla_name
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

    def __init__(self, paas_resource_id=None, paas_accout_id=None, master_order_id=None, tags=None, metas=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        :param tags: 标签，自定义map结构
        :param metas: 元数据，自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_accout_id = paas_accout_id
        self.master_order_id = master_order_id
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
        if self.tags is not None:
            obj_dict["tags"] = self.tags
        if self.metas is not None:
            obj_dict["metas"] = self.metas
        return obj_dict


class V4PaasElbCreateLoadbalancerRequestParam(object):

    def __init__(self, region_id, subnet_id, name, project_id, description=None, private_ip_address=None, vpc_id=None, eip_id=None, resource_type=None, delete_protection=None, client_token=None, sla_name=None, channel_info=None):
        """
        :param region_id: 资源id
        :param subnet_id: 子网ID
        :param name: 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        :param vpc_id: vpc id
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        :param resource_type: 源类型。internal：内网负载均衡，默认；ext6ernal：公网负载均衡（公有云新增，实际不传不影响）
        :param delete_protection: 删除保护。false（不开启）、true（开）。 默认：不开启
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        :param project_id: 企业项目ID，默认"0"
        :param sla_name: lb的规格名称:4.0资源池支持：elb.s1.small，elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large  3.0资源池：支持：CLASSICAL，STANDARD_1，EHANCED_1，ADVANCED_1，HIGH_1，EXTREME_1
        :param channel_info: 渠道侧信息--暂时标记非必填，等公共信息确定方案后完善
        """
        self.region_id = region_id
        self.subnet_id = subnet_id
        self.name = name
        self.description = description
        self.private_ip_address = private_ip_address
        self.vpc_id = vpc_id
        self.eip_id = eip_id
        self.resource_type = resource_type
        self.delete_protection = delete_protection
        self.client_token = client_token
        self.project_id = project_id
        self.sla_name = sla_name
        self.channel_info = channel_info

    def set_description(self, description):
        """
        :param description: 描述，支持拉丁字母、中文、数字, 特殊字符：！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、，，不能以 http: / https: 开头，长度 0 - 128
        """
        self.description = description

    def set_private_ip_address(self, private_ip_address):
        """
        :param private_ip_address: 负载均衡的私有IP地址，不指定则自动分配
        """
        self.private_ip_address = private_ip_address

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: vpc id
        """
        self.vpc_id = vpc_id

    def set_eip_id(self, eip_id):
        """
        :param eip_id: 弹性公网IP的ID。当resourceType=external为必填
        """
        self.eip_id = eip_id

    def set_resource_type(self, resource_type):
        """
        :param resource_type: 源类型。internal：内网负载均衡，默认；ext6ernal：公网负载均衡（公有云新增，实际不传不影响）
        """
        self.resource_type = resource_type

    def set_delete_protection(self, delete_protection):
        """
        :param delete_protection: 删除保护。false（不开启）、true（开）。 默认：不开启
        """
        self.delete_protection = delete_protection

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_sla_name(self, sla_name):
        """
        :param sla_name: lb的规格名称:4.0资源池支持：elb.s1.small，elb.s2.small，elb.s3.small，elb.s4.small，elb.s5.small，elb.s2.large，elb.s3.large，elb.s4.large，elb.s5.large  3.0资源池：支持：CLASSICAL，STANDARD_1，EHANCED_1，ADVANCED_1，HIGH_1，EXTREME_1
        """
        self.sla_name = sla_name

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息--暂时标记非必填，等公共信息确定方案后完善
        """
        self.channel_info = channel_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.project_id is None:
            raise Exception("project_id can not None")

