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


class UpdateDeletionProtectionRequest(CTYunRequest):
    """
    1.云主机必须存在，云主机只有在运行（running）、关机（stopped）或节省关机（shelve）状态才可执行该操作，您可以调用查询云主机列表或获取多台云主机的状态信息查询结果中的instanceStatus字段来确认当前云主机状态   
    2.只有按需付费云主机能开启实例删除保护
    """

    def __init__(self, request_param):
        super(UpdateDeletionProtectionRequest, self).__init__("/v4/ecs/update-deletion-protection", "POST", "ctecs", "application/json")
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
        if self.parameters.deletion_protection is not None:
            body_param["deletionProtection"] = self.parameters.deletion_protection
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
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


class UpdateDeletionProtectionRequestParam(object):

    def __init__(self, region_id, instance_id, deletion_protection, az_name=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 云主机ID
        :param deletion_protection: 实例删除保护参数
        :param az_name: 可用区名称
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.deletion_protection = deletion_protection
        self.az_name = az_name

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称
        """
        self.az_name = az_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.deletion_protection is None:
            raise Exception("deletion_protection can not None")

