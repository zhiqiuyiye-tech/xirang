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


class GetCustomerResourcesRequest(CTYunRequest):
    """
    接口功能介绍：根据regionID查询用户已有资源   
    接口约束：保证输入的资源池id准确无误   
    注:    
    1.regionID不存在的/用户所属VDC未绑定指定资源池/用户所属VDC在指定资源池下无数据，已有资源均返回0；   
    2.本期根据对接需求，仅实现VM、Volume、Public_IP、BMS、Vm_Group五种资源数据。
    """

    def __init__(self, request_param):
        super(GetCustomerResourcesRequest, self).__init__("/v4/region/customer-resources", "GET", "ctecs", "")
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
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetCustomerResourcesRequestParam(object):

    def __init__(self, region_id, project_id=None):
        """
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        """
        self.region_id = region_id
        self.project_id = project_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

