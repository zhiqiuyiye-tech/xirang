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


class HpfsClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('hpfs-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(HpfsClient, self).__init__(credential, config, 'hpfs', '0.1.0', logger, signer)

    def list_sfs(self, list_sfs_request_param):
        """
        /v4/hpfs/list-sfs
        目前底层kmsUUID(加密盘密钥 UUID)、cephID(ceph底层的id)、projectID(资源所属企业项目 ID)，这些字段对不齐。   
    统一分页信息返回部分字段对应不上（和currentCount同级缺少pageSize和pageNo）。
        """
        return self.send(list_sfs_request_param)

    def list_hpfs_zone(self, list_hpfs_zone_request_param):
        """
        /v4/hpfs/list-zone
        查询并行文件指定地域支持的可用区
        """
        return self.send(list_hpfs_zone_request_param)

    def list_hpfs_region(self, list_hpfs_region_request_param):
        """
        /v4/hpfs/list-region
        查询并行文件支持的地域
        """
        return self.send(list_hpfs_region_request_param)

    def list_hpfs_by_sfstype(self, list_hpfs_by_sfstype_request_param):
        """
        /v4/hpfs/list-sfs-by-sfstype
        查询指定存储类型的并行文件列表
        """
        return self.send(list_hpfs_by_sfstype_request_param)

    def count_hpfs_quota(self, count_hpfs_quota_request_param):
        """
        /v4/hpfs/count-quota-sfs
        查询用户并行文件数量配额使用情况
        """
        return self.send(count_hpfs_quota_request_param)

    def list_hpfs_by_cluster(self, list_hpfs_by_cluster_request_param):
        """
        /v4/hpfs/list-sfs-by-cluster
        查询指定集群的并行文件列表
        """
        return self.send(list_hpfs_by_cluster_request_param)

    def resize_sfs(self, resize_sfs_request_param):
        """
        /v4/hpfs/resize-sfs
        1. 并行文件只支持扩容，不支持缩容   
    2. 修改并行文件大小为sfsSize后，所有并行文件总大小不超过用户配额   
       底层集群剩余可用空间大于sfsSize，sfsSize大小区间为[512GB, 1048576GB]，步长为512GB   
       例：sfsSize入参为514GB时，基于512GB的步长，调整为1024GB规格   
    3. 用户配额大小默认为50TB   
       
    资源id和并行文件id输入一个即可（必填一个）
        """
        return self.send(resize_sfs_request_param)

    def new_sfs(self, new_sfs_request_param):
        """
        /v4/hpfs/new-sfs
        1. 用户vpc/subnet资源可用   
    2. regionID资源池支持sfsType类型的并行文件（查询可用区及可用区所支持的文件系统类型：/v4/sfs/zonelist）   
    3. 底层集群剩余可用空间大于sfsSize，sfsSize大小区间为[512GB, 1048576GB]，步长为512GB   
        例：sfsSize入参为514GB时，基于512GB的步长，调整为1024GB规格   
    4. 用户配额大小默认为50TB   
    5. 目前只支持按需下单   
    6. 新开通的文件系统会自动绑定默认权限组   
       
    开通名称不能重复   
    私有协议(即sfsProtocol为hpfs)时 不校验vpc
        """
        return self.send(new_sfs_request_param)

    def refund_sfs(self, refund_sfs_request_param):
        """
        /v4/hpfs/refund-sfs
        资源id和并行文件id输入一个即可（必填一个）   
    并行文件系统已绑定VPC时，无法退订；
        """
        return self.send(refund_sfs_request_param)

    def info_sfs(self, info_sfs_request_param):
        """
        /v4/hpfs/info-sfs
        目前底层kmsUUID(加密盘密钥 UUID)、cephID(ceph底层的id)、projectID(资源所属企业项目 ID)，这些字段对不齐。   
    sfsUID和resourceId必填一项，都存在时sfsUID生效
        """
        return self.send(info_sfs_request_param)

    def rename_hpfs(self, rename_hpfs_request_param):
        """
        /v4/hpfs/rename-sfs
        并行文件重命名
        """
        return self.send(rename_hpfs_request_param)

    def query_cluster_list(self, query_cluster_list_request_param):
        """
        /v4/hpfs/list-cluster
        1. 返回字段remainingStatus（该集群是否可以售卖），V2暂不支持，暂时返回默认值false
        """
        return self.send(query_cluster_list_request_param)

    def info_by_name_sfs(self, info_by_name_sfs_request_param):
        """
        /v4/hpfs/info-by-name-sfs
        并行文件信息查询（基于sfsName+regionID)   
    目前底层kmsUUID(加密盘密钥 UUID)、cephID(ceph底层的id)、projectID(资源所属企业项目 ID)，这些字段对不齐。   
     
        """
        return self.send(info_by_name_sfs_request_param)

    def query_hpfs_cluster_by_device(self, query_hpfs_cluster_by_device_request_param):
        """
        /v4/hpfs/list-cluster-by-device
        1. 返回字段remainingStatus（该集群是否可以售卖），V2暂不支持，暂时返回默认值false
        """
        return self.send(query_hpfs_cluster_by_device_request_param)
