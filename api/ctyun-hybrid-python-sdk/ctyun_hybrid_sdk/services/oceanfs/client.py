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


class OceanfsClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('oceanfs-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(OceanfsClient, self).__init__(credential, config, 'oceanfs', '0.1.0', logger, signer)

    def oceanfs_list_vpc_permission_group(self, oceanfs_list_vpc_permission_group_request_param):
        """
        /v4/oceanfs/list-vpc-permission
        查询文件系统权限组与VPC绑定关系
        """
        return self.send(oceanfs_list_vpc_permission_group_request_param)

    def new_oceanfs_change_permission(self, new_oceanfs_change_permission_request_param):
        """
        /v4/oceanfs/vpc-change-permission
        海量文件VPC换绑权限组（新）
        """
        return self.send(new_oceanfs_change_permission_request_param)

    def oceanfs_new_permission_group(self, oceanfs_new_permission_group_request_param):
        """
        /v4/oceanfs/permission-group/new-permission-group
        海量文件创建权限组
        """
        return self.send(oceanfs_new_permission_group_request_param)

    def renew_sfs(self, renew_sfs_request_param):
        """
        /v4/oceanfs/renew-sfs
        只支持onDemand为false的资源进行续订，即付费方式为包年包月类型的文件系统才支持续订
        """
        return self.send(renew_sfs_request_param)

    def oceanfs_new_permission_group_rule(self, oceanfs_new_permission_group_rule_request_param):
        """
        /v4/oceanfs/permission-rule/new-permission-rule
        海量文件创建权限组规则
        """
        return self.send(oceanfs_new_permission_group_rule_request_param)

    def oceanfs_region_s_rtorage_type(self, oceanfs_region_s_rtorage_type_request_param):
        """
        /v4/oceanfs/region/storagetype
        海量文件资源池支持详情
        """
        return self.send(oceanfs_region_s_rtorage_type_request_param)

    def oceanfs_list_permission_group(self, oceanfs_list_permission_group_request_param):
        """
        /v4/oceanfs/permission-group/list-permission-group
        海量文件返回权限组描述信息
        """
        return self.send(oceanfs_list_permission_group_request_param)

    def oceanfs_modify_permission_group(self, oceanfs_modify_permission_group_request_param):
        """
        /v4/oceanfs/permission-group/modify-permission-group
        海量文件修改权限组
        """
        return self.send(oceanfs_modify_permission_group_request_param)

    def oceanfs_unbind_permission(self, oceanfs_unbind_permission_request_param):
        """
        /v4/oceanfs/unbind-permission
        文件系统VPC解绑权限组
        """
        return self.send(oceanfs_unbind_permission_request_param)

    def oceanfs_bind_permission(self, oceanfs_bind_permission_request_param):
        """
        /v4/oceanfs/bind-permission
        文件系统VPC绑定权限组
        """
        return self.send(oceanfs_bind_permission_request_param)

    def new_oceanfs_unbind_permission(self, new_oceanfs_unbind_permission_request_param):
        """
        /v4/oceanfs/vpc-unbind-permission
        海量文件VPC解绑权限组（新）
        """
        return self.send(new_oceanfs_unbind_permission_request_param)

    def new_oceanfs_bind_permission(self, new_oceanfs_bind_permission_request_param):
        """
        /v4/oceanfs/vpc-bind-permission
        海量文件VPC绑定权限组（新）
        """
        return self.send(new_oceanfs_bind_permission_request_param)

    def resize_oceanfs_sfs(self, resize_oceanfs_sfs_request_param):
        """
        /v4/oceanfs/resize-sfs
        海量文件修改规格
        """
        return self.send(resize_oceanfs_sfs_request_param)

    def list_oceanfs_sfs(self, list_oceanfs_sfs_request_param):
        """
        /v4/oceanfs/list-sfs
        海量文件列表查询
        """
        return self.send(list_oceanfs_sfs_request_param)

    def info_sfs(self, info_sfs_request_param):
        """
        /v4/oceanfs/info-sfs
        根据资源池 ID 和海量文件的sfsUID，查询文件系统详情
        """
        return self.send(info_sfs_request_param)

    def oceanfs_modify_permission_group_rule(self, oceanfs_modify_permission_group_rule_request_param):
        """
        /v4/oceanfs/permission-rule/modify-permission-rule
        海量文件修改权限组规则
        """
        return self.send(oceanfs_modify_permission_group_rule_request_param)

    def oceanfs_list_permission_group_rule(self, oceanfs_list_permission_group_rule_request_param):
        """
        /v4/oceanfs/permission-rule/list-permission-rule
        海量文件返回权限组规则描述信息
        """
        return self.send(oceanfs_list_permission_group_rule_request_param)

    def oceanfs_change_permission(self, oceanfs_change_permission_request_param):
        """
        /v4/oceanfs/change-permission
        文件系统VPC换绑权限组
        """
        return self.send(oceanfs_change_permission_request_param)

    def new_sfs(self, new_sfs_request_param):
        """
        /v4/oceanfs/new-sfs
        创建文件系统
        """
        return self.send(new_sfs_request_param)

    def info_by_name_sfs(self, info_by_name_sfs_request_param):
        """
        /v4/oceanfs/info-by-name-sfs
        根据海量文件名称和资源池ID，查询文件系统详情
        """
        return self.send(info_by_name_sfs_request_param)

    def refund_sfs(self, refund_sfs_request_param):
        """
        /v4/oceanfs/refund-sfs
        海量文件退订   
    文件系统绑定了vpc，退订时会自动解绑
        """
        return self.send(refund_sfs_request_param)

    def oceanfs_delete_permission_group(self, oceanfs_delete_permission_group_request_param):
        """
        /v4/oceanfs/permission-group/delete-permission-group
        海量文件删除权限组
        """
        return self.send(oceanfs_delete_permission_group_request_param)

    def oceanfs_delete_permission_group_rule(self, oceanfs_delete_permission_group_rule_request_param):
        """
        /v4/oceanfs/permission-rule/delete-permission-rule
        海量文件删除权限组规则
        """
        return self.send(oceanfs_delete_permission_group_rule_request_param)

    def opend_list_sfs(self, opend_list_sfs_request_param):
        """
        /v4/oceanfs/opend-list-sfs
        根据资源池 ID ，查询用户已开通文件系统
        """
        return self.send(opend_list_sfs_request_param)
