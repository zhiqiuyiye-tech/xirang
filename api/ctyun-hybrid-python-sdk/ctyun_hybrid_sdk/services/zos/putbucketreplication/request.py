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


class PutBucketReplicationRequest(CTYunRequest):
    """
    开发未对齐原因：混合云与公有云入参差异较大   
    该接口底层不支持，公有云实现为跨域复制
    """

    def __init__(self, request_param):
        super(PutBucketReplicationRequest, self).__init__("/v4/oss/put-bucket-replication", "POST", "zos", "application/json")
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
        if self.parameters.replication_configuration is not None:
            if type(self.parameters.replication_configuration) is dict:
                replication_configuration_dict_value = self.parameters.replication_configuration
            else:
                replication_configuration_dict_value = self.parameters.replication_configuration.get_dic()
            body_param["replicationConfiguration"] = replication_configuration_dict_value
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


class ReplicationConfiguration(object):

    def __init__(self, role, rules, ):
        """
        :param role: 发起者身份标示
        :param rules: 具体配置信息
        """
        self.role = role
        self.rules = rules
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.role is not None:
            obj_dict["role"] = self.role
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
        if self.role is None:
            raise Exception("role can not None")
        if self.rules is None:
            raise Exception("rules can not None")


class Rule(object):

    def __init__(self, status, destination, id=None, priority=None, prefix=None, filter=None, source_selection_criteria=None, existing_object_replication=None):
        """
        :param id: 用来标注具体 Rule 的名称
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        :param priority: 优先级
        :param prefix: 前缀匹配策略，不可重叠，重叠返回错误。前缀匹配根目录为空
        :param filter: 过滤条件
        :param source_selection_criteria: 源选择标准
        :param existing_object_replication: 现有对象复制规则
        :param destination: 目标存储桶信息
        """
        self.id = id
        self.status = status
        self.priority = priority
        self.prefix = prefix
        self.filter = filter
        self.source_selection_criteria = source_selection_criteria
        self.existing_object_replication = existing_object_replication
        self.destination = destination
        self.check_param()

    def set_id(self, id):
        """
        :param id: 用来标注具体 Rule 的名称
        """
        self.id = id

    def set_priority(self, priority):
        """
        :param priority: 优先级
        """
        self.priority = priority

    def set_prefix(self, prefix):
        """
        :param prefix: 前缀匹配策略，不可重叠，重叠返回错误。前缀匹配根目录为空
        """
        self.prefix = prefix

    def set_filter(self, filter):
        """
        :param filter: 过滤条件
        """
        self.filter = filter

    def set_source_selection_criteria(self, source_selection_criteria):
        """
        :param source_selection_criteria: 源选择标准
        """
        self.source_selection_criteria = source_selection_criteria

    def set_existing_object_replication(self, existing_object_replication):
        """
        :param existing_object_replication: 现有对象复制规则
        """
        self.existing_object_replication = existing_object_replication

    def get_dic(self):
        obj_dict = dict()
        if self.id is not None:
            obj_dict["id"] = self.id
        if self.status is not None:
            obj_dict["status"] = self.status
        if self.priority is not None:
            obj_dict["priority"] = self.priority
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.filter is not None:
            if type(self.filter) is dict:
                obj_dict["filter"] = self.filter
            else:
                obj_dict["filter"] = self.filter.get_dic()
        if self.source_selection_criteria is not None:
            if type(self.source_selection_criteria) is dict:
                obj_dict["sourceSelectionCriteria"] = self.source_selection_criteria
            else:
                obj_dict["sourceSelectionCriteria"] = self.source_selection_criteria.get_dic()
        if self.existing_object_replication is not None:
            if type(self.existing_object_replication) is dict:
                obj_dict["existingObjectReplication"] = self.existing_object_replication
            else:
                obj_dict["existingObjectReplication"] = self.existing_object_replication.get_dic()
        if self.destination is not None:
            if type(self.destination) is dict:
                obj_dict["destination"] = self.destination
            else:
                obj_dict["destination"] = self.destination.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")
        if self.destination is None:
            raise Exception("destination can not None")


class Filter(object):

    def __init__(self, prefix=None, tag=None, and_value=None):
        """
        :param prefix: 前缀匹配
        :param tag: 标签
        :param and_value: 多个标签或前缀时不会返
        """
        self.prefix = prefix
        self.tag = tag
        self.and_value = and_value

    def set_prefix(self, prefix):
        """
        :param prefix: 前缀匹配
        """
        self.prefix = prefix

    def set_tag(self, tag):
        """
        :param tag: 标签
        """
        self.tag = tag

    def set_and_value(self, and_value):
        """
        :param and_value: 多个标签或前缀时不会返
        """
        self.and_value = and_value

    def get_dic(self):
        obj_dict = dict()
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.tag is not None:
            if type(self.tag) is dict:
                obj_dict["tag"] = self.tag
            else:
                obj_dict["tag"] = self.tag.get_dic()
        if self.and_value is not None:
            if type(self.and_value) is dict:
                obj_dict["and"] = self.and_value
            else:
                obj_dict["and"] = self.and_value.get_dic()
        return obj_dict


class Tag(object):

    def __init__(self, key=None, value=None):
        """
        :param key: 标签key
        :param value: 标签值
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
        :param value: 标签值
        """
        self.value = value

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.value is not None:
            obj_dict["value"] = self.value
        return obj_dict


class AndModel(object):

    def __init__(self, prefix=None, tags=None):
        """
        :param prefix: 前缀匹配
        :param tags: 标签集合
        """
        self.prefix = prefix
        self.tags = tags

    def set_prefix(self, prefix):
        """
        :param prefix: 前缀匹配
        """
        self.prefix = prefix

    def set_tags(self, tags):
        """
        :param tags: 标签集合
        """
        self.tags = tags

    def get_dic(self):
        obj_dict = dict()
        if self.prefix is not None:
            obj_dict["prefix"] = self.prefix
        if self.tags is not None:
            tags_array = []
            for item in self.tags:
                if type(item) is dict:
                    tags_array.append(item)
                else:
                    tags_array.append(item.get_dic())
            obj_dict["tags"] = tags_array
        return obj_dict


class SourceSelectionCriteria(object):

    def __init__(self, sse_kms_encrypted_objects=None, replica_modifications=None):
        """
        :param sse_kms_encrypted_objects: 指定OSS是否复制通过SSE-KMS加密创建的对象
        :param replica_modifications: 复制修改规则
        """
        self.sse_kms_encrypted_objects = sse_kms_encrypted_objects
        self.replica_modifications = replica_modifications

    def set_sse_kms_encrypted_objects(self, sse_kms_encrypted_objects):
        """
        :param sse_kms_encrypted_objects: 指定OSS是否复制通过SSE-KMS加密创建的对象
        """
        self.sse_kms_encrypted_objects = sse_kms_encrypted_objects

    def set_replica_modifications(self, replica_modifications):
        """
        :param replica_modifications: 复制修改规则
        """
        self.replica_modifications = replica_modifications

    def get_dic(self):
        obj_dict = dict()
        if self.sse_kms_encrypted_objects is not None:
            if type(self.sse_kms_encrypted_objects) is dict:
                obj_dict["sseKmsEncryptedObjects"] = self.sse_kms_encrypted_objects
            else:
                obj_dict["sseKmsEncryptedObjects"] = self.sse_kms_encrypted_objects.get_dic()
        if self.replica_modifications is not None:
            if type(self.replica_modifications) is dict:
                obj_dict["replicaModifications"] = self.replica_modifications
            else:
                obj_dict["replicaModifications"] = self.replica_modifications.get_dic()
        return obj_dict


class SseKmsEncryptedObjects(object):

    def __init__(self, status=None):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def set_status(self, status):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict


class ReplicaModifications(object):

    def __init__(self, status=None):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def set_status(self, status):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict


class ExistingObjectReplication(object):

    def __init__(self, status=None):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def set_status(self, status):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled, Disabled
        """
        self.status = status

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict


class Destination(object):

    def __init__(self, bucket, account=None, storage_class=None, access_control_translation=None, encryption_configuration=None, replication_time=None, metrics=None, delete_marker_replication=None):
        """
        :param bucket: 目标桶
        :param account: 账号
        :param storage_class: 存储类型，枚举值：STANDARD，INTELLIGENT_TIERING，STANDARD_IA。默认值：原存储类型
        :param access_control_translation: 访问控制
        :param encryption_configuration: 加密配置
        :param replication_time: 复制时间
        :param metrics: 指标
        :param delete_marker_replication: 是否可以删除标记复制
        """
        self.bucket = bucket
        self.account = account
        self.storage_class = storage_class
        self.access_control_translation = access_control_translation
        self.encryption_configuration = encryption_configuration
        self.replication_time = replication_time
        self.metrics = metrics
        self.delete_marker_replication = delete_marker_replication
        self.check_param()

    def set_account(self, account):
        """
        :param account: 账号
        """
        self.account = account

    def set_storage_class(self, storage_class):
        """
        :param storage_class: 存储类型，枚举值：STANDARD，INTELLIGENT_TIERING，STANDARD_IA。默认值：原存储类型
        """
        self.storage_class = storage_class

    def set_access_control_translation(self, access_control_translation):
        """
        :param access_control_translation: 访问控制
        """
        self.access_control_translation = access_control_translation

    def set_encryption_configuration(self, encryption_configuration):
        """
        :param encryption_configuration: 加密配置
        """
        self.encryption_configuration = encryption_configuration

    def set_replication_time(self, replication_time):
        """
        :param replication_time: 复制时间
        """
        self.replication_time = replication_time

    def set_metrics(self, metrics):
        """
        :param metrics: 指标
        """
        self.metrics = metrics

    def set_delete_marker_replication(self, delete_marker_replication):
        """
        :param delete_marker_replication: 是否可以删除标记复制
        """
        self.delete_marker_replication = delete_marker_replication

    def get_dic(self):
        obj_dict = dict()
        if self.bucket is not None:
            obj_dict["bucket"] = self.bucket
        if self.account is not None:
            obj_dict["account"] = self.account
        if self.storage_class is not None:
            obj_dict["storageClass"] = self.storage_class
        if self.access_control_translation is not None:
            if type(self.access_control_translation) is dict:
                obj_dict["accessControlTranslation"] = self.access_control_translation
            else:
                obj_dict["accessControlTranslation"] = self.access_control_translation.get_dic()
        if self.encryption_configuration is not None:
            if type(self.encryption_configuration) is dict:
                obj_dict["encryptionConfiguration"] = self.encryption_configuration
            else:
                obj_dict["encryptionConfiguration"] = self.encryption_configuration.get_dic()
        if self.replication_time is not None:
            if type(self.replication_time) is dict:
                obj_dict["replicationTime"] = self.replication_time
            else:
                obj_dict["replicationTime"] = self.replication_time.get_dic()
        if self.metrics is not None:
            if type(self.metrics) is dict:
                obj_dict["metrics"] = self.metrics
            else:
                obj_dict["metrics"] = self.metrics.get_dic()
        if self.delete_marker_replication is not None:
            if type(self.delete_marker_replication) is dict:
                obj_dict["deleteMarkerReplication"] = self.delete_marker_replication
            else:
                obj_dict["deleteMarkerReplication"] = self.delete_marker_replication.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")


class AccessControlTranslation(object):

    def __init__(self, owner=None):
        """
        :param owner: 所有者
        """
        self.owner = owner

    def set_owner(self, owner):
        """
        :param owner: 所有者
        """
        self.owner = owner

    def get_dic(self):
        obj_dict = dict()
        if self.owner is not None:
            obj_dict["owner"] = self.owner
        return obj_dict


class EncryptionConfiguration(object):

    def __init__(self, replica_kms_key_id=None):
        """
        :param replica_kms_key_id: 复制KmsKeyID
        """
        self.replica_kms_key_id = replica_kms_key_id

    def set_replica_kms_key_id(self, replica_kms_key_id):
        """
        :param replica_kms_key_id: 复制KmsKeyID
        """
        self.replica_kms_key_id = replica_kms_key_id

    def get_dic(self):
        obj_dict = dict()
        if self.replica_kms_key_id is not None:
            obj_dict["replicaKmsKeyID"] = self.replica_kms_key_id
        return obj_dict


class ReplicationTime(object):

    def __init__(self, status=None, time=None):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled，Disabled
        :param time: 时间规则
        """
        self.status = status
        self.time = time

    def set_status(self, status):
        """
        :param status: 标识 Rule 是否生效，枚举值：Enabled，Disabled
        """
        self.status = status

    def set_time(self, time):
        """
        :param time: 时间规则
        """
        self.time = time

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        if self.time is not None:
            if type(self.time) is dict:
                obj_dict["time"] = self.time
            else:
                obj_dict["time"] = self.time.get_dic()
        return obj_dict


class Time(object):

    def __init__(self, minutes=None):
        """
        :param minutes: 分钟
        """
        self.minutes = minutes

    def set_minutes(self, minutes):
        """
        :param minutes: 分钟
        """
        self.minutes = minutes

    def get_dic(self):
        obj_dict = dict()
        if self.minutes is not None:
            obj_dict["minutes"] = self.minutes
        return obj_dict


class Metrics(object):

    def __init__(self, status=None, event_threshold=None):
        """
        :param status: Enabled | Disabled
        :param event_threshold: 阈值
        """
        self.status = status
        self.event_threshold = event_threshold

    def set_status(self, status):
        """
        :param status: Enabled | Disabled
        """
        self.status = status

    def set_event_threshold(self, event_threshold):
        """
        :param event_threshold: 阈值
        """
        self.event_threshold = event_threshold

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        if self.event_threshold is not None:
            if type(self.event_threshold) is dict:
                obj_dict["eventThreshold"] = self.event_threshold
            else:
                obj_dict["eventThreshold"] = self.event_threshold.get_dic()
        return obj_dict


class EventThreshold(object):

    def __init__(self, minutes=None):
        """
        :param minutes: 分钟
        """
        self.minutes = minutes

    def set_minutes(self, minutes):
        """
        :param minutes: 分钟
        """
        self.minutes = minutes

    def get_dic(self):
        obj_dict = dict()
        if self.minutes is not None:
            obj_dict["minutes"] = self.minutes
        return obj_dict


class DeleteMarkerReplication(object):

    def __init__(self, status=None):
        """
        :param status: Enabled | Disabled
        """
        self.status = status

    def set_status(self, status):
        """
        :param status: Enabled | Disabled
        """
        self.status = status

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        return obj_dict


class PutBucketReplicationRequestParam(object):

    def __init__(self, region_id, bucket, replication_configuration, ):
        """
        :param region_id: 资源池id
        :param bucket: 桶名称
        :param replication_configuration: 请求支付配置
        """
        self.region_id = region_id
        self.bucket = bucket
        self.replication_configuration = replication_configuration

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.replication_configuration is None:
            raise Exception("replication_configuration can not None")

