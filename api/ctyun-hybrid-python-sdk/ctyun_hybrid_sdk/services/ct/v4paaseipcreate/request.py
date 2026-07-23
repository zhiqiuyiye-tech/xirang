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


class V4PaasEipCreateRequest(CTYunRequest):
    """
    用于创建弹性IP：   
    本接口为同步接口，调用成功后会同步返回底层创建的eipID。   
    
    """

    def __init__(self, request_param):
        super(V4PaasEipCreateRequest, self).__init__("/v4/paas/eip/create", "POST", "ct", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
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

    def __init__(self, paas_resource_id=None, paas_accout_id=None, master_order_id=None, tags=None, metas=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: 中台主订单ID，IaaS记入话单，用来关联订单和资源
        :param tags: 标签，自定义map结构--不支持
        :param metas: 元数据，自定义map结构--不支持
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
        :param tags: 标签，自定义map结构--不支持
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 元数据，自定义map结构--不支持
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


class V4PaasEipCreateRequestParam(object):

    def __init__(self, region_id, name, bandwidth, client_token=None, project_id=None, description=None, channel_info=None):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）(差异点说明：2.0暂无此参数)
        :param region_id: 资源池 ID
        :param project_id: 企业项目ID，默认为用户所在的默认企业项目
        :param name: 弹性 IP 名称，长度为2～32字符 支持使用中文、字母、数字、-、_，只能以中文或字母开头。名称不能重复
        :param bandwidth: 弹性 IP 带宽，峰值带宽上限默认最大上限值是3000，若云管配置中心设置的带宽上限值大于3000，则以云管设置的参数上限为准
        :param description: eip描述，0~128字符
        :param channel_info: 渠道侧信息，后续完善。暂时空
        """
        self.client_token = client_token
        self.region_id = region_id
        self.project_id = project_id
        self.name = name
        self.bandwidth = bandwidth
        self.description = description
        self.channel_info = channel_info

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一（实际没用到）(差异点说明：2.0暂无此参数)
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认为用户所在的默认企业项目
        """
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: eip描述，0~128字符
        """
        self.description = description

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息，后续完善。暂时空
        """
        self.channel_info = channel_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.bandwidth is None:
            raise Exception("bandwidth can not None")

