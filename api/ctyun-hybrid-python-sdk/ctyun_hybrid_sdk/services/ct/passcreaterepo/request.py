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


class PassCreateRepoRequest(CTYunRequest):
    """
    创建云硬盘备份存储库   
    1.目前不支持autoRenewStatus（是否自动续订）字段   
    2.底层size属性不支持默认，需要必传
    """

    def __init__(self, request_param):
        super(PassCreateRepoRequest, self).__init__("/v4/paas/ebs-backup/repo/create", "POST", "ct", "application/json")
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
        if self.parameters.repository_name is not None:
            body_param["repositoryName"] = self.parameters.repository_name
        if self.parameters.size is not None:
            body_param["size"] = self.parameters.size
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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

    def __init__(self, paas_resource_id=None, paas_account_id=None, master_order_id=None):
        """
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id

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

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        return obj_dict


class PassCreateRepoRequestParam(object):

    def __init__(self, region_id, repository_name, size, client_token=None, project_id=None, channel_info=None):
        """
        :param client_token: 客户端存根
        :param region_id: 资源池id
        :param repository_name: 长度限制2-63，支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param size: 云硬盘备份存储库容量，10-1024000，默认100
        :param project_id: 企业项目ID，默认“0”
        :param channel_info: paas接口指定参数
        """
        self.client_token = client_token
        self.region_id = region_id
        self.repository_name = repository_name
        self.size = size
        self.project_id = project_id
        self.channel_info = channel_info

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根
        """
        self.client_token = client_token

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，默认“0”
        """
        self.project_id = project_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: paas接口指定参数
        """
        self.channel_info = channel_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.repository_name is None:
            raise Exception("repository_name can not None")
        if self.size is None:
            raise Exception("size can not None")

