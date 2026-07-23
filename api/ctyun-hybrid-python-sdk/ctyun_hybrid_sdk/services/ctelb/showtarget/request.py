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


class ShowTargetRequest(CTYunRequest):
    """
    查看后端服务详情
    """

    def __init__(self, request_param):
        super(ShowTargetRequest, self).__init__("/v4/elb/show-target", "GET", "ctelb", "")
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
        if self.parameters.id is not None:
            query_param["ID"] = self.parameters.id
        if self.parameters.instance_type is not None:
            query_param["instanceType"] = self.parameters.instance_type
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowTargetRequestParam(object):

    def __init__(self, region_id, id, instance_type=None):
        """
        :param region_id: 资源池ID
        :param id: 主机组成员id(可查询后端服务列表获取主机组成员的id）   
         
        :param instance_type: 后端服务类型，IP--查询后端IP类型的成员，不传或其余值默认查询主机和裸金属类型的后端服务   
         （对齐v1参数，在v2中成员id唯一确定，无需区分类型，该参数不做处理）
        """
        self.region_id = region_id
        self.id = id
        self.instance_type = instance_type

    def set_instance_type(self, instance_type):
        """
        :param instance_type: 后端服务类型，IP--查询后端IP类型的成员，不传或其余值默认查询主机和裸金属类型的后端服务   
         （对齐v1参数，在v2中成员id唯一确定，无需区分类型，该参数不做处理）
        """
        self.instance_type = instance_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.id is None:
            raise Exception("id can not None")

