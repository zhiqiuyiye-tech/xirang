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


class CtClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ct-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtClient, self).__init__(credential, config, 'ct', '0.1.0', logger, signer)

    def v4_paas_ecs_update_flavor_spec(self, v4_paas_ecs_update_flavor_spec_request_param):
        """
        /v4/paas/ecs/update-flavor-spec
        云主机修改规格(工单)
        """
        return self.send(v4_paas_ecs_update_flavor_spec_request_param)

    def v4_paas_vpc_create_nat_gateway(self, v4_paas_vpc_create_nat_gateway_request_param):
        """
        /v4/paas/vpc/create-nat-gateway
        用于创建NAT网关：   
    本接口为同步接口，创建成功后同步返回natGatewayID。
        """
        return self.send(v4_paas_vpc_create_nat_gateway_request_param)

    def v4_paas_eip_delete(self, v4_paas_eip_delete_request_param):
        """
        /v4/paas/eip/delete
        本接口用于删除弹性IP：   
    本接口为同步接口，调用成功说明底层执行成功。   
    
        """
        return self.send(v4_paas_eip_delete_request_param)

    def paas_ecs_batch_create_lite_vm(self, paas_ecs_batch_create_lite_vm_request_param):
        """
        /v4/paas/ecs/batch-create-lite-vm
        多台开通时fixedIP不能进行指定，指定后开通一台后其余会报错。   
    instanceName在批量开通多台时会按照 001 ，顺序递增。
        """
        return self.send(paas_ecs_batch_create_lite_vm_request_param)

    def v4_paas_vpce_delete_endpoint(self, v4_paas_vpce_delete_endpoint_request_param):
        """
        /v4/paas/vpce/delete-endpoint
        本接口为同步接口，调用成功说明底层执行成功。
        """
        return self.send(v4_paas_vpce_delete_endpoint_request_param)

    def pass_delete_backup(self, pass_delete_backup_request_param):
        """
        /v4/paas/ebs-backup/delete
        开发未对齐原因：混合云返回删除信息，公有云不返回参数
        """
        return self.send(pass_delete_backup_request_param)

    def v4_paas_eip_modify_spec(self, v4_paas_eip_modify_spec_request_param):
        """
        /v4/paas/eip/modify-spec
        用于修改弹性公网 IP 带宽峰值：   
    本接口为同步接口，调用成功说明底层执行成功。   
    
        """
        return self.send(v4_paas_eip_modify_spec_request_param)

    def pass_delete_repo(self, pass_delete_repo_request_param):
        """
        /v4/paas/ebs-backup/repo/delete
        退订云硬盘备份存储库
        """
        return self.send(pass_delete_repo_request_param)

    def v4_paas_ebs_snapshot_create_ebs_snap(self, v4_paas_ebs_snapshot_create_ebs_snap_request_param):
        """
        /v4/paas/ebs_snapshot/create-ebs-snap
        本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。查询接口为/v4/job/info；保留策略暂不支持
        """
        return self.send(v4_paas_ebs_snapshot_create_ebs_snap_request_param)

    def paas_ebm_create_instance(self, paas_ebm_create_instance_request_param):
        """
        /v4/paas/ebm/delete
        批量删除物理机（工单）
        """
        return self.send(paas_ebm_create_instance_request_param)

    def v4_paas_elb_delete_loadbalancer(self, v4_paas_elb_delete_loadbalancer_request_param):
        """
        /v4/paas/elb/delete-loadbalancer
        本接口用于删除负载均衡实例：   
    本接口为同步接口，调用成功则说明底层执行成功。
        """
        return self.send(v4_paas_elb_delete_loadbalancer_request_param)

    def v4_paas_job_cancel(self, v4_paas_job_cancel_request_param):
        """
        /v4/paas/job/cancel
        撤销创建任务
        """
        return self.send(v4_paas_job_cancel_request_param)

    def v4_paas_elb_create_loadbalancer(self, v4_paas_elb_create_loadbalancer_request_param):
        """
        /v4/paas/elb/create-loadbalancer
        本接口用于创建负载均衡实例：   
    本接口为同步接口，调用成功后会同步返回底层创建的实例ID。   
    
        """
        return self.send(v4_paas_elb_create_loadbalancer_request_param)

    def v4_paas_ebs_new_ebs(self, v4_paas_ebs_new_ebs_request_param):
        """
        /v4/paas/ebs/new-ebs
        创建云硬盘(工单)
        """
        return self.send(v4_paas_ebs_new_ebs_request_param)

    def v4_paas_vpce_create_endpoint(self, v4_paas_vpce_create_endpoint_request_param):
        """
        /v4/paas/vpce/create-endpoint
        创建VPC终端节点PAAS
        """
        return self.send(v4_paas_vpce_create_endpoint_request_param)

    def v4_paas_ebs_snapshot_delete_ebs_snap(self, v4_paas_ebs_snapshot_delete_ebs_snap_request_param):
        """
        /v4/paas/ebs_snapshot/delete-ebs-snap
        1.本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。   
    2.该接口目前不支持多个删除 查询接口为/v4/job/info
        """
        return self.send(v4_paas_ebs_snapshot_delete_ebs_snap_request_param)

    def v4_paas_ebs_refund_ebs(self, v4_paas_ebs_refund_ebs_request_param):
        """
        /v4/paas/ebs/refund-ebs
        删除云硬盘(工单)
        """
        return self.send(v4_paas_ebs_refund_ebs_request_param)

    def pass_create_backup(self, pass_create_backup_request_param):
        """
        /v4/paas/ebs-backup/create-backup
        开发未对齐原因：混合云返回异步任务ID，公有云返回云硬盘备份对象
        """
        return self.send(pass_create_backup_request_param)

    def v4_paas_ecs_clone_instance(self, v4_paas_ecs_clone_instance_request_param):
        """
        /v4/paas/ecs/clone-instance
        克隆云主机(工单)
        """
        return self.send(v4_paas_ecs_clone_instance_request_param)

    def pass_renew_repo(self, pass_renew_repo_request_param):
        """
        /v4/paas/ebs-backup/repo/renew
        续订云硬盘备份存储库
        """
        return self.send(pass_renew_repo_request_param)

    def pass_create_repo(self, pass_create_repo_request_param):
        """
        /v4/paas/ebs-backup/repo/create
        创建云硬盘备份存储库   
    1.目前不支持autoRenewStatus（是否自动续订）字段   
    2.底层size属性不支持默认，需要必传
        """
        return self.send(pass_create_repo_request_param)

    def v4_paas_vpc_delete_nat_gateway(self, v4_paas_vpc_delete_nat_gateway_request_param):
        """
        /v4/paas/vpc/delete-nat-gateway
        本接口用于删除NAT网关：   
    本接口为同步接口，调用成功说明底层执行成功。
        """
        return self.send(v4_paas_vpc_delete_nat_gateway_request_param)

    def v4_paas_ecs_snapshot_create(self, v4_paas_ecs_snapshot_create_request_param):
        """
        /v4/paas/ecs/snapshot/create
        1.云主机快照目前不计费，快照信息创建的时候，不需要登记Paas订单，无需生成话单   
    2.本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。   
    3.查询接口为/v4/job/info
        """
        return self.send(v4_paas_ecs_snapshot_create_request_param)

    def v4_paas_ebs_resize_ebs(self, v4_paas_ebs_resize_ebs_request_param):
        """
        /v4/paas/ebs/resize-ebs
        变更云硬盘配置(工单)
        """
        return self.send(v4_paas_ebs_resize_ebs_request_param)

    def v4_paas_ecs_batch_delete(self, v4_paas_ecs_batch_delete_request_param):
        """
        /v4/paas/ecs/batch-delete
        1、 云主机下无快照、虚拟IP
        """
        return self.send(v4_paas_ecs_batch_delete_request_param)

    def paas_ebs_list_by_resource(self, paas_ebs_list_by_resource_request_param):
        """
        /v4/paas/ebs/list
        云硬盘信息列表_PAAS(可通过resourceID查询)
        """
        return self.send(paas_ebs_list_by_resource_request_param)

    def v4_paas_vpc_modify_nat_gateway_attribute(self, v4_paas_vpc_modify_nat_gateway_attribute_request_param):
        """
        /v4/paas/vpc/modify-nat-gateway-attribute
        变配接口只支持资源升级操作
        """
        return self.send(v4_paas_vpc_modify_nat_gateway_attribute_request_param)

    def paas_ebs_list(self, paas_ebs_list_request_param):
        """
        /v4/paas/ebs/list-ebs
        云硬盘信息列表_PAAS
        """
        return self.send(paas_ebs_list_request_param)

    def v4_paas_job_info(self, v4_paas_job_info_request_param):
        """
        /v4/paas/job/info
        本接口用于查询批量资源工单任务的执行结果（开通/变配/退订/续订等）：   
    - 本接口支持多个产品通用，包括云主机和物理机。
        """
        return self.send(v4_paas_job_info_request_param)

    def v4_paas_eip_create(self, v4_paas_eip_create_request_param):
        """
        /v4/paas/eip/create
        用于创建弹性IP：   
    本接口为同步接口，调用成功后会同步返回底层创建的eipID。   
    
        """
        return self.send(v4_paas_eip_create_request_param)

    def v4_paas_ecs_snapshot_create_instance(self, v4_paas_ecs_snapshot_create_instance_request_param):
        """
        /v4/paas/ecs/snapshot/create-instance
        快照创建云主机(工单)   
    - 至少存在一个快照   
    - 快照的状态为可用   
    - 快照原本的云主机存在
        """
        return self.send(v4_paas_ecs_snapshot_create_instance_request_param)

    def v4_paas_ebs_new_from_snapshot_ebs_snap(self, v4_paas_ebs_new_from_snapshot_ebs_snap_request_param):
        """
        /v4/paas/ebs/new-from-snapshot-ebs-snap
        快照创建云硬盘(工单)
        """
        return self.send(v4_paas_ebs_new_from_snapshot_ebs_snap_request_param)

    def v4_paas_ecs_snapshot_delete(self, v4_paas_ecs_snapshot_delete_request_param):
        """
        /v4/paas/ecs/snapshot-delete
        本接口用于删除云主机快照 查询接口为/v4/job/info
        """
        return self.send(v4_paas_ecs_snapshot_delete_request_param)

    def paas_restore_ebs_backup(self, paas_restore_ebs_backup_request_param):
        """
        /v4/paas/ebs-backup/restore-backup
        ###### 云硬盘备份恢复：是指将备份的内容恢复到磁盘里，不是恢复被删的备份   
    开发未对齐原因：混合云返回异步任务ID，公有不返回
        """
        return self.send(paas_restore_ebs_backup_request_param)

    def v4_paas_ebm_create_instance(self, v4_paas_ebm_create_instance_request_param):
        """
        /v4/paas/ebm/create-instance
        创建物理机（工单）
        """
        return self.send(v4_paas_ebm_create_instance_request_param)

    def v4_paas_ecs_batch_create_instances(self, v4_paas_ecs_batch_create_instances_request_param):
        """
        /v4/paas/ecs/batch-create-instances
        多台开通时fixedIP不能进行指定，指定后开通一台后其余会报错。
    instanceName在批量开通多台时会按照 001 ，顺序递增。
    sysVolumeID 此参数暂不支持。
        """
        return self.send(v4_paas_ecs_batch_create_instances_request_param)

    def v4_ecs_flavor_list(self, v4_ecs_flavor_list_request_param):
        """
        /v4/ecs/flavor/list
        查询一个或多个云主机规格资源_PAAS
    该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息,并允许用户根据云主机规格的特殊字段进行筛选。
    注意：如果传了flavorID，则azName为必填；如果只传regionID，则可查询所有数据，azName不是必填的。
        """
        return self.send(v4_ecs_flavor_list_request_param)
