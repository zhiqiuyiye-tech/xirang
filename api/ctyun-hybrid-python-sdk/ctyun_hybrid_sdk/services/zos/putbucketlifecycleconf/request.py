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


class PutBucketLifecycleConfRequest(CTYunRequest):
    """
    1、规则启用时，expiration、noncurrentVersionExpiration、noncurrentVersionTransitions、transitions四个参数必传一项；   
    2、transitions字段 -- 公有云有该字段，混合云v1不支持=》混合云v2兼容   
    3、由于混合云v2控制台限制，expiration和transitions中选择days或date需要保持一致，要么都是days，要么都是date；   
    4、newerNoncurrentVersions、objectSizeGreaterThan和objectSizeLessThan，公有云未有该参数，兼容V1处理。此外注意：公有云文档、底层文档和aws官网文档都没有给出该值的范围限制。目前V2就只做了大于等于0的限制处理，不允许负数的情况。其余情况的错误信息由底层错误信息透传返回。
    """

    def __init__(self, request_param):
        super(PutBucketLifecycleConfRequest, self).__init__("/v4/oss/put-bucket-lifecycle-conf", "POST", "zos", "application/json")
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
        if self.parameters.lifecycle_configuration is not None:
            if type(self.parameters.lifecycle_configuration) is dict:
                lifecycle_configuration_dict_value = self.parameters.lifecycle_configuration
            else:
                lifecycle_configuration_dict_value = self.parameters.lifecycle_configuration.get_dic()
            body_param["lifecycleConfiguration"] = lifecycle_configuration_dict_value
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


class LifecycleConfiguration(object):

    def __init__(self, rules, ):
        """
        :param rules: 生命周期规则 不设置传 []
        """
        self.rules = rules
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.rules is not None:
            rules_array = []
            for item in self.rules:
                if type(item) is dict:
                    rules_array.append(item)
                else:
                    rules_array.append(item.get_dic())
            obj_dict["rules"] = rules_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.rules is None:
            raise Exception("rules can not None")


class Rule(object):

    def __init__(self, status, prefix=None, id=None, expiration=None, filter=None, noncurrent_version_expiration=None, noncurrent_version_transitions=None, abort_incomplete_multipart_upload=None, transitions=None):
        """
        :param status: 标识是否应用规则  可选值：Enabled, Disabled
        :param prefix: 标识应用规则的对象前缀
        :param id: 标识唯一的规则
        :param expiration: 当前文件过期策略
        :param filter: 过滤应用规则的对象
        :param noncurrent_version_expiration: 历史版本过期策略
        :param noncurrent_version_transitions: 指定生命周期规则的过渡规则，描述非当前对象何时过渡到特定的存储类别
        :param abort_incomplete_multipart_upload: 碎片过期策略
        :param transitions: 指定桶内对象何时过渡到指定的存储类别
        """
        self.status = status
        self.prefix = prefix
        self.id = id
        self.expiration = expiration
        self.filter = filter
        self.noncurrent_version_expiration = noncurrent_version_expiration
        self.noncurrent_version_transitions = noncurrent_version_transitions
        self.abort_incomplete_multipart_upload = abort_incomplete_multipart_upload
        self.transitions = transitions
        self.check_param()

    def set_prefix(self, prefix):
        """
        :param prefix: 标识应用规则的对象前缀
        """
        self.prefix = prefix

    def set_id(self, id):
        """
        :param id: 标识唯一的规则
        """
        self.id = id

    def set_expiration(self, expiration):
        """
        :param expiration: 当前文件过期策略
        """
        self.expiration = expiration

    def set_filter(self, filter):
        """
        :param filter: 过滤应用规则的对象
        """
        self.filter = filter

    def set_noncurrent_version_expiration(self, noncurrent_version_expiration):
        """
        :param noncurrent_version_expiration: 历史版本过期策略
        """
        self.noncurrent_version_expiration = noncurrent_version_expiration

    def set_noncurrent_version_transitions(self, noncurrent_version_transitions):
        """
        :param noncurrent_version_transitions: 指定生命周期规则的过渡规则，描述非当前对象何时过渡到特定的存储类别
        """
        self.noncurrent_version_transitions = noncurrent_version_transitions

    def set_abort_incomplete_multipart_upload(self, abort_incomplete_multipart_upload):
        """
        :param abort_incomplete_multipart_upload: 碎片过期策略
        """
        self.abort_incomplete_multipart_upload = abort_incomplete_multipart_upload

    def set_transitions(self, transitions):
        """
        :param transitions: 指定桶内对象何时过渡到指定的存储类别
        """
        self.transitions = transitions

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.id is not None:
            obj_dict["ID"] = self.id
        if self.expiration is not None:
            if type(self.expiration) is dict:
                obj_dict["expiration"] = self.expiration
            else:
                obj_dict["expiration"] = self.expiration.get_dic()
        if self.filter is not None:
            if type(self.filter) is dict:
                obj_dict["filter"] = self.filter
            else:
                obj_dict["filter"] = self.filter.get_dic()
        if self.noncurrent_version_expiration is not None:
            if type(self.noncurrent_version_expiration) is dict:
                obj_dict["noncurrentVersionExpiration"] = self.noncurrent_version_expiration
            else:
                obj_dict["noncurrentVersionExpiration"] = self.noncurrent_version_expiration.get_dic()
        if self.noncurrent_version_transitions is not None:
            noncurrent_version_transitions_array = []
            for item in self.noncurrent_version_transitions:
                if type(item) is dict:
                    noncurrent_version_transitions_array.append(item)
                else:
                    noncurrent_version_transitions_array.append(item.get_dic())
            obj_dict["noncurrentVersionTransitions"] = noncurrent_version_transitions_array
        if self.abort_incomplete_multipart_upload is not None:
            if type(self.abort_incomplete_multipart_upload) is dict:
                obj_dict["abortIncompleteMultipartUpload"] = self.abort_incomplete_multipart_upload
            else:
                obj_dict["abortIncompleteMultipartUpload"] = self.abort_incomplete_multipart_upload.get_dic()
        if self.transitions is not None:
            transitions_array = []
            for item in self.transitions:
                if type(item) is dict:
                    transitions_array.append(item)
                else:
                    transitions_array.append(item.get_dic())
            obj_dict["transitions"] = transitions_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")


class Expiration(object):

    def __init__(self, days=None, date=None, expired_object_delete_marker=None):
        """
        :param days: 当前文件过期时间   单位天，Date与Days二选一；且与参数 date 以及 expiredObjectDeleteMarker 不能共存
        :param date: 当前文件的过期日期 日期为ISO8601格式，必须为UTC午夜0时，例如：2022-10-18T02:24:40Z，且与参数 expiredObjectDeleteMarker 以及 days 不能共存
        :param expired_object_delete_marker: 指定是否自动移除过期删除标记。如果设置为true，删除标记将过期；如果设置为 false，则策略不执行任何操作。且与参数 date 以及 days 不能共存
        """
        self.days = days
        self.date = date
        self.expired_object_delete_marker = expired_object_delete_marker

    def set_days(self, days):
        """
        :param days: 当前文件过期时间   单位天，Date与Days二选一；且与参数 date 以及 expiredObjectDeleteMarker 不能共存
        """
        self.days = days

    def set_date(self, date):
        """
        :param date: 当前文件的过期日期 日期为ISO8601格式，必须为UTC午夜0时，例如：2022-10-18T02:24:40Z，且与参数 expiredObjectDeleteMarker 以及 days 不能共存
        """
        self.date = date

    def set_expired_object_delete_marker(self, expired_object_delete_marker):
        """
        :param expired_object_delete_marker: 指定是否自动移除过期删除标记。如果设置为true，删除标记将过期；如果设置为 false，则策略不执行任何操作。且与参数 date 以及 days 不能共存
        """
        self.expired_object_delete_marker = expired_object_delete_marker

    def get_dic(self):
        obj_dict = dict()
        if self.days is not None:
            obj_dict["days"] = self.days
        if self.date is not None:
            obj_dict["date"] = self.date
        if self.expired_object_delete_marker is not None:
            obj_dict["expiredObjectDeleteMarker"] = self.expired_object_delete_marker
        return obj_dict


class Filter(object):

    def __init__(self, and_value=None, prefix=None, object_size_greater_than=None, object_size_less_than=None, tag=None):
        """
        :param and_value: 只有单个标签或前缀时不会返回
        :param prefix: 前缀
        :param object_size_greater_than: 规则适用的最小对象大小
        :param object_size_less_than: 规则适用的最大对象大小
        :param tag: 标签
        """
        self.and_value = and_value
        self.prefix = prefix
        self.object_size_greater_than = object_size_greater_than
        self.object_size_less_than = object_size_less_than
        self.tag = tag

    def set_and_value(self, and_value):
        """
        :param and_value: 只有单个标签或前缀时不会返回
        """
        self.and_value = and_value

    def set_prefix(self, prefix):
        """
        :param prefix: 前缀
        """
        self.prefix = prefix

    def set_object_size_greater_than(self, object_size_greater_than):
        """
        :param object_size_greater_than: 规则适用的最小对象大小
        """
        self.object_size_greater_than = object_size_greater_than

    def set_object_size_less_than(self, object_size_less_than):
        """
        :param object_size_less_than: 规则适用的最大对象大小
        """
        self.object_size_less_than = object_size_less_than

    def set_tag(self, tag):
        """
        :param tag: 标签
        """
        self.tag = tag

    def get_dic(self):
        obj_dict = dict()
        if self.and_value is not None:
            if type(self.and_value) is dict:
                obj_dict["and"] = self.and_value
            else:
                obj_dict["and"] = self.and_value.get_dic()
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.object_size_greater_than is not None:
            obj_dict["objectSizeGreaterThan"] = self.object_size_greater_than
        if self.object_size_less_than is not None:
            obj_dict["objectSizeLessThan"] = self.object_size_less_than
        if self.tag is not None:
            if type(self.tag) is dict:
                obj_dict["tag"] = self.tag
            else:
                obj_dict["tag"] = self.tag.get_dic()
        return obj_dict


class AndModel(object):

    def __init__(self, tags=None, prefix=None, object_size_greater_than=None, object_size_less_than=None):
        """
        :param tags: 
        :param prefix: 标识应用规则的对象前缀
        :param object_size_greater_than: 规则适用的最小对象大小
        :param object_size_less_than: 规则适用的最大对象大小
        """
        self.tags = tags
        self.prefix = prefix
        self.object_size_greater_than = object_size_greater_than
        self.object_size_less_than = object_size_less_than

    def set_tags(self, tags):
        """
        :param tags: 
        """
        self.tags = tags

    def set_prefix(self, prefix):
        """
        :param prefix: 标识应用规则的对象前缀
        """
        self.prefix = prefix

    def set_object_size_greater_than(self, object_size_greater_than):
        """
        :param object_size_greater_than: 规则适用的最小对象大小
        """
        self.object_size_greater_than = object_size_greater_than

    def set_object_size_less_than(self, object_size_less_than):
        """
        :param object_size_less_than: 规则适用的最大对象大小
        """
        self.object_size_less_than = object_size_less_than

    def get_dic(self):
        obj_dict = dict()
        if self.tags is not None:
            tags_array = []
            for item in self.tags:
                if type(item) is dict:
                    tags_array.append(item)
                else:
                    tags_array.append(item.get_dic())
            obj_dict["tags"] = tags_array
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.object_size_greater_than is not None:
            obj_dict["objectSizeGreaterThan"] = self.object_size_greater_than
        if self.object_size_less_than is not None:
            obj_dict["objectSizeLessThan"] = self.object_size_less_than
        return obj_dict


class Tag(object):

    def __init__(self, key=None, value=None):
        """
        :param key: 标签key
        :param value: 标签value
        """
        self.key = key
        self.value = value

    def set_key(self, key):
        """
        :param key: 标签key
        """
        self.key = key

    def set_value(self, value):
        """
        :param value: 标签value
        """
        self.value = value

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.value is not None:
            obj_dict["value"] = self.value
        return obj_dict


class NoncurrentVersionExpiration(object):

    def __init__(self, noncurrent_days=None, newer_noncurrent_versions=None):
        """
        :param noncurrent_days: 历史版本过期时间   单位天
        :param newer_noncurrent_versions: 指定 OSS 将保留多少个非当前版本
        """
        self.noncurrent_days = noncurrent_days
        self.newer_noncurrent_versions = newer_noncurrent_versions

    def set_noncurrent_days(self, noncurrent_days):
        """
        :param noncurrent_days: 历史版本过期时间   单位天
        """
        self.noncurrent_days = noncurrent_days

    def set_newer_noncurrent_versions(self, newer_noncurrent_versions):
        """
        :param newer_noncurrent_versions: 指定 OSS 将保留多少个非当前版本
        """
        self.newer_noncurrent_versions = newer_noncurrent_versions

    def get_dic(self):
        obj_dict = dict()
        if self.noncurrent_days is not None:
            obj_dict["noncurrentDays"] = self.noncurrent_days
        if self.newer_noncurrent_versions is not None:
            obj_dict["newerNoncurrentVersions"] = self.newer_noncurrent_versions
        return obj_dict


class NoncurrentVersionTransition(object):

    def __init__(self, noncurrent_days=None, newer_noncurrent_versions=None, storage_class=None):
        """
        :param noncurrent_days: 历史版本过期时间 单位天
        :param newer_noncurrent_versions: 指定 OSS 将保留多少个非当前版本
        :param storage_class: 用于存储对象的存储类，例如：STANDARD
        """
        self.noncurrent_days = noncurrent_days
        self.newer_noncurrent_versions = newer_noncurrent_versions
        self.storage_class = storage_class

    def set_noncurrent_days(self, noncurrent_days):
        """
        :param noncurrent_days: 历史版本过期时间 单位天
        """
        self.noncurrent_days = noncurrent_days

    def set_newer_noncurrent_versions(self, newer_noncurrent_versions):
        """
        :param newer_noncurrent_versions: 指定 OSS 将保留多少个非当前版本
        """
        self.newer_noncurrent_versions = newer_noncurrent_versions

    def set_storage_class(self, storage_class):
        """
        :param storage_class: 用于存储对象的存储类，例如：STANDARD
        """
        self.storage_class = storage_class

    def get_dic(self):
        obj_dict = dict()
        if self.noncurrent_days is not None:
            obj_dict["noncurrentDays"] = self.noncurrent_days
        if self.newer_noncurrent_versions is not None:
            obj_dict["newerNoncurrentVersions"] = self.newer_noncurrent_versions
        if self.storage_class is not None:
            obj_dict["storageClass"] = self.storage_class
        return obj_dict


class AbortIncompleteMultipartUpload(object):

    def __init__(self, days_after_initiation=None):
        """
        :param days_after_initiation: 碎片过期时间   单位天
        """
        self.days_after_initiation = days_after_initiation

    def set_days_after_initiation(self, days_after_initiation):
        """
        :param days_after_initiation: 碎片过期时间   单位天
        """
        self.days_after_initiation = days_after_initiation

    def get_dic(self):
        obj_dict = dict()
        if self.days_after_initiation is not None:
            obj_dict["daysAfterInitiation"] = self.days_after_initiation
        return obj_dict


class Transition(object):

    def __init__(self, storage_class, date=None, days=None):
        """
        :param date: 指示对象何时转换到指定的存储类，与 days 不能共存
        :param days: 指示对象在创建后转换到指定存储类的天数，与 date 不能共存。该值必须是正整数
        :param storage_class: 该对象过渡到的存储类，可选值为 GLACIER， STANDARD_IA
        """
        self.date = date
        self.days = days
        self.storage_class = storage_class
        self.check_param()

    def set_date(self, date):
        """
        :param date: 指示对象何时转换到指定的存储类，与 days 不能共存
        """
        self.date = date

    def set_days(self, days):
        """
        :param days: 指示对象在创建后转换到指定存储类的天数，与 date 不能共存。该值必须是正整数
        """
        self.days = days

    def get_dic(self):
        obj_dict = dict()
        if self.date is not None:
            obj_dict["date"] = self.date
        if self.days is not None:
            obj_dict["days"] = self.days
        if self.storage_class is not None:
            obj_dict["storageClass"] = self.storage_class
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.storage_class is None:
            raise Exception("storage_class can not None")


class PutBucketLifecycleConfRequestParam(object):

    def __init__(self, region_id, bucket, lifecycle_configuration, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param lifecycle_configuration: 生命周期参数
        """
        self.region_id = region_id
        self.bucket = bucket
        self.lifecycle_configuration = lifecycle_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.lifecycle_configuration is None:
            raise Exception("lifecycle_configuration can not None")

