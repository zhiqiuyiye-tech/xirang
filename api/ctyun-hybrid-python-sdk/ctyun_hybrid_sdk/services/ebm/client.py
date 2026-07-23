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


class EbmClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ebm-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(EbmClient, self).__init__(credential, config, 'ebm', '0.1.0', logger, signer)

    def reboot_instances(self, reboot_instances_request_param):
        """
        /v4/ebm/reboot
        只有在running状态下才能重启，否则报错
        """
        return self.send(reboot_instances_request_param)

    def reset_password(self, reset_password_request_param):
        """
        /v4/ebm/change-password
        修改物理机登录密码
        """
        return self.send(reset_password_request_param)

    def query_instances(self, query_instances_request_param):
        """
        /v4/ebm/list
        查询物理机列表接口
        """
        return self.send(query_instances_request_param)

    def reinstall_instance(self, reinstall_instance_request_param):
        """
        /v4/ebm/rebuild
        物理机重装系统,**注意**： 混合云redoRaid不支持
        """
        return self.send(reinstall_instance_request_param)

    def renew_ebm(self, renew_ebm_request_param):
        """
        /v4/ebm/renew
        续订物理机
        """
        return self.send(renew_ebm_request_param)

    def ebm_delegate_create(self, ebm_delegate_create_request_param):
        """
        /v4/ebm/delegate/create
        接口约束：使用限制，本接口只支持在开启资源委托的4.0资源池使用
        """
        return self.send(ebm_delegate_create_request_param)

    def plus_list_instance(self, plus_list_instance_request_param):
        """
        /v4/ebm/list-instance
        物理机状态列表   
    status参数取值列表   
       
    序号	status	说明   
    1	CREATING	创建中   
    2	STARTING	启动中   
    3	RUNNING	运行中   
    4	STOPPING	关机中   
    5	STOPPED	已关机   
    6	RESTARTING	重启中   
    7	ERROR	故障中   
    8	REINSTALLING	重装系统中   
    9	MAINTAINING	维护中   
    10	RESETTING_PASSWORD	重置密码中   
    11	DELETE	删除   
    12	ADDACH_VOLUME_IN_RUNNING	运行状态挂载卷中   
    13	DETACH_VOLUME_IN_RUNNING	运行状态卸载卷中   
    14	ADDACH_VOLUME_IN_STOPPED	关机状态挂载卷中   
    15	DETACH_VOLUME_IN_STOPPED	关机状态卸载卷中   
    16	ADDING_NETWORK	添加网卡中   
    17	DELETING_NETWORK	删除网卡中   
    18	TRANSFERING	迁移中   
    19	EXPORT_IMAGE	导出镜像中   
    20	MODIFY_NETWORK	重置网络中   
    21	RESETTING_HOSTNAME	重置hostname中   
    22	UNSUBSCRIBING	包年包月物理机退订中   
    23	UNSUBSCRIBED	包年包月物理机已退订   
    RUNNING 运行中 可进行关机、重启操作、挂载卷、卸载卷、添加网卡、删除网卡   
    STOPPED 已关机 可进行开机、重装、重置密码、删除、挂载卷、卸载卷、添加网卡、删除网卡、重置内网IP   
    ERROR 故障 可进行删除操作   
    
        """
        return self.send(plus_list_instance_request_param)

    def start_instances(self, start_instances_request_param):
        """
        /v4/ebm/power-on
        物理机开机
        """
        return self.send(start_instances_request_param)

    def detach_ebm_volume(self, detach_ebm_volume_request_param):
        """
        /v4/ebm/detach-volume
        物理机卸载卷   
       
    注意：当资源池为3.0时，azName字段需填写default
        """
        return self.send(detach_ebm_volume_request_param)

    def delete_instances(self, delete_instances_request_param):
        """
        /v4/ebm/delete
        物理机退订，直接销毁 从底层删除，不进入回收站。   
    删除返回字段未对齐多resources   
    只有开机、关机、和错误状态下才能退订
        """
        return self.send(delete_instances_request_param)

    def query_devices_stock(self, query_devices_stock_request_param):
        """
        /v4/ebm/device-stock-list
        查询物理机库存
        """
        return self.send(query_devices_stock_request_param)

    def instance_device_type(self, instance_device_type_request_param):
        """
        /v4/ebm/instance-device-type
        根据实例ID查询对应套餐信息
        """
        return self.send(instance_device_type_request_param)

    def describe_bms_instance(self, describe_bms_instance_request_param):
        """
        /v4/ebm/describe
        通过参数查询单台物理机信息。混合云返回字段publicIpv6，privateIPv6,vipUUIDList,vipList未对齐
        """
        return self.send(describe_bms_instance_request_param)

    def instance_attached_volume_id_list(self, instance_attached_volume_id_list_request_param):
        """
        /v4/ebm/instance-attached-volume-id-list
        根据实例ID查询对应挂载卷ID 
        """
        return self.send(instance_attached_volume_id_list_request_param)

    def run_instances(self, run_instances_request_param):
        """
        /v4/ebm/create
        创建物理机，参数bandwidthType，ipv6Address未对齐   
    创建物理机有两种，一种是普通版一种是弹性。   
    通过deviceType的规格来区分普通版和弹性--调用/v4/ebm/device-type-list查询套餐信息(根据cloudBoot是否支持云盘启动来区分，支持的就是弹性的 不支持就是普通版)。   
    支持智能网卡的就用普通子网 不支持的用裸金属子网。   
    普通版的需要指定硬盘id(systemVolumeRaidUUID,dataVolumeRaidUUID),   
    弹性的需要创建云盘(diskList)。
        """
        return self.send(run_instances_request_param)

    def plus_describe_instance(self, plus_describe_instance_request_param):
        """
        /v4/ebm/describe-instance
        通过参数查询单台物理机信息，私有云中返回字段regionID，privateIPv6 私有云不支持返回。
        """
        return self.send(plus_describe_instance_request_param)

    def ebm_list_lite_vdc(self, ebm_list_lite_vdc_request_param):
        """
        /v4/ebm/list-lite-vdc
        裸金属轻量信息列表-vdc
        """
        return self.send(ebm_list_lite_vdc_request_param)

    def ecs_delete_delegate(self, ecs_delete_delegate_request_param):
        """
        /v4/ebm/delegate/delete
        接口约束：使用限制，本接口只支持在开启资源委托的4.0资源池使用
        """
        return self.send(ecs_delete_delegate_request_param)

    def ebm_delegate_list(self, ebm_delegate_list_request_param):
        """
        /v4/ebm/delegate/list
        接口约束：使用限制，本接口只支持在开启资源委托的4.0资源池使用
        """
        return self.send(ebm_delegate_list_request_param)

    def add_nic(self, add_nic_request_param):
        """
        /v4/ebm/add-nic
        添加物理机网卡   
    1.普通版不支持添加安全组   
    2.添加网卡需要关机状态   
    3.普通版本不支持添加网卡
        """
        return self.send(add_nic_request_param)

    def query_raid_types(self, query_raid_types_request_param):
        """
        /v4/ebm/raid-type-list
        查询物理机本地盘可选择的raid类型
        """
        return self.send(query_raid_types_request_param)

    def ebm_delegate_update(self, ebm_delegate_update_request_param):
        """
        /v4/ebm/delegate/update
        接口约束：使用限制，本接口只支持在开启资源委托的4.0资源池使用
        """
        return self.send(ebm_delegate_update_request_param)

    def metadata_batch_update(self, metadata_batch_update_request_param):
        """
        /v4/ebm/metadata/batch-update
        只有弹性裸金属制成元数据
        """
        return self.send(metadata_batch_update_request_param)

    def instance_image(self, instance_image_request_param):
        """
        /v4/ebm/instance-image
        根据实例ID查询所使用的镜像信息
        """
        return self.send(instance_image_request_param)

    def vnc(self, vnc_request_param):
        """
        /v4/ebm/vnc
        获取物理机实例vnc地址
        """
        return self.send(vnc_request_param)

    def attach_ebm_volume(self, attach_ebm_volume_request_param):
        """
        /v4/ebm/attach-volume
        物理机挂载卷：   
    1. 裸金属的底层设备类型必须支持云硬盘   
    2. 如果是3.0资源池，则必须先关机   
    3. 裸金属实例和云硬盘必须在一个可用区下
        """
        return self.send(attach_ebm_volume_request_param)

    def instance_interface_list(self, instance_interface_list_request_param):
        """
        /v4/ebm/instance-interface-list
        根据物理机实例UUID查询网卡信息列表。
        """
        return self.send(instance_interface_list_request_param)

    def metadata_list(self, metadata_list_request_param):
        """
        /v4/ebm/metadata/list
        查询物理机的元数据信息，只有4.0弹性裸金属才支持元数据，普通裸金属不支持
        """
        return self.send(metadata_list_request_param)

    def metadata_batch_create(self, metadata_batch_create_request_param):
        """
        /v4/ebm/metadata/batch-create
        只有弹性裸金属支持元数据
        """
        return self.send(metadata_batch_create_request_param)

    def stop_instances(self, stop_instances_request_param):
        """
        /v4/ebm/power-off
        物理机关机
        """
        return self.send(stop_instances_request_param)

    def create_ebm_instance(self, create_ebm_instance_request_param):
        """
        /v4/ebm/create-instance
        创建物理机
        """
        return self.send(create_ebm_instance_request_param)

    def update_security_group(self, update_security_group_request_param):
        """
        /v4/ebm/update-security-group
        更新物理机安全组
        """
        return self.send(update_security_group_request_param)

    def query_device_types(self, query_device_types_request_param):
        """
        /v4/ebm/device-type-list
        获取资源池内的物理机套餐信息
        """
        return self.send(query_device_types_request_param)

    def query_images(self, query_images_request_param):
        """
        /v4/ebm/image-list
        通过参数查询物理机可支持的镜像，查询条件 imageUUID，osName，osVersion不支持   
       
    bits返回类型与v1未对齐
        """
        return self.send(query_images_request_param)

    def remove_nic(self, remove_nic_request_param):
        """
        /v4/ebm/remove-nic
        删除物理机网卡
        """
        return self.send(remove_nic_request_param)
