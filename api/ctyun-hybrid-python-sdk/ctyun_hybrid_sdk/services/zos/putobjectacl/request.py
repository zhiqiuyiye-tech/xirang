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


class PutObjectAclRequest(CTYunRequest):
    """
    注意：   
    ACL枚举值中aws-exec-read, bucket-owner-read, bucket-owner-full-control为兼容混合云v1字段。与底层确认，暂不支持aws-exec-read   
    grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）
    """

    def __init__(self, request_param):
        super(PutObjectAclRequest, self).__init__("/v4/oss/put-object-acl", "POST", "zos", "application/json")
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
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
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
        if self.parameters.version_id is not None:
            body_param["versionID"] = self.parameters.version_id
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
        :param owner: 所有者
        :param grants: 授权信息
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

    def __init__(self, grantee, permission, ):
        """
        :param grantee: 
        :param permission: 权限，为 WRITE, WRITE_ACP, FULL_CONTROL, READ, READ_ACP 之中的值 WRITE：向桶中写对象的权限 WRITE_ACP：修改桶的访问控制权限的能力 READ：读取桶中文件列表的能力 READ_ACP：获取桶的访问控制权限的能力 FULL_CONTROL：同桶的所属者相同的权限，以上能力都具有
        """
        self.grantee = grantee
        self.permission = permission
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.grantee is not None:
            if type(self.grantee) is dict:
                obj_dict["grantee"] = self.grantee
            else:
                obj_dict["grantee"] = self.grantee.get_dic()
        if self.permission is not None:
            obj_dict["permission"] = self.permission
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.grantee is None:
            raise Exception("grantee can not None")
        if self.permission is None:
            raise Exception("permission can not None")


class Grantee(object):

    def __init__(self, type, email_address=None, display_name=None, id=None, uri=None):
        """
        :param email_address: 邮箱地址
        :param type: 用户类型， CanonicalUser，AmazonCustomerByEmail，Group 三者之一。type 为 CanonicalUser 时，必填 ID；为 AmazonCustomerByEmail，必填 emailAddress；为 Group 必填URI。另外，使用 AmazonCustomerByEmail 时，将会保存其指向到的 CanonicalUser 类型的用户
        :param display_name: 展示名称（即被授权对象存储用户名称）
        :param id: 被授权者（即被授权对象存储用户ID）,Type为'CanonicalUser'，则该字段必须
        :param uri: URI，不存在时为 null
        """
        self.email_address = email_address
        self.type = type
        self.display_name = display_name
        self.id = id
        self.uri = uri
        self.check_param()

    def set_email_address(self, email_address):
        """
        :param email_address: 邮箱地址
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
        :param uri: URI，不存在时为 null
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


class PutObjectAclRequestParam(object):

    def __init__(self, region_id, key, bucket, acl=None, access_control_policy=None, version_id=None):
        """
        :param region_id: 资源池id
        :param key: 对象名
        :param bucket: 桶名称
        :param acl: ACL 配置，（ACL、accessControlPolicy两种方式不可同时使用，每次只能给一种参数赋值）
        :param access_control_policy: 访问控制策略（ACL、accessControlPolicy两种方式不可同时使用，每次只能给一种参数赋值）
        :param version_id: 多版本场景下，指定对象的特定版本
        """
        self.region_id = region_id
        self.key = key
        self.bucket = bucket
        self.acl = acl
        self.access_control_policy = access_control_policy
        self.version_id = version_id

    def set_acl(self, acl):
        """
        :param acl: ACL 配置，（ACL、accessControlPolicy两种方式不可同时使用，每次只能给一种参数赋值）
        """
        self.acl = acl

    def set_access_control_policy(self, access_control_policy):
        """
        :param access_control_policy: 访问控制策略（ACL、accessControlPolicy两种方式不可同时使用，每次只能给一种参数赋值）
        """
        self.access_control_policy = access_control_policy

    def set_version_id(self, version_id):
        """
        :param version_id: 多版本场景下，指定对象的特定版本
        """
        self.version_id = version_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key is None:
            raise Exception("key can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")

