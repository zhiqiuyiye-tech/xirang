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


class V4PaasEipDeleteRequest(CTYunRequest):
    """
    本接口用于删除弹性IP：   
    本接口为同步接口，调用成功说明底层执行成功。   
    
    """

    def __init__(self, request_param):
        super(V4PaasEipDeleteRequest, self).__init__("/v4/paas/eip/delete", "POST", "ct", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.eip_id is not None:
            body_param["eipID"] = self.parameters.eip_id
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


class V4PaasEipDeleteRequestParam(object):

    def __init__(self, region_id, eip_id, project_id=None, channel_info=None):
        """
        :param region_id: 资源池 ID
        :param project_id: 企业项目 ID
        :param eip_id: 弹性IP实例ID
        :param channel_info: 渠道侧信息，暂时空。不支持
        """
        self.region_id = region_id
        self.project_id = project_id
        self.eip_id = eip_id
        self.channel_info = channel_info

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID
        """
        self.project_id = project_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息，暂时空。不支持
        """
        self.channel_info = channel_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.eip_id is None:
            raise Exception("eip_id can not None")

