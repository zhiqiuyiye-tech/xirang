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


class UpdateListenerAttrRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容4.0资源池
    """

    def __init__(self, request_param):
        super(UpdateListenerAttrRequest, self).__init__("/v4/elb/update-listener-attr", "POST", "ctelb", "application/json")
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
        if self.parameters.listener_id is not None:
            body_param["listenerID"] = self.parameters.listener_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.access_control_id is not None:
            body_param["accessControlID"] = self.parameters.access_control_id
        if self.parameters.access_control_type is not None:
            body_param["accessControlType"] = self.parameters.access_control_type
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


class UpdateListenerAttrRequestParam(object):

    def __init__(self, region_id, listener_id, name=None, description=None, access_control_id=None, access_control_type=None):
        """
        :param region_id: 资源池id
        :param listener_id: 监听器id
        :param name: 名称
        :param description: 描述
        :param access_control_id: 访问控制ID
        :param access_control_type: 访问控制类型。取值范围：Close（未启用）、White（白名单）、Black（黑名单
        """
        self.region_id = region_id
        self.listener_id = listener_id
        self.name = name
        self.description = description
        self.access_control_id = access_control_id
        self.access_control_type = access_control_type

    def set_name(self, name):
        """
        :param name: 名称
        """
        self.name = name

    def set_description(self, description):
        """
        :param description: 描述
        """
        self.description = description

    def set_access_control_id(self, access_control_id):
        """
        :param access_control_id: 访问控制ID
        """
        self.access_control_id = access_control_id

    def set_access_control_type(self, access_control_type):
        """
        :param access_control_type: 访问控制类型。取值范围：Close（未启用）、White（白名单）、Black（黑名单
        """
        self.access_control_type = access_control_type

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.listener_id is None:
            raise Exception("listener_id can not None")

