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


class EcsKeypairCreateNewRequest(CTYunRequest):
    """
    此接口用来创建一对SSH密钥对。系统会为您保管密钥的公钥部分，并返回未加密私钥。您需要自行妥善保管私钥部分。
    """

    def __init__(self, request_param):
        super(EcsKeypairCreateNewRequest, self).__init__("/v4/ecs/keypair/create-keypair", "POST", "ctecs", "application/json")
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
        if self.parameters.key_pair_name is not None:
            body_param["keyPairName"] = self.parameters.key_pair_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class EcsKeypairCreateNewRequestParam(object):

    def __init__(self, region_id, key_pair_name, project_id=None):
        """
        :param region_id: 资源池ID
        :param key_pair_name: 密钥对名称,密钥对名称2-63字符，支持使用字母，数字，中划线(-)，只能以字母开头，只能以字母或者数字结尾，不能重名
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.key_pair_name = key_pair_name
        self.project_id = project_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key_pair_name is None:
            raise Exception("key_pair_name can not None")

