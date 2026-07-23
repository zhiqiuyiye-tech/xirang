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


class PutBucketPolicyRequest(CTYunRequest):
    """
    设置存储空间授权策略
    """

    def __init__(self, request_param):
        super(PutBucketPolicyRequest, self).__init__("/v4/oss/put-bucket-policy", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.policy is not None:
            if type(self.parameters.policy) is dict:
                policy_dict_value = self.parameters.policy
            else:
                policy_dict_value = self.parameters.policy.get_dic()
            body_param["policy"] = policy_dict_value
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

    def __init__(self, version, statement, id=None):
        """
        :param version: 当前支持"2012-10-17"
        :param statement: 桶策略描述，定义完整的权限控制。
        :param id: 桶策略ID，桶策略的唯一标识
        """
        self.version = version
        self.statement = statement
        self.id = id
        self.check_param()

    def set_id(self, id):
        """
        :param id: 桶策略ID，桶策略的唯一标识
        """
        self.id = id

    def get_dic(self):
        obj_dict = dict()
        if self.version is not None:
            obj_dict["Version"] = self.version
        if self.statement is not None:
            statement_array = []
            for item in self.statement:
                if type(item) is dict:
                    statement_array.append(item)
                else:
                    statement_array.append(item.get_dic())
            obj_dict["Statement"] = statement_array
        if self.id is not None:
            obj_dict["Id"] = self.id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.version is None:
            raise Exception("version can not None")
        if self.statement is None:
            raise Exception("statement can not None")


class Statement(object):

    def __init__(self, resource, principal, action, effect, sid=None, condition=None):
        """
        :param resource: 存储桶、对象、访问点和作业是您可以允许或拒绝其权限的 Amazon S3 资源。
        :param principal: 被授权人，即指定本条桶策略描述所作用的用户，支持通配符“*”，表示所有用户。当对某个user进行授权时，Principal格式为"AWS": "arn:aws:s3:::user/userId",userId为对象存储用户id;   
         支持使用object或string格式   
         使用string入参时，可穿"*"或者"\\"AWS\\":\\"arn:aws:s3:::user/userId\\""   
         使用object入参时支持"AWS": "arn:aws:s3:::user/userId"
        :param action: 操作，即指定本条桶策略描述所作用的ZOS操作。以列表形式表示，可配置多条操作，以逗号间隔。支持通配符”*“，表示该资源能进行的所有操作。常用的Action有"s3:GetObject"，"s3:GetObjectAcl"，"s3:PutObject"， "s3:PutObjectAcl"等
        :param effect: 桶策略的效果，即指定本条桶策略描述的权限是接受请求还是拒绝请求。 接受请求：配置为“Allow”， 拒绝请求：配置为“Deny”
        :param sid: 本条桶策略描述的ID
        :param condition: 条件语句，指定本条桶策略所限制的条件。可以通过Condition对ZOS资源设置防盗链，形如： "Condition": {"StringEquals":{"aws:Referer":["www.example.com"]}，此时如果Effect为“Allow”，则允许来自"www.example.com"的请求；如果为“Deny”，则拒绝。
        """
        self.resource = resource
        self.principal = principal
        self.action = action
        self.effect = effect
        self.sid = sid
        self.condition = condition
        self.check_param()

    def set_sid(self, sid):
        """
        :param sid: 本条桶策略描述的ID
        """
        self.sid = sid

    def set_condition(self, condition):
        """
        :param condition: 条件语句，指定本条桶策略所限制的条件。可以通过Condition对ZOS资源设置防盗链，形如： "Condition": {"StringEquals":{"aws:Referer":["www.example.com"]}，此时如果Effect为“Allow”，则允许来自"www.example.com"的请求；如果为“Deny”，则拒绝。
        """
        self.condition = condition

    def get_dic(self):
        obj_dict = dict()
        if self.resource is not None:
            obj_dict["Resource"] = self.resource
        if self.principal is not None:
            obj_dict["Principal"] = self.principal
        if self.action is not None:
            obj_dict["Action"] = self.action
        if self.effect is not None:
            obj_dict["Effect"] = self.effect
        if self.sid is not None:
            obj_dict["Sid"] = self.sid
        if self.condition is not None:
            obj_dict["Condition"] = self.condition
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.resource is None:
            raise Exception("resource can not None")
        if self.principal is None:
            raise Exception("principal can not None")
        if self.action is None:
            raise Exception("action can not None")
        if self.effect is None:
            raise Exception("effect can not None")


class PutBucketPolicyRequestParam(object):

    def __init__(self, bucket, region_id, policy, ):
        """
        :param bucket: 桶名称
        :param region_id: 资源池ID
        :param policy: 设置在bucket上的策略
        """
        self.bucket = bucket
        self.region_id = region_id
        self.policy = policy

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.policy is None:
            raise Exception("policy can not None")

