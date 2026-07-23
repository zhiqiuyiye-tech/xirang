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


class UpdateAclAttributeRequest(CTYunRequest):
    """
    修改acl 属性
    """

    def __init__(self, request_param):
        super(UpdateAclAttributeRequest, self).__init__("/v4/acl/update", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.acl_id is not None:
            body_param["aclID"] = self.parameters.acl_id
        if self.parameters.enabled is not None:
            body_param["enabled"] = self.parameters.enabled
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


class UpdateAclAttributeRequestParam(object):

    def __init__(self, region_id, name, acl_id, description=None, enabled=None):
        """
        :param region_id: 资源池ID
        :param name: 长度为2-32位，支持英文字母、中文、数字、特殊符号_(下划线) -(中划线) /(斜杠) ，中文/英文字母开头
        :param description: ACL描述，长度为0-50字符   
         支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        :param acl_id: ACL ID
        :param enabled: 是否启用disable,enable
        """
        self.region_id = region_id
        self.name = name
        self.description = description
        self.acl_id = acl_id
        self.enabled = enabled

    def set_description(self, description):
        """
        :param description: ACL描述，长度为0-50字符   
         支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        """
        self.description = description

    def set_enabled(self, enabled):
        """
        :param enabled: 是否启用disable,enable
        """
        self.enabled = enabled

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.acl_id is None:
            raise Exception("acl_id can not None")

