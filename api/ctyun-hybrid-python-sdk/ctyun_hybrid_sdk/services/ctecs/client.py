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


class CtecsClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctecs-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtecsClient, self).__init__(credential, config, 'ctecs', '0.1.0', logger, signer)

    def keypair_details(self, keypair_details_request_param):
        """
        /v4/ecs/keypair/details
        此接口提供用户查询SSH密钥对功能。系统会接收用户输入的查询条件，并返回符合条件的密钥对详细信息。用户可根据此接口的返回值了解对应条件下的密钥对信息。
        """
        return self.send(keypair_details_request_param)

    def get_instance_list_lite_vdc(self, get_instance_list_lite_vdc_request_param):
        """
        /v4/ecs/instance-list-lite-vdc
        v2.2.5版本支持
        """
        return self.send(get_instance_list_lite_vdc_request_param)

    def backup_details(self, backup_details_request_param):
        """
        /v4/ecs/backup/details
        查询云主机备份详情
        """
        return self.send(backup_details_request_param)

    def batch_start_instances(self, batch_start_instances_request_param):
        """
        /v4/ecs/batch-start-instances
        批量开机云主机(1.15)   
    1. 确保当前请求资源池下，这些云主机存在（即instanceIDList中逗号分隔的ID真实存在且与regionID相对应）<br/>   
    2. 云主机需要处于关机状态（stopped），您可以调用查询云主机列表</a>或获取多台云主机的状态信息</a>查询结果中的instanceStatus字段来确认当前云主机状态<br />   
    3. 批量开启云主机的最大数量为50台
        """
        return self.send(batch_start_instances_request_param)

    def snapshot_policy_enable(self, snapshot_policy_enable_request_param):
        """
        /v4/ecs/snapshot-policy/enable
        启用云主机快照策略
        """
        return self.send(snapshot_policy_enable_request_param)

    def exec_backup_policy(self, exec_backup_policy_request_param):
        """
        /v4/ecs/backup-policy/backup-instances
        执行云主机备份策略
        """
        return self.send(exec_backup_policy_request_param)

    def volume_list_by_vm(self, volume_list_by_vm_request_param):
        """
        /v4/volume/list-by-vm
        查询云主机挂载的云硬盘
        """
        return self.send(volume_list_by_vm_request_param)

    def ecs_instance_list(self, ecs_instance_list_request_param):
        """
        /v4/ecs/instance-list
        该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机的部分信息。混合云请求、返回字段projectID不支持。   
       
    vmState:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中   
    create_failed:创建失败
        """
        return self.send(ecs_instance_list_request_param)

    def ecs_snapshot_create(self, ecs_snapshot_create_request_param):
        """
        /v4/ecs/snapshot-create
        创建云主机快照
        """
        return self.send(ecs_snapshot_create_request_param)

    def create_command(self, create_command_request_param):
        """
        /v4/cloud-assistant/create-command
        调用此接口可以创建一条云助手命令
        """
        return self.send(create_command_request_param)

    def openapi_ecs_ports_list_v4(self, openapi_ecs_ports_list_v4_request_param):
        """
        /v4/ecs/ports/list
        查询网卡列表
        """
        return self.send(openapi_ecs_ports_list_v4_request_param)

    def get_ecs_flavors(self, get_ecs_flavors_request_param):
        """
        /v4/common/get-ecs-flavors
        查询资源池虚机规格信息 请使用/v4/ecs/flavor/list
        """
        return self.send(get_ecs_flavors_request_param)

    def ecs_batch_new(self, ecs_batch_new_request_param):
        """
        /v4/ecs/batch-new
        支持批量创建按量付费或包年包月云主机   
    注意：   
    1.系统盘参数syshd大小必须大于等于镜像的大小。   
    2.子网类型不能为裸机属子网。
        """
        return self.send(ecs_batch_new_request_param)

    def ecs_snapshot_batch_update_new(self, ecs_snapshot_batch_update_new_request_param):
        """
        /v4/ecs/snapshot/batch-update
        批量更改云主机快照名称和描述
        """
        return self.send(ecs_snapshot_batch_update_new_request_param)

    def ecs_snapshot_batch_update(self, ecs_snapshot_batch_update_request_param):
        """
        /v4/ecs/snapshot-batch-update
        批量更改云主机快照名称和描述
        """
        return self.send(ecs_snapshot_batch_update_request_param)

    def openapi_ecs_paas_details_v4(self, openapi_ecs_paas_details_v4_request_param):
        """
        /v4/ecs/paas-details
        该接口提供用户一台或多台云主机信息查询功能，用户可以根据此接口的返回值了解自己云主机的详细信息。   
    请求字段projectID，useChannel不支持，返回字段projectID，privateIPv6，shareIPList未对齐   
       
    vmState:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
        """
        return self.send(openapi_ecs_paas_details_v4_request_param)

    def volume_detach(self, volume_detach_request_param):
        """
        /v4/ecs/volume/detach
        云主机卸载云硬盘
        """
        return self.send(volume_detach_request_param)

    def ecs_userdata(self, ecs_userdata_request_param):
        """
        /v4/ecs/userdata
        查询自定义数据
        """
        return self.send(ecs_userdata_request_param)

    def assign_secondary_private_ips_to_port(self, assign_secondary_private_ips_to_port_request_param):
        """
        /v4/ecs/ports/assign-secondary-private-ips
        网卡关联辅助私网IP   
       
    ### 接口约束   
    secondaryPrivateIps 和 secondaryPrivateIpCount 在同一次请求中，同时只能传入一个。
        """
        return self.send(assign_secondary_private_ips_to_port_request_param)

    def ecs_attach_share_interface(self, ecs_attach_share_interface_request_param):
        """
        /v4/ecs/attach-share-interface
        给云主机添加共享网卡
        """
        return self.send(ecs_attach_share_interface_request_param)

    def create_instance(self, create_instance_request_param):
        """
        /v4/ecs/create-instance
        1. 目前不支持预付费账户创建按需付费类型云主机   
    2. 计费模式选择包年包月计费方式时，需要填写订购周期类型与订购时长   
    3. 自动分配弹性IP（extIP="1"）时，需要填写弹性IP版本（ipVersion）与带宽大小（bandwidth）；使用已有的弹性IP（extIP="2"）时，需要填写弹性IP的版本（ipVersion），和对应弹性IP的ID（eipID或ipv6AddressID）   
    4. 挂载网卡时，子网与虚拟私有云存在对应关系，确保子网属于当前虚拟私有云   
    5. 云主机绑定多个标签时，标签键（参数labelKey）不可重复，单台云主机最多可绑定10个标签   
    6. 因对接方原因，instanceName允许重复
        """
        return self.send(create_instance_request_param)

    def query_by_resource_id(self, query_by_resource_id_request_param):
        """
        /v4/ecs/queryByResourceId
        resourceId查询云主机   
    vmState:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
        """
        return self.send(query_by_resource_id_request_param)

    def snapshot_policy_unbind_instances(self, snapshot_policy_unbind_instances_request_param):
        """
        /v4/ecs/snapshot-policy/unbind-instances
        快照策略解绑云主机
        """
        return self.send(snapshot_policy_unbind_instances_request_param)

    def ecs_live_migrate(self, ecs_live_migrate_request_param):
        """
        /v4/ecs/live-migrate
        云主机热迁移
        """
        return self.send(ecs_live_migrate_request_param)

    def instance_details(self, instance_details_request_param):
        """
        /v4/ecs/instance-details
        该接口提供用户一台云主机信息查询功能，用户可以根据此接口的返回值了解自己云主机的详细信息。   
    
        """
        return self.send(instance_details_request_param)

    def get_volume_statistics(self, get_volume_statistics_request_param):
        """
        /v4/ecs/volume/statistics
        查询用户云硬盘统计信息
        """
        return self.send(get_volume_statistics_request_param)

    def list_ecs_type(self, list_ecs_type_request_param):
        """
        /v4/ecs/type-list
        该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息，并允许用户根据云主机规格的特殊字段进行筛选。用户可以根据此接口的返回值了解自己可使用的云主机规格有哪些。
        """
        return self.send(list_ecs_type_request_param)

    def ecs_affinity_group_unbind_one(self, ecs_affinity_group_unbind_one_request_param):
        """
        /v4/ecs/affinity-group/unbind-one
        可以根据用户给定的云主机与云主机组，将云主机移除出云主机组   
       
    ### 接口约束   
       
    1. 该接口为异步操作，返回成功代表命令成功下发，需要配合查询云主机所在云主机组接口进行检查   
    2. 当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用[新版本接口](https://www.ctyun.cn/document/10026730/10106275)，新版本接口更加规范，覆盖场景更全。
        """
        return self.send(ecs_affinity_group_unbind_one_request_param)

    def backup_vm_details(self, backup_vm_details_request_param):
        """
        /v4/ecs/backup/instance-details
        通过虚机ID获取虚拟机最新状态，主要获取虚拟机磁盘挂载信息
        """
        return self.send(backup_vm_details_request_param)

    def detach_ecs_keypair(self, detach_ecs_keypair_request_param):
        """
        /v4/ecs/keypair/detach-instance
        为Linux云主机解绑SSH密钥对   
       
    ### 接口约束   
       
    1.云主机必须存在，2 云主机状态必须是运行中，3 云主机操作系统必须为linux，4 密钥对名称必须存在，5 云主机必须已经绑定了此密钥对
        """
        return self.send(detach_ecs_keypair_request_param)

    def ecs_metadata_create(self, ecs_metadata_create_request_param):
        """
        /v4/ecs/metadata-create
        仅4.0支持，为云主机创建元数据，云主机需为运行中或者关机状态
        """
        return self.send(ecs_metadata_create_request_param)

    def delete_metadata(self, delete_metadata_request_param):
        """
        /v4/ecs/metadata/delete
        仅4.0支持，删除云主机元数据，云主机需为运行中或者关机状态
        """
        return self.send(delete_metadata_request_param)

    def update_ecs_metadata(self, update_ecs_metadata_request_param):
        """
        /v4/ecs/metadata-update
        仅4.0支持，为云主机更新元数据，云主机需为运行中或者关机状态   
    
        """
        return self.send(update_ecs_metadata_request_param)

    def describe_send_file_results(self, describe_send_file_results_request_param):
        """
        /v4/cloud-assistant/describe-send-file-results
        调用此接口可以查询上传到弹性云主机或物理机的文件的结果
        """
        return self.send(describe_send_file_results_request_param)

    def detach_port(self, detach_port_request_param):
        """
        /v4/ecs/ports/detach
        网卡解绑实例   
    ### 接口约束   
    当前仅支持虚拟机
        """
        return self.send(detach_port_request_param)

    def list_sfs_instance_v41(self, list_sfs_instance_v41_request_param):
        """
        /v4/ecs/sfs/vms-list
        可以根据用户查询对应的文件系统关联的云主机列表(仅4.0支持)
        """
        return self.send(list_sfs_instance_v41_request_param)

    def ecs_check_migrate(self, ecs_check_migrate_request_param):
        """
        /v4/ecs/check-ecs-migrate
        云主机热迁移校验
        """
        return self.send(ecs_check_migrate_request_param)

    def ecs_keypair_create_new(self, ecs_keypair_create_new_request_param):
        """
        /v4/ecs/keypair/create-keypair
        此接口用来创建一对SSH密钥对。系统会为您保管密钥的公钥部分，并返回未加密私钥。您需要自行妥善保管私钥部分。
        """
        return self.send(ecs_keypair_create_new_request_param)

    def ecs_batch_password_update(self, ecs_batch_password_update_request_param):
        """
        /v4/ecs/batch-password-update
        更新多台云主机的密码
        """
        return self.send(ecs_batch_password_update_request_param)

    def ecs_describe_regions(self, ecs_describe_regions_request_param):
        """
        /v4/ecs/describe-regions
        查询账户启用的资源池信息
        """
        return self.send(ecs_describe_regions_request_param)

    def details_instance_backup(self, details_instance_backup_request_param):
        """
        /v4/ecs/backup-details
        查询云主机备份详情
        """
        return self.send(details_instance_backup_request_param)

    def ecs_simplify_list(self, ecs_simplify_list_request_param):
        """
        /v4/ecs/simplify-list
        查询云主机列表
        """
        return self.send(ecs_simplify_list_request_param)

    def snapshot_policy_details(self, snapshot_policy_details_request_param):
        """
        /v4/ecs/snapshot-policy/details
        查询云主机快照策略详情
        """
        return self.send(snapshot_policy_details_request_param)

    def snapshot_list_vdc(self, snapshot_list_vdc_request_param):
        """
        /v4/ecs/snapshot/list-vdc
        查询云主机快照列表，该接口1.16.06及以上云管版本支持。
        """
        return self.send(snapshot_list_vdc_request_param)

    def get_ca_agent(self, get_ca_agent_request_param):
        """
        /v4/cloud-assistant/get-ca-agent
        调用此接口可以查询一台或多台弹性云主机、物理机内是否安装了云助手agent   
    说明：仅支持批量查询弹性云主机或物理机是否安装了云助手agent，不支持混合查询
        """
        return self.send(get_ca_agent_request_param)

    def get_command(self, get_command_request_param):
        """
        /v4/cloud-assistant/get-command
        调用此接口可以查询用户手动创建的云助手命令或者云助手公共命令详情信息
        """
        return self.send(get_command_request_param)

    def delete_repo(self, delete_repo_request_param):
        """
        /v4/ecs/backup-repo/delete
        1. 存储库有备份支持退订，会进行自动删除，只限制可删除的备份   
    2. 存在创建中或其他的ing状态的退订也会失败   
    3.混合云退订不限制购买后7天，与公有云不一致
        """
        return self.send(delete_repo_request_param)

    def ecs_unsubscribe(self, ecs_unsubscribe_request_param):
        """
        /v4/ecs/unsubscribe
        支持退订或者销毁云主机，默认直接销毁，要求：   
     1.云主机必须存在   
     2.释放云主机前请先检查云主机是否绑定虚拟IP，如果有请先解绑虚拟IP   
     3.请检查云主机是否存在快照，如果存在快照不允许释放云主机   
     4.云主机处于关机状态下才可释放
        """
        return self.send(ecs_unsubscribe_request_param)

    def snapshot_policy_update(self, snapshot_policy_update_request_param):
        """
        /v4/ecs/snapshot-policy/update
        修改云主机快照策略
        """
        return self.send(snapshot_policy_update_request_param)

    def query_affinity_group_instance(self, query_affinity_group_instance_request_param):
        """
        /v4/ecs/affinity-group/list-instance
        可以根据用户给定的云主机组，查询云主机组内云主机的详细信息，参考公有云：   
    https://eop.ctyun.cn/ebp/ctapiDocument/search?sid=25&api=8320&data=87&isNormal=1&vid=81
        """
        return self.send(query_affinity_group_instance_request_param)

    def get_metadata_v41(self, get_metadata_v41_request_param):
        """
        /v4/ecs/metadata-get
        仅4.0支持，查询云主机的元数据，云主机需为运行中或者关机状态
        """
        return self.send(get_metadata_v41_request_param)

    def vnc_details(self, vnc_details_request_param):
        """
        /v4/ecs/vnc/details
        查询一台云主机的Web管理终端地址。   
    #### 调用VNC OpenAPI接口获取Token   
    * 调用接口获取Token信息， token 信息就是websocket协议访问地址。   
    1. 使用noVNC等client进行访问，以noVNC为例，具体操作步骤如下：   
       
      -  本地启动noVNC服务，打开vnc页面；   
      -  点击左侧`⚙`，打开`高级`-`WebSocket`，在`主机`中，填写协议的地址   
      -  点击右侧连接按钮，即可访问   
       
    2.若要直接使用返回信息进行vnc远程登录，需保证调用方所在的浏览器中可访问到云管系统登录地址，并使用拼接后的完整地址访问：   
       
    完整访问地址为：wss://云管系统登录地址ip:端口+该接口返回的所有内容；   
       
    协议使用wss/ws取决于是云管访问是https还是http；   
       
    拼接的完整地址示例：wss://10.246.81.250:40117/osnmvnc1/ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE3Njc3NzgsImlhdCI6MTc0MTc2NDE3OCwidXNlcl9pZCI6IjYwNGFiOTdmYjg0NDYxMWU5MzViOWI3OTYxZmIyMTc5IiwicHJvamVjdF9pZCI6IjEzNTE2MWMyYTZkNzkwYzg0YzczYTQ3MDI0MjJlZGNmIiwiZG9tYWluX2lkIjoiZGVmYXVsdCIsInJvbGVzIjpbInVzZXIiXSwiY29uc3VtZXJfaWQiOiIiLCJpc3N1ZWRfYXQiOiIyMDI1LTAzLTEyVDA3OjIyOjU4LjAwMDAwMFoiLCJleHBpcmVfYXQiOiIyMDI1LTAzLTEyVDA4OjIyOjU4LjAwMDAwMFoiLCJNZXRob2QiOlsicGFzc3dvcmQiXX0.fdqxwwXDEAVSXUbu2m3D06hMwqK49mABYAXSKGcxCPQ&instanceId=6cf210e3-7f20-84f7-4eb3-a3b6399f42a3   
       
    接口调通之后会返回VNC的登录页面。   
       
    若调用websocket接口返回403，可在调用接口时headers里增加如下参数：   
    Pragma: no-cache   
    Cache-Control: no-cache   
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36   
    Origin: https://云管系统登录地址ip:端口   
    Accept-Encoding: gzip, deflate, br, zstd   
    
        """
        return self.send(vnc_details_request_param)

    def ecs_delete_delegate(self, ecs_delete_delegate_request_param):
        """
        /v4/ecs/delegate/delete
        接口功能介绍：该接口提供用户云主机清除绑定的委托能力，委托信息将以用户元数据数据形式存入，无委托情况下，清除委托依旧返回正确（执行委托置空操作）。   
    接口约束：   
    	确保当前请求资源池下，该云主机存在（即instanceID真实存在且与regionID相对应）   
    	云主机只有在运行（running）或关机（stopped）状态才可执行该操作   
    	目前该功能仅支持多可用区类型资源池
        """
        return self.send(ecs_delete_delegate_request_param)

    def ecs_batch_reboot(self, ecs_batch_reboot_request_param):
        """
        /v4/ecs/batch-reboot
        批量重启云主机
        """
        return self.send(ecs_batch_reboot_request_param)

    def create_instance_backup(self, create_instance_backup_request_param):
        """
        /v4/ecs/backup-create
        创建云主机备份   
    底层暂时支持返回：创建备份对应的异步任务uuid
        """
        return self.send(create_instance_backup_request_param)

    def backup_statistics(self, backup_statistics_request_param):
        """
        /v4/ecs/backup/statistics
        通过虚机ID获取虚拟机最新状态，主要获取虚拟机磁盘挂载信息
        """
        return self.send(backup_statistics_request_param)

    def ecs_password_update(self, ecs_password_update_request_param):
        """
        /v4/ecs/password-update
        更新云主机的密码,此接口为同步接口。   
       
    ### 接口约束   
       
    1. 云主机必须处于运行状态
        """
        return self.send(ecs_password_update_request_param)

    def ecs_affinity_group_ecs_list(self, ecs_affinity_group_ecs_list_request_param):
        """
        /v4/ecs/affinity-group/ecs-list
        可以根据用户给定的云主机组，查询云主机组内云主机的详细信息
        """
        return self.send(ecs_affinity_group_ecs_list_request_param)

    def show_port(self, show_port_request_param):
        """
        /v4/ecs/ports/show
        查询网卡信息
        """
        return self.send(show_port_request_param)

    def ecs_instance_label_list_lite_v_d_c(self, ecs_instance_label_list_lite_v_d_c_request_param):
        """
        /v4/ecs/instance-label-list-lite-vdc
        云主机轻量信息列表(带标签)
        """
        return self.send(ecs_instance_label_list_lite_v_d_c_request_param)

    def ecs_query_async_results(self, ecs_query_async_results_request_param):
        """
        /v4/ecs/query-async-results
        该接口通过一个或多个异步任务的jobID查询任务执行的结果。   
    
        """
        return self.send(ecs_query_async_results_request_param)

    def vm_cpu_latest_metric_data(self, vm_cpu_latest_metric_data_request_param):
        """
        /v4/ecs/vm-cpu-latest-metric-data
        注：该接口不推荐使用。建议使用-->实时监控数据：云主机(/v4.1/monitor/query-vm-latestmetricdata)
        """
        return self.send(vm_cpu_latest_metric_data_request_param)

    def update_deletion_protection(self, update_deletion_protection_request_param):
        """
        /v4/ecs/update-deletion-protection
        1.云主机必须存在，云主机只有在运行（running）、关机（stopped）或节省关机（shelve）状态才可执行该操作，您可以调用查询云主机列表或获取多台云主机的状态信息查询结果中的instanceStatus字段来确认当前云主机状态   
    2.只有按需付费云主机能开启实例删除保护
        """
        return self.send(update_deletion_protection_request_param)

    def ecs_keypair_describe(self, ecs_keypair_describe_request_param):
        """
        /v4/ecs/keypair/describe
        此接口提供用户查询SSH密钥对功能。系统会接收用户输入的查询条件，并返回符合条件的密钥对详细信息。用户可根据此接口的返回值了解对应条件下的密钥对信息。
        """
        return self.send(ecs_keypair_describe_request_param)

    def snapshot_policy_delete(self, snapshot_policy_delete_request_param):
        """
        /v4/ecs/snapshot-policy/delete
        删除云主机快照策略
        """
        return self.send(snapshot_policy_delete_request_param)

    def ecs_batch_update_instances(self, ecs_batch_update_instances_request_param):
        """
        /v4/ecs/batch-update-instances
        1. 确保当前请求资源池下，这些云主机存在（即instanceID真实存在且与regionID相对应）   
    2. 修改前后的displayName须不一样   
    3. 云主机只有在运行（running）、关机（stopped）或节省关机（shelve）状态才可执行该操作，您可以调用查询云主机列表或获取多台云主机的状态信息查询结果中的instanceStatus字段来确认当前云主机状态
        """
        return self.send(ecs_batch_update_instances_request_param)

    def vm_network_latest_metric_data(self, vm_network_latest_metric_data_request_param):
        """
        /v4/ecs/vm-network-latest-metric-data
        注：该接口不推荐使用。建议使用-->实时监控数据：云主机(/v4.1/monitor/query-vm-latestmetricdata)
        """
        return self.send(vm_network_latest_metric_data_request_param)

    def ecs_details(self, ecs_details_request_param):
        """
        /v4/ecs/details
        一台或多台ECS实例的详细信息.    
       
    vmState:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
        """
        return self.send(ecs_details_request_param)

    def ecs_backup_delete(self, ecs_backup_delete_request_param):
        """
        /v4/ecs/backup-delete
        删除云主机备份
        """
        return self.send(ecs_backup_delete_request_param)

    def ecs_batch_update(self, ecs_batch_update_request_param):
        """
        /v4/ecs/batch-update
        更新多台云主机的部分信息。
        """
        return self.send(ecs_batch_update_request_param)

    def snapshot_policy_task_list(self, snapshot_policy_task_list_request_param):
        """
        /v4/ecs/snapshot-policy/task-list
        查询云主机快照任务列表
        """
        return self.send(snapshot_policy_task_list_request_param)

    def ecs_keypair_import(self, ecs_keypair_import_request_param):
        """
        /v4/ecs/keypair/import
        导入由其他工具产生的RSA密钥对的公钥部分，密钥对的类型必须是SSH或x509。
        """
        return self.send(ecs_keypair_import_request_param)

    def create_instance_backup_v41(self, create_instance_backup_v41_request_param):
        """
        /v4/ecs/backup/create
        创建云主机备份   
    底层暂时支持返回：创建备份对应的异步任务uuid
        """
        return self.send(create_instance_backup_v41_request_param)

    def keypair_attach_instance(self, keypair_attach_instance_request_param):
        """
        /v4/ecs/keypair/attach-instance
        此接口提供用户绑定SSH密钥对到云主机功能。系统会接收用户输入的云主机id和SSH密钥对，将对应SSH密钥对绑定到对应云主机上。   
    1.云主机必须存在，2.需要云主机处于运行中（running）状态，3.需要云主机的操作系统必须为linux，4.密钥对名称必须存在, 5云主机和密钥对同属于同一个用户 6云主机和密钥对同属于同一个可用区7云主机不能已经绑定了此密钥对
        """
        return self.send(keypair_attach_instance_request_param)

    def openapi_ecs_query_host_info_v4(self, openapi_ecs_query_host_info_v4_request_param):
        """
        /v4/ecs/query-host-info
        该接口通过云主机ID查询云主机所在宿主机信息。**注意**:ID或instanceID必传其中一个，公有云为ID   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.AvailableZoneNotFound -- 非法的可用区   
    Compute.Param.Error -- 参数错误   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.Host.NotFoundError -- 非法的宿主机   
    Compute.CommonInternalError -- 内部错误
        """
        return self.send(openapi_ecs_query_host_info_v4_request_param)

    def job_query(self, job_query_request_param):
        """
        /v4/ecs/job/query
        该接口通过一个或多个异步任务的jobID查询任务执行的结果。查询多个异步任务的结果（网关转发到/v4/ecs/query-async-results）
        """
        return self.send(job_query_request_param)

    def resume_instance(self, resume_instance_request_param):
        """
        /v4/ecs/resume
        该接口提供用户恢复一台云主机功能。   
       
    ### 接口约束   
    云主机必须处于已挂起状态
        """
        return self.send(resume_instance_request_param)

    def snapshot_policy_list(self, snapshot_policy_list_request_param):
        """
        /v4/ecs/snapshot-policy/list
        查询云主机快照策略列表
        """
        return self.send(snapshot_policy_list_request_param)

    def describe_availability_zones(self, describe_availability_zones_request_param):
        """
        /v4/ecs/describe-availability-zones
        查询账户指定资源池中可用区的信息。
        """
        return self.send(describe_availability_zones_request_param)

    def ecs_affinity_group_bind_one(self, ecs_affinity_group_bind_one_request_param):
        """
        /v4/ecs/affinity-group/bind-one
        可以根据用户给定的云主机与云主机组，将云主机添加进云主机组   
       
    ### 接口约束   
       
    1. 该接口为异步操作，返回成功代表命令成功下发，需要配合查询云主机所在云主机组接口进行检查
        """
        return self.send(ecs_affinity_group_bind_one_request_param)

    def ecs_batch_delete(self, ecs_batch_delete_request_param):
        """
        /v4/ecs/batch-delete
        批量退订或者销毁云主机，默认直接销毁，要求：   
     1.云主机必须存在   
     2.批量释放资源一次不能超过10个   
     3.释放云主机前请先检查云主机是否绑定虚拟IP，如果有请先解绑虚拟IP   
     4.请检查云主机是否存在快照，如果存在快照不允许释放云主机   
     5.云主机处于关机状态下才可释放   
       
    未对齐：   
    1. 混合云v2订单侧批量退订接口不支持包周期和按需同时退订，所以只能退订时只能单个去循环退订，返回最后一个资源的订单id
        """
        return self.send(ecs_batch_delete_request_param)

    def instance_attach_sfs_v41(self, instance_attach_sfs_v41_request_param):
        """
        /v4/ecs/sfs/attach
        此接口提供用户实现云主机挂载一个或多个文件系统的功能(仅4.0支持)   
       
    1. 云主机须处于运行状态   
    2. 云主机和文件系统应属于同一个VPC   
    3. 云主机最多可挂载5个文件   
    4. 云主机仅支持部分镜像类型挂载，windows镜像：windows server 2012 数据中心版 R2 64位中文版（主镜像）、windows server 2012 标准版 R2 64位中文版、windows server 2016 数据中心版 64位中文版、windows server 2019 数据中心版 64位中文版。linux镜像：CentOS-7.8-x86_64、CentOS-7.9-x86_64（主镜像）、 CentOS-8.0-x86_64、 CentOS-8.1-x86_64、 CentOS-8.2-x86_64、Ubuntu-18.04-x86_64、Ubuntu-20.04-x86_64、Ctyunos-2.0.1_220311-x86_64
        """
        return self.send(instance_attach_sfs_v41_request_param)

    def ecs_batch_rebuild(self, ecs_batch_rebuild_request_param):
        """
        /v4/ecs/batch-rebuild
        该接口提供用户重装多台云主机功能，通过填写相应云主机ID、镜像ID和密码对云主机进行重装。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    2. 若云主机存在快照，不允许执行重装操作。
        """
        return self.send(ecs_batch_rebuild_request_param)

    def ecs_create(self, ecs_create_request_param):
        """
        /v4/ecs/create
        支持创建一台按量付费或包年包月的云主机   
    注意：   
    1.系统盘参数syshd大小必须大于等于镜像的大小。   
    2.子网类型不能为裸机属子网。   
    3. 因对接方原因，instanceName允许重复   
    
        """
        return self.send(ecs_create_request_param)

    def ecs_affinity_group_list(self, ecs_affinity_group_list_request_param):
        """
        /v4/ecs/affinity-group-list
        查询云主机组列表或者详情
        """
        return self.send(ecs_affinity_group_list_request_param)

    def update_instance_backup(self, update_instance_backup_request_param):
        """
        /v4/ecs/backup-update
        更改云主机备份名称和描述
        """
        return self.send(update_instance_backup_request_param)

    def ecs_reboot(self, ecs_reboot_request_param):
        """
        /v4/ecs/reboot
        该接口提供用户重启一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
        """
        return self.send(ecs_reboot_request_param)

    def instance_details_v41(self, instance_details_v41_request_param):
        """
        /v4.1/ecs/instance-details
        该接口提供用户一台云主机信息查询功能，用户可以根据此接口的返回值了解自己云主机的详细信息。   
    
        """
        return self.send(instance_details_v41_request_param)

    def ecs_recover_unsubscribed(self, ecs_recover_unsubscribed_request_param):
        """
        /v4/ecs/recover-unsubscribed-instance
        批量恢复云主机，要求：   
     1.云主机必须存在   
     2.批量恢复资源一次不能超过10个   
     3.云主机必须在回收站，处于退订状态
        """
        return self.send(ecs_recover_unsubscribed_request_param)

    def ecs_affinity_group_create(self, ecs_affinity_group_create_request_param):
        """
        /v4/ecs/affinity-group-create
        创建云主机组
        """
        return self.send(ecs_affinity_group_create_request_param)

    def keypair_import(self, keypair_import_request_param):
        """
        /v4/ecs/keypair/import-keypair
        导入由其他工具产生的RSA密钥对的公钥部分，密钥对的类型必须是SSH或x509。   
    
        """
        return self.send(keypair_import_request_param)

    def ecs_statistics_volume(self, ecs_statistics_volume_request_param):
        """
        /v4/ecs/statistics-volume
        查询用户云硬盘统计信息
        """
        return self.send(ecs_statistics_volume_request_param)

    def batch_delete_metadata_v41(self, batch_delete_metadata_v41_request_param):
        """
        /v4/ecs/metadata-batch-delete
        仅4.0支持，批量删除云主机元数据，如果某个云主机的元数据删除失败，则返回值返回该云主机id。
        """
        return self.send(batch_delete_metadata_v41_request_param)

    def delete_command(self, delete_command_request_param):
        """
        /v4/cloud-assistant/delete-command
        调用此接口可删除用户自己创建的云助手命令
        """
        return self.send(delete_command_request_param)

    def ecs_rebuild(self, ecs_rebuild_request_param):
        """
        /v4/ecs/rebuild
        该接口提供用户重装一台云主机功能，通过填写相应云主机ID、镜像ID和密码对云主机进行重装。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    2. 云主机不能存在快照。
        """
        return self.send(ecs_rebuild_request_param)

    def affinity_group_ccreate(self, affinity_group_ccreate_request_param):
        """
        /v4/ecs/affinity-group/create
        创建云主机组。
        """
        return self.send(affinity_group_ccreate_request_param)

    def volume_list(self, volume_list_request_param):
        """
        /v4/ecs/volume/list
        查询云主机的云硬盘列表。请求asc，sort 字段不支持，返回字段diskMode未对齐，isEncrypt字段不支持
        """
        return self.send(volume_list_request_param)

    def affinity_group_list(self, affinity_group_list_request_param):
        """
        /v4/ecs/affinity-group/list
        查询云主机组列表或者详情
        """
        return self.send(affinity_group_list_request_param)

    def modify_instance_type_tags(self, modify_instance_type_tags_request_param):
        """
        /v4/ecs/flavor/tag-add
        设置云主机实例规格标签
        """
        return self.send(modify_instance_type_tags_request_param)

    def ecs_list_by_type_families(self, ecs_list_by_type_families_request_param):
        """
        /v4/ecs/list-by-typefamilies
        该接口提供用户根据指定规格族查询云主机的名称、云主机ID及规格详情
        """
        return self.send(ecs_list_by_type_families_request_param)

    def ecs_affinity_group_bind_check(self, ecs_affinity_group_bind_check_request_param):
        """
        /v4/ecs/affinity-group/bind-check
        接口功能介绍   
    可以根据用户给定的云主机与云主机组，校验当前情况下是否可以将云主机加入主机组。如果可以则返回值中needMigrate字段为0，反之则需要将云主机迁移。   
       
    接口约束   
    当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用新版本接口，新版本接口更加规范，覆盖场景更全。   
    云主机需处于运行中（running）或关机（stopped）状态
        """
        return self.send(ecs_affinity_group_bind_check_request_param)

    def attach_port(self, attach_port_request_param):
        """
        /v4/ecs/ports/attach
        网卡绑定实例   
    ### 接口约束   
    当前仅支持虚拟机
        """
        return self.send(attach_port_request_param)

    def list_instances(self, list_instances_request_param):
        """
        /v4/ecs/list-instances
        该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机信息。   
    **注意**：混合云请求字段projectID不支持，返回字段projectID未对齐
        """
        return self.send(list_instances_request_param)

    def ecs_volume_attach(self, ecs_volume_attach_request_param):
        """
        /v4/ecs/volume_attach
        支持云主机挂载云硬盘   
    云主机下限制挂载云硬盘个数上限为20
        """
        return self.send(ecs_volume_attach_request_param)

    def create_eip(self, create_eip_request_param):
        """
        /v4/ecs/eip/create
        调用此接口可创建弹性公网IP（Elastic IP Address，简称EIP）。混合云目前入参缺失bandwidthID，demandBillingType这两个字段。非必填，暂不做调整
        """
        return self.send(create_eip_request_param)

    def get_volume_usage(self, get_volume_usage_request_param):
        """
        /v4/ecs/volume/usage
        1. 此接口V2.2.5.9，V2.2.6.3及以上版本支持；   
    2. 返回-1表示当前无法获取该云盘的真实使用量；   
    3. 仅轻量混合云支持， 3.0/4.0暂不支持；   
    4. 云主机不存在或者未查找到该云主机关联的云盘信息时,results返回null.
        """
        return self.send(get_volume_usage_request_param)

    def ecs_update(self, ecs_update_request_param):
        """
        /v4/ecs/update
        修改一台实例的部分信息
        """
        return self.send(ecs_update_request_param)

    def ecs_fix_ip_list(self, ecs_fix_ip_list_request_param):
        """
        /v4/ecs/fix-ip-list
        根据云主机ID，查询云主机的固定IP。
        """
        return self.send(ecs_fix_ip_list_request_param)

    def ecs_backup_usage(self, ecs_backup_usage_request_param):
        """
        /v4/ecs/backup-usage
        查看云主机备份空间占用大小
        """
        return self.send(ecs_backup_usage_request_param)

    def ecs_ip_show(self, ecs_ip_show_request_param):
        """
        /v4/ecs/host/ip-show
        通过云主机IP查询宿主机IP列表
        """
        return self.send(ecs_ip_show_request_param)

    def affinity_group_list_vdc(self, affinity_group_list_vdc_request_param):
        """
        /v4/ecs/affinity-group/list-vdc
        查询云主机组列表或者详情，该接口1.16.06及以上云管版本支持。
        """
        return self.send(affinity_group_list_vdc_request_param)

    def ecs_snapshot_status(self, ecs_snapshot_status_request_param):
        """
        /v4/ecs/snapshot-status
        查询云主机快照状态   
    
        """
        return self.send(ecs_snapshot_status_request_param)

    def ecs_instance_list_audit(self, ecs_instance_list_audit_request_param):
        """
        /v4/ecs/instance-list-audit
        该接口提供用户多台云主机信息查询功能，用户可以根据此接口的返回值得到多台云主机的部分信息。混合云请求、返回字段projectID不支持。   
       
    status:   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backuping: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshoting: 快照创建中
        """
        return self.send(ecs_instance_list_audit_request_param)

    def get_commands(self, get_commands_request_param):
        """
        /v4/cloud-assistant/get-commands
        调用此接口可以查询用户手动创建的云助手命令或者云助手公共命令
        """
        return self.send(get_commands_request_param)

    def update_instance_backup_v41(self, update_instance_backup_v41_request_param):
        """
        /v4/ecs/backup/update
        更改云主机备份名称和描述
        """
        return self.send(update_instance_backup_v41_request_param)

    def ecs_snapshot_restore(self, ecs_snapshot_restore_request_param):
        """
        /v4/ecs/snapshot-restore
        恢复云主机快照   
       
    ### 接口约束   
       
    1. 至少存在一个快照   
    2. 快照的状态为可用   
    3. 云主机存在且状态为关机
        """
        return self.send(ecs_snapshot_restore_request_param)

    def local_disk_extend_cancel(self, local_disk_extend_cancel_request_param):
        """
        /v4/ecs/localdisk/extend-cancel
        1 支持一次取消多个AZ下多个虚机的多个本地盘的预占。   
    2 本地盘状态为 allocated 时自动跳过，视为成功。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.LocalDisk.CancelFailed -- 取消预占失败   
    Compute.CommonInternalError -- 内部错误
        """
        return self.send(local_disk_extend_cancel_request_param)

    def create_metadata(self, create_metadata_request_param):
        """
        /v4/ecs/metadata/create
        仅4.0支持，为云主机创建元数据，云主机需为运行中或者关机状态   
    
        """
        return self.send(create_metadata_request_param)

    def query_instance_under_host(self, query_instance_under_host_request_param):
        """
        /v4/ecs/instance-under-host
        混合云自定义接口(v2.2.4支持)，v1云管按照自己协议返回未做额外处理。所以返回体中涉及ID均为UUID，状态均为云管支持状态。最外层额外提供了ecsID云管ID返回。
        """
        return self.send(query_instance_under_host_request_param)

    def ecs_volume_update(self, ecs_volume_update_request_param):
        """
        /v4/ecs/volume_update
        修改云硬盘
        """
        return self.send(ecs_volume_update_request_param)

    def get_ecs_resource_assess_hybrid(self, get_ecs_resource_assess_hybrid_request_param):
        """
        /v4/ecs/get-resources-assess
        statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.AvailableZoneNotFound -- 非法的可用区   
    Compute.Param.Error -- 参数错误   
    Compute.CommonInternalError -- 内部错误   
    
        """
        return self.send(get_ecs_resource_assess_hybrid_request_param)

    def suspend_instance(self, suspend_instance_request_param):
        """
        /v4/ecs/suspend
        该接口提供用户挂起一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
        """
        return self.send(suspend_instance_request_param)

    def ecs_flavor_network_update(self, ecs_flavor_network_update_request_param):
        """
        /v4/ecs/flavor-network-update
        支持对一台已经关机中的云主机进行带宽或规格的变更   
       
    #### 接口约束   
    1. 目标云主机处于关机或节省关机状态，仅支持具有弹性公网IP的云主机进行带宽变更   
    2. 云主机已挂载的云硬盘状态不能处于“镜像制作中”   
    3. 当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用新版本接口，新版本接口更加规范，覆盖场景更全。
        """
        return self.send(ecs_flavor_network_update_request_param)

    def delete_ecs_metadata(self, delete_ecs_metadata_request_param):
        """
        /v4/ecs/metadata-delete
        仅4.0支持，删除云主机元数据，云主机需为运行中或者关机状态
        """
        return self.send(delete_ecs_metadata_request_param)

    def batch_reboot_instances(self, batch_reboot_instances_request_param):
        """
        /v4/ecs/batch-reboot-instances
        批量重启云主机(1.15)   
    1.确保当前请求资源池下，这些云主机存在（即instanceIDList中逗号分隔的ID真实存在且与regionID相对应）<br/>   
    2.云主机需要处于开机状态（running），您可以调用查询云主机列表</a>或获取多台云主机的状态信息</a>查询结果中的instanceStatus字段来确认当前云主机状态<br />   
    3.批量重启云主机的最大数量为50台
        """
        return self.send(batch_reboot_instances_request_param)

    def ecs_start(self, ecs_start_request_param):
        """
        /v4/ecs/start
           
    该接口提供用户开启一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    
        """
        return self.send(ecs_start_request_param)

    def v4_ecs_clone_instance(self, v4_ecs_clone_instance_request_param):
        """
        /v4/ecs/clone-instance
        1. 被克隆云主机存在，且云主机处于运行中（running）或关机（stopped）状态   
    2. 目前不支持预付费账户创建按需付费类型云主机   
    3. 计费模式选择包年包月计费方式时，需要填写订购周期类型与订购时长   
    4. 挂载网卡时，子网与虚拟私有云存在对应关系，确保子网属于当前虚拟私有云   
    5. 云主机已挂载的云硬盘状态不能处于“镜像制作中”
        """
        return self.send(v4_ecs_clone_instance_request_param)

    def update_ebs_by_disk_id(self, update_ebs_by_disk_id_request_param):
        """
        /v4/ecs/volume/update
        修改云硬盘
        """
        return self.send(update_ebs_by_disk_id_request_param)

    def ecs_backup_list(self, ecs_backup_list_request_param):
        """
        /v4/ecs/backup/list
        查询云主机备份列表   
    - 推荐使用新接口：/v4/ecs/backup/list   
    
        """
        return self.send(ecs_backup_list_request_param)

    def extend_volume(self, extend_volume_request_param):
        """
        /v4/ecs/volume/extend
        扩容云硬盘
        """
        return self.send(extend_volume_request_param)

    def job_info(self, job_info_request_param):
        """
        /v4/job/info
        查看job资源操作任务状态，例如开关机，重启。   
    resourceId字段将废弃，暂时保留，兼容旧接口。   
    增加uuid（资源的唯一id）字段   
    注意：该接口不支持paas批量任务查询，paas批量请使用/v4/paas/job/info
        """
        return self.send(job_info_request_param)

    def create_instance_by_instance_backup(self, create_instance_by_instance_backup_request_param):
        """
        /v4/ecs/backup/create-instance
        注意：必须是当前用户的安全组 安全组和网卡的vpc必须一致
        """
        return self.send(create_instance_by_instance_backup_request_param)

    def snapshot_policy_disable(self, snapshot_policy_disable_request_param):
        """
        /v4/ecs/snapshot-policy/disable
        停用云主机快照策略
        """
        return self.send(snapshot_policy_disable_request_param)

    def query_instanc_id_v41(self, query_instanc_id_v41_request_param):
        """
        /v4/ecs/order/query-uuid
        1.订单状态：目前仅支持完成-3/施工失败-5/开通中-14   
    2.资源UUID：仅返回云主机resourceID集合。如果是VM/EIP分多子订单这种退订场景，会仅返回VM的resourceID，但是orderStatus还是会以VM和EIP共同的为准
        """
        return self.send(query_instanc_id_v41_request_param)

    def describe_invocation_results(self, describe_invocation_results_request_param):
        """
        /v4/cloud-assistant/describe-invocation-results
        查询一条或多条云助手命令在弹性云主机、物理机中执行结果
        """
        return self.send(describe_invocation_results_request_param)

    def vm_cpu_history_metric_data(self, vm_cpu_history_metric_data_request_param):
        """
        /v4/ecs/vm-cpu-history-metric-data
        该接口不推荐使用。建议使用-->历史监控数据：云主机(/v4.1/monitor/query-vm-historymetricdata)
        """
        return self.send(vm_cpu_history_metric_data_request_param)

    def batch_stop_instances(self, batch_stop_instances_request_param):
        """
        /v4/ecs/batch-stop-instances
        批量关机云主机(1.15)   
    1. 确保当前请求资源池下，这些云主机存在（即instanceIDList中逗号分隔的ID真实存在且与regionID相对应）<br/>   
    2. 云主机需要处于开机状态（running），您可以调用查询云主机列表</a>或获取多台云主机的状态信息</a>查询结果中的instanceStatus字段来确认当前云主机状态<br />   
    3. 批量关闭云主机的最大数量为50台
        """
        return self.send(batch_stop_instances_request_param)

    def ecs_host_page_list(self, ecs_host_page_list_request_param):
        """
        /v4/hosts/by-page
        查询宿主机列表
        """
        return self.send(ecs_host_page_list_request_param)

    def list_backup_policy(self, list_backup_policy_request_param):
        """
        /v4/ecs/backup-policy/list
        查询云主机备份策略列表
        """
        return self.send(list_backup_policy_request_param)

    def volume_attach(self, volume_attach_request_param):
        """
        /v4/ecs/volume/attach
        云主机挂载云硬盘
        """
        return self.send(volume_attach_request_param)

    def ecs_stop(self, ecs_stop_request_param):
        """
        /v4/ecs/stop
        该接口提供用户关闭一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
        """
        return self.send(ecs_stop_request_param)

    def metadata_details(self, metadata_details_request_param):
        """
        /v4/ecs/metadata/details
        仅4.0支持，查询云主机的元数据，云主机需为运行中或者关机状态
        """
        return self.send(metadata_details_request_param)

    def vm_network_history_metric_data(self, vm_network_history_metric_data_request_param):
        """
        /v4/ecs/vm-network-history-metric-data
        该接口不推荐使用。建议使用-->历史监控数据：云主机(/v4.1/monitor/query-vm-historymetricdata)   
    
        """
        return self.send(vm_network_history_metric_data_request_param)

    def describe_ecs_by_snapshot(self, describe_ecs_by_snapshot_request_param):
        """
        /v4/ecs/snapshot-query
        根据快照查询虚拟机
        """
        return self.send(describe_ecs_by_snapshot_request_param)

    def ecs_affinity_group_delete(self, ecs_affinity_group_delete_request_param):
        """
        /v4/ecs/affinity-group-delete
        删除云主机组
        """
        return self.send(ecs_affinity_group_delete_request_param)

    def ecs_statistics(self, ecs_statistics_request_param):
        """
        /v4/ecs/statistics-instance
        查询用户云主机统计信息
        """
        return self.send(ecs_statistics_request_param)

    def snapshot_create(self, snapshot_create_request_param):
        """
        /v4/ecs/snapshot/create
        创建云主机快照
        """
        return self.send(snapshot_create_request_param)

    def list_instance_backup(self, list_instance_backup_request_param):
        """
        /v4/ecs/backup-list
        查询云主机备份列表
        """
        return self.send(list_instance_backup_request_param)

    def keypair_attach_ecs(self, keypair_attach_ecs_request_param):
        """
        /v4/ecs/keypair/attach
           
    此接口提供用户绑定SSH密钥对到云主机功能。系统会接收用户输入的云主机id和SSH密钥对，将对应SSH密钥对绑定到对应云主机上。   
    1.云主机必须存在，2.需要云主机处于运行中（running）状态，3.需要云主机的操作系统必须为linux，4.密钥对名称必须存在 ,5云主机和密钥对同属于同一个用户, 6云主机和密钥对同属于同一个可用区,7云主机不能已经绑定了此密钥对   
       
    ### 接口约束   
       
    1. 需要云主机处于工作状态   
    2. 需要云主机的操作系统必须为linux
        """
        return self.send(keypair_attach_ecs_request_param)

    def ecs_disk_list_by_ecs_ids(self, ecs_disk_list_by_ecs_ids_request_param):
        """
        /v4/ecs/disk/list-by-ecs-ids
        查询云硬盘列表。**注意**：请求asc，sort 字段不支持，返回字段diskMode未对齐，encrypted字段不支持,暂为默认值
        """
        return self.send(ecs_disk_list_by_ecs_ids_request_param)

    def snapshot_policy_bind_instances(self, snapshot_policy_bind_instances_request_param):
        """
        /v4/ecs/snapshot-policy/bind-instances
        快照策略绑定云主机
        """
        return self.send(snapshot_policy_bind_instances_request_param)

    def ecs_host_details(self, ecs_host_details_request_param):
        """
        /v4/hosts/host-details
        查询宿主机详情
        """
        return self.send(ecs_host_details_request_param)

    def unassign_ipv6_from_port(self, unassign_ipv6_from_port_request_param):
        """
        /v4/ecs/ports/unassign-ipv6
        单个网卡解绑多个 IPv6 地址
        """
        return self.send(unassign_ipv6_from_port_request_param)

    def port_create(self, port_create_request_param):
        """
        /v4/ecs/ports/create
        创建弹性网卡
        """
        return self.send(port_create_request_param)

    def ecs_keypair_delete(self, ecs_keypair_delete_request_param):
        """
        /v4/ecs/keypair/delete
        此接口供用户用来删除SSH密钥对。系统会根据您输入的SSH密钥对的名称删除对应的密钥对，并返回删除成功信息。   
    
        """
        return self.send(ecs_keypair_delete_request_param)

    def ecs_resubscribe(self, ecs_resubscribe_request_param):
        """
        /v4/ecs/resubscribe
        续订一台包周期的云主机
        """
        return self.send(ecs_resubscribe_request_param)

    def update_metadata(self, update_metadata_request_param):
        """
        /v4/ecs/metadata/update
        仅4.0支持，为云主机更新元数据，云主机需为运行中或者关机状态
        """
        return self.send(update_metadata_request_param)

    def delete_backup_policy(self, delete_backup_policy_request_param):
        """
        /v4/ecs/backup-policy/delete
        删除云主机备份策略
        """
        return self.send(delete_backup_policy_request_param)

    def ecs_query_snapshot(self, ecs_query_snapshot_request_param):
        """
        /v4/ecs/query_vm_snapshot
        统计云主机快照个数
        """
        return self.send(ecs_query_snapshot_request_param)

    def update_affinity_group(self, update_affinity_group_request_param):
        """
        /v4/ecs/affinity-group-update
        更新云主机组
        """
        return self.send(update_affinity_group_request_param)

    def vm_mem_history_metric_data(self, vm_mem_history_metric_data_request_param):
        """
        /v4/ecs/vm-mem-history-metric-data
        该接口不推荐使用。建议使用-->历史监控数据：云主机(/v4.1/monitor/query-vm-historymetricdata)   
    
        """
        return self.send(vm_mem_history_metric_data_request_param)

    def get_customer_resources(self, get_customer_resources_request_param):
        """
        /v4/region/customer-resources
        接口功能介绍：根据regionID查询用户已有资源   
    接口约束：保证输入的资源池id准确无误   
    注:    
    1.regionID不存在的/用户所属VDC未绑定指定资源池/用户所属VDC在指定资源池下无数据，已有资源均返回0；   
    2.本期根据对接需求，仅实现VM、Volume、Public_IP、BMS、Vm_Group五种资源数据。
        """
        return self.send(get_customer_resources_request_param)

    def instance_detach_sfs_v41(self, instance_detach_sfs_v41_request_param):
        """
        /v4/ecs/sfs/detach
        此接口提供用户实现云主机卸载一个或多个文件系统的功能(仅4.0支持)   
       
    1. 云主机须处于运行状态   
    2. 云主机和文件系统应属于同一个VPC   
    3. 云主机仅支持部分镜像类型挂载，windows镜像：windows server 2012 数据中心版 R2 64位中文版（主镜像）、windows server 2012 标准版 R2 64位中文版、windows server 2016 数据中心版 64位中文版、windows server 2019 数据中心版 64位中文版。linux镜像：CentOS-7.8-x86_64、CentOS-7.9-x86_64（主镜像）、 CentOS-8.0-x86_64、 CentOS-8.1-x86_64、 CentOS-8.2-x86_64、Ubuntu-18.04-x86_64、Ubuntu-20.04-x86_64、Ctyunos-2.0.1_220311-x86_64
        """
        return self.send(instance_detach_sfs_v41_request_param)

    def ecs_backup_batch_update(self, ecs_backup_batch_update_request_param):
        """
        /v4/ecs/backup-batch-update
        批量更改云主机备份名称和描述
        """
        return self.send(ecs_backup_batch_update_request_param)

    def send_file(self, send_file_request_param):
        """
        /v4/cloud-assistant/send-file
        调用此接口可以上传文件到弹性云主机、物理机内部   
    说明：仅支持批量上传文件到弹性云主机或物理机内部，不支持混合上传，仅支持Linux系统   
       
    接口约束   
    1）弹性云主机、物理机必须处于运行状态；   
    2）弹性云主机、物理机中必须安装天翼云云助手且服务处于运行状态。
        """
        return self.send(send_file_request_param)

    def ecs_backup_ecs_resource(self, ecs_backup_ecs_resource_request_param):
        """
        /v4/ecs/backup-instance-resource
        统计用户虚机盘总大小及备份总个数
        """
        return self.send(ecs_backup_ecs_resource_request_param)

    def ecs_query_async_result(self, ecs_query_async_result_request_param):
        """
        /v4/ecs/query-async-result
        该接口通过一个异步任务的jobID查询任务执行的结果。   
    
        """
        return self.send(ecs_query_async_result_request_param)

    def ecs_host_monitor(self, ecs_host_monitor_request_param):
        """
        /v4/monitor/ph
        查询宿主机信息及使用率
        """
        return self.send(ecs_host_monitor_request_param)

    def ecs_snapshot_update_new(self, ecs_snapshot_update_new_request_param):
        """
        /v4/ecs/snapshot/update
        更改云主机快照名称和描述
        """
        return self.send(ecs_snapshot_update_new_request_param)

    def ecs_keypair_create(self, ecs_keypair_create_request_param):
        """
        /v4/ecs/keypair/create
        此接口用来创建一对SSH密钥对。系统会为您保管密钥的公钥部分，并返回未加密私钥。您需要自行妥善保管私钥部分。   
    
        """
        return self.send(ecs_keypair_create_request_param)

    def modify_instance_type_spec(self, modify_instance_type_spec_request_param):
        """
        /v4/ecs/flavor/spec-update
        设置云主机实例规格额外属性
        """
        return self.send(modify_instance_type_spec_request_param)

    def list_flavor(self, list_flavor_request_param):
        """
        /v4/ecs/flavor/list
        该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息,并允许用户根据云主机规格的特殊字段进行筛选。用户可以根据此接口的返回值了解自己可使用的云主机规格有哪些。   
    **注意**： 如果您传了flavorID 则azName 为必填。如果只传regionID 则可查询所有数据，azName不是必填的   
    
        """
        return self.send(list_flavor_request_param)

    def assign_ipv6_to_port(self, assign_ipv6_to_port_request_param):
        """
        /v4/ecs/ports/assign-ipv6
        单个网卡关联多个IPv6地址
        """
        return self.send(assign_ipv6_to_port_request_param)

    def ecs_status_list(self, ecs_status_list_request_param):
        """
        /v4/ecs/status-list
        获取多台云主机的状态信息   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
        """
        return self.send(ecs_status_list_request_param)

    def o_a_get_utility_ecs(self, o_a_get_utility_ecs_request_param):
        """
        /v4/report/utility/ecs
        2.2.5版本上线
        """
        return self.send(o_a_get_utility_ecs_request_param)

    def ecs_type_families(self, ecs_type_families_request_param):
        """
        /v4/ecs/type-families
        该接口提供用户可用规格族列表查询功能，每种规格族代表不同种类的云主机规格，用户可以根据此接口的返回值了解自己可使用的规格族有哪些。    
    规格族说明如下：    
    云主机-二代机：X86云主机,包含通用型s2、内存优化型m2。s2、m2实例规格簇均为cpu共享型，上线时间较早。    
    云主机-三代机：X86云主机,包含通用型S3、计算增强型c3、内存优化型m3。S3实例规格簇为cpu共享型，c3、m3实例规格簇为cpu独享,软硬件升级，性能增强。    
    云主机-六代机：X86云主机,包含通用型s6、通用计算增强c6、内存优化型m6。S6实例规格簇为cpu共享型，c6、m6实例规格簇为cpu独享,性能优良，能承载不同业务需求。    
    云主机-七代机：X86云主机,包含通用型s7、通用计算增强c7、内存优化型m7。通用型S7实例规格簇为cpu共享型，c7、m7实例规格簇为cpu独享,提供更大规格更优性能，能满足更高业务需要。    
    国产化云主机：X86与ARM云主机,包含鲲鹏计算增强型kc1、海光计算增强型hc1、飞腾计算增强型fc1、鲲鹏内存优化型km1、海光内存优化型hm1、飞腾内存优化型fm1，对安全性有较高要求的政府或企业应用。    
    本地盘云主机：X86云主机，包含云主机规格（ip3），提供数据盘为本地盘的云主机。    
    GPU云主机：包含图形加速基础型G5、图形加速基础型G7；计算加速型P2V、计算加速型PI7、计算加速型P8A、计算加速型PS4、计算加速型PI3、计算加速型PI2；图形加速基础型G6、图形加速基础型G7。
        """
        return self.send(ecs_type_families_request_param)

    def ecs_backup_restore(self, ecs_backup_restore_request_param):
        """
        /v4/ecs/backup-restore
        恢复云主机备份到源云主机实例   
       
    底层暂时只支持返回：云主机备份恢复对应的异步任务uuid
        """
        return self.send(ecs_backup_restore_request_param)

    def query_ecs_remaining_count(self, query_ecs_remaining_count_request_param):
        """
        /v4/ecs/query-remaining-count
           
    通过指定资源池、可用区、规格，查询理想余量情况
        """
        return self.send(query_ecs_remaining_count_request_param)

    def ecs_attach_delegate(self, ecs_attach_delegate_request_param):
        """
        /v4/ecs/delegate/attach
        接口功能介绍：该接口提供用户云主机绑定委托能力，委托信息将以用户元数据数据形式存入   
    接口约束：   
    	确保当前请求资源池下，该云主机存在（即instanceID真实存在且与regionID相对应）   
    	确保委托名称（delegateName）对应委托存在   
    	云主机只有在运行（running）或关机（stopped）状态才可执行该操作   
    	目前该功能仅支持多可用区类型资源池
        """
        return self.send(ecs_attach_delegate_request_param)

    def reset_password(self, reset_password_request_param):
        """
        /v4/ecs/reset-password
        更新云主机的密码,此接口为同步接口。   
       
    ### 接口约束   
       
    1. 云主机必须处于运行状态   
    
        """
        return self.send(reset_password_request_param)

    def local_disk_extend(self, local_disk_extend_request_param):
        """
        /v4/ecs/localdisk/extend
        1 只支持单个本地盘扩容操作，不支持并发扩容，建议调用侧编排1个虚机上多块本地盘顺序扩容。   
    2 预占扩容：之前通过预占接口预占过空间，会校验传入localDiskSize是否等于原大小+预占大小。   
    3 直接扩容：之前未执行过预占，直接以传入localDiskSize为准，需大于原大小。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.CommonInternalError -- 内部错误
        """
        return self.send(local_disk_extend_request_param)

    def ecs_vnc_show(self, ecs_vnc_show_request_param):
        """
        /v4/ecs/vnc-show
        #### 调用VNC OpenAPI接口获取Token   
    * 调用接口获取Token信息， token 信息就是websocket协议访问地址。   
    1. 使用noVNC等client进行访问，以noVNC为例，具体操作步骤如下：   
       
      -  本地启动noVNC服务，打开vnc页面；   
      -  点击左侧`⚙`，打开`高级`-`WebSocket`，在`主机`中，填写协议的地址   
      -  点击右侧连接按钮，即可访问   
       
    2.若要直接使用返回信息进行vnc远程登录，需保证调用方所在的浏览器中可访问到云管系统登录地址，并使用拼接后的完整地址访问：   
       
    完整访问地址为：wss://云管系统登录地址ip:端口+该接口返回的所有内容；   
       
    协议使用wss/ws取决于是云管访问是https还是http；   
       
    拼接的完整地址示例：wss://10.246.81.250:40117/osnmvnc1/ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE3Njc3NzgsImlhdCI6MTc0MTc2NDE3OCwidXNlcl9pZCI6IjYwNGFiOTdmYjg0NDYxMWU5MzViOWI3OTYxZmIyMTc5IiwicHJvamVjdF9pZCI6IjEzNTE2MWMyYTZkNzkwYzg0YzczYTQ3MDI0MjJlZGNmIiwiZG9tYWluX2lkIjoiZGVmYXVsdCIsInJvbGVzIjpbInVzZXIiXSwiY29uc3VtZXJfaWQiOiIiLCJpc3N1ZWRfYXQiOiIyMDI1LTAzLTEyVDA3OjIyOjU4LjAwMDAwMFoiLCJleHBpcmVfYXQiOiIyMDI1LTAzLTEyVDA4OjIyOjU4LjAwMDAwMFoiLCJNZXRob2QiOlsicGFzc3dvcmQiXX0.fdqxwwXDEAVSXUbu2m3D06hMwqK49mABYAXSKGcxCPQ&instanceId=6cf210e3-7f20-84f7-4eb3-a3b6399f42a3   
       
    接口调通之后会返回VNC的登录页面。   
       
    若调用websocket接口返回403，可在调用接口时headers里增加如下参数：   
    Pragma: no-cache   
    Cache-Control: no-cache   
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36   
    Origin: https://云管系统登录地址ip:端口   
    Accept-Encoding: gzip, deflate, br, zstd   
    
        """
        return self.send(ecs_vnc_show_request_param)

    def region_customer_quotas(self, region_customer_quotas_request_param):
        """
        /v4/region/customer-quotas
        接口功能介绍：根据regionID查询用户配额   
    接口约束：保证输入的资源池id准确无误   
    注:    
    1.region未开启配额的，返回公有云默认配额数；   
    2.本期根据对接需求，2.2.4 版本仅实现vm_limit、memory_limit、vcpu_limit、pm_limit_per_platform、volume_size_limit、total_volume_limit六种资源的配额动态查询，其余返回公有云默认配额数。
        """
        return self.send(region_customer_quotas_request_param)

    def ecs_status_sync(self, ecs_status_sync_request_param):
        """
        /v4/ecs/sync
        云主机同步状态
        """
        return self.send(ecs_status_sync_request_param)

    def resize_instance(self, resize_instance_request_param):
        """
        /v4/ecs/resize
        支持对一台已经关机中的云主机进行规格变更   
       
    ### 接口约束   
       
    1. 目标云主机处于关机中   
    2. 仅支持规格向高配变更
        """
        return self.send(resize_instance_request_param)

    def snapshot_policy_instance_list(self, snapshot_policy_instance_list_request_param):
        """
        /v4/ecs/snapshot-policy/instance-list
        查询快照策略绑定云主机列表
        """
        return self.send(snapshot_policy_instance_list_request_param)

    def ecs_backup_ecs_total_volume_size(self, ecs_backup_ecs_total_volume_size_request_param):
        """
        /v4/ecs/backup-instance-total-volume-size
        云主机备份查询虚机磁盘大小
        """
        return self.send(ecs_backup_ecs_total_volume_size_request_param)

    def modify_command(self, modify_command_request_param):
        """
        /v4/cloud-assistant/modify-command
        调用此接口可以修改用户自己创建的云助手命令内容、命令参数等信息
        """
        return self.send(modify_command_request_param)

    def affinity_groupbind_instance_check_v41(self, affinity_groupbind_instance_check_v41_request_param):
        """
        /v4/ecs/affinity-group/bind-instance-check
        接口功能介绍   
    可以根据用户给定的云主机与云主机组，校验当前情况下是否可以将云主机加入主机组。如果可以则返回值中needMigrate字段为0，反之则需要将云主机迁移。   
       
    接口约束   
    当前页面接口为旧版 API，未来根据实际使用情况可能退役，推荐使用新版本接口，新版本接口更加规范，覆盖场景更全。   
    云主机需处于运行中（running）或关机（stopped）状态
        """
        return self.send(affinity_groupbind_instance_check_v41_request_param)

    def ecs_batch_stop(self, ecs_batch_stop_request_param):
        """
        /v4/ecs/batch-stop
        停止一台或多台实例
        """
        return self.send(ecs_batch_stop_request_param)

    def ecs_backup_status(self, ecs_backup_status_request_param):
        """
        /v4/ecs/backup-status
        查询云主机备份状态
        """
        return self.send(ecs_backup_status_request_param)

    def query_ecs_local_disk(self, query_ecs_local_disk_request_param):
        """
        /v4/ecs/localdisk
        statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.Ecs.NotFound -- 非法的云主机   
    Compute.CommonInternalError -- 内部错误
        """
        return self.send(query_ecs_local_disk_request_param)

    def run_command(self, run_command_request_param):
        """
        /v4/cloud-assistant/run-command
        调用此接口在一台或多台弹性云主机或物理机中执行一段Shell、PowerShell、Bat或Python类型的脚本命令   
    接口约束：   
    1.弹性云主机、物理机必须处于运行状态；   
    2.弹性云主机、物理机中必须安装天翼云云助手且服务处于运行状态；
        """
        return self.send(run_command_request_param)

    def resize_backup_repo(self, resize_backup_repo_request_param):
        """
        /v4/ecs/backup-repo/upgrade
        扩容云主机备份存储库   
    size：混合云是增量大小，与公有云不一致
        """
        return self.send(resize_backup_repo_request_param)

    def invoke_command(self, invoke_command_request_param):
        """
        /v4/cloud-assistant/invoke-command
        调用此接口为一台或多台弹性云主机或物理机触发一条云助手命令   
    说明：仅支持批量为弹性云主机或物理机触发云助手命令，不支持混合触发   
       
    接口约束   
    1.弹性云主机、物理机必须处于运行状态   
    2.弹性云主机、物理机中必须安装天翼云云助手且服务处于运行状态
        """
        return self.send(invoke_command_request_param)

    def ports_unassign_secondaryprivateips_v41(self, ports_unassign_secondaryprivateips_v41_request_param):
        """
        /v4/ecs/ports/unassign-secondary-private-ips
        单个网卡解绑多个 IPv6 地址
        """
        return self.send(ports_unassign_secondaryprivateips_v41_request_param)

    def ecs_affinity_group_get(self, ecs_affinity_group_get_request_param):
        """
        /v4/ecs/affinity-group-get
        可以根据用户给定的云主机，查询云主机所在的云主机组信息
        """
        return self.send(ecs_affinity_group_get_request_param)

    def ecs_status(self, ecs_status_request_param):
        """
        /v4/ecs/ecs-status
        获取一组云主机的状态   
    1.16版本之前云主机状态:   
    Backuping:备份中,   
    Creating:创建中,   
    EXPIRED:已到期,   
    Rebuilding:重装,   
    Restarting:重启中,   
    ACTIVE:运行中，   
    Starting:开机中,   
    SHUTOFF:已关机,   
    Stopping:关机中,   
    ERROR:错误,   
    SNAPSHOTING:快照创建中   
       
    1.16版本之后云主机状态:   
    backingup: 备份中，   
    creating: 创建中，   
    expired: 已到期，   
    freezing: 冻结中，   
    rebuild: 重装   
    restarting: 重启中，   
    running: 运行中,   
    starting: 开机中，   
    stopped: 已关机，   
    stopping: 关机中，   
    error: 错误，ERROR   
    snapshotting: 快照创建中
        """
        return self.send(ecs_status_request_param)

    def snapshot_list(self, snapshot_list_request_param):
        """
        /v4/ecs/snapshot/list
        查询云主机快照列表
        """
        return self.send(snapshot_list_request_param)

    def local_disk_extend_occupy(self, local_disk_extend_occupy_request_param):
        """
        /v4/ecs/localdisk/extend-occupy
        1 支持一次预占多个AZ下多个虚机的多个本地盘，部分失败会回滚所有已成功的预占。   
    2 本地盘状态为已预占状态occupied时，不能再次发起预占。   
    3 传入localDisizeSize为扩容后的盘大小。   
       
    statusCode=800是正常返回，900接口报错。   
    [errorCode]   
    Compute.RegionNotFound -- 非法的资源池   
    Compute.Param.Error -- 参数错误   
    Compute.LocalDisk.NotFound -- 非法的本地盘   
    Compute.LocalDisk.OccupyFailed -- 预占失败   
    Compute.CommonInternalError -- 内部错误
        """
        return self.send(local_disk_extend_occupy_request_param)

    def vm_disk_history_metric_data(self, vm_disk_history_metric_data_request_param):
        """
        /v4/ecs/vm-disk-history-metric-data
        该接口不推荐使用。建议使用-->历史监控数据：云主机(/v4.1/monitor/query-vm-historymetricdata)   
    
        """
        return self.send(vm_disk_history_metric_data_request_param)

    def share_interface_attach(self, share_interface_attach_request_param):
        """
        /v4/ecs/share-interface/attach
        给云主机添加共享网卡
        """
        return self.send(share_interface_attach_request_param)

    def query_ecs_snapshot_policy_list_vdc(self, query_ecs_snapshot_policy_list_vdc_request_param):
        """
        /v4/ecs/snapshot-policy/list-vdc
        该接口1.16.06及以上云管版本支持。
        """
        return self.send(query_ecs_snapshot_policy_list_vdc_request_param)

    def list_instance_sfs_v41(self, list_instance_sfs_v41_request_param):
        """
        /v4/ecs/sfs/list
        可以根据虚机查询绑定的文件系统列表(仅4.0支持)
        """
        return self.send(list_instance_sfs_v41_request_param)

    def backup_policy_list_instances(self, backup_policy_list_instances_request_param):
        """
        /v4/ecs/backup-policy/list-instances
        查询云主机备份策略绑定云主机信息
        """
        return self.send(backup_policy_list_instances_request_param)

    def create_repo(self, create_repo_request_param):
        """
        /v4/ecs/backup-repo/create
        创建云主机备份存储库   
    1.目前不支持autoRenewStatus（是否自动续订）字段   
    2.底层size属性不支持默认，需要必传   
       
    
        """
        return self.send(create_repo_request_param)

    def rebuild_instance(self, rebuild_instance_request_param):
        """
        /v4/ecs/rebuild-instance
        该接口提供用户重装一台云主机功能，通过填写相应云主机ID、镜像ID，您可以调用[imageID](https://www.ctyun.cn/document/10026730/10040588)查看最新的天翼云具体资源池的镜像列表和密码对云主机进行重装。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    2. 云主机不能存在快照
        """
        return self.send(rebuild_instance_request_param)

    def ecs_snapshot_details(self, ecs_snapshot_details_request_param):
        """
        /v4/ecs/snapshot-details
        查询云主机快照详情   
    1.14返回:   
    {   
    	"description": "成功",   
    	"errorCode": "SUCCESS",   
    	"message": "success",   
    	"returnObj": [   
    		{   
    			"azName": "az3",   
    			"createAt": "2023-04-10T09:39:16.444482Z",   
    			"customerID": 2065,   
    			"description": "",   
    			"instanceID": "e993eff4-12c3-23cf-6a5a-196bb235496a",   
    			"instanceSnapshotName": "ecs-snapshot-041001",   
    			"instanceStatus": "ACTIVE",   
    			"isMaz": false,   
    			"isPaas": false,   
    			"members": [   
    				{   
    					"isBootable": false,   
    					"isEncrypted": false,   
    					"snapshotID": "d2cfda04-dae6-40b0-9375-07a778cb0a92",   
    					"snapshotStatus": "available",   
    					"volumeID": "2ac4d787-3812-4818-a3ce-8fa0b58c47ec",   
    					"volumeName": "hytest-022801-data-1",   
    					"volumeSize": 20,   
    					"volumeTypeName": "SAS-public"   
    				},   
    				{   
    					"isBootable": true,   
    					"isEncrypted": false,   
    					"snapshotID": "a0505d41-b217-4372-8233-87e40e6fe51a",   
    					"snapshotStatus": "available",   
    					"volumeID": "0f8c9554-f762-4c50-8cb0-99af02a0c7fe",   
    					"volumeName": "hytest-022801-volume-000",   
    					"volumeSize": 40,   
    					"volumeTypeName": "SAS-public"   
    				}   
    			],   
    			"snapshotID": "04294618-c941-8ba7-dee7-c8d19f3bf14d",   
    			"status": "available",   
    			"updateAt": "2023-04-10T09:41:06.620707Z"   
    		}   
    	],   
    	"statusCode": 800   
    }   
    1.15版本返回:   
    {   
    	"description": "成功 X-Trace-ID-->a685899ccbbe2f37",   
    	"errorCode": "SUCCESS",   
    	"message": "success",   
    	"returnObj": {   
    		"totalPage": 1,   
    		"currentCount": 1,   
    		"totalCount": 1,   
    		"results": [   
    			{   
    				"azName": "az1",   
    				"createAt": "2024-01-01T07:00:02.515775Z",   
    				"customerID": 1000000957,   
    				"instanceID": "f4f7bf5d-f592-32df-92ec-0b417ef6f650",   
    				"instanceSnapshotName": "auto_vm_snap-87aa04fb-20240101070000-s814",   
    				"instanceStatus": "SHUTOFF",   
    				"isMaz": false,   
    				"isPaas": false,   
    				"members": [],   
    				"snapshotID": "3b6be2a8-3e47-e82b-cb22-daa78a20a6e7",   
    				"status": "available",   
    				"updateAt": "2024-01-02T02:46:21.953592Z"   
    			}   
    		]   
    	},   
    	"statusCode": 800   
    }
        """
        return self.send(ecs_snapshot_details_request_param)

    def create_backup_policy(self, create_backup_policy_request_param):
        """
        /v4/ecs/backup-policy/create
        创建云主机备份策略
        """
        return self.send(create_backup_policy_request_param)

    def ecs_snapshot_update(self, ecs_snapshot_update_request_param):
        """
        /v4/ecs/snapshot-update
        更改云主机快照名称和描述
        """
        return self.send(ecs_snapshot_update_request_param)

    def reboot_instance(self, reboot_instance_request_param):
        """
        /v4/ecs/reboot-instance
        该接口提供用户重启一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
        """
        return self.send(reboot_instance_request_param)

    def vm_mem_latest_metric_data(self, vm_mem_latest_metric_data_request_param):
        """
        /v4/ecs/vm-mem-latest-metric-data
        注：该接口不推荐使用。建议使用-->实时监控数据：云主机(/v4.1/monitor/query-vm-latestmetricdata)
        """
        return self.send(vm_mem_latest_metric_data_request_param)

    def set_ecs_storage_pool_capacity_alert_threshold(self, set_ecs_storage_pool_capacity_alert_threshold_request_param):
        """
        /v4/ecs/backup-repo/set-capacity-alert-threshold
        2.2.6新增
        """
        return self.send(set_ecs_storage_pool_capacity_alert_threshold_request_param)

    def resubscribe_instance(self, resubscribe_instance_request_param):
        """
        /v4/ecs/resubscribe-instance
        续订一台包周期的云主机
        """
        return self.send(resubscribe_instance_request_param)

    def delete_port(self, delete_port_request_param):
        """
        /v4/ecs/ports/delete
        删除弹性网卡
        """
        return self.send(delete_port_request_param)

    def ecs_keypair_detach(self, ecs_keypair_detach_request_param):
        """
        /v4/ecs/keypair/detach
        为Linux云主机解绑SSH密钥对   
       
    ### 接口约束   
    1.云主机必须存在，2 云主机状态必须是运行中，3 云主机操作系统必须为linux，4 密钥对名称必须存在，5 云主机必须已经绑定了此密钥对
        """
        return self.send(ecs_keypair_detach_request_param)

    def get_ins_backup_list_by_vdc(self, get_ins_backup_list_by_vdc_request_param):
        """
        /v4/ecs/backup/list-vdc
        查询云主机备份列表   
    
        """
        return self.send(get_ins_backup_list_by_vdc_request_param)

    def snapshot_policy_create(self, snapshot_policy_create_request_param):
        """
        /v4/ecs/snapshot-policy/create
        创建云主机快照策略
        """
        return self.send(snapshot_policy_create_request_param)

    def live_resize_instance_v41(self, live_resize_instance_v41_request_param):
        """
        /v4/ecs/live-resize
        该接口提供云主机热变配功能，即开机状态实现变更规格   
    准备工作：   
      构造请求：在调用前需要了解如何构造请求，详情查看构造请求   
      认证鉴权：openapi请求需要进行加密调用，详细查看认证鉴权   
    注意事项：   
      确认当前云主机是否可进行热变配，您可以通过接口查询云主机支持的热变配规格信息获取当前云主机是否可以进行热变配，以及可以热变配规格信息   
       
    热变配当前支持规格和镜像信息为（不同资源池下的镜像和规格支持情况不同，以查询云主机支持热变配规格信息接口的返回值为准）：   
    支持的云主机镜像：   
      CentOS：CentOS 7.6 64位、CentOS 7.8 64位、CentOS 7.9 64位、CentOS 8.0 64位、CentOS 8.1 64位、CentOS 8.2 64位、CentOS 8.4 64位   
      CTyunOS：CTyunOS 2.0.1-21.06.4 64位、CTyunOS 3-23.01 64位   
      KylinOS：KylinOS V10 SP1 64位、KylinOS V10 SP2 64位   
      其他：openEuler 22.03 SP2 64位、UnionTechOS V20 1050u1e 64位   
       
    支持的云主机规格：   
      除二代机以外的规格且vcpu≥32   
       
    #### 接口约束   
    1. 只支持升级规格，且不支持跨代升配（例如，原本云主机规格为m6.large.8，不可以变配为m7.xlarge.8）   
    2. 对于存量的云主机（2023年12月31日以前创建的云主机），无法使用当前功能   
    3. 同代升配能否支持取决于numa拓扑，以及CPU和内存均不能变小且至少有一个变大。   
    4. 当前云主机处于开机状态   
    5. 云主机已挂载的云硬盘状态不能处于“镜像制作中”
        """
        return self.send(live_resize_instance_v41_request_param)

    def ecs_hosts_statistics(self, ecs_hosts_statistics_request_param):
        """
        /v4/hosts/statistics
        查询资源池云主机、宿主机总数
        """
        return self.send(ecs_hosts_statistics_request_param)

    def query_resize_flavor(self, query_resize_flavor_request_param):
        """
        /v4/ecs/query-resize-flavor
        判断一台云主机是否可以通过指定规格进行变配
        """
        return self.send(query_resize_flavor_request_param)

    def renew_repo(self, renew_repo_request_param):
        """
        /v4/ecs/backup-repo/renew
        续订云主机备份存储库
        """
        return self.send(renew_repo_request_param)

    def list_repo(self, list_repo_request_param):
        """
        /v4/ecs/backup-repo/list
        查询云主机备份详情   
    
        """
        return self.send(list_repo_request_param)

    def ecs_batch_start(self, ecs_batch_start_request_param):
        """
        /v4/ecs/batch-start
        启动一台或多台实例
        """
        return self.send(ecs_batch_start_request_param)

    def ecs_snapshot_list(self, ecs_snapshot_list_request_param):
        """
        /v4/ecs/snapshot-list
        查询云主机快照列表
        """
        return self.send(ecs_snapshot_list_request_param)

    def availability_zones_details(self, availability_zones_details_request_param):
        """
        /v4/ecs/availability-zones/details
        查询账户指定资源池中可用区的信息
        """
        return self.send(availability_zones_details_request_param)

    def list_repo_by_vdc(self, list_repo_by_vdc_request_param):
        """
        /v4/ecs/backup-repo/list-vdc
        查询云主机备份详情   
    
        """
        return self.send(list_repo_by_vdc_request_param)

    def ecs_snapshot_delete(self, ecs_snapshot_delete_request_param):
        """
        /v4/ecs/snapshot-delete
        删除云主机快照
        """
        return self.send(ecs_snapshot_delete_request_param)

    def ecs_backup_ecs_query(self, ecs_backup_ecs_query_request_param):
        """
        /v4/ecs/backup-instance-query
        通过虚机ID获取虚拟机最新状态，主要获取虚拟机磁盘挂载信息
        """
        return self.send(ecs_backup_ecs_query_request_param)

    def backup_status(self, backup_status_request_param):
        """
        /v4/ecs/backup/status
        查询云主机备份状态   
    接口约束   
     1.云主机备份必须存在
        """
        return self.send(backup_status_request_param)

    def stop_instance(self, stop_instance_request_param):
        """
        /v4/ecs/stop-instance
        该接口提供用户关闭一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于开机状态。
        """
        return self.send(stop_instance_request_param)

    def ecs_disk_list(self, ecs_disk_list_request_param):
        """
        /v4/ecs/disk/list
        查询云硬盘列表。**注意**：请求asc，sort 字段不支持，返回字段diskMode未对齐，encrypted字段不支持,暂为默认值
        """
        return self.send(ecs_disk_list_request_param)

    def backup_batch_update(self, backup_batch_update_request_param):
        """
        /v4/ecs/backup/batch-update
        批量更改云主机备份名称和描述
        """
        return self.send(backup_batch_update_request_param)

    def delete_eip(self, delete_eip_request_param):
        """
        /v4/ecs/eip/delete
        调用此接口可删除 EIP。   
       
    ### 接口约束   
    待删除的EIP需未绑定任何云产品实例。
        """
        return self.send(delete_eip_request_param)

    def start_instance(self, start_instance_request_param):
        """
        /v4/ecs/start-instance
           
    该接口提供用户开启一台云主机功能。   
       
    ### 接口约束   
       
    1. 云主机需要处于关机状态。   
    
        """
        return self.send(start_instance_request_param)

    def vm_disk_latest_metric_data(self, vm_disk_latest_metric_data_request_param):
        """
        /v4/ecs/vm-disk-latest-metric-data
        注：该接口不推荐使用。建议使用-->实时监控数据：云主机(/v4.1/monitor/query-vm-latestmetricdata)   
    
        """
        return self.send(vm_disk_latest_metric_data_request_param)
