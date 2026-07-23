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


class ListVmPoolRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容4.0资源池
    """

    def __init__(self, request_param):
        super(ListVmPoolRequest, self).__init__("/v4/elb/list-vm-pool", "GET", "ctelb", "")
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
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        if self.parameters.target_group_id is not None:
            query_param["targetGroupID"] = self.parameters.target_group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListVmPoolRequestParam(object):

    def __init__(self, region_id, name=None, target_group_id=None):
        """
        :param region_id: 资源池id
        :param name: 服务组名称
        :param target_group_id: 服务组id
        """
        self.region_id = region_id
        self.name = name
        self.target_group_id = target_group_id

    def set_name(self, name):
        """
        :param name: 服务组名称
        """
        self.name = name

    def set_target_group_id(self, target_group_id):
        """
        :param target_group_id: 服务组id
        """
        self.target_group_id = target_group_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

