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


class CdaPhysicalLineUpdateRequest(CTYunRequest):
    """
    物理专线未绑定专线网关时，可修改本端对端互联ip和专线类型   
    如单栈变双栈，双栈变单栈等.如果物理专线已经绑定了专线网关，只能修改带宽和物理专线名称。
    """

    def __init__(self, request_param):
        super(CdaPhysicalLineUpdateRequest, self).__init__("/v4/cda/physical-line/update", "POST", "cda", "application/json")
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
        if self.parameters.line_id is not None:
            body_param["lineID"] = self.parameters.line_id
        if self.parameters.bandwidth is not None:
            body_param["bandwidth"] = self.parameters.bandwidth
        if self.parameters.line_name is not None:
            body_param["lineName"] = self.parameters.line_name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.line_code is not None:
            body_param["lineCode"] = self.parameters.line_code
        if self.parameters.location is not None:
            body_param["location"] = self.parameters.location
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


class CdaPhysicalLineUpdateRequestParam(object):

    def __init__(self, region_id, line_id, bandwidth=None, line_name=None, description=None, line_code=None, location=None):
        """
        :param region_id: 资源池id
        :param line_id: 物理专线 ID
        :param bandwidth: 带宽(M), 范围1-999999999，int64
        :param line_name: 物理专线名字,长度2-63，不支持中文 、中文符号
        :param description: 描述，长度为2-200字符 不支持中文 、中文符号
        :param line_code: 电路代号（此功能私有云不支持，传了无作用）
        :param location: 接入位置
        """
        self.region_id = region_id
        self.line_id = line_id
        self.bandwidth = bandwidth
        self.line_name = line_name
        self.description = description
        self.line_code = line_code
        self.location = location

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth: 带宽(M), 范围1-999999999，int64
        """
        self.bandwidth = bandwidth

    def set_line_name(self, line_name):
        """
        :param line_name: 物理专线名字,长度2-63，不支持中文 、中文符号
        """
        self.line_name = line_name

    def set_description(self, description):
        """
        :param description: 描述，长度为2-200字符 不支持中文 、中文符号
        """
        self.description = description

    def set_line_code(self, line_code):
        """
        :param line_code: 电路代号（此功能私有云不支持，传了无作用）
        """
        self.line_code = line_code

    def set_location(self, location):
        """
        :param location: 接入位置
        """
        self.location = location

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.line_id is None:
            raise Exception("line_id can not None")

