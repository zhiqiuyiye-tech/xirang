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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class ZosClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('zos-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(ZosClient, self).__init__(credential, config, 'zos', '0.1.0', logger, signer)

    def put_bucket_tagging(self, put_bucket_tagging_request_param):
        """
        /v4/oss/put-bucket-tagging
        设置存储空间标签
        """
        return self.send(put_bucket_tagging_request_param)

    def put_object_tagging(self, put_object_tagging_request_param):
        """
        /v4/oss/put-object-tagging
        设置或更新对象（Object）的标签（Tagging）信息
        """
        return self.send(put_object_tagging_request_param)

    def get_bucket_location(self, get_bucket_location_request_param):
        """
        /v4/oss/get-bucket-location
        查询存储空间位置信息
        """
        return self.send(get_bucket_location_request_param)

    def list_object_versions(self, list_object_versions_request_param):
        """
        /v4/oss/list-object-versions
        开发未对齐原因：v1版本只实现了/v4/oss/list-objects接口对应了公有云的/v4/oss/list-object-versions接口功能，   
    v2版本和公有云对齐开发两个接口，该接口取消deleteMarkers字段接口和contents中isLatest、versionID字段，需要此信息请使用/v4/oss/list-object-versions接口
        """
        return self.send(list_object_versions_request_param)

    def get_bucket_acl(self, get_bucket_acl_request_param):
        """
        /v4/oss/get-bucket-acl
        注意：   
    返回参数grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）
        """
        return self.send(get_bucket_acl_request_param)

    def get_object_retention(self, get_object_retention_request_param):
        """
        /v4/oss/get-object-retention
        获取对象合规保留配置
        """
        return self.send(get_object_retention_request_param)

    def put_bucket_referer(self, put_bucket_referer_request_param):
        """
        /v4/oss/put-bucket-referer
        防盗链设置
        """
        return self.send(put_bucket_referer_request_param)

    def delete_bucket(self, delete_bucket_request_param):
        """
        /v4/oss/delete-bucket
        删除桶
        """
        return self.send(delete_bucket_request_param)

    def get_bucket_versioning(self, get_bucket_versioning_request_param):
        """
        /v4/oss/get-bucket-versioning
        查询存储空间版本控制配置
        """
        return self.send(get_bucket_versioning_request_param)

    def put_bucket_replication(self, put_bucket_replication_request_param):
        """
        /v4/oss/put-bucket-replication
        开发未对齐原因：混合云与公有云入参差异较大   
    该接口底层不支持，公有云实现为跨域复制
        """
        return self.send(put_bucket_replication_request_param)

    def get_bucket_referer(self, get_bucket_referer_request_param):
        """
        /v4/oss/get-bucket-referer
        查询防盗链配置
        """
        return self.send(get_bucket_referer_request_param)

    def list_parts(self, list_parts_request_param):
        """
        /v4/oss/list-parts
        查询特定分段上传中的已上传的分段的信息
        """
        return self.send(list_parts_request_param)

    def get_bucket_usage(self, get_bucket_usage_request_param):
        """
        /v4/oss/get-bucket-usage
        查询oss桶使用量
        """
        return self.send(get_bucket_usage_request_param)

    def delete_directory(self, delete_directory_request_param):
        """
        /v4/oss/delete-directory
        删除文件夹
        """
        return self.send(delete_directory_request_param)

    def get_bucket_lifecycle_conf(self, get_bucket_lifecycle_conf_request_param):
        """
        /v4/oss/get-bucket-lifecycle-conf
        生命周期查询
        """
        return self.send(get_bucket_lifecycle_conf_request_param)

    def put_object_acl(self, put_object_acl_request_param):
        """
        /v4/oss/put-object-acl
        注意：   
    ACL枚举值中aws-exec-read, bucket-owner-read, bucket-owner-full-control为兼容混合云v1字段。与底层确认，暂不支持aws-exec-read   
    grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）
        """
        return self.send(put_object_acl_request_param)

    def put_bucket_versioning(self, put_bucket_versioning_request_param):
        """
        /v4/oss/put-bucket-versioning
        开启合规保留的桶无法关闭桶版本控制
        """
        return self.send(put_bucket_versioning_request_param)

    def complete_multipart_upload(self, complete_multipart_upload_request_param):
        """
        /v4/oss/complete-multipart-upload
        接口通过合并之前的上传片段来完成一次分片上传过程。    
       
    用户首先初始化分片上传过程，然后通过Upload Part接口上传所有分片。在成功将一次分片上传过程的所有相关片段上传之后，调用这个接口来结束分片上传过程。当收到这个请求的时候，OOS会以分片号升序排列的方式将所有片段依次拼接来创建一个新的对象。在这个Complete Multipart Upload请求中，用户需要提供一个片段列表。同时，必须确保这个片段列表中的所有片段必须是已经上传完成的，Complete Multipart Upload操作会将片段列表中提供的片段拼接起来。对片段列表中的每个片段，需要提供该片段上传完成时返回的ETag头的值和对应的分片号。   
       
     OOS提供了不合并片段也可以读取Object内容的功能。在没有调用Complete Multipart Upload接口合并片段时，也可以通过调用Get Object接口来获取文件内容，OOS会根据最近一次创建的uploadId，以分片号升序的方式顺序读取片段内容，返回给客户端。
        """
        return self.send(complete_multipart_upload_request_param)

    def put_object_retention(self, put_object_retention_request_param):
        """
        /v4/oss/put-object-retention
        设置对象合规保留配置
        """
        return self.send(put_object_retention_request_param)

    def get_object_cluster_detail(self, get_object_cluster_detail_request_param):
        """
        /v4/object-storage/info-cluster
        查询对象存储集群详情
        """
        return self.send(get_object_cluster_detail_request_param)

    def get_bucket_logging(self, get_bucket_logging_request_param):
        """
        /v4/oss/get-bucket-logging
        注意：   
    返回参数中grantee中ID（被授权者）为对象存储用户的ID（非云管用户ID）
        """
        return self.send(get_bucket_logging_request_param)

    def list_object_clusters(self, list_object_clusters_request_param):
        """
        /v4/object-storage/list-cluster
        查询对象存储集群列表
        """
        return self.send(list_object_clusters_request_param)

    def list_object_cluster_nodes(self, list_object_cluster_nodes_request_param):
        """
        /v4/object-storage/list-node
        查询对象存储集群节点列表
        """
        return self.send(list_object_cluster_nodes_request_param)

    def get_bucket_usage_chart(self, get_bucket_usage_chart_request_param):
        """
        /v4/oss/get-bucket-usage-chart
        查询oss桶流量和请求次数
        """
        return self.send(get_bucket_usage_chart_request_param)

    def get_object_info_hybrid(self, get_object_info_hybrid_request_param):
        """
        /v4/oss/get-object-info
        1. 文件key为文件前缀+文件名称；   
    2. versionID可为空，未开启版本控制该字段为空（请求时也可使用null或者不传）   
    3. key和versionID确定唯一一个版本文件，当key不正确或者versionID不正确时，会返回not found错误信息   
    4. 返回参数中grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）
        """
        return self.send(get_object_info_hybrid_request_param)

    def put_object_storage_type(self, put_object_storage_type_request_param):
        """
        /v4/oss/put-object-storage-type
        3.0不支持其他存储方式（低频、归档）
        """
        return self.send(put_object_storage_type_request_param)

    def unfreeze_object(self, unfreeze_object_request_param):
        """
        /v4/oss/unfreeze-object
        只有归档对象才可解冻
        """
        return self.send(unfreeze_object_request_param)

    def get_bucket_cors(self, get_bucket_cors_request_param):
        """
        /v4/oss/get-bucket-cors
        跨域资源共享查询
        """
        return self.send(get_bucket_cors_request_param)

    def get_bucket_replication_region(self, get_bucket_replication_region_request_param):
        """
        /v4/oss/get-bucket-replication-region
        底层sdk未有对应的函数查询可复制的Bucket所在地域，该接口暂不支持
        """
        return self.send(get_bucket_replication_region_request_param)

    def multipart_upload_hybrid(self, multipart_upload_hybrid_request_param):
        """
        /v4/oss/action-multipart-upload
        该接口用于实现分片上传操作中片段的上传。   
       
    在上传任何一个分片之前，必须执行Initial Multipart Upload操作来初始化分片上传操作，初始化成功后，OOS会返回一个上传ID，这是一个唯一的标识，用户必须在调用Upload Part接口时加入该ID。   
       
    分片号PartNumber可以唯一标识一个片段并且定义该分片在对象中的位置，范围从1到10000。如果用户用之前上传过的片段的分片号来上传新的分片，之前的分片将会被覆盖。   
       
    除了最后一个分片外，所有分片的都不小于5M，最后一个分片的大小不受限制。   
       
    为了确保数据不会由于网络传输而毁坏，需要在每个分片上传请求中指定Content-MD5头，OOS通过提供的Content-MD5值来检查数据的完整性，如果不匹配，则会返回一个错误信息。   
       
    与V1暂未对齐，V1中body使用string类型，V2使用文件流上传[form-data格式]
        """
        return self.send(multipart_upload_hybrid_request_param)

    def list_all_parts(self, list_all_parts_request_param):
        """
        /v4/oss/list-all-parts
        v2.1.4.x版本修改对象储存调用链后，该接口功能无法实现，暂不提供
        """
        return self.send(list_all_parts_request_param)

    def delete_bucket_cors(self, delete_bucket_cors_request_param):
        """
        /v4/oss/delete-bucket-cors
        跨域资源共享删除
        """
        return self.send(delete_bucket_cors_request_param)

    def delete_bucket_policy(self, delete_bucket_policy_request_param):
        """
        /v4/oss/delete-bucket-policy
        删除存储空间授权策略
        """
        return self.send(delete_bucket_policy_request_param)

    def get_object_lock_conf(self, get_object_lock_conf_request_param):
        """
        /v4/oss/get-object-lock-conf
        请求获取存储空间的对象锁定配置
        """
        return self.send(get_object_lock_conf_request_param)

    def abort_multipart_upload(self, abort_multipart_upload_request_param):
        """
        /v4/oss/abort-multipart-upload
        用于取消MultipartUpload事件并删除对应的Part数据
        """
        return self.send(abort_multipart_upload_request_param)

    def get_oss_service_status(self, get_oss_service_status_request_param):
        """
        /v4/oss/get-oss-service-status
        查询对象存储开通状态
        """
        return self.send(get_oss_service_status_request_param)

    def get_bucket_replication(self, get_bucket_replication_request_param):
        """
        /v4/oss/get-bucket-replication
        查询存储空间复制规则
        """
        return self.send(get_bucket_replication_request_param)

    def new_oss(self, new_oss_request_param):
        """
        /v4/oss/new
        对象存储服务开通（工单）
        """
        return self.send(new_oss_request_param)

    def head_bucket(self, head_bucket_request_param):
        """
        /v4/oss/head-bucket
        查询存储空间是否有权访问或是否存在
        """
        return self.send(head_bucket_request_param)

    def get_endpoint(self, get_endpoint_request_param):
        """
        /v4/oss/get-endpoint
        访问控制【endpoint】查询
        """
        return self.send(get_endpoint_request_param)

    def delete_bucket_replication(self, delete_bucket_replication_request_param):
        """
        /v4/oss/delete-bucket-replication
        删除Bucket的复制配置
        """
        return self.send(delete_bucket_replication_request_param)

    def put_bucket_quota(self, put_bucket_quota_request_param):
        """
        /v4/oss/put-bucket-quota
        对桶配额进行修改。
        """
        return self.send(put_bucket_quota_request_param)

    def list_object_cluster_pools(self, list_object_cluster_pools_request_param):
        """
        /v4/object-storage/list-pool
        查询对象存储集群存储池列表
        """
        return self.send(list_object_cluster_pools_request_param)

    def create_directory(self, create_directory_request_param):
        """
        /v4/oss/create-directory
        创建文件夹
        """
        return self.send(create_directory_request_param)

    def get_bucket_request_payment(self, get_bucket_request_payment_request_param):
        """
        /v4/oss/get-bucket-request-payment
        查询存储空间请求支付配置
        """
        return self.send(get_bucket_request_payment_request_param)

    def create_multipart_upload(self, create_multipart_upload_request_param):
        """
        /v4/oss/create-multipart-upload
        实现初始化分片上传，成功执行此请求以后会返回 Upload ID 用于后续的分块上传
        """
        return self.send(create_multipart_upload_request_param)

    def delete_objects(self, delete_objects_request_param):
        """
        /v4/oss/delete-objects
        versionID不带版本的传"null"，带版本的传版本id才会真正的删除掉
        """
        return self.send(delete_objects_request_param)

    def put_bucket_request_payment(self, put_bucket_request_payment_request_param):
        """
        /v4/oss/put-bucket-request-payment
        设置存储空间请求支付配置
        """
        return self.send(put_bucket_request_payment_request_param)

    def put_bucket_cors(self, put_bucket_cors_request_param):
        """
        /v4/oss/put-bucket-cors
        跨域资源共享更新
        """
        return self.send(put_bucket_cors_request_param)

    def get_object_cluster_pool_detail(self, get_object_cluster_pool_detail_request_param):
        """
        /v4/object-storage/info-pool
        查询对象存储集群存储池详情
        """
        return self.send(get_object_cluster_pool_detail_request_param)

    def delete_bucket_encryption(self, delete_bucket_encryption_request_param):
        """
        /v4/oss/delete-bucket-encryption
        删除存储空间默认加密配置
        """
        return self.send(delete_bucket_encryption_request_param)

    def delete_object(self, delete_object_request_param):
        """
        /v4/oss/delete-object
        versionID不带版本的传"null"，带版本的传版本id才会真正的删除掉
        """
        return self.send(delete_object_request_param)

    def delete_bucket_acl_hybrid(self, delete_bucket_acl_hybrid_request_param):
        """
        /v4/oss/delete-bucket-acl
        桶acl策略删除
        """
        return self.send(delete_bucket_acl_hybrid_request_param)

    def get_fragment_num(self, get_fragment_num_request_param):
        """
        /v4/oss/get-fragment-num
        查询对象桶碎片数量
        """
        return self.send(get_fragment_num_request_param)

    def put_bucket_policy(self, put_bucket_policy_request_param):
        """
        /v4/oss/put-bucket-policy
        设置存储空间授权策略
        """
        return self.send(put_bucket_policy_request_param)

    def create_bucket_acl_hybrid(self, create_bucket_acl_hybrid_request_param):
        """
        /v4/oss/create-bucket-acl
        桶acl策略创建
        """
        return self.send(create_bucket_acl_hybrid_request_param)

    def get_keys(self, get_keys_request_param):
        """
        /v4/oss/get-keys
        查询 ACCESS_KEY 以及 SECRECT_KEY
        """
        return self.send(get_keys_request_param)

    def list_multipart_uploads(self, list_multipart_uploads_request_param):
        """
        /v4/oss/list-multipart-uploads
        查询正在进行中的分段上传
        """
        return self.send(list_multipart_uploads_request_param)

    def get_bucket_count(self, get_bucket_count_request_param):
        """
        /v4/oss/get-bucket-count
        查询oss桶总数
        """
        return self.send(get_bucket_count_request_param)

    def create_bucket(self, create_bucket_request_param):
        """
        /v4/oss/create-bucket
        创建对象存储桶   
    1. 桶名称（长度3~63;只能有大小写字母、数字、.、-;禁止两个英文句号（.）或英文句号（.）和中划线（-）相邻;禁止以英文句号（.）和中划线（-）开头或结尾;禁止使用IP地址）；桶名称不可重复   
    2. ACL桶权限枚举值：（'private', 'public-read', 'public-read-write', 'authenticated-read'）   
    3. 存储类型，目前支持STANDARD、STANDARD_IA和GLACIER，默认STANDARD   
    4. AZ策略:可选值为single-az，multi-az，默认为single-az
        """
        return self.send(create_bucket_request_param)

    def put_object_num(self, put_object_num_request_param):
        """
        /v4/oss/get-object-num
        查询对象桶对象数量（不含碎片）
        """
        return self.send(put_object_num_request_param)

    def head_object(self, head_object_request_param):
        """
        /v4/oss/head-object
        查询对象是否存在
        """
        return self.send(head_object_request_param)

    def update_bucket_acl_hybrid(self, update_bucket_acl_hybrid_request_param):
        """
        /v4/oss/update-bucket-acl
        桶acl策略修改
        """
        return self.send(update_bucket_acl_hybrid_request_param)

    def get_bucket_statistics(self, get_bucket_statistics_request_param):
        """
        /v4/oss/get-bucket-statistics
        查询桶统计信息
        """
        return self.send(get_bucket_statistics_request_param)

    def list_open_api_oss_user(self, list_open_api_oss_user_request_param):
        """
        /v4/oss/list-user
        查询oss用户列表
        """
        return self.send(list_open_api_oss_user_request_param)

    def delete_bucket_logging(self, delete_bucket_logging_request_param):
        """
        /v4/oss/delete-bucket-logging
        删除日志转存
        """
        return self.send(delete_bucket_logging_request_param)

    def get_object_cluster_node_detail(self, get_object_cluster_node_detail_request_param):
        """
        /v4/object-storage/info-node
        查询对象存储集群节点详情
        """
        return self.send(get_object_cluster_node_detail_request_param)

    def put_bucket_logging(self, put_bucket_logging_request_param):
        """
        /v4/oss/put-bucket-logging
        注意：   
    1. grantee中ID（被授权者）为对象存储用户的ID（非云管用户ID）   
    2. grantee中type枚举为CanonicalUser、AmazonCustomerByEmail；当type=CanonicalUser时，ID不得为空；当type=AmazonCustomerByEmail时，emailAddress不得为空；
        """
        return self.send(put_bucket_logging_request_param)

    def query_new_order_price(self, query_new_order_price_request_param):
        """
        /v4/oss/new-order/query-price
        ZOS资源包询价
        """
        return self.send(query_new_order_price_request_param)

    def put_bucket_encryption(self, put_bucket_encryption_request_param):
        """
        /v4/oss/put-bucket-encryption
        设置存储空间默认加密配置
        """
        return self.send(put_bucket_encryption_request_param)

    def get_object_acl(self, get_object_acl_request_param):
        """
        /v4/oss/get-object-acl
        注意：   
    返回参数grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）
        """
        return self.send(get_object_acl_request_param)

    def put_object_header(self, put_object_header_request_param):
        """
        /v4/oss/put-object-header
        与公有云对齐，未与v1对齐：v1包含参数versionID，但实现逻辑为通过copy对象为新的对象修改header,无法对历史版本对象修改http头
        """
        return self.send(put_object_header_request_param)

    def delete_bucket_tagging(self, delete_bucket_tagging_request_param):
        """
        /v4/oss/delete-bucket-tagging
        删除存储空间标签
        """
        return self.send(delete_bucket_tagging_request_param)

    def put_object_lock_conf(self, put_object_lock_conf_request_param):
        """
        /v4/oss/put-object-lock-conf
        要测试该接口，在创建桶时，需要设置ObjectLockEnabledForBucket为true
        """
        return self.send(put_object_lock_conf_request_param)

    def delete_object_tagging(self, delete_object_tagging_request_param):
        """
        /v4/oss/delete-object-tagging
        多版本场景下versionID必传，不然无法删除标签
        """
        return self.send(delete_object_tagging_request_param)

    def get_oss_storage_config(self, get_oss_storage_config_request_param):
        """
        /v4/oss/storage-config
        冗余策略:   
    SINGLE-AZ: 单AZ存储   
    MULTI-AZ: 多AZ存储   
    存储类型:    
    取值范围：["STANDARD", "STANDARD_IA", "GLACIER"]   
    STANDARD: 标准存储   
    STANDARD_IA: 低频存储   
    GLACIER: 归档存储
        """
        return self.send(get_oss_storage_config_request_param)

    def put_bucket_acl(self, put_bucket_acl_request_param):
        """
        /v4/oss/put-bucket-acl
        注意：   
    1. grantee和owner中ID（被授权者）为对象存储用户的ID（非云管用户ID）   
    2. ACL、accessControlPolicy两种方式必填其一，但不可同时使用，每次只能给一种参数赋值
        """
        return self.send(put_bucket_acl_request_param)

    def delete_bucket_lifecycle_conf(self, delete_bucket_lifecycle_conf_request_param):
        """
        /v4/oss/delete-bucket-lifecycle-conf
        生命周期删除
        """
        return self.send(delete_bucket_lifecycle_conf_request_param)

    def put_bucket_lifecycle_conf(self, put_bucket_lifecycle_conf_request_param):
        """
        /v4/oss/put-bucket-lifecycle-conf
        1、规则启用时，expiration、noncurrentVersionExpiration、noncurrentVersionTransitions、transitions四个参数必传一项；   
    2、transitions字段 -- 公有云有该字段，混合云v1不支持=》混合云v2兼容   
    3、由于混合云v2控制台限制，expiration和transitions中选择days或date需要保持一致，要么都是days，要么都是date；   
    4、newerNoncurrentVersions、objectSizeGreaterThan和objectSizeLessThan，公有云未有该参数，兼容V1处理。此外注意：公有云文档、底层文档和aws官网文档都没有给出该值的范围限制。目前V2就只做了大于等于0的限制处理，不允许负数的情况。其余情况的错误信息由底层错误信息透传返回。
        """
        return self.send(put_bucket_lifecycle_conf_request_param)

    def get_bucket_info(self, get_bucket_info_request_param):
        """
        /v4/oss/get-bucket-info
        查询桶的基础信息和用量数据。
        """
        return self.send(get_bucket_info_request_param)

    def copy_object(self, copy_object_request_param):
        """
        /v4/oss/copy-object
        复制对象(拷贝文件到其它桶)
        """
        return self.send(copy_object_request_param)

    def get_bucket_policy(self, get_bucket_policy_request_param):
        """
        /v4/oss/get-bucket-policy
        查询存储空间授权策略
        """
        return self.send(get_bucket_policy_request_param)

    def generate_object_download_link(self, generate_object_download_link_request_param):
        """
        /v4/oss/generate-object-download-link
        生成对象临时下载链接
        """
        return self.send(generate_object_download_link_request_param)

    def put_object_hybrid(self, put_object_hybrid_request_param):
        """
        /v4/oss/put-object
        s3 sdk接口不支持append操作，append和appendPosition字段暂不生效   
    与V1暂未对齐，V1中body使用string类型，V2使用文件流上传[form-data格式]；V2 otherParams字段需要将object转为string，格式为：{"contentType": "utf-8"}
        """
        return self.send(put_object_hybrid_request_param)

    def get_bucket_tagging(self, get_bucket_tagging_request_param):
        """
        /v4/oss/get-bucket-tagging
        查询存储空间标签
        """
        return self.send(get_bucket_tagging_request_param)

    def copy_multipart_upload_hybrid(self, copy_multipart_upload_hybrid_request_param):
        """
        /v4/oss/copy-multipart-upload
        可以将已经存在的Object作为分段上传的片段，拷贝生成一个新的片段。UploadId为新对象的分片上传ID。在上传任何一个分片之前，必须执行create-multipart-upload操作来初始化分片上传操作，初始化成功后，OOS会返回一个上传ID，这是一个唯一的标识，用户必须在调用Copy Part接口时加入该ID。   
       
    开发未对齐原因：公有云没有该接口，按照py接口开发的
        """
        return self.send(copy_multipart_upload_hybrid_request_param)

    def list_objects(self, list_objects_request_param):
        """
        /v4/oss/list-objects
        开发未对齐原因：v1版本只实现了/v4/oss/list-objects接口对应了公有云的/v4/oss/list-object-versions接口功能，   
    v2版本和公有云对齐开发两个接口，该接口取消deleteMarkers字段接口和contents中isLatest、versionID字段，需要此信息请使用/v4/oss/list-object-versions接口
        """
        return self.send(list_objects_request_param)

    def generate_object_upload_link(self, generate_object_upload_link_request_param):
        """
        /v4/oss/generate-object-upload-link
        接口生成的上传链接为put类型接口，v2和v1生成链接不一致，返回的fields为无意义参数可忽略；   
    入参与公有云对齐，未与v1对齐，无versionID入参   
    通过生成链接上传的文件，查询会有延迟，需等待云管将数据从底层同步后才能在云管查询到
        """
        return self.send(generate_object_upload_link_request_param)

    def get_bucket_website(self, get_bucket_website_request_param):
        """
        /v4/oss/get-bucket-website
        查询存储空间静态网站配置信息
        """
        return self.send(get_bucket_website_request_param)

    def list_buckets(self, list_buckets_request_param):
        """
        /v4/oss/list-buckets
        查询所有桶
        """
        return self.send(list_buckets_request_param)

    def query_bucket_acl_hybrid(self, query_bucket_acl_hybrid_request_param):
        """
        /v4/oss/query-bucket-acl
        桶acl策略查询
        """
        return self.send(query_bucket_acl_hybrid_request_param)

    def put_bucket_website(self, put_bucket_website_request_param):
        """
        /v4/oss/put-bucket-website
        若传入参数redirectAllRequestsTo，则indexDocument, errorDocument, routingRules不生效。
        """
        return self.send(put_bucket_website_request_param)

    def get_bucket_encryption(self, get_bucket_encryption_request_param):
        """
        /v4/oss/get-bucket-encryption
        查询存储空间默认加密配置
        """
        return self.send(get_bucket_encryption_request_param)

    def delete_bucket_website(self, delete_bucket_website_request_param):
        """
        /v4/oss/delete-bucket-website
        删除存储空间静态网站配置信息
        """
        return self.send(delete_bucket_website_request_param)

    def get_object_tagging(self, get_object_tagging_request_param):
        """
        /v4/oss/get-object-tagging
        查询对象（Object）标签
        """
        return self.send(get_object_tagging_request_param)
