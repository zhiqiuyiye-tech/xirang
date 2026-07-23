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


class CreateImageFromEcsSnapshotRequest(CTYunRequest):
    """
    云主机快照创建系统盘镜像
    """

    def __init__(self, request_param):
        super(CreateImageFromEcsSnapshotRequest, self).__init__("/v4/image/create-from-ecs-snapshot", "POST", "ctimage", "application/json")
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
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.image_name is not None:
            body_param["imageName"] = self.parameters.image_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class CreateImageFromEcsSnapshotRequestParam(object):

    def __init__(self, region_id, snapshot_id, image_name, description=None):
        """
        :param region_id: 资源池ID
        :param snapshot_id: 云主机快照ID
        :param image_name: 镜像名称;名称不能和已有的重复；长度为2-32字符 支持使用字母、数字、中划线（-），只能以字母开头、以数字或字母结尾
        :param description: 镜像描述；长度最大255
        """
        self.region_id = region_id
        self.snapshot_id = snapshot_id
        self.image_name = image_name
        self.description = description

    def set_description(self, description):
        """
        :param description: 镜像描述；长度最大255
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")
        if self.image_name is None:
            raise Exception("image_name can not None")

