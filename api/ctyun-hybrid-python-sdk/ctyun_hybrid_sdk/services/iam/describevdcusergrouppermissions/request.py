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


class DescribeVdcUserGroupPermissionsRequest(CTYunRequest):
    """
    查询VDC用户组绑定策略
    """

    def __init__(self, request_param):
        super(DescribeVdcUserGroupPermissionsRequest, self).__init__("/v1/vdc/list-user-group-permissions", "GET", "iam", "")
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
        if self.parameters.strategy_name is not None:
            query_param["strategyName"] = self.parameters.strategy_name
        if self.parameters.range is not None:
            query_param["range"] = self.parameters.range
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.region_type is not None:
            query_param["regionType"] = self.parameters.region_type
        if self.parameters.group_id is not None:
            query_param["groupID"] = self.parameters.group_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class DescribeVdcUserGroupPermissionsRequestParam(object):

    def __init__(self, page, page_size, group_id, strategy_name=None, range=None, type=None, region_type=None):
        """
        :param page: 页数   
         
        :param page_size: 每页显示条数，最大为100
        :param strategy_name: 策略名称
        :param range: 策略授权范围 范围 1-全局 2-资源池
        :param type: 策略类型 1-系统策略 2-自定义策略
        :param region_type: 资源池类型,华为公有云:huawei；CTStack 4.0:ctstackv4；CTStack 3.0:tstackv3；天翼云公有云:ctyun；Ctstack Lite:ctstacklite
        :param group_id: 用户组id
        """
        self.page = page
        self.page_size = page_size
        self.strategy_name = strategy_name
        self.range = range
        self.type = type
        self.region_type = region_type
        self.group_id = group_id

    def set_strategy_name(self, strategy_name):
        """
        :param strategy_name: 策略名称
        """
        self.strategy_name = strategy_name

    def set_range(self, range):
        """
        :param range: 策略授权范围 范围 1-全局 2-资源池
        """
        self.range = range

    def set_type(self, type):
        """
        :param type: 策略类型 1-系统策略 2-自定义策略
        """
        self.type = type

    def set_region_type(self, region_type):
        """
        :param region_type: 资源池类型,华为公有云:huawei；CTStack 4.0:ctstackv4；CTStack 3.0:tstackv3；天翼云公有云:ctyun；Ctstack Lite:ctstacklite
        """
        self.region_type = region_type

    def check_param(self):
        """
        the param required check
        """
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")
        if self.group_id is None:
            raise Exception("group_id can not None")

