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


class AssociateSecondaryCidrsToVpcRequest(CTYunRequest):
    """
    VPC 绑定扩展网段
    """

    def __init__(self, request_param):
        super(AssociateSecondaryCidrsToVpcRequest, self).__init__("/v4/vpc/associate-secondary-cidrs", "POST", "ctvpc", "application/json")
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
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.cidrs is not None:
            body_param["cidrs"] = self.parameters.cidrs
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


class AssociateSecondaryCidrsToVpcRequestParam(object):

    def __init__(self, region_id, vpc_id, cidrs, az_name=None, project_id=None, client_token=None):
        """
        :param region_id: 资源池ID
        :param az_name: 可用区名称(该参数未使用，输入无意义)
        :param project_id: 企业项目ID（非必填，并且此字段在私有云不具有实际意义）
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        :param vpc_id: vpc id
        :param cidrs: 是Array类型，里面的内容是String，要绑定的扩展网段ip 注意:此参数为数组
        """
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.client_token = client_token
        self.vpc_id = vpc_id
        self.cidrs = cidrs

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(该参数未使用，输入无意义)
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID（非必填，并且此字段在私有云不具有实际意义）
        """
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.cidrs is None:
            raise Exception("cidrs can not None")

