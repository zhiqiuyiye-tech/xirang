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


class CreateVpcPeerConnectionRequest(CTYunRequest):
    """
    - 创建非跨账户对等连接时，无需传acceptEmail字段。   
    - 创建跨账户对等连接时，虚拟私有云需要与发起方和接收方账户对应，接收方邮箱需要为真实用户邮箱。   
    - 适用于1.15.2版本以后
    """

    def __init__(self, request_param):
        super(CreateVpcPeerConnectionRequest, self).__init__("/v4/vpc/create-vpc-peer-connection", "POST", "ctvpc", "application/json")
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
        if self.parameters.request_vpc_id is not None:
            body_param["requestVpcID"] = self.parameters.request_vpc_id
        if self.parameters.request_vpc_name is not None:
            body_param["requestVpcName"] = self.parameters.request_vpc_name
        if self.parameters.request_vpc_cidr is not None:
            body_param["requestVpcCidr"] = self.parameters.request_vpc_cidr
        if self.parameters.accept_vpc_id is not None:
            body_param["acceptVpcID"] = self.parameters.accept_vpc_id
        if self.parameters.accept_vpc_name is not None:
            body_param["acceptVpcName"] = self.parameters.accept_vpc_name
        if self.parameters.accept_vpc_cidr is not None:
            body_param["acceptVpcCidr"] = self.parameters.accept_vpc_cidr
        if self.parameters.accept_email is not None:
            body_param["acceptEmail"] = self.parameters.accept_email
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.remote_project_id is not None:
            body_param["remoteProjectID"] = self.parameters.remote_project_id
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


class CreateVpcPeerConnectionRequestParam(object):

    def __init__(self, request_vpc_id, request_vpc_name, request_vpc_cidr, accept_vpc_id, name, region_id, client_token=None, accept_vpc_name=None, accept_vpc_cidr=None, accept_email=None, project_id=None, remote_project_id=None):
        """
        :param client_token: 唯一token（非必填，并且此字段在私有云不具有实际意义）
        :param request_vpc_id: 发起方网络ID
        :param request_vpc_name: 本端VPC名称
        :param request_vpc_cidr: 本端vpc的网段
        :param accept_vpc_id: 接收方网络ID
        :param accept_vpc_name: 对端vpc的名称，acceptEmail不为空的时候，不能为空
        :param accept_vpc_cidr: 对端vpc的网段 acceptEmai不为空的时候，不能为空
        :param accept_email: 接收方客户邮箱，跨账户时为必填项
        :param name: 名称（符长度2-32个字段，允许中文、英文、数字和特殊字符-_，只能以中英文开头，不可重名）
        :param region_id: 资源池id
        :param project_id: 企业项目id，默认为本端vpc所属企业项目或者用户默认企业项目，vpc共享企业项目场景需指定
        :param remote_project_id: 远端vpc企业项目id，默认为远端vpc所属企业项目，vpc共享企业项目场景需指定
        """
        self.client_token = client_token
        self.request_vpc_id = request_vpc_id
        self.request_vpc_name = request_vpc_name
        self.request_vpc_cidr = request_vpc_cidr
        self.accept_vpc_id = accept_vpc_id
        self.accept_vpc_name = accept_vpc_name
        self.accept_vpc_cidr = accept_vpc_cidr
        self.accept_email = accept_email
        self.name = name
        self.region_id = region_id
        self.project_id = project_id
        self.remote_project_id = remote_project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 唯一token（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def set_accept_vpc_name(self, accept_vpc_name):
        """
        :param accept_vpc_name: 对端vpc的名称，acceptEmail不为空的时候，不能为空
        """
        self.accept_vpc_name = accept_vpc_name

    def set_accept_vpc_cidr(self, accept_vpc_cidr):
        """
        :param accept_vpc_cidr: 对端vpc的网段 acceptEmai不为空的时候，不能为空
        """
        self.accept_vpc_cidr = accept_vpc_cidr

    def set_accept_email(self, accept_email):
        """
        :param accept_email: 接收方客户邮箱，跨账户时为必填项
        """
        self.accept_email = accept_email

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目id，默认为本端vpc所属企业项目或者用户默认企业项目，vpc共享企业项目场景需指定
        """
        self.project_id = project_id

    def set_remote_project_id(self, remote_project_id):
        """
        :param remote_project_id: 远端vpc企业项目id，默认为远端vpc所属企业项目，vpc共享企业项目场景需指定
        """
        self.remote_project_id = remote_project_id

    def check_param(self):
        """
        the param required check
        """
        if self.request_vpc_id is None:
            raise Exception("request_vpc_id can not None")
        if self.request_vpc_name is None:
            raise Exception("request_vpc_name can not None")
        if self.request_vpc_cidr is None:
            raise Exception("request_vpc_cidr can not None")
        if self.accept_vpc_id is None:
            raise Exception("accept_vpc_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

