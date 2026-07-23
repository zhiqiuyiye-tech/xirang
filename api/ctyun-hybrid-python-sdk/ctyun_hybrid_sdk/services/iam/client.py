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


class IamClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('iam-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(IamClient, self).__init__(credential, config, 'iam', '0.1.0', logger, signer)

    def delete_iam_strategy(self, delete_iam_strategy_request_param):
        """
        /v1/policy/iam/deleteStrategy
        删除策略-IAM
        """
        return self.send(delete_iam_strategy_request_param)

    def get_groups_openapi_hub(self, get_groups_openapi_hub_request_param):
        """
        /v1/user/hub/get-user-groups
        查询用户组列表-hub
        """
        return self.send(get_groups_openapi_hub_request_param)

    def openapi_create_service(self, openapi_create_service_request_param):
        """
        /v1/service/createService
        服务管理创建
        """
        return self.send(openapi_create_service_request_param)

    def delete_enterprise_project(self, delete_enterprise_project_request_param):
        """
        /v1/project/deleteEnterpriseProject
        删除企业项目
        """
        return self.send(delete_enterprise_project_request_param)

    def list_i_a_m_users(self, list_i_a_m_users_request_param):
        """
        /v1/user/iam/list
        IAM认证-用户列表查询 
        """
        return self.send(list_i_a_m_users_request_param)

    def describe_iam_strategies(self, describe_iam_strategies_request_param):
        """
        /v1/policy/iam/queryStrategy
        获取策略列表-IAM
        """
        return self.send(describe_iam_strategies_request_param)

    def user_attach_user_to_group_hub(self, user_attach_user_to_group_hub_request_param):
        """
        /v1/user/hub/userSetGroup
        用户批量加入用户组,传入什么用户组id，用户就只拥有这些用户组id，用户不能加入的用户组会过滤掉
        """
        return self.send(user_attach_user_to_group_hub_request_param)

    def clone_vdc_user_group(self, clone_vdc_user_group_request_param):
        """
        /v1/vdc/clone-user-group
        克隆VDC用户组
        """
        return self.send(clone_vdc_user_group_request_param)

    def bind_i_a_m_user_group_strategies(self, bind_i_a_m_user_group_strategies_request_param):
        """
        /v1/userGroup/iam/bind-strategies
        IAM认证-用户组绑定策略
        """
        return self.send(bind_i_a_m_user_group_strategies_request_param)

    def openapi_update_service(self, openapi_update_service_request_param):
        """
        /v1/service/updateService
        服务管理编辑
        """
        return self.send(openapi_update_service_request_param)

    def iam_user_group_un_bind_user(self, iam_user_group_un_bind_user_request_param):
        """
        /v1/userGroup/iam/unbind-users
        IAM认证-用户组解绑用户
        """
        return self.send(iam_user_group_un_bind_user_request_param)

    def get_quota_state(self, get_quota_state_request_param):
        """
        /v1/quota/state
        获取租户(VDC)的配额是否开启
        """
        return self.send(get_quota_state_request_param)

    def list_vdc_user_groups(self, list_vdc_user_groups_request_param):
        """
        /v1/vdc/list-user-groups
        VDC用户组列表查询
        """
        return self.send(list_vdc_user_groups_request_param)

    def list_i_a_m_user_groups(self, list_i_a_m_user_groups_request_param):
        """
        /v1/userGroup/iam/list
        IAM认证-用户组列表查询
        """
        return self.send(list_i_a_m_user_groups_request_param)

    def create_i_a_m_user_group(self, create_i_a_m_user_group_request_param):
        """
        /v1/userGroup/iam/create
        IAM认证-用户组新增
        """
        return self.send(create_i_a_m_user_group_request_param)

    def openapi_update_permission(self, openapi_update_permission_request_param):
        """
        /v1/permission/updatePermission
        权限修改
        """
        return self.send(openapi_update_permission_request_param)

    def update_i_a_m_user_group(self, update_i_a_m_user_group_request_param):
        """
        /v1/userGroup/iam/update
        IAM认证-用户组编辑
        """
        return self.send(update_i_a_m_user_group_request_param)

    def lock_i_a_m_user(self, lock_i_a_m_user_request_param):
        """
        /v1/user/iam/lock
        IAM认证-用户锁定
        """
        return self.send(lock_i_a_m_user_request_param)

    def openapi_delete_service(self, openapi_delete_service_request_param):
        """
        /v1/service/deleteService
        服务管理删除
        """
        return self.send(openapi_delete_service_request_param)

    def bind_vdc_users_to_user_gourp(self, bind_vdc_users_to_user_gourp_request_param):
        """
        /v1/vdc/bind-users-to-user-group
        VDC用户组绑定用户
        """
        return self.send(bind_vdc_users_to_user_gourp_request_param)

    def describe_i_a_m_user_group_strategies(self, describe_i_a_m_user_group_strategies_request_param):
        """
        /v1/userGroup/iam/strategies
        IAM认证-用户组绑定策略查询
        """
        return self.send(describe_i_a_m_user_group_strategies_request_param)

    def list_vdc_users(self, list_vdc_users_request_param):
        """
        /v1/vdc/list-users
        VDC用户列表查询
        """
        return self.send(list_vdc_users_request_param)

    def add_vdc_user_group_permissions(self, add_vdc_user_group_permissions_request_param):
        """
        /v1/vdc/add-user-group-permissions
        VDC用户组绑定策略
        """
        return self.send(add_vdc_user_group_permissions_request_param)

    def update_iam_strategy(self, update_iam_strategy_request_param):
        """
        /v1/policy/iam/updateStrategy
        编辑自定义策略-IAM
        """
        return self.send(update_iam_strategy_request_param)

    def describe_vdc_query_strategy(self, describe_vdc_query_strategy_request_param):
        """
        /v1/policy/vdc/queryStrategy
        获取策略列表-VDC
        """
        return self.send(describe_vdc_query_strategy_request_param)

    def describe_strategy(self, describe_strategy_request_param):
        """
        /v1/policy/iam/getStrategyById
        获取策略详情-IAM
        """
        return self.send(describe_strategy_request_param)

    def create_iam_strategy(self, create_iam_strategy_request_param):
        """
        /v1/policy/iam/createStrategy
        创建自定义策略-IAM
        """
        return self.send(create_iam_strategy_request_param)

    def delete_i_a_m_user_group(self, delete_i_a_m_user_group_request_param):
        """
        /v1/userGroup/iam/delete
        IAM认证-用户组删除
        """
        return self.send(delete_i_a_m_user_group_request_param)

    def openapi_get_permission_list(self, openapi_get_permission_list_request_param):
        """
        /v1/permission/getPermissionList
        查询权限列表
        """
        return self.send(openapi_get_permission_list_request_param)

    def openapi_create_permission(self, openapi_create_permission_request_param):
        """
        /v1/permission/createPermission
        权限新增
        """
        return self.send(openapi_create_permission_request_param)

    def update_vdc_user_group(self, update_vdc_user_group_request_param):
        """
        /v1/vdc/update-user-group
        修改VDC用户组
        """
        return self.send(update_vdc_user_group_request_param)

    def create_vdc_user_group(self, create_vdc_user_group_request_param):
        """
        /v1/vdc/create-user-group
        创建VDC用户组
        """
        return self.send(create_vdc_user_group_request_param)

    def unbind_vdc_user_from_user_group(self, unbind_vdc_user_from_user_group_request_param):
        """
        /v1/vdc/unbind-users-from-user-group
        VDC用户组解绑用户
        """
        return self.send(unbind_vdc_user_from_user_group_request_param)

    def update_vdc_strategy(self, update_vdc_strategy_request_param):
        """
        /v1/policy/vdc/updateStrategy
        编辑自定义策略-VDC
        """
        return self.send(update_vdc_strategy_request_param)

    def get_quota_meta_data(self, get_quota_meta_data_request_param):
        """
        /v1/quota/metaData
        获取所有配额的元数据
        """
        return self.send(get_quota_meta_data_request_param)

    def clone_vdc_strategy(self, clone_vdc_strategy_request_param):
        """
        /v1/policy/vdc/cloneStrategy
        克隆策略-VDC
        """
        return self.send(clone_vdc_strategy_request_param)

    def change_vdc_user_password(self, change_vdc_user_password_request_param):
        """
        /v1/vdc/user/change-password
        VDC用户修改密码 
        """
        return self.send(change_vdc_user_password_request_param)

    def get_enterprise_project_vdc(self, get_enterprise_project_vdc_request_param):
        """
        /v1/project/getEpList/vdc
        查询VDC企业项目-列表
        """
        return self.send(get_enterprise_project_vdc_request_param)

    def describe_vdc_get_strategy_byid(self, describe_vdc_get_strategy_byid_request_param):
        """
        /v1/policy/vdc/getStrategyById
        获取策略详情-VDC
        """
        return self.send(describe_vdc_get_strategy_byid_request_param)

    def iam_user_group_bind_user(self, iam_user_group_bind_user_request_param):
        """
        /v1/userGroup/iam/bind-users
        IAM认证-用户组绑定用户
        """
        return self.send(iam_user_group_bind_user_request_param)

    def bind_vdc_user_group_to_user(self, bind_vdc_user_group_to_user_request_param):
        """
        /v1/vdc/bind-user-groups-to-user
        VDC用户绑定用户组 
        """
        return self.send(bind_vdc_user_group_to_user_request_param)

    def describe_vdc_user_group_permissions(self, describe_vdc_user_group_permissions_request_param):
        """
        /v1/vdc/list-user-group-permissions
        查询VDC用户组绑定策略
        """
        return self.send(describe_vdc_user_group_permissions_request_param)

    def openapi_delete_permission(self, openapi_delete_permission_request_param):
        """
        /v1/permission/deletePermission
        权限删除
        """
        return self.send(openapi_delete_permission_request_param)

    def openapi_get_permission_details(self, openapi_get_permission_details_request_param):
        """
        /v1/permission/getPermissionDetails
        查询权限详情
        """
        return self.send(openapi_get_permission_details_request_param)

    def openapi_get_service_list(self, openapi_get_service_list_request_param):
        """
        /v1/service/getServiceList
        服务管理列表
        """
        return self.send(openapi_get_service_list_request_param)

    def unlock_i_a_m_user(self, unlock_i_a_m_user_request_param):
        """
        /v1/user/iam/unlock
        IAM认证-用户解锁
        """
        return self.send(unlock_i_a_m_user_request_param)

    def delete_vdc_user_group_permissions(self, delete_vdc_user_group_permissions_request_param):
        """
        /v1/vdc/delete-user-group-permissions
        VDC用户组解绑策略
        """
        return self.send(delete_vdc_user_group_permissions_request_param)

    def clone_iam_strategy(self, clone_iam_strategy_request_param):
        """
        /v1/policy/iam/cloneStrategy
        克隆策略-IAM
        """
        return self.send(clone_iam_strategy_request_param)

    def query_quota_used(self, query_quota_used_request_param):
        """
        /v1/quota/queryQuotaUsed
        获取配额详情接口
        """
        return self.send(query_quota_used_request_param)

    def bind_i_a_m_user_to_user_group(self, bind_i_a_m_user_to_user_group_request_param):
        """
        /v1/user/iam/bind-to-user-groups
        IAM认证-用户绑定用户组
        """
        return self.send(bind_i_a_m_user_to_user_group_request_param)

    def update_quota_limit(self, update_quota_limit_request_param):
        """
        /v1/quota/updateQuotaLimit
        修改配额上限接口
        """
        return self.send(update_quota_limit_request_param)

    def get_vdc_user_group(self, get_vdc_user_group_request_param):
        """
        /v1/vdc/get-user-group
        VDC用户组详情查询
        """
        return self.send(get_vdc_user_group_request_param)

    def unbind_i_a_m_user_group_strategies(self, unbind_i_a_m_user_group_strategies_request_param):
        """
        /v1/userGroup/iam/unbind-strategies
        IAM认证-用户组解绑策略
        """
        return self.send(unbind_i_a_m_user_group_strategies_request_param)

    def delete_vdc_strategy(self, delete_vdc_strategy_request_param):
        """
        /v1/policy/vdc/deleteStrategy
        删除策略-VDC
        """
        return self.send(delete_vdc_strategy_request_param)

    def get_quota_state_iaas(self, get_quota_state_iaas_request_param):
        """
        /v1/quota/queryQuotaUsedIaaS
        根据主账号ID、VDCID、企业项目ID，获取所有配额的已用量   
    
        """
        return self.send(get_quota_state_iaas_request_param)

    def unbind_i_a_m_user_from_user_group(self, unbind_i_a_m_user_from_user_group_request_param):
        """
        /v1/user/iam/unbind-from-user-groups
        IAM认证-用户解绑用户组
        """
        return self.send(unbind_i_a_m_user_from_user_group_request_param)

    def delete_vdc_user_group(self, delete_vdc_user_group_request_param):
        """
        /v1/vdc/delete-user-group
        删除VDC用户组
        """
        return self.send(delete_vdc_user_group_request_param)

    def unbind_vdc_user_group_from_user(self, unbind_vdc_user_group_from_user_request_param):
        """
        /v1/vdc/unbind-user-groups-from-user
        VDC用户解绑用户组
        """
        return self.send(unbind_vdc_user_group_from_user_request_param)
