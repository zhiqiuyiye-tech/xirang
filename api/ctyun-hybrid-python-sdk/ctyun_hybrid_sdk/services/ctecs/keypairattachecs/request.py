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


class KeypairAttachEcsRequest(CTYunRequest):
    """
       
    此接口提供用户绑定SSH密钥对到云主机功能。系统会接收用户输入的云主机id和SSH密钥对，将对应SSH密钥对绑定到对应云主机上。   
    1.云主机必须存在，2.需要云主机处于运行中（running）状态，3.需要云主机的操作系统必须为linux，4.密钥对名称必须存在 ,5云主机和密钥对同属于同一个用户, 6云主机和密钥对同属于同一个可用区,7云主机不能已经绑定了此密钥对   
       
    ### 接口约束   
       
    1. 需要云主机处于工作状态   
    2. 需要云主机的操作系统必须为linux
    """

    def __init__(self, request_param):
        super(KeypairAttachEcsRequest, self).__init__("/v4/ecs/keypair/attach", "POST", "ctecs", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
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


class KeypairAttachEcsRequestParam(object):

    def __init__(self, region_id, key_pair_name, id, ):
        """
        :param region_id: 区域ID
        :param key_pair_name: 密钥对名称
        :param id: 云主机ID
        """
        self.region_id = region_id
        self.key_pair_name = key_pair_name
        self.id = id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key_pair_name is None:
            raise Exception("key_pair_name can not None")
        if self.id is None:
            raise Exception("id can not None")

