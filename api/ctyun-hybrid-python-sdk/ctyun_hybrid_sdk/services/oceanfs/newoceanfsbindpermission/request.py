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

from ctyun_hybrid_sdk.core.request import CTYunRequest


class NewOceanfsBindPermissionRequest(CTYunRequest):
    """
    海量文件VPC绑定权限组（新）
    """

    def __init__(self, request_param):
        super(NewOceanfsBindPermissionRequest, self).__init__("/v4/oceanfs/vpc-bind-permission", "POST", "oceanfs", "application/json")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        body_param = dict()
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.permission_group_fuid is not None:
            body_param["permissionGroupFuid"] = self.parameters.permission_group_fuid
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.is_vpce is not None:
            body_param["isVpce"] = self.parameters.is_vpce
        if self.parameters.subnet_id is not None:
            body_param["subnetID"] = self.parameters.subnet_id
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class NewOceanfsBindPermissionRequestParam(object):

    def __init__(self, region_id, permission_group_fuid, sfs_uid, vpc_id, is_vpce=None, subnet_id=None):
        """
        :param region_id: 资源池ID
        :param permission_group_fuid: 权限组ID
        :param sfs_uid: 文件系统ID
        :param vpc_id: vpcID
        :param is_vpce: 文件系统绑定VPC时是否自动创建VPC终端节点。开启后本服务将为您创建免费的VPC终端节点（VPCE），连接文件存储服务。创建VPCE后将返回该VPC专属的挂载地址，通常需要1~3分钟。暂不支持
        :param subnet_id: 普通子网ID，当isVpce为true时必填。暂不支持
        """
        self.region_id = region_id
        self.permission_group_fuid = permission_group_fuid
        self.sfs_uid = sfs_uid
        self.vpc_id = vpc_id
        self.is_vpce = is_vpce
        self.subnet_id = subnet_id

    def set_is_vpce(self, is_vpce):
        """
        :param is_vpce: 文件系统绑定VPC时是否自动创建VPC终端节点。开启后本服务将为您创建免费的VPC终端节点（VPCE），连接文件存储服务。创建VPCE后将返回该VPC专属的挂载地址，通常需要1~3分钟。暂不支持
        """
        self.is_vpce = is_vpce

    def set_subnet_id(self, subnet_id):
        """
        :param subnet_id: 普通子网ID，当isVpce为true时必填。暂不支持
        """
        self.subnet_id = subnet_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.permission_group_fuid is None:
            raise Exception("permission_group_fuid can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")

