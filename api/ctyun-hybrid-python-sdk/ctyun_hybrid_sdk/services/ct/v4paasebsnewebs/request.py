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


class V4PaasEbsNewEbsRequest(CTYunRequest):
    """
    创建云硬盘(工单)
    """

    def __init__(self, request_param):
        super(V4PaasEbsNewEbsRequest, self).__init__("/v4/paas/ebs/new-ebs", "POST", "ct", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.disk_type is not None:
            body_param["diskType"] = self.parameters.disk_type
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
        if self.parameters.is_encrypt is not None:
            body_param["isEncrypt"] = self.parameters.is_encrypt
        if self.parameters.cmk_id is not None:
            body_param["cmkID"] = self.parameters.cmk_id
        if self.parameters.disk_mode is not None:
            body_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.disk_name is not None:
            body_param["diskName"] = self.parameters.disk_name
        if self.parameters.multi_attach is not None:
            body_param["multiAttach"] = self.parameters.multi_attach
        if self.parameters.image_id is not None:
            body_param["imageID"] = self.parameters.image_id
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

    def __init__(self, paas_resource_id, paas_accout_id, master_order_id, tags=None, metas=None):
        """
        :param paas_resource_id: paas资源ID。变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_accout_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: paas账号，资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param tags: 标签，自定义map结构
        :param metas: 元数据，自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_accout_id = paas_accout_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas
        self.check_param()

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
            if type(self.tags) is dict:
                obj_dict["tags"] = self.tags
            else:
                obj_dict["tags"] = self.tags.get_dic()
        if self.metas is not None:
            if type(self.metas) is dict:
                obj_dict["metas"] = self.metas
            else:
                obj_dict["metas"] = self.metas.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")
        if self.paas_accout_id is None:
            raise Exception("paas_accout_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")


class Tags(object):

    def __init__(self, ebs_attr, ):
        """
        :param ebs_attr: 
        """
        self.ebs_attr = ebs_attr
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.ebs_attr is not None:
            obj_dict["ebs_attr"] = self.ebs_attr
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.ebs_attr is None:
            raise Exception("ebs_attr can not None")


class Metas(object):

    def __init__(self, ebs_attr, ):
        """
        :param ebs_attr: 
        """
        self.ebs_attr = ebs_attr
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.ebs_attr is not None:
            obj_dict["ebs_attr"] = self.ebs_attr
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.ebs_attr is None:
            raise Exception("ebs_attr can not None")


class V4PaasEbsNewEbsRequestParam(object):

    def __init__(self, client_token, region_id, disk_type, disk_size, is_encrypt, disk_mode, disk_name, channel_info=None, az_name=None, project_id=None, cmk_id=None, multi_attach=None, image_id=None):
        """
        :param channel_info: 渠道侧信息
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param az_name: 如果是4.0资源池，必须提供可用区名称
        :param project_id: 企业项目ID，默认"0"
        :param disk_type: 磁盘分类 ，取值范围:[SAS=SAS盘,SATA=SATA盘,SSD-genric=SSD-genric盘,SSD=SSD盘]
        :param disk_size: 磁盘容量 单位是GB 10-32768
        :param is_encrypt: 磁盘加密标志 ，取值范围:[true=加密,false=不加密]
        :param cmk_id: 对称密钥uuid
        :param disk_mode: 磁盘属性，取值范围:[FCSAN=FCSAN,ISCSI=ISCSI,VBD=VBD]
        :param disk_name: 磁盘名称 ，长度2~64,不支持中文
        :param multi_attach: 默认false
        :param image_id: 支持用系统盘镜像创建系统盘，或者数据盘镜像创建数据盘，所创建的数据盘的所在地域要与镜像源一致，容量不可小于镜像对应的磁盘容量，不支持批量创建操作，从镜像创建的数据盘不支持加密、iSCSI和FCSAN高级配置
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.is_encrypt = is_encrypt
        self.cmk_id = cmk_id
        self.disk_mode = disk_mode
        self.disk_name = disk_name
        self.multi_attach = multi_attach
        self.image_id = image_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 渠道侧信息
        """
        self.channel_info = channel_info

    def set_az_name(self, az_name):
        """
        :param az_name: 如果是4.0资源池，必须提供可用区名称
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认"0"
        """
        self.project_id = project_id

    def set_cmk_id(self, cmk_id):
        """
        :param cmk_id: 对称密钥uuid
        """
        self.cmk_id = cmk_id

    def set_multi_attach(self, multi_attach):
        """
        :param multi_attach: 默认false
        """
        self.multi_attach = multi_attach

    def set_image_id(self, image_id):
        """
        :param image_id: 支持用系统盘镜像创建系统盘，或者数据盘镜像创建数据盘，所创建的数据盘的所在地域要与镜像源一致，容量不可小于镜像对应的磁盘容量，不支持批量创建操作，从镜像创建的数据盘不支持加密、iSCSI和FCSAN高级配置
        """
        self.image_id = image_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.disk_type is None:
            raise Exception("disk_type can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")
        if self.is_encrypt is None:
            raise Exception("is_encrypt can not None")
        if self.disk_mode is None:
            raise Exception("disk_mode can not None")
        if self.disk_name is None:
            raise Exception("disk_name can not None")

