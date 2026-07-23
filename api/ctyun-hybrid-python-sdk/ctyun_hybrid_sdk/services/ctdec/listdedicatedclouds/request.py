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


class ListDedicatedCloudsRequest(CTYunRequest):
    """
    获取专属云列表
    """

    def __init__(self, request_param):
        super(ListDedicatedCloudsRequest, self).__init__("/v4/dec/list", "GET", "ctdec", "")
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
        if self.parameters.az_name is not None:
            query_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            query_param["projectID"] = self.parameters.project_id
        if self.parameters.dec_id is not None:
            query_param["decID"] = self.parameters.dec_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListDedicatedCloudsRequestParam(object):

    def __init__(self, region_id, az_name=None, project_id=None, dec_id=None):
        """
        :param region_id: 资源池ID，e.g. nm8
        :param az_name: 多az标识-必传，e.g. az1
        :param project_id: 企业项目ID，不传返回全部项目下数据
        :param dec_id: 专属云ID，传则查询指定专属云
        """
        self.region_id = region_id
        self.az_name = az_name
        self.project_id = project_id
        self.dec_id = dec_id

    def set_az_name(self, az_name):
        """
        :param az_name: 多az标识-必传，e.g. az1
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID，不传返回全部项目下数据
        """
        self.project_id = project_id

    def set_dec_id(self, dec_id):
        """
        :param dec_id: 专属云ID，传则查询指定专属云
        """
        self.dec_id = dec_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

