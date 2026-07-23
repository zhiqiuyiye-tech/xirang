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


class PushAlertIssueHybridRequest(CTYunRequest):
    """
    用户可以自行推送的告警事件，非系统自动产生，可以在告警历史中查询到。
    """

    def __init__(self, request_param):
        super(PushAlertIssueHybridRequest, self).__init__("/v4/monitor/push-alert-issue", "POST", "monitor", "application/json")
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
        if self.parameters.issue_list is not None:
            issue_list = []
            if isinstance(self.parameters.issue_list, list):
                for item in self.parameters.issue_list:
                    if type(item) is dict:
                        issue_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        issue_list.append(item_dict_value)
            else:
                issue_list.append(self.parameters.issue_list.get_dic())
            body_param["issueList"] = issue_list
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


class Issue(object):

    def __init__(self, status, clock, trigger_id, issue_id, ):
        """
        :param status: 本参数表示状态。取值范围：   
         0：正常。   
         1：告警。   
         根据以上范围取值。
        :param clock: 告警事件触发时间
        :param trigger_id: 告警规则ID（混合云管存在的告警规则）
        :param issue_id: 告警事件UUID（可自定义输入字段）
        """
        self.status = status
        self.clock = clock
        self.trigger_id = trigger_id
        self.issue_id = issue_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.status is not None:
            obj_dict["status"] = self.status
        if self.clock is not None:
            obj_dict["clock"] = self.clock
        if self.trigger_id is not None:
            obj_dict["triggerID"] = self.trigger_id
        if self.issue_id is not None:
            obj_dict["issueID"] = self.issue_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.status is None:
            raise Exception("status can not None")
        if self.clock is None:
            raise Exception("clock can not None")
        if self.trigger_id is None:
            raise Exception("trigger_id can not None")
        if self.issue_id is None:
            raise Exception("issue_id can not None")


class PushAlertIssueHybridRequestParam(object):

    def __init__(self, issue_list, ):
        """
        :param issue_list:  注意:此参数为数组
        """
        self.issue_list = issue_list

    def check_param(self):
        """
        the param required check
        """
        if self.issue_list is None:
            raise Exception("issue_list can not None")

