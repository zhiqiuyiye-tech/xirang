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


class GetMetadataV41Request(CTYunRequest):
    """
    仅4.0支持，查询云主机的元数据，云主机需为运行中或者关机状态
    """

    def __init__(self, request_param):
        super(GetMetadataV41Request, self).__init__("/v4/ecs/metadata-get", "POST", "ctecs", "application/json")
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
        if self.parameters.id is not None:
            body_param["ID"] = self.parameters.id
        if self.parameters.metadata_key is not None:
            body_param["metadataKey"] = self.parameters.metadata_key
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


class GetMetadataV41RequestParam(object):

    def __init__(self, region_id, id, az_name, metadata_key=None):
        """
        :param region_id: 资源池ID
        :param id: 实例ID
        :param metadata_key: 元数据字段，如缺省则查询云主机所有元数据字段
        :param az_name: 公有云必传（单可用区传default），混合云不必传
        """
        self.region_id = region_id
        self.id = id
        self.metadata_key = metadata_key
        self.az_name = az_name

    def set_metadata_key(self, metadata_key):
        """
        :param metadata_key: 元数据字段，如缺省则查询云主机所有元数据字段
        """
        self.metadata_key = metadata_key

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")

