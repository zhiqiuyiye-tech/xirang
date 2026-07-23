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


class CreateRuleRequest(CTYunRequest):
    """
    创建转发规则   
       
    #### 备注   
    * 不支持 3.0，因为 3.0 是异步逻辑，4.0 是同步逻辑
    """

    def __init__(self, request_param):
        super(CreateRuleRequest, self).__init__("/v4/elb/create-rule", "POST", "ctelb", "application/json")
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
        if self.parameters.action is not None:
            if type(self.parameters.action) is dict:
                action_dict_value = self.parameters.action
            else:
                action_dict_value = self.parameters.action.get_dic()
            body_param["action"] = action_dict_value
        if self.parameters.conditions is not None:
            if type(self.parameters.conditions) is dict:
                conditions_dict_value = self.parameters.conditions
            else:
                conditions_dict_value = self.parameters.conditions.get_dic()
            body_param["conditions"] = conditions_dict_value
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.listener_id is not None:
            body_param["listenerID"] = self.parameters.listener_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.priority is not None:
            body_param["priority"] = self.parameters.priority
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class Action(object):

    def __init__(self, type, forward_config=None, redirect_listener_id=None):
        """
        :param type: 默认规则动作类型。取值范围：forward、redirect、deny(目前暂不支持配置为deny)
        :param forward_config: 转发配置，当type为forward时，此字段必填
        :param redirect_listener_id: 重定向监听器ID，当type为redirect时，此字段必填
        """
        self.type = type
        self.forward_config = forward_config
        self.redirect_listener_id = redirect_listener_id
        self.check_param()

    def set_forward_config(self, forward_config):
        """
        :param forward_config: 转发配置，当type为forward时，此字段必填
        """
        self.forward_config = forward_config

    def set_redirect_listener_id(self, redirect_listener_id):
        """
        :param redirect_listener_id: 重定向监听器ID，当type为redirect时，此字段必填
        """
        self.redirect_listener_id = redirect_listener_id

    def get_dic(self):
        obj_dict = dict()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.forward_config is not None:
            if type(self.forward_config) is dict:
                obj_dict["forwardConfig"] = self.forward_config
            else:
                obj_dict["forwardConfig"] = self.forward_config.get_dic()
        if self.redirect_listener_id is not None:
            obj_dict["redirectListenerID"] = self.redirect_listener_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class ForwardConfig(object):

    def __init__(self, target_groups, ):
        """
        :param target_groups: 后端服务组
        """
        self.target_groups = target_groups
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.target_groups is not None:
            target_groups_array = []
            for item in self.target_groups:
                if type(item) is dict:
                    target_groups_array.append(item)
                else:
                    target_groups_array.append(item.get_dic())
            obj_dict["targetGroups"] = target_groups_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.target_groups is None:
            raise Exception("target_groups can not None")


class TargetGroup(object):

    def __init__(self, target_group_id, weight=None):
        """
        :param target_group_id: 后端服务组ID
        :param weight: 权重，取值范围：1-256。传0或不传默认为100
        """
        self.target_group_id = target_group_id
        self.weight = weight
        self.check_param()

    def set_weight(self, weight):
        """
        :param weight: 权重，取值范围：1-256。传0或不传默认为100
        """
        self.weight = weight

    def get_dic(self):
        obj_dict = dict()
        if self.target_group_id is not None:
            obj_dict["targetGroupID"] = self.target_group_id
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.target_group_id is None:
            raise Exception("target_group_id can not None")


class Conditions(object):

    def __init__(self, type, server_name_config=None, url_path_config=None):
        """
        :param server_name_config: 服务名称（type为server_name时必传）
        :param type: server_name 、url_path
        :param url_path_config: 匹配路径（type为url_path时必传）
        """
        self.server_name_config = server_name_config
        self.type = type
        self.url_path_config = url_path_config
        self.check_param()

    def set_server_name_config(self, server_name_config):
        """
        :param server_name_config: 服务名称（type为server_name时必传）
        """
        self.server_name_config = server_name_config

    def set_url_path_config(self, url_path_config):
        """
        :param url_path_config: 匹配路径（type为url_path时必传）
        """
        self.url_path_config = url_path_config

    def get_dic(self):
        obj_dict = dict()
        if self.server_name_config is not None:
            if type(self.server_name_config) is dict:
                obj_dict["serverNameConfig"] = self.server_name_config
            else:
                obj_dict["serverNameConfig"] = self.server_name_config.get_dic()
        if self.type is not None:
            obj_dict["type"] = self.type
        if self.url_path_config is not None:
            if type(self.url_path_config) is dict:
                obj_dict["urlPathConfig"] = self.url_path_config
            else:
                obj_dict["urlPathConfig"] = self.url_path_config.get_dic()
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")


class ServerNameConfig(object):

    def __init__(self, server_name=None):
        """
        :param server_name: 域名
        """
        self.server_name = server_name

    def set_server_name(self, server_name):
        """
        :param server_name: 域名
        """
        self.server_name = server_name

    def get_dic(self):
        obj_dict = dict()
        if self.server_name is not None:
            obj_dict["serverName"] = self.server_name
        return obj_dict


class UrlPathConfig(object):

    def __init__(self, match_type, url_paths, ):
        """
        :param match_type: 匹配类型。取值范围：ABSOLUTE，PREFIX，REG
        :param url_paths: 匹配路径
        """
        self.match_type = match_type
        self.url_paths = url_paths
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.match_type is not None:
            obj_dict["matchType"] = self.match_type
        if self.url_paths is not None:
            obj_dict["urlPaths"] = self.url_paths
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.match_type is None:
            raise Exception("match_type can not None")
        if self.url_paths is None:
            raise Exception("url_paths can not None")


class CreateRuleRequestParam(object):

    def __init__(self, action, conditions, listener_id, region_id, description=None, priority=None, client_token=None):
        """
        :param action: 规则目标
        :param conditions: 匹配规则数据
        :param description: 描述，长度为0-100字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        :param listener_id: 监听器ID
        :param region_id: 区域ID
        :param priority: 底层不支持传参或修改，实际无效果
        :param client_token: 公有云需要暂无实际作用（非必填，并且此字段在私有云不具有实际意义）
        """
        self.action = action
        self.conditions = conditions
        self.description = description
        self.listener_id = listener_id
        self.region_id = region_id
        self.priority = priority
        self.client_token = client_token

    def set_description(self, description):
        """
        :param description: 描述，长度为0-100字符 支持使用中文、字母、数字、特殊符号！@#￥%……&*（） —— -+={}《》？：“”【】、；‘'，。、
        """
        self.description = description

    def set_priority(self, priority):
        """
        :param priority: 底层不支持传参或修改，实际无效果
        """
        self.priority = priority

    def set_client_token(self, client_token):
        """
        :param client_token: 公有云需要暂无实际作用（非必填，并且此字段在私有云不具有实际意义）
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.action is None:
            raise Exception("action can not None")
        if self.conditions is None:
            raise Exception("conditions can not None")
        if self.listener_id is None:
            raise Exception("listener_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

