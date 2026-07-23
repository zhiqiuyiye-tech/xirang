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


class DeleteAclRuleRequest(CTYunRequest):
    """
    只有用户创建的ACL规则才能删除，ACL默认创建的ACL规则不允许删除   
    删除aclrules：支持批量删除   
    1.15版本：解决格式不对齐问题   
    
    """

    def __init__(self, request_param):
        super(DeleteAclRuleRequest, self).__init__("/v4/acl-rule/delete", "POST", "ctvpc", "application/json")
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
        if self.parameters.acl_id is not None:
            body_param["aclID"] = self.parameters.acl_id
        if self.parameters.acl_rule_id_list is not None:
            body_param["aclRuleIDList"] = self.parameters.acl_rule_id_list
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


class DeleteAclRuleRequestParam(object):

    def __init__(self, region_id, acl_id, acl_rule_id_list, ):
        """
        :param region_id: 资源池ID
        :param acl_id: ACL的id
        :param acl_rule_id_list: ACL规则id列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.acl_id = acl_id
        self.acl_rule_id_list = acl_rule_id_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.acl_id is None:
            raise Exception("acl_id can not None")
        if self.acl_rule_id_list is None:
            raise Exception("acl_rule_id_list can not None")

