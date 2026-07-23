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


class AsyncCreateTargetRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容4.0资源池   
    如果是批量创建多个，其中一个出错时会返回错误，可能出现部分创建成功，部分失败的场景
    """

    def __init__(self, request_param):
        super(AsyncCreateTargetRequest, self).__init__("/v4/elb/async-create-vm", "POST", "ctelb", "application/json")
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
        if self.parameters.target_group_id is not None:
            body_param["targetGroupID"] = self.parameters.target_group_id
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.targets is not None:
            targets = []
            if isinstance(self.parameters.targets, list):
                for item in self.parameters.targets:
                    if type(item) is dict:
                        targets.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        targets.append(item_dict_value)
            else:
                targets.append(self.parameters.targets.get_dic())
            body_param["targets"] = targets
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


class Target(object):

    def __init__(self, instance_id, address, weight, protocol_port, instance_type, ):
        """
        :param instance_id: 后端服务主机 id
        :param address: 后端服务主机主网卡所在的 IP
        :param weight: 后端服务主机权重: 1 - 256
        :param protocol_port: 后端服务监听端口，1-65535
        :param instance_type: 后端服务主机类型，支持vm、bm类型
        """
        self.instance_id = instance_id
        self.address = address
        self.weight = weight
        self.protocol_port = protocol_port
        self.instance_type = instance_type
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.instance_id is not None:
            obj_dict["instanceID"] = self.instance_id
        if self.address is not None:
            obj_dict["address"] = self.address
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        if self.protocol_port is not None:
            obj_dict["protocolPort"] = self.protocol_port
        if self.instance_type is not None:
            obj_dict["instanceType"] = self.instance_type
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.address is None:
            raise Exception("address can not None")
        if self.weight is None:
            raise Exception("weight can not None")
        if self.protocol_port is None:
            raise Exception("protocol_port can not None")
        if self.instance_type is None:
            raise Exception("instance_type can not None")


class AsyncCreateTargetRequestParam(object):

    def __init__(self, region_id, target_group_id, client_token, targets, ):
        """
        :param region_id: 
        :param target_group_id: 
        :param client_token: 
        :param targets:  注意:此参数为数组
        """
        self.region_id = region_id
        self.target_group_id = target_group_id
        self.client_token = client_token
        self.targets = targets

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.target_group_id is None:
            raise Exception("target_group_id can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.targets is None:
            raise Exception("targets can not None")

