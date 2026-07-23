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


class CreateBucketRequest(CTYunRequest):
    """
    创建对象存储桶   
    1. 桶名称（长度3~63;只能有大小写字母、数字、.、-;禁止两个英文句号（.）或英文句号（.）和中划线（-）相邻;禁止以英文句号（.）和中划线（-）开头或结尾;禁止使用IP地址）；桶名称不可重复   
    2. ACL桶权限枚举值：（'private', 'public-read', 'public-read-write', 'authenticated-read'）   
    3. 存储类型，目前支持STANDARD、STANDARD_IA和GLACIER，默认STANDARD   
    4. AZ策略:可选值为single-az，multi-az，默认为single-az
    """

    def __init__(self, request_param):
        super(CreateBucketRequest, self).__init__("/v4/oss/create-bucket", "POST", "zos", "application/json")
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
        if self.parameters.is_encrypted is not None:
            body_param["isEncrypted"] = self.parameters.is_encrypted
        if self.parameters.storage_type is not None:
            body_param["storageType"] = self.parameters.storage_type
        if self.parameters.az_policy is not None:
            body_param["AZPolicy"] = self.parameters.az_policy
        if self.parameters.other_bucket_info is not None:
            if type(self.parameters.other_bucket_info) is dict:
                other_bucket_info_dict_value = self.parameters.other_bucket_info
            else:
                other_bucket_info_dict_value = self.parameters.other_bucket_info.get_dic()
            body_param["otherBucketInfo"] = other_bucket_info_dict_value
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


class OtherBucketInfo(object):

    def __init__(self, object_lock_enabled_for_bucket=None, location_constraint=None):
        """
        :param object_lock_enabled_for_bucket: Bucket是否开启合规保留功能，开启之后才能设置保留策略，开启后自动开启版本控制
        :param location_constraint: bucket的Region(资源池id)信息
        """
        self.object_lock_enabled_for_bucket = object_lock_enabled_for_bucket
        self.location_constraint = location_constraint

    def set_object_lock_enabled_for_bucket(self, object_lock_enabled_for_bucket):
        """
        :param object_lock_enabled_for_bucket: Bucket是否开启合规保留功能，开启之后才能设置保留策略，开启后自动开启版本控制
        """
        self.object_lock_enabled_for_bucket = object_lock_enabled_for_bucket

    def set_location_constraint(self, location_constraint):
        """
        :param location_constraint: bucket的Region(资源池id)信息
        """
        self.location_constraint = location_constraint

    def get_dic(self):
        obj_dict = dict()
        if self.object_lock_enabled_for_bucket is not None:
            obj_dict["ObjectLockEnabledForBucket"] = self.object_lock_enabled_for_bucket
        if self.location_constraint is not None:
            obj_dict["locationConstraint"] = self.location_constraint
        return obj_dict


class CreateBucketRequestParam(object):

    def __init__(self, region_id, bucket, acl, is_encrypted=None, storage_type=None, az_policy=None, other_bucket_info=None):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称（长度3~63;只能有大小写字母、数字、.、-;禁止两个英文句号（.）或英文句号（.）和中划线（-）相邻;禁止以英文句号（.）和中划线（-）开头或结尾;禁止使用IP地址）；桶名称不可重复
        :param acl: 桶权限。（'private', 'public-read', 'public-read-write', 'authenticated-read'）
        :param is_encrypted: 是否开启服务端加密。默认为false。若开启加密，算法默认使用AES256
        :param storage_type: 存储类型，目前支持STANDARD、STANDARD_IA和GLACIER，默认STANDARD
        :param az_policy: AZ策略:可选值为single-az，multi-az，默认为single-az
        :param other_bucket_info: 其他创建桶信息
        """
        self.region_id = region_id
        self.bucket = bucket
        self.acl = acl
        self.is_encrypted = is_encrypted
        self.storage_type = storage_type
        self.az_policy = az_policy
        self.other_bucket_info = other_bucket_info

    def set_is_encrypted(self, is_encrypted):
        """
        :param is_encrypted: 是否开启服务端加密。默认为false。若开启加密，算法默认使用AES256
        """
        self.is_encrypted = is_encrypted

    def set_storage_type(self, storage_type):
        """
        :param storage_type: 存储类型，目前支持STANDARD、STANDARD_IA和GLACIER，默认STANDARD
        """
        self.storage_type = storage_type

    def set_az_policy(self, az_policy):
        """
        :param az_policy: AZ策略:可选值为single-az，multi-az，默认为single-az
        """
        self.az_policy = az_policy

    def set_other_bucket_info(self, other_bucket_info):
        """
        :param other_bucket_info: 其他创建桶信息
        """
        self.other_bucket_info = other_bucket_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.acl is None:
            raise Exception("acl can not None")

