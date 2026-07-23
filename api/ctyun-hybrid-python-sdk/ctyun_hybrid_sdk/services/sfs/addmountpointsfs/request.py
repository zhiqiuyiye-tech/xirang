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


class AddMountpointSfsRequest(CTYunRequest):
    """
    该接口只支持3.0资源池
    """

    def __init__(self, request_param):
        super(AddMountpointSfsRequest, self).__init__("/v4/sfs/add-mountpoint-sfs", "POST", "sfs", "application/json")
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
        if self.parameters.sfs_uid is not None:
            body_param["sfsUID"] = self.parameters.sfs_uid
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
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


class AddMountpointSfsRequestParam(object):

    def __init__(self, region_id, sfs_uid, vpc_id, subnet_id, ):
        """
        :param region_id: 资源池ID
        :param sfs_uid: 弹性文件系统ID
        :param vpc_id: 可以通过查询VPC列表获取，如需新增可以创建VPC
        :param subnet_id: 可以通过查询子网列表获取，如需新增可以创建子网。
        """
        self.region_id = region_id
        self.sfs_uid = sfs_uid
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.subnet_id is None:
            raise Exception("subnet_id can not None")

