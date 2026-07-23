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


class PutBucketLoggingRequest(CTYunRequest):
    """
    注意：   
    1. grantee中ID（被授权者）为对象存储用户的ID（非云管用户ID）   
    2. grantee中type枚举为CanonicalUser、AmazonCustomerByEmail；当type=CanonicalUser时，ID不得为空；当type=AmazonCustomerByEmail时，emailAddress不得为空；
    """

    def __init__(self, request_param):
        super(PutBucketLoggingRequest, self).__init__("/v4/oss/put-bucket-logging", "POST", "zos", "application/json")
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
        if self.parameters.bucket_logging_status is not None:
            if type(self.parameters.bucket_logging_status) is dict:
                bucket_logging_status_dict_value = self.parameters.bucket_logging_status
            else:
                bucket_logging_status_dict_value = self.parameters.bucket_logging_status.get_dic()
            body_param["bucketLoggingStatus"] = bucket_logging_status_dict_value
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


class BucketLoggingStatus(object):

    def __init__(self, logging_enabled, ):
        """
        :param logging_enabled: 设置日志转存 设置日志转存时TargetBucket，TargetPrefix必传
        """
        self.logging_enabled = logging_enabled
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.logging_enabled is not None:
            if type(self.logging_enabled) is dict:
                obj_dict["loggingEnabled"] = self.logging_enabled
            else:
                obj_dict["loggingEnabled"] = self.logging_enabled.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.logging_enabled is None:
            raise Exception("logging_enabled can not None")


class LoggingEnabled(object):

    def __init__(self, target_bucket, target_prefix, target_grants=None):
        """
        :param target_bucket: 目标桶名
        :param target_prefix: 日志对象前缀
        :param target_grants: 授权信息的容器
        """
        self.target_bucket = target_bucket
        self.target_prefix = target_prefix
        self.target_grants = target_grants
        self.check_param()

    def set_target_grants(self, target_grants):
        """
        :param target_grants: 授权信息的容器
        """
        self.target_grants = target_grants

    def get_dic(self):
        obj_dict = dict()
        if self.target_bucket is not None:
            obj_dict["targetBucket"] = self.target_bucket
        if self.target_prefix is not None:
            obj_dict["targetPrefix"] = self.target_prefix
        if self.target_grants is not None:
            target_grants_array = []
            for item in self.target_grants:
                if type(item) is dict:
                    target_grants_array.append(item)
                else:
                    target_grants_array.append(item.get_dic())
            obj_dict["targetGrants"] = target_grants_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.target_bucket is None:
            raise Exception("target_bucket can not None")
        if self.target_prefix is None:
            raise Exception("target_prefix can not None")


class TargetGrant(object):

    def __init__(self, permission, grantee, ):
        """
        :param permission: 分配给存储空间的被授权者的日志记录权限。支持 FULL_CONTROL，READ，WRITE
        :param grantee: 被授予权限的人
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

    def __init__(self, type, email_address=None, display_name=None, id=None):
        """
        :param type: 被授权者类型；CanonicalUser或AmazonCustomerByEmail
        :param email_address: 被授权者邮箱
        :param display_name: 被授权者展示名称（即被授权对象存储用户名称）
        :param id: 被授权者（即被授权对象存储用户ID）
        """
        self.type = type
        self.email_address = email_address
        self.display_name = display_name
        self.id = id
        self.check_param()

    def set_email_address(self, email_address):
        """
        :param email_address: 被授权者邮箱
        """
        self.email_address = email_address

    def set_display_name(self, display_name):
        """
        :param display_name: 被授权者展示名称（即被授权对象存储用户名称）
        """
        self.display_name = display_name

    def set_id(self, id):
        """
        :param id: 被授权者（即被授权对象存储用户ID）
        """
        self.id = id

    def get_dic(self):
        obj_dict = dict()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.email_address is not None:
            obj_dict["emailAddress"] = self.email_address
        if self.display_name is not None:
            obj_dict["displayName"] = self.display_name
        if self.id is not None:
            obj_dict["ID"] = self.id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class PutBucketLoggingRequestParam(object):

    def __init__(self, region_id, bucket, bucket_logging_status, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param bucket_logging_status: 日志参数
        """
        self.region_id = region_id
        self.bucket = bucket
        self.bucket_logging_status = bucket_logging_status

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.bucket_logging_status is None:
            raise Exception("bucket_logging_status can not None")

