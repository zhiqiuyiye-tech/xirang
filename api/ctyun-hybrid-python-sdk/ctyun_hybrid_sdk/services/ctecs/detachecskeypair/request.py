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


class DetachEcsKeypairRequest(CTYunRequest):
    """
    为Linux云主机解绑SSH密钥对   
       
    ### 接口约束   
       
    1.云主机必须存在，2 云主机状态必须是运行中，3 云主机操作系统必须为linux，4 密钥对名称必须存在，5 云主机必须已经绑定了此密钥对
    """

    def __init__(self, request_param):
        super(DetachEcsKeypairRequest, self).__init__("/v4/ecs/keypair/detach-instance", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.key_pair_name is not None:
            body_param["keyPairName"] = self.parameters.key_pair_name
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


class DetachEcsKeypairRequestParam(object):

    def __init__(self, region_id, instance_id, key_pair_name, ):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param key_pair_name: 不传自动填充主机绑定密钥对(对齐公有云必传，混合云v1不传)
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.key_pair_name = key_pair_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.key_pair_name is None:
            raise Exception("key_pair_name can not None")

