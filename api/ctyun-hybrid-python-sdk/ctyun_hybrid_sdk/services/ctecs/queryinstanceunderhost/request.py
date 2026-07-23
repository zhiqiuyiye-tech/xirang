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


class QueryInstanceUnderHostRequest(CTYunRequest):
    """
    混合云自定义接口(v2.2.4支持)，v1云管按照自己协议返回未做额外处理。所以返回体中涉及ID均为UUID，状态均为云管支持状态。最外层额外提供了ecsID云管ID返回。
    """

    def __init__(self, request_param):
        super(QueryInstanceUnderHostRequest, self).__init__("/v4/ecs/instance-under-host", "GET", "ctecs", "")
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
        if self.parameters.host_name is not None:
            query_param["hostName"] = self.parameters.host_name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryInstanceUnderHostRequestParam(object):

    def __init__(self, region_id, host_name, ):
        """
        :param region_id: 资源id
        :param host_name: 宿主机名称
        """
        self.region_id = region_id
        self.host_name = host_name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.host_name is None:
            raise Exception("host_name can not None")

