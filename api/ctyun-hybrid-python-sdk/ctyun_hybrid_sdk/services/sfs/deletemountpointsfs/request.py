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


class DeleteMountpointSfsRequest(CTYunRequest):
    """
    注意：sfsUID是文件系统id   
    该接口只支持3.0资源池
    """

    def __init__(self, request_param):
        super(DeleteMountpointSfsRequest, self).__init__("/v4/sfs/delete-mountpoint-sfs", "POST", "sfs", "application/json")
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
        if self.parameters.mount_point_id is not None:
            body_param["mountPointID"] = self.parameters.mount_point_id
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


class DeleteMountpointSfsRequestParam(object):

    def __init__(self, region_id, sfs_uid, mount_point_id, ):
        """
        :param region_id: 资源池
        :param sfs_uid: 注：这是文件系统id
        :param mount_point_id: 文件系统挂载点ID
        """
        self.region_id = region_id
        self.sfs_uid = sfs_uid
        self.mount_point_id = mount_point_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.sfs_uid is None:
            raise Exception("sfs_uid can not None")
        if self.mount_point_id is None:
            raise Exception("mount_point_id can not None")

