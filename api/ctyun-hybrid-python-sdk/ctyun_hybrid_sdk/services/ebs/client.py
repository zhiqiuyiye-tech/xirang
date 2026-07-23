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


class EbsClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ebs-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(EbsClient, self).__init__(credential, config, 'ebs', '0.1.0', logger, signer)

    def get_block_cluster_detail(self, get_block_cluster_detail_request_param):
        """
        /v4/block-storage/info-cluster
        查询块存储集群详情
        """
        return self.send(get_block_cluster_detail_request_param)

    def iaas_ebs_new_new(self, iaas_ebs_new_new_request_param):
        """
        /v4/ebs/new-ebs
        支持按需/包年包月创建云硬盘。   
    云硬盘名称：diskName和name[兼容v1]，不能同时为空，不能同时非空，只传一个；
        """
        return self.send(iaas_ebs_new_new_request_param)

    def list_block_cluster_pools(self, list_block_cluster_pools_request_param):
        """
        /v4/block-storage/list-pool
        查询块存储集群存储池列表
        """
        return self.send(list_block_cluster_pools_request_param)

    def modify_policy_ebs_snap(self, modify_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/modify-policy-ebs-snap
        修改云硬盘自动快照策略
        """
        return self.send(modify_policy_ebs_snap_request_param)

    def query_policy_ebs_snap(self, query_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/query-policy-ebs-snap
        查询云硬盘自动快照策略
        """
        return self.send(query_policy_ebs_snap_request_param)

    def volume_spec_assess(self, volume_spec_assess_request_param):
        """
        /v4/ebs/spec-assess
        对指定资源池可用区下的硬盘类型开通大小进行可行性校验（可批量校验）   
    入参为[regiongID,azID,volumeType]的总容量，[regiongID,azID,volumeType]不可重复   
    notAllowedInfo返回校验失败的数据   
    接口返回成功，notAllowedInfo为空则代表全部校验成功
        """
        return self.send(volume_spec_assess_request_param)

    def delete_ebs_snap(self, delete_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/delete-ebs-snap
        开发未对齐原因：混合云直接删除(非异步任务)，公有云走工单删除   
    **删除云硬盘快照**：该接口现在为同步接口，不返回jobid
        """
        return self.send(delete_ebs_snap_request_param)

    def update_ebs_snapshots_strategy_hybrid(self, update_ebs_snapshots_strategy_hybrid_request_param):
        """
        /v4/ebs/snapshots_strategy/update
        快照策略 修改。   
    **注意**：（开发未对齐）公有云无此接口，按照py接口开发
        """
        return self.send(update_ebs_snapshots_strategy_hybrid_request_param)

    def ebs_asyn_rep_stop(self, ebs_asyn_rep_stop_request_param):
        """
        /v4/async_rep/stop
        停止异步复制pair对复制，底层暂不支持
        """
        return self.send(ebs_asyn_rep_stop_request_param)

    def renew_ebs(self, renew_ebs_request_param):
        """
        /v4/ebs/renew-ebs
        云硬盘续订
        """
        return self.send(renew_ebs_request_param)

    def iaas_ebs_ebsrefund_new(self, iaas_ebs_ebsrefund_new_request_param):
        """
        /v4/ebs/refund-ebs
        支持退订一块包周期计费/按需的云硬盘。退订云硬盘后，将退还对应部分云硬盘费用。当云硬盘状态为“未挂载”时，才可以退订。
        """
        return self.send(iaas_ebs_ebsrefund_new_request_param)

    def ebs_info_by_name_ebs(self, ebs_info_by_name_ebs_request_param):
        """
        /v4/ebs/info-by-name-ebs
        基于资源池ID和云硬盘名称查询云硬盘详情。
        """
        return self.send(ebs_info_by_name_ebs_request_param)

    def ebs_new(self, ebs_new_request_param):
        """
        /v4/ebs/new
        支持按需/包年包月创建云硬盘。
        """
        return self.send(ebs_new_request_param)

    def get_ebs_spec_list(self, get_ebs_spec_list_request_param):
        """
        /v4/ebs/list-spec
        2.2.5版本支持
        """
        return self.send(get_ebs_spec_list_request_param)

    def ebs_list(self, ebs_list_request_param):
        """
        /v4/ebs/list
        云硬盘信息列表   
    1. 冗余返回results，兼容V1字段   
    2.2.6版本: 新增diskBus挂载协议字段返回。
        """
        return self.send(ebs_list_request_param)

    def iaas_ebs_attach_new(self, iaas_ebs_attach_new_request_param):
        """
        /v4/ebs/attach-ebs
        支持云硬盘挂载至某一云主机。   
    云主机下限制挂载云硬盘个数上限为20
        """
        return self.send(iaas_ebs_attach_new_request_param)

    def modify_policy_status_ebs_snap(self, modify_policy_status_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/modify-policy-status-ebs-snap
        启用或关闭云硬盘自动快照策略
        """
        return self.send(modify_policy_status_ebs_snap_request_param)

    def list_block_cluster_nodes(self, list_block_cluster_nodes_request_param):
        """
        /v4/block-storage/list-node
        查询块存储集群存储节点列表
        """
        return self.send(list_block_cluster_nodes_request_param)

    def create_ebs_snapshots_strategy_hybrid(self, create_ebs_snapshots_strategy_hybrid_request_param):
        """
        /v4/ebs/snapshots_strategy/create
        快照策略 创建。**注意**开发未对齐原因：公有云无此接口，按照py接口开发
        """
        return self.send(create_ebs_snapshots_strategy_hybrid_request_param)

    def batch_rollback_ebs_snap(self, batch_rollback_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/batch-rollback-ebs-snap
        批量快照回滚（批量重置云硬盘）
        """
        return self.send(batch_rollback_ebs_snap_request_param)

    def get_block_cluster_node_detail(self, get_block_cluster_node_detail_request_param):
        """
        /v4/block-storage/info-node
        查询块存储集群存储节点详情
        """
        return self.send(get_block_cluster_node_detail_request_param)

    def query_ebs_snap_list(self, query_ebs_snap_list_request_param):
        """
        /v4/ebs_snapshot/list-ebs-snap
        查询云硬盘快照列表
        """
        return self.send(query_ebs_snap_list_request_param)

    def new_from_snapshot_ebs_snap(self, new_from_snapshot_ebs_snap_request_param):
        """
        /v4/ebs/new-from-snapshot-ebs-snap
        从快照创建云硬盘
        """
        return self.send(new_from_snapshot_ebs_snap_request_param)

    def create_ebs_asyn_rep(self, create_ebs_asyn_rep_request_param):
        """
        /v4/async_rep/create
        底层暂不支持
        """
        return self.send(create_ebs_asyn_rep_request_param)

    def batch_refund_ebs(self, batch_refund_ebs_request_param):
        """
        /v4/ebs/batch-refund-ebs
        批量退订多个云硬盘，支持部分成功模式。每个云硬盘独立处理，互不影响。   
       
    **业务校验规则（按顺序）：**   
    1. 数量限制：最多10个（接口级错误）   
    2. RegionID一致性：所有云硬盘必须在同一RegionID（接口级错误）   
    3. 云硬盘不存在 → `Storage.Ebs.NotFound`   
    4. 状态非available → `Storage.Ebs.NotAvailableStatus`   
    5. 已在回收站(freezed=true) → `Storage.Ebs.AlreadyInRecycleBin`   
    6. 绑定快照/备份策略 → `Storage.Ebs.BindPolicy`   
    7. 包年包月已到期 → `Storage.Ebs.YearMonthExpired`   
    
        """
        return self.send(batch_refund_ebs_request_param)

    def ebs_attach(self, ebs_attach_request_param):
        """
        /v4/ebs/attach
        支持云硬盘挂载至某一云主机。   
    注意：   
    1. V1版本regionID是必传项，公有云官网regionID为选填项，V2对齐公有云；规则为：regionID可不传，如果传了regionID，该字段会被校验；   
    2. 云主机下限制挂载云硬盘个数上限为20
        """
        return self.send(ebs_attach_request_param)

    def ebs_asyn_rep_fault_conversion(self, ebs_asyn_rep_fault_conversion_request_param):
        """
        /v4/async_rep/fault_conversion
        异步复制pair对故障切换，底层暂不支持
        """
        return self.send(ebs_asyn_rep_fault_conversion_request_param)

    def ebs_asyn_rep_query(self, ebs_asyn_rep_query_request_param):
        """
        /v4/async_rep/query
        查询异步复制pair对，底层暂不支持
        """
        return self.send(ebs_asyn_rep_query_request_param)

    def query_ebs_snap_size(self, query_ebs_snap_size_request_param):
        """
        /v4/ebs_snapshot/query_size
        参数请求方式说明：该GET请求参数通过body传输   
    
        """
        return self.send(query_ebs_snap_size_request_param)

    def query_ebs_by_id(self, query_ebs_by_id_request_param):
        """
        /v4/ebs/info-ebs
        基于磁盘ID查询云硬盘详情。   
    ** 注意**： 此接口原始接口支持GET body 请求模式 从1.14.28 版本 修改为支持GET Query模式并对老版本进行了兼容，公有云同步修改为GET Query模式。如您使用的版本低于1.14.28 请使用GET body 请求模式 进行请求   
    增加diskId兼容
        """
        return self.send(query_ebs_by_id_request_param)

    def cancel_policy_ebs_snap(self, cancel_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/cancel-policy-ebs-snap
        取消关联云硬盘自动快照策略 
        """
        return self.send(cancel_policy_ebs_snap_request_param)

    def ebs_asyn_rep_modify(self, ebs_asyn_rep_modify_request_param):
        """
        /v4/async_rep/modify
        修改异步复制pair对，底层暂不支持
        """
        return self.send(ebs_asyn_rep_modify_request_param)

    def list_block_clusters(self, list_block_clusters_request_param):
        """
        /v4/block-storage/list-cluster
        查询块存储集群列表
        """
        return self.send(list_block_clusters_request_param)

    def query_policy_ebs_snap_vdc(self, query_policy_ebs_snap_vdc_request_param):
        """
        /v4/ebs_snapshot/query-policy-ebs-snap-vdc
        查询云硬盘自动快照策略-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
        """
        return self.send(query_policy_ebs_snap_vdc_request_param)

    def get_block_cluster_pool_detail(self, get_block_cluster_pool_detail_request_param):
        """
        /v4/block-storage/info-pool
        查询块存储集群存储池详情
        """
        return self.send(get_block_cluster_pool_detail_request_param)

    def ebs_resize(self, ebs_resize_request_param):
        """
        /v4/ebs/resize
        云硬盘修改规格 (云硬盘升级-工单流程)
        """
        return self.send(ebs_resize_request_param)

    def apply_policy_ebs_snap(self, apply_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/apply-policy-ebs-snap
        关联云硬盘自动快照策略
        """
        return self.send(apply_policy_ebs_snap_request_param)

    def ebs_renew(self, ebs_renew_request_param):
        """
        /v4/ebs/renew
        云硬盘续订（旧）
        """
        return self.send(ebs_renew_request_param)

    def query_ebs_list(self, query_ebs_list_request_param):
        """
        /v4/ebs/list-ebs
        查询某可用区全部云硬盘详情。   
    2.2.6版本: 新增diskBus挂载协议字段返回。
        """
        return self.send(query_ebs_list_request_param)

    def ebs_list_vdc(self, ebs_list_vdc_request_param):
        """
        /v4/ebs/list-vdc
        云硬盘信息列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。   
    2.2.6版本: 新增diskBus挂载协议字段返回。
        """
        return self.send(ebs_list_vdc_request_param)

    def batch_renew_ebs(self, batch_renew_ebs_request_param):
        """
        /v4/ebs/batch-renew-ebs
        批量续订多个云硬盘，支持部分成功模式。每个云硬盘独立处理，互不影响。   
    三元组: ebs:ebs:BatchRenewEbs   
    **业务校验规则（按顺序）：**   
    1. 数量限制：最多10个.`Storage.Ebs.BatchRenewExceedLimit`   
    2. RegionID一致性：所有云硬盘必须在同一RegionID `Storage.Ebs.BatchRenewRegionNotMatch`   
    3. 云硬盘ID为空 → `Storage.Ebs.BatchRenewEmptySelection`   
    4. 状态不支持 → `Storage.Ebs.CreatingStatusNotSupportRenew`   
    
        """
        return self.send(batch_renew_ebs_request_param)

    def ebs_asyn_rep_reverse_rep(self, ebs_asyn_rep_reverse_rep_request_param):
        """
        /v4/async_rep/reverse_rep
        异步复制pair对反向复制，底层暂不支持
        """
        return self.send(ebs_asyn_rep_reverse_rep_request_param)

    def iaas_ebs_detach_new(self, iaas_ebs_detach_new_request_param):
        """
        /v4/ebs/detach-ebs
        支持将某一云硬盘从云主机卸载。   
       
    ### 接口约束   
    只有数据盘支持卸载操作，系统盘不支持卸载。
        """
        return self.send(iaas_ebs_detach_new_request_param)

    def rollback_ebs_snap(self, rollback_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/rollback-ebs-snap
        混合云v1 azName为非必填且不需要传传参；v2兼容公有云和v1，azName为非必填，当资源池为4.0且传了azName则对azName进行参数校验   
    接口约束：1.快照状态为可用且快照源云硬盘为可用（云硬盘处于未挂载状态或已挂载但云主机关机）； 2.只支持回滚至源云硬盘，不支持回滚至其他云硬盘
        """
        return self.send(rollback_ebs_snap_request_param)

    def delete_policy_ebs_snap(self, delete_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/delete-policy-ebs-snap
        删除云硬盘自动快照策略
        """
        return self.send(delete_policy_ebs_snap_request_param)

    def ebs_info_by_name(self, ebs_info_by_name_request_param):
        """
        /v4/ebs/info-by-name
        基于名字查询云硬盘详情
        """
        return self.send(ebs_info_by_name_request_param)

    def ebs_asyn_rep_activate(self, ebs_asyn_rep_activate_request_param):
        """
        /v4/async_rep/activate
        异步复制pair对激活，底层暂不支持
        """
        return self.send(ebs_asyn_rep_activate_request_param)

    def ebs_detach(self, ebs_detach_request_param):
        """
        /v4/ebs/detach
        云硬盘解绑
        """
        return self.send(ebs_detach_request_param)

    def query_size_ebs_snap(self, query_size_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/query_size-ebs-snap
        查询快照使用容量
        """
        return self.send(query_size_ebs_snap_request_param)

    def delete_ebs_snapshot(self, delete_ebs_snapshot_request_param):
        """
        /v4/ebs_snapshot/delete
        支持批量删除，仅支持批量删除同一个卷下的多个快照；   
    开发未对齐原因：混合云直接删除(非异步任务)，公有云走工单删除
        """
        return self.send(delete_ebs_snapshot_request_param)

    def delete_ebs_asyn_rep(self, delete_ebs_asyn_rep_request_param):
        """
        /v4/async_rep/delete
        底层暂不支持
        """
        return self.send(delete_ebs_asyn_rep_request_param)

    def delete_ebs_snapshots_strategy_hybrid(self, delete_ebs_snapshots_strategy_hybrid_request_param):
        """
        /v4/ebs/snapshots_strategy/delete
        快照策略 删除。开发未对齐原因：公有云无此接口，按照py接口开发
        """
        return self.send(delete_ebs_snapshots_strategy_hybrid_request_param)

    def resize_ebs(self, resize_ebs_request_param):
        """
        /v4/ebs/resize-ebs
        支持云硬盘变配。目前只支持增加磁盘容量。   
    支持云主机订购的系统盘及数据盘扩容。
        """
        return self.send(resize_ebs_request_param)

    def iaas_ebs_info(self, iaas_ebs_info_request_param):
        """
        /v4/ebs/info
        基于资源ID查询云硬盘
        """
        return self.send(iaas_ebs_info_request_param)

    def ebs_refund(self, ebs_refund_request_param):
        """
        /v4/ebs/refund
        退订云硬盘(工单流程)
        """
        return self.send(ebs_refund_request_param)

    def create_ebs_snapshot(self, create_ebs_snapshot_request_param):
        """
        /v4/ebs_snapshot/create
        开发未对齐原因：混合云直接创建，公有云走工单创建
        """
        return self.send(create_ebs_snapshot_request_param)

    def create_policy_ebs_snap(self, create_policy_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/create-policy-ebs-snap
        创建云硬盘自动快照策略
        """
        return self.send(create_policy_ebs_snap_request_param)

    def create_ebs_snap(self, create_ebs_snap_request_param):
        """
        /v4/ebs_snapshot/create-ebs-snap
        开发未对齐原因：混合云直接创建，公有云走工单创建
        """
        return self.send(create_ebs_snap_request_param)

    def ebs_update_attr(self, ebs_update_attr_request_param):
        """
        /v4/ebs/update-attr
        2.2.3及以上版本支持
        """
        return self.send(ebs_update_attr_request_param)

    def list_ecs_snap(self, list_ecs_snap_request_param):
        """
        /v4/ebs_snapshot/list
        参数请求方式说明：该GET请求参数通过body传输
        """
        return self.send(list_ecs_snap_request_param)

    def list_ecs_snap_vdc(self, list_ecs_snap_vdc_request_param):
        """
        /v4/ebs_snapshot/list-vdc
        查询快照列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
        """
        return self.send(list_ecs_snap_vdc_request_param)
