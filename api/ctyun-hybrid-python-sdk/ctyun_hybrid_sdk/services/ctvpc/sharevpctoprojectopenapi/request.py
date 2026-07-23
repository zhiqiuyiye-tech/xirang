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


class ShareVpcToProjectOpenapiRequest(CTYunRequest):
    """
    共享vpc到企业项目
    """

    def __init__(self, request_param):
        super(ShareVpcToProjectOpenapiRequest, self).__init__("/v4/vpc/share-to-project", "POST", "ctvpc", "application/json")
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
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.project_ids is not None:
            body_param["projectIDs"] = self.parameters.project_ids
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


class ShareVpcToProjectOpenapiRequestParam(object):

    def __init__(self, vpc_id, region_id, project_ids=None):
        """
        :param vpc_id: vpc id
        :param region_id: 资源池 id
        :param project_ids: 企业项目id列表，全量更新，参数不传不更新 注意:此参数为数组
        """
        self.vpc_id = vpc_id
        self.region_id = region_id
        self.project_ids = project_ids

    def set_project_ids(self, project_ids):
        """
        :param project_ids: 企业项目id列表，全量更新，参数不传不更新
        """
        self.project_ids = project_ids

    def check_param(self):
        """
        the param required check
        """
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

