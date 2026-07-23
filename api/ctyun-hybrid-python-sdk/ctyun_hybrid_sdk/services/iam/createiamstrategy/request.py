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


class CreateIamStrategyRequest(CTYunRequest):
    """
    创建自定义策略-IAM
    """

    def __init__(self, request_param):
        super(CreateIamStrategyRequest, self).__init__("/v1/policy/iam/createStrategy", "POST", "iam", "application/json")
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
        if self.parameters.strategy_content is not None:
            if type(self.parameters.strategy_content) is dict:
                strategy_content_dict_value = self.parameters.strategy_content
            else:
                strategy_content_dict_value = self.parameters.strategy_content.get_dic()
            body_param["strategyContent"] = strategy_content_dict_value
        if self.parameters.strategy_name is not None:
            body_param["strategyName"] = self.parameters.strategy_name
        if self.parameters.range is not None:
            body_param["range"] = self.parameters.range
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
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


class StrategyContent(object):

    def __init__(self, version, statement, ):
        """
        :param version: 版本，1.1
        :param statement: 策略描述
        """
        self.version = version
        self.statement = statement
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.version is not None:
            obj_dict["Version"] = self.version
        if self.statement is not None:
            statement_array = []
            for item in self.statement:
                if type(item) is dict:
                    statement_array.append(item)
                else:
                    statement_array.append(item.get_dic())
            obj_dict["Statement"] = statement_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.version is None:
            raise Exception("version can not None")
        if self.statement is None:
            raise Exception("statement can not None")


class Statement(object):

    def __init__(self, resource, effect, action, ):
        """
        :param resource: 仅支持"*"
        :param effect: action允许或拒绝 Allow-允许 Deny-拒绝
        :param action: 三元组列表
        """
        self.resource = resource
        self.effect = effect
        self.action = action
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.resource is not None:
            obj_dict["Resource"] = self.resource
        if self.effect is not None:
            obj_dict["Effect"] = self.effect
        if self.action is not None:
            obj_dict["Action"] = self.action
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.resource is None:
            raise Exception("resource can not None")
        if self.effect is None:
            raise Exception("effect can not None")
        if self.action is None:
            raise Exception("action can not None")


class CreateIamStrategyRequestParam(object):

    def __init__(self, strategy_content, strategy_name, range, description=None):
        """
        :param strategy_content: 策略内容
        :param strategy_name: 策略名称，长度为3-20字符，支持中文汉字，大、小写字母，数字，支持特殊符号下划线、中划线、括号
        :param range: 策略范围 1-全局 2-资源池
        :param description: 策略描述，最长100
        """
        self.strategy_content = strategy_content
        self.strategy_name = strategy_name
        self.range = range
        self.description = description

    def set_description(self, description):
        """
        :param description: 策略描述，最长100
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.strategy_content is None:
            raise Exception("strategy_content can not None")
        if self.strategy_name is None:
            raise Exception("strategy_name can not None")
        if self.range is None:
            raise Exception("range can not None")

