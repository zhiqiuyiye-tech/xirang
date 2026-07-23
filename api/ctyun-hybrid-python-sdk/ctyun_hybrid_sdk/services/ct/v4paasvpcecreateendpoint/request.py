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


class V4PaasVpceCreateEndpointRequest(CTYunRequest):
    """
    创建VPC终端节点PAAS
    """

    def __init__(self, request_param):
        super(V4PaasVpceCreateEndpointRequest, self).__init__("/v4/paas/vpce/create-endpoint", "POST", "ct", "application/json")
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
        if self.parameters.endpoint_name is not None:
            body_param["endpointName"] = self.parameters.endpoint_name
        if self.parameters.endpoint_service_id is not None:
            body_param["endpointServiceID"] = self.parameters.endpoint_service_id
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.whitelist is not None:
            body_param["whitelist"] = self.parameters.whitelist
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.ip is not None:
            body_param["IP"] = self.parameters.ip
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.open_dns is not None:
            body_param["openDns"] = self.parameters.open_dns
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
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        :param tags: 自定义map结构
        :param metas: 自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas

    def set_paas_resource_id(self, paas_resource_id):
        """
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        """
        self.paas_resource_id = paas_resource_id

    def set_paas_account_id(self, paas_account_id):
        """
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        """
        self.paas_account_id = paas_account_id

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        """
        self.master_order_id = master_order_id

    def set_tags(self, tags):
        """
        :param tags: 自定义map结构
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 自定义map结构
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


class V4PaasVpceCreateEndpointRequestParam(object):

    def __init__(self, client_token, region_id, endpoint_name, endpoint_service_id, vpc_id, subnet_id, channel_info=None, whitelist=None, type=None, ip=None, description=None, az_name=None, project_id=None, open_dns=None):
        """
        :param channel_info: 当前并未处理。应是必填
        :param client_token: 避免重复请求，10秒内不能重复使用
        :param region_id: 资源池ID
        :param endpoint_name: 终端节点名称，只能由数字，字母，_-组成不能以数字和_-开头，长度2-28
        :param endpoint_service_id: 终端节点关联的终端节点服务
        :param vpc_id: VPCID
        :param whitelist: 白名单 注意:此参数为数组
        :param subnet_id: 子网id
        :param type: 接口还是反向，interface:接口，reverse:反向（PaaS独有）
        :param ip: vpc address
        :param description: 描述信息
        :param az_name: 1.0遗留参数，目前无实际用途
        :param project_id: 1.0遗留参数，目前无实际用途
        :param open_dns: 是否开启私网域名 false：关闭；true：开启 默认false
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.endpoint_name = endpoint_name
        self.endpoint_service_id = endpoint_service_id
        self.vpc_id = vpc_id
        self.whitelist = whitelist
        self.subnet_id = subnet_id
        self.type = type
        self.ip = ip
        self.description = description
        self.az_name = az_name
        self.project_id = project_id
        self.open_dns = open_dns

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 当前并未处理。应是必填
        """
        self.channel_info = channel_info

    def set_whitelist(self, whitelist):
        """
        :param whitelist: 白名单
        """
        self.whitelist = whitelist

    def set_type(self, type):
        """
        :param type: 接口还是反向，interface:接口，reverse:反向（PaaS独有）
        """
        self.type = type

    def set_ip(self, ip):
        """
        :param ip: vpc address
        """
        self.ip = ip

    def set_description(self, description):
        """
        :param description: 描述信息
        """
        self.description = description

    def set_az_name(self, az_name):
        """
        :param az_name: 1.0遗留参数，目前无实际用途
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 1.0遗留参数，目前无实际用途
        """
        self.project_id = project_id

    def set_open_dns(self, open_dns):
        """
        :param open_dns: 是否开启私网域名 false：关闭；true：开启 默认false
        """
        self.open_dns = open_dns

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.endpoint_name is None:
            raise Exception("endpoint_name can not None")
        if self.endpoint_service_id is None:
            raise Exception("endpoint_service_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

