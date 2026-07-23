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


class DescribeAuditlogsRequest(CTYunRequest):
    """
    审计日志查询，注意请求的开始时间结束时间为UnixMilli 时间戳 或者Unix时间戳，开始时间结束时间必填，最长可以获取7天的日志，获取的是当前用户的日志，如需获取更大范围权限可以联系运维获取方案
    """

    def __init__(self, request_param):
        super(DescribeAuditlogsRequest, self).__init__("/v1/audit/auditlogs", "GET", "audit", "")
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
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.page_no is not None:
            query_param["pageNo"] = self.parameters.page_no
        if self.parameters.resource_id is not None:
            query_param["resourceID"] = self.parameters.resource_id
        if self.parameters.operation_name is not None:
            query_param["operationName"] = self.parameters.operation_name
        if self.parameters.action is not None:
            query_param["action"] = self.parameters.action
        if self.parameters.event_type is not None:
            query_param["eventType"] = self.parameters.event_type
        if self.parameters.start_time is not None:
            query_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            query_param["endTime"] = self.parameters.end_time
        if self.parameters.trace_id is not None:
            query_param["traceId"] = self.parameters.trace_id
        if self.parameters.request_id is not None:
            query_param["requestId"] = self.parameters.request_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeAuditlogsRequestParam(object):

    def __init__(self, start_time, end_time, page_size=None, page_no=None, resource_id=None, operation_name=None, action=None, event_type=None, trace_id=None, request_id=None):
        """
        :param page_size: 默认值10 每页条数
        :param page_no: 默认值1 页码
        :param resource_id: 资源id
        :param operation_name: 操作名称
        :param action: 动作，支持 query、create、update、 delete 、login
        :param event_type: 请求类型 Console 控制台  OpenAPI 混合云openapi请求
        :param start_time: 查询开始时间，时间戳格式
        :param end_time: 查询结束时间，时间戳格式
        :param trace_id: 链路跟踪traceId
        :param request_id: 请求使用requestid
        """
        self.page_size = page_size
        self.page_no = page_no
        self.resource_id = resource_id
        self.operation_name = operation_name
        self.action = action
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.trace_id = trace_id
        self.request_id = request_id

    def set_page_size(self, page_size):
        """
        :param page_size: 默认值10 每页条数
        """
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 默认值1 页码
        """
        self.page_no = page_no

    def set_resource_id(self, resource_id):
        """
        :param resource_id: 资源id
        """
        self.resource_id = resource_id

    def set_operation_name(self, operation_name):
        """
        :param operation_name: 操作名称
        """
        self.operation_name = operation_name

    def set_action(self, action):
        """
        :param action: 动作，支持 query、create、update、 delete 、login
        """
        self.action = action

    def set_event_type(self, event_type):
        """
        :param event_type: 请求类型 Console 控制台  OpenAPI 混合云openapi请求
        """
        self.event_type = event_type

    def set_trace_id(self, trace_id):
        """
        :param trace_id: 链路跟踪traceId
        """
        self.trace_id = trace_id

    def set_request_id(self, request_id):
        """
        :param request_id: 请求使用requestid
        """
        self.request_id = request_id

    def check_param(self):
        """
        the param required check
        """
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")

