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


class DescribeInvocationResultsRequest(CTYunRequest):
    """
    查询一条或多条云助手命令在弹性云主机、物理机中执行结果
    """

    def __init__(self, request_param):
        super(DescribeInvocationResultsRequest, self).__init__("/v4/cloud-assistant/describe-invocation-results", "POST", "ctecs", "application/json")
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
        if self.parameters.command_id is not None:
            body_param["commandID"] = self.parameters.command_id
        if self.parameters.invoked_id is not None:
            body_param["invokedID"] = self.parameters.invoked_id
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class DescribeInvocationResultsRequestParam(object):

    def __init__(self, region_id, command_id=None, invoked_id=None, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param command_id: 命令ID，精确查询
        :param invoked_id: 命令执行ID，精确查询
        :param page_no: 当前页码，不传默认值为1
        :param page_size: 分页查询时设置的每页行数，不传默认值为1，最大值为100，传超过100按100查询
        """
        self.region_id = region_id
        self.command_id = command_id
        self.invoked_id = invoked_id
        self.page_no = page_no
        self.page_size = page_size

    def set_command_id(self, command_id):
        """
        :param command_id: 命令ID，精确查询
        """
        self.command_id = command_id

    def set_invoked_id(self, invoked_id):
        """
        :param invoked_id: 命令执行ID，精确查询
        """
        self.invoked_id = invoked_id

    def set_page_no(self, page_no):
        """
        :param page_no: 当前页码，不传默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时设置的每页行数，不传默认值为1，最大值为100，传超过100按100查询
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

