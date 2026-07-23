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


class MetadataDetailsRequest(CTYunRequest):
    """
    仅4.0支持，查询云主机的元数据，云主机需为运行中或者关机状态
    """

    def __init__(self, request_param):
        super(MetadataDetailsRequest, self).__init__("/v4/ecs/metadata/details", "GET", "ctecs", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_id is not None:
            query_param["instanceID"] = self.parameters.instance_id
        if self.parameters.metadata_key is not None:
            query_param["metadataKey"] = self.parameters.metadata_key
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class MetadataDetailsRequestParam(object):

    def __init__(self, region_id, instance_id, metadata_key=None):
        """
        :param region_id: 资源池ID
        :param instance_id: 实例ID
        :param metadata_key: 元数据字段，如缺省则查询云主机所有元数据字段
        """
        self.region_id = region_id
        self.instance_id = instance_id
        self.metadata_key = metadata_key

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
        if self.instance_id is None:
            raise Exception("instance_id can not None")

