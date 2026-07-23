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


class ShowTargetGroupRequest(CTYunRequest):
    """
    查看后端服务组信息   
    
    """

    def __init__(self, request_param):
        super(ShowTargetGroupRequest, self).__init__("/v4/elb/show-target-group", "GET", "ctelb", "")
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
        if self.parameters.target_group_id is not None:
            query_param["targetGroupID"] = self.parameters.target_group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ShowTargetGroupRequestParam(object):

    def __init__(self, region_id, id=None, target_group_id=None):
        """
        :param region_id: 资源池ID
        :param id: 主机组ID（ ID和targetGroupID 不可同时为空） 
        :param target_group_id: 对齐公有云，主机组ID，建议优先使用（ ID和targetGroupID 不可同时为空） 
        """
        self.region_id = region_id
        self.id = id
        self.target_group_id = target_group_id

    def set_id(self, id):
        """
        :param id: 主机组ID（ ID和targetGroupID 不可同时为空） 
        """
        self.id = id

    def set_target_group_id(self, target_group_id):
        """
        :param target_group_id: 对齐公有云，主机组ID，建议优先使用（ ID和targetGroupID 不可同时为空） 
        """
        self.target_group_id = target_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

