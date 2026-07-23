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


class PutBucketAclRequest(CTYunRequest):
    """
    注意：   
    1. grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）   
    2. ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值
    """

    def __init__(self, request_param):
        super(PutBucketAclRequest, self).__init__("/v4/oss/put-bucket-acl", "POST", "zos", "application/json")
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
        if self.parameters.acl is not None:
            body_param["ACL"] = self.parameters.acl
        if self.parameters.access_control_policy is not None:
            if type(self.parameters.access_control_policy) is dict:
                access_control_policy_dict_value = self.parameters.access_control_policy
            else:
                access_control_policy_dict_value = self.parameters.access_control_policy.get_dic()
            body_param["accessControlPolicy"] = access_control_policy_dict_value
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


class AccessControlPolicy(object):

    def __init__(self, owner, grants, ):
        """
        :param owner: Bucket所有者
        :param grants: 被授权用户可以对桶进行read, write, read ACP, and write ACP操作
        """
        self.owner = owner
        self.grants = grants
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.owner is not None:
            if type(self.owner) is dict:
                obj_dict["owner"] = self.owner
            else:
                obj_dict["owner"] = self.owner.get_dic()
        if self.grants is not None:
            grants_array = []
            for item in self.grants:
                if type(item) is dict:
                    grants_array.append(item)
                else:
                    grants_array.append(item.get_dic())
            obj_dict["grants"] = grants_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.owner is None:
            raise Exception("owner can not None")
        if self.grants is None:
            raise Exception("grants can not None")


class Owner(object):

    def __init__(self, display_name, id, ):
        """
        :param display_name: 展示名称（即对象存储用户名称）
        :param id: 用户ID（即对象存储用户ID）
        """
        self.display_name = display_name
        self.id = id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.display_name is not None:
            obj_dict["displayName"] = self.display_name
        if self.id is not None:
            obj_dict["ID"] = self.id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.display_name is None:
            raise Exception("display_name can not None")
        if self.id is None:
            raise Exception("id can not None")


class Grant(object):

    def __init__(self, permission, grantee, ):
        """
        :param permission: 权限，为 WRITE, WRITE_ACP, FULL_CONTROL, READ, READ_ACP 之中的值
        :param grantee: 被授权用户
        """
        self.permission = permission
        self.grantee = grantee
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.permission is not None:
            obj_dict["permission"] = self.permission
        if self.grantee is not None:
            if type(self.grantee) is dict:
                obj_dict["grantee"] = self.grantee
            else:
                obj_dict["grantee"] = self.grantee.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.permission is None:
            raise Exception("permission can not None")
        if self.grantee is None:
            raise Exception("grantee can not None")


class Grantee(object):

    def __init__(self, type, email_address=None, display_name=None, id=None, uri=None):
        """
        :param email_address: 邮箱地址,如果Type为'AmazonCustomerByEmail'，则该字段必须
        :param type: 被授权用户类型， 取值范围 'CanonicalUser' 'AmazonCustomerByEmail' 'Group'
        :param display_name: 展示名称（即被授权对象存储用户名称）
        :param id: 被授权者（即被授权对象存储用户ID）,Type为'CanonicalUser'，则该字段必须
        :param uri: URI，如果Type为'Group'，则该字段必须
        """
        self.email_address = email_address
        self.type = type
        self.display_name = display_name
        self.id = id
        self.uri = uri
        self.check_param()

    def set_email_address(self, email_address):
        """
        :param email_address: 邮箱地址,如果Type为'AmazonCustomerByEmail'，则该字段必须
        """
        self.email_address = email_address

    def set_display_name(self, display_name):
        """
        :param display_name: 展示名称（即被授权对象存储用户名称）
        """
        self.display_name = display_name

    def set_id(self, id):
        """
        :param id: 被授权者（即被授权对象存储用户ID）,Type为'CanonicalUser'，则该字段必须
        """
        self.id = id

    def set_uri(self, uri):
        """
        :param uri: URI，如果Type为'Group'，则该字段必须
        """
        self.uri = uri

    def get_dic(self):
        obj_dict = dict()
        if self.email_address is not None:
            obj_dict["emailAddress"] = self.email_address
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.display_name is not None:
            obj_dict["displayName"] = self.display_name
        if self.id is not None:
            obj_dict["ID"] = self.id
        if self.uri is not None:
            obj_dict["URI"] = self.uri
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class PutBucketAclRequestParam(object):

    def __init__(self, region_id, bucket, acl=None, access_control_policy=None):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param acl: ACL 配置，（ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值）
        :param access_control_policy: 访问控制策略，（ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值）
        """
        self.region_id = region_id
        self.bucket = bucket
        self.acl = acl
        self.access_control_policy = access_control_policy

    def set_acl(self, acl):
        """
        :param acl: ACL 配置，（ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值）
        """
        self.acl = acl

    def set_access_control_policy(self, access_control_policy):
        """
        :param access_control_policy: 访问控制策略，（ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值）
        """
        self.access_control_policy = access_control_policy

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")

