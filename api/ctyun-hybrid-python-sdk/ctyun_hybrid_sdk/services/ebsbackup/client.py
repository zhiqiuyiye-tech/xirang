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


class EbsbackupClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ebsbackup-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(EbsbackupClient, self).__init__(credential, config, 'ebsbackup', '0.1.0', logger, signer)

    def list_backup_policy(self, list_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/list-policies
        查询云硬盘备份策略
        """
        return self.send(list_backup_policy_request_param)

    def list_backup_repo(self, list_backup_repo_request_param):
        """
        /v4/ebs-backup/repo/list-repos
        v2版本混合云管对过期状态存储库支持继续使用，故active对应可用状态存储库，expired对应禁用状态存储库   
    2.2.6版本新增支持返回容量告警阈值capacityAlertThreshold
        """
        return self.send(list_backup_repo_request_param)

    def list_storage_pool_s3_users(self, list_storage_pool_s3_users_request_param):
        """
        /v4/ebs-backup/repo/list-s3-users
        2.2.6新增   
    注：此接口只返回已与存储库关联的S3用户列表，而非全量。
        """
        return self.send(list_storage_pool_s3_users_request_param)

    def execute_ebs_backup_policy(self, execute_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/execute
        执行云硬盘备份策略。需要状态为启用，并绑定存储库和云硬盘   
    **注意**：（开发未对齐）混合云返回异步任务ID，公有云不返回参数
        """
        return self.send(execute_ebs_backup_policy_request_param)

    def ebs_backup_policy_unbind_disks(self, ebs_backup_policy_unbind_disks_request_param):
        """
        /v4/ebs-backup/policy/unbind-disks
        云硬盘备份策略解绑云硬盘
        """
        return self.send(ebs_backup_policy_unbind_disks_request_param)

    def create_ebs_backup(self, create_ebs_backup_request_param):
        """
        /v4/ebs-backup/create
        开发未对齐原因：混合云返回异步任务ID，公有云返回云硬盘备份对象
        """
        return self.send(create_ebs_backup_request_param)

    def update_ebs_backup_policy(self, update_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/update
        修改云盘备份策略   
    resourceCount代码暂未支持该属性
        """
        return self.send(update_ebs_backup_policy_request_param)

    def list_ebs_backup_repo(self, list_ebs_backup_repo_request_param):
        """
        /v4/ebs-backup/repo/list
        v2版本混合云管对过期状态存储库支持继续使用，故active对应可用状态存储库，expired对应禁用状态存储库；兼容v1接口，available-可用;unavailable-禁用；     
       
    v2排序不支持usedSize   
    2.2.6版本新增支持返回容量告警阈值capacityAlertThreshold   
    
        """
        return self.send(list_ebs_backup_repo_request_param)

    def list_ebs_backup_vdc(self, list_ebs_backup_vdc_request_param):
        """
        /v4/ebs-backup/list-vdc
        查询云硬盘备份列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
        """
        return self.send(list_ebs_backup_vdc_request_param)

    def resize_repo(self, resize_repo_request_param):
        """
        /v4/ebs-backup/repo/resize
        扩容云硬盘备份存储库   
    size：混合云是增量大小，与公有云不一致
        """
        return self.send(resize_repo_request_param)

    def show_ebs_backup_policy_task(self, show_ebs_backup_policy_task_request_param):
        """
        /v4/ebs-backup/policy/show-task
        查询备份策略创建的备份任务
        """
        return self.send(show_ebs_backup_policy_task_request_param)

    def list_ebs_backup_policy_tasks(self, list_ebs_backup_policy_tasks_request_param):
        """
        /v4/ebs-backup/policy/list-tasks
        查询备份策略创建的备份任务列表
        """
        return self.send(list_ebs_backup_policy_tasks_request_param)

    def ebs_backup_policy_unbind_volumes(self, ebs_backup_policy_unbind_volumes_request_param):
        """
        /v4/ebs-backup/policy/unbind-volumes
        云盘备份策略解绑云硬盘
        """
        return self.send(ebs_backup_policy_unbind_volumes_request_param)

    def list_ebs_backup_policy(self, list_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/list
        参数返回和v1未对齐，v1返回列表为returnObj.results，v2实现对齐公有云使用returnObj.policyList
        """
        return self.send(list_ebs_backup_policy_request_param)

    def ebs_backup_policy_unbind_repo(self, ebs_backup_policy_unbind_repo_request_param):
        """
        /v4/ebs-backup/policy/unbind-repo
        云盘备份策略解绑备份库
        """
        return self.send(ebs_backup_policy_unbind_repo_request_param)

    def show_backup(self, show_backup_request_param):
        """
        /v4/ebs-backup/show-backup
        查询云硬盘备份信息详情_新
        """
        return self.send(show_backup_request_param)

    def list_backup(self, list_backup_request_param):
        """
        /v4/ebs-backup/list-backups
        目前 diskType(云硬盘类型) 底层返回和公有云文档对不齐   
    encrypted（云硬盘是否加密）底层没有该字段无法对齐
        """
        return self.send(list_backup_request_param)

    def list_ebs_backup_policy_vdc(self, list_ebs_backup_policy_vdc_request_param):
        """
        /v4/ebs-backup/policy/list-vdc
        查询云硬盘备份策略列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
        """
        return self.send(list_ebs_backup_policy_vdc_request_param)

    def delete_ebs_backup(self, delete_ebs_backup_request_param):
        """
        /v4/ebs-backup/delete
        开发未对齐原因：混合云返回删除信息，公有云不返回参数
        """
        return self.send(delete_ebs_backup_request_param)

    def renew_repo(self, renew_repo_request_param):
        """
        /v4/ebs-backup/repo/renew
        续订云硬盘备份存储库
        """
        return self.send(renew_repo_request_param)

    def ebs_backup_policy_bind_repo(self, ebs_backup_policy_bind_repo_request_param):
        """
        /v4/ebs-backup/policy/bind-repo
        云盘备份策略绑定备份库
        """
        return self.send(ebs_backup_policy_bind_repo_request_param)

    def delete_ebs_backup_policy(self, delete_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/delete
        删除云盘备份策略
        """
        return self.send(delete_ebs_backup_policy_request_param)

    def ebs_backup_policy_bind_disks(self, ebs_backup_policy_bind_disks_request_param):
        """
        /v4/ebs-backup/policy/bind-disks
        云硬盘备份策略绑定云硬盘
        """
        return self.send(ebs_backup_policy_bind_disks_request_param)

    def set_storage_pool_capacity_alert_threshold(self, set_storage_pool_capacity_alert_threshold_request_param):
        """
        /v4/ebs-backup/repo/set-capacity-alert-threshold
        2.2.6新增
        """
        return self.send(set_storage_pool_capacity_alert_threshold_request_param)

    def query_backup_task_list(self, query_backup_task_list_request_param):
        """
        /v4/ebs-backup/task/list-task
        查询云硬盘备份任务列表
        """
        return self.send(query_backup_task_list_request_param)

    def create_repo(self, create_repo_request_param):
        """
        /v4/ebs-backup/repo/create
        创建云硬盘备份存储库   
    1.目前不支持autoRenewStatus（是否自动续订）字段   
    2.底层size属性不支持默认，需要必传
        """
        return self.send(create_repo_request_param)

    def list_ebs_backup(self, list_ebs_backup_request_param):
        """
        /v4/ebs-backup/list
        可选参数 暂时不添加示例值   
    推荐使用 /v4/ebs-backup/list-backups 接口
        """
        return self.send(list_ebs_backup_request_param)

    def restore_backup(self, restore_backup_request_param):
        """
        /v4/ebs-backup/restore-backup
        ###### 云硬盘备份恢复：是指将备份的内容恢复到磁盘里，不是恢复被删的备份   
    开发未对齐原因：混合云返回异步任务ID，公有不返回
        """
        return self.send(restore_backup_request_param)

    def disable_ebs_backup_policy(self, disable_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/disable
        停用云硬盘备份策略
        """
        return self.send(disable_ebs_backup_policy_request_param)

    def restore_ebs_backup(self, restore_ebs_backup_request_param):
        """
        /v4/ebs-backup/restore
        开发未对齐原因：混合云返回异步任务ID，公有不返回
        """
        return self.send(restore_ebs_backup_request_param)

    def create_backup(self, create_backup_request_param):
        """
        /v4/ebs-backup/create-backup
        开发未对齐原因：混合云返回异步任务ID，公有云返回云硬盘备份对象
        """
        return self.send(create_backup_request_param)

    def list_ebs_backup_policy_disks(self, list_ebs_backup_policy_disks_request_param):
        """
        /v4/ebs-backup/policy/list-disks
        diskMode（云硬盘模式） 未对齐
        """
        return self.send(list_ebs_backup_policy_disks_request_param)

    def show_ebs_backup_usage(self, show_ebs_backup_usage_request_param):
        """
        /v4/ebs-backup/usage
        查看云硬盘备份的存储占用大小
        """
        return self.send(show_ebs_backup_usage_request_param)

    def delete_repo(self, delete_repo_request_param):
        """
        /v4/ebs-backup/repo/delete
        退订云硬盘备份存储库
        """
        return self.send(delete_repo_request_param)

    def list_ebs_backup_repo_vdc(self, list_ebs_backup_repo_vdc_request_param):
        """
        /v4/ebs-backup/repo/list-vdc
        查询云硬盘备份库列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。   
    2.2.6版本新增支持返回容量告警阈值capacityAlertThreshold
        """
        return self.send(list_ebs_backup_repo_vdc_request_param)

    def enable_ebs_backup_policy(self, enable_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/enable
        启用云硬盘备份策略
        """
        return self.send(enable_ebs_backup_policy_request_param)

    def ebs_backup_policy_bind_volumes(self, ebs_backup_policy_bind_volumes_request_param):
        """
        /v4/ebs-backup/policy/bind-volumes
        云硬盘只能绑定一个备份策略，如果一个云硬盘已经绑定了备份策略，再次调用该接口绑定新的备份策略，旧的备份策略会自动解绑。云硬盘和备份策略需要是同一所属用户。
        """
        return self.send(ebs_backup_policy_bind_volumes_request_param)

    def update_ebs_backup_repo(self, update_ebs_backup_repo_request_param):
        """
        /v4/ebs-backup/repo/update
        更新云硬盘备份存储库信息
        """
        return self.send(update_ebs_backup_repo_request_param)

    def show_ebs_backup(self, show_ebs_backup_request_param):
        """
        /v4/ebs-backup/show
        云硬盘备份详情查询
        """
        return self.send(show_ebs_backup_request_param)

    def create_ebs_backup_policy(self, create_ebs_backup_policy_request_param):
        """
        /v4/ebs-backup/policy/create
        创建云硬盘备份策略
        """
        return self.send(create_ebs_backup_policy_request_param)
