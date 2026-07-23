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


class CreateBucketACLHybridRequest(CTYunRequest):
    """
    桶acl策略创建
    """

    def __init__(self, request_param):
        super(CreateBucketACLHybridRequest, self).__init__("/v4/oss/create-bucket-acl", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.policy_list is not None:
            policy_list = []
            if isinstance(self.parameters.policy_list, list):
                for item in self.parameters.policy_list:
                    if type(item) is dict:
                        policy_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        policy_list.append(item_dict_value)
            else:
                policy_list.append(self.parameters.policy_list.get_dic())
            body_param["policyList"] = policy_list
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


class Policy(object):

    def __init__(self, user_id, permission_list, ):
        """
        :param user_id: 不可与桶acl策略中已有的用户id重复
        :param permission_list: 'WRITE' 桶写入权限, 'WRITE_ACP' ACL写入权限, 'READ' 桶读取权限, 'READ_ACP' ACL读取权限, 'FULL_CONTROL' 所有权限，相当于前面4个权限之和，当桶或acl权限未设置时默认设置为读，但不可桶和acl均不设置权限
        """
        self.user_id = user_id
        self.permission_list = permission_list
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.user_id is not None:
            obj_dict["userId"] = self.user_id
        if self.permission_list is not None:
            obj_dict["permissionList"] = self.permission_list
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.user_id is None:
            raise Exception("user_id can not None")
        if self.permission_list is None:
            raise Exception("permission_list can not None")


class CreateBucketACLHybridRequestParam(object):

    def __init__(self, region_id, bucket, policy_list, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param policy_list: 策略列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.bucket = bucket
        self.policy_list = policy_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.policy_list is None:
            raise Exception("policy_list can not None")

