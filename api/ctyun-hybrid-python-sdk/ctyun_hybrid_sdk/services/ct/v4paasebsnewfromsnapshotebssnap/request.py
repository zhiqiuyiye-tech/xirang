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


class V4PaasEbsNewFromSnapshotEbsSnapRequest(CTYunRequest):
    """
    快照创建云硬盘(工单)
    """

    def __init__(self, request_param):
        super(V4PaasEbsNewFromSnapshotEbsSnapRequest, self).__init__("/v4/paas/ebs/new-from-snapshot-ebs-snap", "POST", "ct", "application/json")
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
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.disk_size is not None:
            body_param["diskSize"] = self.parameters.disk_size
        if self.parameters.disk_mode is not None:
            body_param["diskMode"] = self.parameters.disk_mode
        if self.parameters.disk_name is not None:
            body_param["diskName"] = self.parameters.disk_name
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


class V4PaasEbsNewFromSnapshotEbsSnapRequestParam(object):

    def __init__(self, client_token, region_id, snapshot_id, disk_size, disk_mode, disk_name, channel_info=None, project_id=None):
        """
        :param channel_info: 
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 资源池ID
        :param project_id: 企业项目ID，默认"0"
        :param snapshot_id: 快照ID
        :param disk_size: 磁盘容量
        :param disk_mode: 磁盘属性，取值范围:[FCSAN=FCSAN,ISCSI=ISCSI,VBD=VBD]
        :param disk_name: 磁盘名称 
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.project_id = project_id
        self.snapshot_id = snapshot_id
        self.disk_size = disk_size
        self.disk_mode = disk_mode
        self.disk_name = disk_name

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 
        """
        self.channel_info = channel_info

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认"0"
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")
        if self.disk_size is None:
            raise Exception("disk_size can not None")
        if self.disk_mode is None:
            raise Exception("disk_mode can not None")
        if self.disk_name is None:
            raise Exception("disk_name can not None")

