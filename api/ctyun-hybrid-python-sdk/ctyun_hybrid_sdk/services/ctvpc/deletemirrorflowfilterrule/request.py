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


class DeleteMirrorFlowFilterRuleRequest(CTYunRequest):
    """
    删除过滤规则
    """

    def __init__(self, request_param):
        super(DeleteMirrorFlowFilterRuleRequest, self).__init__("/v4/mirrorflow/delete-filter-rule", "POST", "ctvpc", "application/json")
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
        if self.parameters.mirror_filter_rule_id is not None:
            body_param["mirrorFilterRuleID"] = self.parameters.mirror_filter_rule_id
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


class DeleteMirrorFlowFilterRuleRequestParam(object):

    def __init__(self, region_id, mirror_filter_rule_id, ):
        """
        :param region_id: 区域ID
        :param mirror_filter_rule_id: 名称
        """
        self.region_id = region_id
        self.mirror_filter_rule_id = mirror_filter_rule_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.mirror_filter_rule_id is None:
            raise Exception("mirror_filter_rule_id can not None")

