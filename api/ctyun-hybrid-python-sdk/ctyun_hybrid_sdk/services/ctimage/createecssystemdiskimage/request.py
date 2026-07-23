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


class CreateEcsSystemDiskImageRequest(CTYunRequest):
    """
    创建私有系统盘镜像   
    接口约束：   
    云主机为关机或者云行中，系统盘为已挂载，非中间态
    """

    def __init__(self, request_param):
        super(CreateEcsSystemDiskImageRequest, self).__init__("/v4/image/create", "POST", "ctimage", "application/json")
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
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.image_name is not None:
            body_param["imageName"] = self.parameters.image_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class CreateEcsSystemDiskImageRequestParam(object):

    def __init__(self, region_id, instance_id, image_name, description=None, az_name=None, project_id=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机id
        :param image_name: 镜像名称;不能和已有名称重复;长度2～32位，只能包含大小写字母、数字和-。只能以大小写字母开头
        :param description: 镜像描述；长度最大255
        :param az_name: 可用区
        :param project_id: 企业项目 ID，默认值 0。  
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.image_name = image_name
        self.description = description
        self.az_name = az_name
        self.project_id = project_id

    def set_description(self, description):
        """
        :param description: 镜像描述；长度最大255
        """
        self.description = description

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目 ID，默认值 0。  
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.image_name is None:
            raise Exception("image_name can not None")

