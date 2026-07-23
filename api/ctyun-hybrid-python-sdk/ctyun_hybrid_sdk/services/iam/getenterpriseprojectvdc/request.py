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


class GetEnterpriseProjectVdcRequest(CTYunRequest):
    """
    查询VDC企业项目-列表
    """

    def __init__(self, request_param):
        super(GetEnterpriseProjectVdcRequest, self).__init__("/v1/project/getEpList/vdc", "GET", "iam", "")
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
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.vdc_id is not None:
            query_param["vdcId"] = self.parameters.vdc_id
        if self.parameters.project_status is not None:
            query_param["projectStatus"] = self.parameters.project_status
        if self.parameters.project_name is not None:
            query_param["projectName"] = self.parameters.project_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class GetEnterpriseProjectVdcRequestParam(object):

    def __init__(self, page, page_size, vdc_id, project_status=None, project_name=None):
        """
        :param page: 页码 大于等于1
        :param page_size: 页面大小 大于等于1，超过100默认为100
        :param vdc_id: vdcid
        :param project_status: 企业项目状态 1-未开始 2-进行中 3-已结束
        :param project_name: 企业项目名称
        """
        self.page = page
        self.page_size = page_size
        self.vdc_id = vdc_id
        self.project_status = project_status
        self.project_name = project_name

    def set_project_status(self, project_status):
        """
        :param project_status: 企业项目状态 1-未开始 2-进行中 3-已结束
        """
        self.project_status = project_status

    def set_project_name(self, project_name):
        """
        :param project_name: 企业项目名称
        """
        self.project_name = project_name

    def check_param(self):
        """
        the param required check
        """
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")
        if self.vdc_id is None:
            raise Exception("vdc_id can not None")

