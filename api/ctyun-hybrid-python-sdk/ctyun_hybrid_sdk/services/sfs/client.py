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


class SfsClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('sfs-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(SfsClient, self).__init__(credential, config, 'sfs', '0.1.0', logger, signer)

    def total_storage(self, total_storage_request_param):
        """
        /v4/sfs/total-storage
        查询文件系统总容量
        """
        return self.send(total_storage_request_param)

    def list_user_sfs_vdc(self, list_user_sfs_vdc_request_param):
        """
        /v4/sfs/list-sfs-vdc
        可用区账户弹性文件列表查询-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
        """
        return self.send(list_user_sfs_vdc_request_param)

    def permission_group_new(self, permission_group_new_request_param):
        """
        /v4/sfs/permission-group/new
        弹性文件创建权限组
        """
        return self.send(permission_group_new_request_param)

    def sfs_refund_sfs(self, sfs_refund_sfs_request_param):
        """
        /v4/sfs/refund-sfs
        1. 弹性文件下已绑定挂载点/vpc会自动解绑   
    2. 删除前置：弹性文件的状态不是创建中（creating）状态
        """
        return self.send(sfs_refund_sfs_request_param)

    def sfs_free_size_sfs(self, sfs_free_size_sfs_request_param):
        """
        /v4/sfs/free-storage
        查询文件系统剩余容量
        """
        return self.send(sfs_free_size_sfs_request_param)

    def sfs_list_mountpoint(self, sfs_list_mountpoint_request_param):
        """
        /v4/sfs/list-mountpoint-sfs
        对齐公有云，v1文档未有该接口定义
        """
        return self.send(sfs_list_mountpoint_request_param)

    def sfs_delete_permission_sfs(self, sfs_delete_permission_sfs_request_param):
        """
        /v4/sfs/permission-group/delete-permission-group
        1. 不支持删除默认权限组   
    1. 权限组绑定了弹性文件时，不支持删除   
    3. 权限组下创建了权限组规则时，不支持删除
        """
        return self.send(sfs_delete_permission_sfs_request_param)

    def sfs_band_read(self, sfs_band_read_request_param):
        """
        /v4/sfs/band-read
        查询文件系统历史读带宽流量信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
        """
        return self.send(sfs_band_read_request_param)

    def get_file_cluster_detail(self, get_file_cluster_detail_request_param):
        """
        /v4/file-storage/info-cluster
        查询文件存储集群详情
        """
        return self.send(get_file_cluster_detail_request_param)

    def sfs_destroy(self, sfs_destroy_request_param):
        """
        /v4/sfs/destroy
        销毁缓冲区内（冻结状态）弹性文件
        """
        return self.send(sfs_destroy_request_param)

    def permission_rule_list(self, permission_rule_list_request_param):
        """
        /v4/sfs/permission-rule/list
        返回权限组规则描述信息
        """
        return self.send(permission_rule_list_request_param)

    def sfs_resize_sfs(self, sfs_resize_sfs_request_param):
        """
        /v4/sfs/resize-sfs
        注意：   
    1. 只能进行扩容操作，容量需要大于现有文件系统容量大小，最大为327680GB
        """
        return self.send(sfs_resize_sfs_request_param)

    def sfs_band_write(self, sfs_band_write_request_param):
        """
        /v4/sfs/band-write
        查询文件系统历史写带宽流量信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
        """
        return self.send(sfs_band_write_request_param)

    def sfs_used_size_sfs(self, sfs_used_size_sfs_request_param):
        """
        /v4/sfs/used-storage
        查询文件系统已使用容量
        """
        return self.send(sfs_used_size_sfs_request_param)

    def v4_sfs_region_storagetype(self, v4_sfs_region_storagetype_request_param):
        """
        /v4/sfs/region/storagetype
        用于展示弹性文件下列信息：   
    （1）所支持的协议类型   
    （2）所支持的弹性文件类型   
    （3）资源池下的az列表
        """
        return self.send(v4_sfs_region_storagetype_request_param)

    def history_storage(self, history_storage_request_param):
        """
        /v4/sfs/history-storage
        查询文件系统已使用容量历史信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
        """
        return self.send(history_storage_request_param)

    def modify_quota(self, modify_quota_request_param):
        """
        /v4/sfs/modify-quota
        quotaSize：配额设置如10MB 10GB形式，长度至少为3位，最后两位为单位；quotaSize不能设置为0（即：取消限制）
        """
        return self.send(modify_quota_request_param)

    def sfs_new_permission_sfs(self, sfs_new_permission_sfs_request_param):
        """
        /v4/sfs/permission-group/new-permission-group
        租户在某个资源池下的权限组个数上限目前为20个   
    
        """
        return self.send(sfs_new_permission_sfs_request_param)

    def list_file_clusters(self, list_file_clusters_request_param):
        """
        /v4/file-storage/list-cluster
        查询文件存储集群列表
        """
        return self.send(list_file_clusters_request_param)

    def sfs_iops_write(self, sfs_iops_write_request_param):
        """
        /v4/sfs/iops-write
        查询文件系统历史写IOPS信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
        """
        return self.send(sfs_iops_write_request_param)

    def permission_rule_new(self, permission_rule_new_request_param):
        """
        /v4/sfs/permission-rule/new
        1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 默认权限组不支持创建规则
        """
        return self.send(permission_rule_new_request_param)

    def sfs_used_rate_sfs(self, sfs_used_rate_sfs_request_param):
        """
        /v4/sfs/rate-storage
        查询文件系统使用率
        """
        return self.send(sfs_used_rate_sfs_request_param)

    def sfs_create_sfs(self, sfs_create_sfs_request_param):
        """
        /v4/sfs/info-sfs
        1、弹性文件状态（sfsStatus）部分字典值无法与公有云对齐，具体参考字段说明。   
    2、linux物理机共享路径（phySharePath），暂不与公有云对齐，底层不支持。
        """
        return self.send(sfs_create_sfs_request_param)

    def query_sfs_by_vpc_id(self, query_sfs_by_vpc_id_request_param):
        """
        /v4/sfs/list-sfs-by-vpcid
        查询vpc下的文件系统列表
        """
        return self.send(query_sfs_by_vpc_id_request_param)

    def get_file_cluster_node_detail(self, get_file_cluster_node_detail_request_param):
        """
        /v4/file-storage/info-node
        查询文件存储集群存储节点详情
        """
        return self.send(get_file_cluster_node_detail_request_param)

    def sfs_zone_listsfs(self, sfs_zone_listsfs_request_param):
        """
        /v4/sfs/zonelist
        注意：目前底层只有performance和capacity类型，fileSystemType传入hdd_e，列表返回为空。
        """
        return self.send(sfs_zone_listsfs_request_param)

    def sfs_open_list_sfs(self, sfs_open_list_sfs_request_param):
        """
        /v4/sfs/opend-list-sfs
        查询租户已开通文件系统列表
        """
        return self.send(sfs_open_list_sfs_request_param)

    def query_prices(self, query_prices_request_param):
        """
        /v4/sfs/upgrade-order/query-prices
        通过资源池ID和续订文件系统相关参数、查询文件系统续订订单价格
        """
        return self.send(query_prices_request_param)

    def permission_group_delete(self, permission_group_delete_request_param):
        """
        /v4/sfs/permission-group/delete
        弹性文件删除权限组
        """
        return self.send(permission_group_delete_request_param)

    def rename_s_f_s(self, rename_s_f_s_request_param):
        """
        /v4/sfs/rename-sfs
        文件系统重命名
        """
        return self.send(rename_s_f_s_request_param)

    def sfs_new_snapshot_sfs(self, sfs_new_snapshot_sfs_request_param):
        """
        /v4/sfs/snapshot/new
        弹性文件创建快照
        """
        return self.send(sfs_new_snapshot_sfs_request_param)

    def v4_sfs_restore(self, v4_sfs_restore_request_param):
        """
        /v4/sfs/restore
        恢复文件系统
        """
        return self.send(v4_sfs_restore_request_param)

    def sfs_unbind_vpc_sfs(self, sfs_unbind_vpc_sfs_request_param):
        """
        /v4/sfs/vpc-unbind-permission
        文件系统VPC解绑权限组
        """
        return self.send(sfs_unbind_vpc_sfs_request_param)

    def sfs_list_vpc_sfs(self, sfs_list_vpc_sfs_request_param):
        """
        /v4/sfs/list-vpc-permission
        vpcFuID（vpc fuid）、vpcCidr（vpc cidr）、permissionGroupIsDefault（是否为默认权限组）、permissionGroupDescription（权限组描述） 字段暂不支持
        """
        return self.send(sfs_list_vpc_sfs_request_param)

    def v4_sfs_permission_group_list(self, v4_sfs_permission_group_list_request_param):
        """
        /v4/sfs/permission-group/list
        弹性文件返回权限组描述信息
        """
        return self.send(v4_sfs_permission_group_list_request_param)

    def permission_rule_modify(self, permission_rule_modify_request_param):
        """
        /v4/sfs/permission-rule/modify
        1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 默认权限组不支持创建规则   
    * 入参：公有云没有permissionGroupID参数，兼容v1加入permissionGroupID入参，修改为非必填参数，传了permissionGroupID会对该参数校验；   
    * 返参 v1的returnObj是数组类型，公有云是object类型；   
    
        """
        return self.send(permission_rule_modify_request_param)

    def list_permission(self, list_permission_request_param):
        """
        /v4/sfs/list-permission
        查询文件系统权限组与VPC绑定关系
        """
        return self.send(list_permission_request_param)

    def sfs_bind_vpc_sfs(self, sfs_bind_vpc_sfs_request_param):
        """
        /v4/sfs/vpc-bind-permission
        文件系统VPC绑定权限组
        """
        return self.send(sfs_bind_vpc_sfs_request_param)

    def list_file_cluster_pools(self, list_file_cluster_pools_request_param):
        """
        /v4/file-storage/list-pool
        查询文件存储集群存储池列表
        """
        return self.send(list_file_cluster_pools_request_param)

    def sfs_renew_sfs(self, sfs_renew_sfs_request_param):
        """
        /v4/sfs/renew
        文件系统续订
        """
        return self.send(sfs_renew_sfs_request_param)

    def sfs_info(self, sfs_info_request_param):
        """
        /v4/sfs/info
        查询文件系统信息
        """
        return self.send(sfs_info_request_param)

    def sfs_unbind_permission(self, sfs_unbind_permission_request_param):
        """
        /v4/sfs/unbind-permission
        文件系统的VPC解绑权限组
        """
        return self.send(sfs_unbind_permission_request_param)

    def sfs_delete_snapshot_sfs(self, sfs_delete_snapshot_sfs_request_param):
        """
        /v4/sfs/snapshot/delete
        弹性文件删除快照
        """
        return self.send(sfs_delete_snapshot_sfs_request_param)

    def get_file_cluster_pool_detail(self, get_file_cluster_pool_detail_request_param):
        """
        /v4/file-storage/info-pool
        查询文件存储集群存储池详情
        """
        return self.send(get_file_cluster_pool_detail_request_param)

    def sfs_modify_permission_sfs(self, sfs_modify_permission_sfs_request_param):
        """
        /v4/sfs/permission-group/modify-permission-group
        不支持修改默认权限组
        """
        return self.send(sfs_modify_permission_sfs_request_param)

    def delete_mountpoint_sfs(self, delete_mountpoint_sfs_request_param):
        """
        /v4/sfs/delete-mountpoint-sfs
        注意：sfsUID是文件系统id   
    该接口只支持3.0资源池
        """
        return self.send(delete_mountpoint_sfs_request_param)

    def sfs_list_permission_rule_sfs(self, sfs_list_permission_rule_sfs_request_param):
        """
        /v4/sfs/permission-rule/list-permission-rule
        注意：   
    1. permissionGroupFuid和permissionRuleFuid至少存在一个   
    2. pageNo默认为1，pageSize默认为10，取值[1, 100]，超过上限时默认取上限值   
    3. 当前接口使用前请使用资源池概况信息查询接口查询对应的资源池信息，如资源池信息"regionVersion": "v4.0",即可使用；如资源池信息"regionVersion": "v3.0", 则不可使用。
        """
        return self.send(sfs_list_permission_rule_sfs_request_param)

    def sfs_modify_permission_rule_sfs(self, sfs_modify_permission_rule_sfs_request_param):
        """
        /v4/sfs/permission-rule/modify-permission-rule
        1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 该接口仅支持资源池信息"regionVersion": "v4.0"
        """
        return self.send(sfs_modify_permission_rule_sfs_request_param)

    def sfs_info_by_name(self, sfs_info_by_name_request_param):
        """
        /v4/sfs/info-by-name
        1、弹性文件状态（sfsStatus）部分字典值无法与公有云对齐，具体参考字段说明。   
    2、linux物理机共享路径（phySharePath），暂不与公有云对齐，底层不支持。
        """
        return self.send(sfs_info_by_name_request_param)

    def sfs_new_permission_rule_sfs(self, sfs_new_permission_rule_sfs_request_param):
        """
        /v4/sfs/permission-rule/new-permission-rule
        1. 优先级不能重复   
    2. 授权地址不能重复   
    3. 支持ipv4，ipv6。同一权限组，创建权限组规则的时候下面的authAddr不能重复   
    4. 当前接口使用前请使用资源池概况信息查询接口查询对应的资源池信息，如资源池信息"regionVersion": "v4.0",即可使用；如资源池信息"regionVersion": "v3.0", 则不可使用。   
    5. V2云管侧userPermission暂只支持no_root_squash权限
        """
        return self.send(sfs_new_permission_rule_sfs_request_param)

    def sfs_rollback_snapshot_sfs(self, sfs_rollback_snapshot_sfs_request_param):
        """
        /v4/sfs/snapshot/rollback
        弹性文件回滚快照
        """
        return self.send(sfs_rollback_snapshot_sfs_request_param)

    def sfs_list_snapshot_sfs(self, sfs_list_snapshot_sfs_request_param):
        """
        /v4/sfs/snapshot/list
        弹性文件查询快照
        """
        return self.send(sfs_list_snapshot_sfs_request_param)

    def sfs_set_read_sfs(self, sfs_set_read_sfs_request_param):
        """
        /v4/sfs/ro
        设置文件系统只读；   
    3.0资源池底层不支持HPFS和CIFS的海量文件
        """
        return self.send(sfs_set_read_sfs_request_param)

    def sfs_set_read_write_sfs(self, sfs_set_read_write_sfs_request_param):
        """
        /v4/sfs/rw
        设置文件系统读写   
    3.0资源池底层不支持HPFS和CIFS的海量文件
        """
        return self.send(sfs_set_read_write_sfs_request_param)

    def sfs_iops_read(self, sfs_iops_read_request_param):
        """
        /v4/sfs/iops-read
        查询文件系统历史读IOPS信息，fuser_last_updated取得文件系统在云管的更新时间，UID兼容了云管ID和底层UUID
        """
        return self.send(sfs_iops_read_request_param)

    def list_mountpoint(self, list_mountpoint_request_param):
        """
        /v4/sfs/list-mountpoint
        注意：resourceID是文件系统id   
    V2文件系统为绑定权限组，返回权限组相关参数暂时为空
        """
        return self.send(list_mountpoint_request_param)

    def delete_mountpoint(self, delete_mountpoint_request_param):
        """
        /v4/sfs/delete-mountpoint
        注意：resourceID是文件系统id   
    该接口只支持3.0资源池   
    
        """
        return self.send(delete_mountpoint_request_param)

    def sfs_new(self, sfs_new_request_param):
        """
        /v4/sfs/new
        支持创建按需计费/包年包月的弹性文件系统   
    1. 弹性文件类型枚举：capacity/performance/massive/hpfs_perf   
    2. 协议类型枚举：nfs/cifs/hpfs(3.0)   
    3. 包年包月：最大周期不能超过5年/60个月
        """
        return self.send(sfs_new_request_param)

    def modify_permission_group(self, modify_permission_group_request_param):
        """
        /v4/sfs/permission-group/modify
        弹性文件修改权限组
        """
        return self.send(modify_permission_group_request_param)

    def list_file_cluster_nodes(self, list_file_cluster_nodes_request_param):
        """
        /v4/file-storage/list-node
        查询文件存储集群存储节点列表
        """
        return self.send(list_file_cluster_nodes_request_param)

    def sfs_create_query_prices(self, sfs_create_query_prices_request_param):
        """
        /v4/sfs/new-order/query-prices
        未与公有云对齐：   
    公有云使用volumeType确定弹性文件类型进行询价；【该字段目前不起作用，请使用sfsType和sfsProtocol】   
    V2通过sfsType[文件系统类型]和sfsProtocol[协议类型]确定一个销售品后进行询价；
        """
        return self.send(sfs_create_query_prices_request_param)

    def v4_sfs_refund(self, v4_sfs_refund_request_param):
        """
        /v4/sfs/refund
        1. 弹性文件下已绑定挂载点/vpc会自动解绑   
    2. 删除前置：弹性文件的状态不是创建中（creating）状态
        """
        return self.send(v4_sfs_refund_request_param)

    def sfs_change_vpc_sfs(self, sfs_change_vpc_sfs_request_param):
        """
        /v4/sfs/vpc-change-permission
        文件系统VPC换绑权限组
        """
        return self.send(sfs_change_vpc_sfs_request_param)

    def add_quota(self, add_quota_request_param):
        """
        /v4/sfs/add-quota
        quotaSize：配额设置如10MB 10GB形式，长度至少为3位，最后两位为单位；quotaSize不能设置为0（即：取消限制）；设置的所有quotaSize之和不能大于文件系统总容量
        """
        return self.send(add_quota_request_param)

    def del_quota(self, del_quota_request_param):
        """
        /v4/sfs/del-quota
        删除文件系统目录配额
        """
        return self.send(del_quota_request_param)

    def permission_rule_delete(self, permission_rule_delete_request_param):
        """
        /v4/sfs/permission-rule/delete
        弹性文件删除已有权限组规则
        """
        return self.send(permission_rule_delete_request_param)

    def sfs_list_read_write_sfs(self, sfs_list_read_write_sfs_request_param):
        """
        /v4/sfs/list-rw
        查看文件系统只读/读写信息
        """
        return self.send(sfs_list_read_write_sfs_request_param)

    def add_mountpoint_sfs(self, add_mountpoint_sfs_request_param):
        """
        /v4/sfs/add-mountpoint-sfs
        该接口只支持3.0资源池
        """
        return self.send(add_mountpoint_sfs_request_param)

    def sfs_list_permission_sfs(self, sfs_list_permission_sfs_request_param):
        """
        /v4/sfs/permission-group/list-permission-group
        弹性文件 返回权限组描述信息（新军规）
        """
        return self.send(sfs_list_permission_sfs_request_param)

    def sfs_new_sfs(self, sfs_new_sfs_request_param):
        """
        /v4/sfs/new-sfs
        1、入参与公有云对齐，其中onDemand 默认值，暂不与公有云对齐。   
    2、响应对象中资源明细信息暂不与公有云对齐   
    3、底层不支持isEncrypt设置为true，kmsUUID在此值为true时传递了也没效果。
        """
        return self.send(sfs_new_sfs_request_param)

    def sfs_modify_snapshot_sfs(self, sfs_modify_snapshot_sfs_request_param):
        """
        /v4/sfs/snapshot/modify
        弹性文件修改快照   
    
        """
        return self.send(sfs_modify_snapshot_sfs_request_param)

    def change_permission(self, change_permission_request_param):
        """
        /v4/sfs/change-permission
        v1 accessGroupId为int类型，v2为string类型
        """
        return self.send(change_permission_request_param)

    def sfs_resize(self, sfs_resize_request_param):
        """
        /v4/sfs/resize
        弹性文件修改规格   
       
    1. 弹性文件只支持扩容，不支持缩容   
    2. 最小需要大于原始大小，最大为327680GB
        """
        return self.send(sfs_resize_request_param)

    def sfs_bind_permission(self, sfs_bind_permission_request_param):
        """
        /v4/sfs/bind-permission
        文件系统VPC绑定权限组
        """
        return self.send(sfs_bind_permission_request_param)

    def sfs_info_by_name_sfs(self, sfs_info_by_name_sfs_request_param):
        """
        /v4/sfs/info-by-name-sfs
        1、弹性文件状态（sfsStatus）部分字典值无法与公有云对齐，具体参考字段说明。   
    2、linux物理机共享路径（phySharePath），暂不与公有云对齐，底层不支持。   
    
        """
        return self.send(sfs_info_by_name_sfs_request_param)

    def opend_list(self, opend_list_request_param):
        """
        /v4/sfs/opend-list
        v1入参为bodyjson  v2是param；    
    出参v1 mountCount和updateTime类型为string，公有云为int
        """
        return self.send(opend_list_request_param)

    def sfs_query_prices(self, sfs_query_prices_request_param):
        """
        /v4/sfs/renew-order/query-prices
        通过资源池ID和续订文件系统相关参数、查询文件系统续订订单价格   
    只支持onDemand为false的资源进行询价
        """
        return self.send(sfs_query_prices_request_param)

    def list_user_sfs(self, list_user_sfs_request_param):
        """
        /v4/sfs/list-sfs
        可用区账户弹性文件列表查询（新军规）
        """
        return self.send(list_user_sfs_request_param)

    def v4_sfs_list(self, v4_sfs_list_request_param):
        """
        /v4/sfs/list
        可用区账户弹性文件列表查询
        """
        return self.send(v4_sfs_list_request_param)
