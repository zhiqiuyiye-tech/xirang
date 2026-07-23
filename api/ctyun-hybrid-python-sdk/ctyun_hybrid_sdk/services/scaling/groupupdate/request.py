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


class GroupUpdateRequest(CTYunRequest):
    """
    修改一个弹性伸缩组
    """

    def __init__(self, request_param):
        super(GroupUpdateRequest, self).__init__("/v4/scaling/group/update", "POST", "scaling", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.max_count is not None:
            body_param["maxCount"] = self.parameters.max_count
        if self.parameters.min_count is not None:
            body_param["minCount"] = self.parameters.min_count
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.use_lb is not None:
            body_param["useLb"] = self.parameters.use_lb
        if self.parameters.move_out_strategy is not None:
            body_param["moveOutStrategy"] = self.parameters.move_out_strategy
        if self.parameters.recovery_mode is not None:
            body_param["recoveryMode"] = self.parameters.recovery_mode
        if self.parameters.health_mode is not None:
            body_param["healthMode"] = self.parameters.health_mode
        if self.parameters.health_period is not None:
            body_param["healthPeriod"] = self.parameters.health_period
        if self.parameters.lb_list is not None:
            lb_list = []
            if isinstance(self.parameters.lb_list, list):
                for item in self.parameters.lb_list:
                    if type(item) is dict:
                        lb_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        lb_list.append(item_dict_value)
            else:
                lb_list.append(self.parameters.lb_list.get_dic())
            body_param["lbList"] = lb_list
        if self.parameters.config_id is not None:
            body_param["configID"] = self.parameters.config_id
        if self.parameters.subnet_id_list is not None:
            body_param["subnetIDList"] = self.parameters.subnet_id_list
        if self.parameters.maz_info is not None:
            if type(self.parameters.maz_info) is dict:
                maz_info_dict_value = self.parameters.maz_info
            else:
                maz_info_dict_value = self.parameters.maz_info.get_dic()
            body_param["mazInfo"] = maz_info_dict_value
        if self.parameters.expected_count is not None:
            body_param["expectedCount"] = self.parameters.expected_count
        if self.parameters.security_group_id_list is not None:
            body_param["securityGroupIDList"] = self.parameters.security_group_id_list
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


class Lb(object):

    def __init__(self, id, host_group_id, port, weight, ):
        """
        :param id: 负载均衡ID
        :param host_group_id: 主机组ID，本质上绑定的是主机组
        :param port: 端口号 取值范围1到65536
        :param weight: 权重取值 范围1到256
        """
        self.id = id
        self.host_group_id = host_group_id
        self.port = port
        self.weight = weight
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.id is not None:
            obj_dict["id"] = self.id
        if self.host_group_id is not None:
            obj_dict["hostGroupID"] = self.host_group_id
        if self.port is not None:
            obj_dict["port"] = self.port
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.id is None:
            raise Exception("id can not None")
        if self.host_group_id is None:
            raise Exception("host_group_id can not None")
        if self.port is None:
            raise Exception("port can not None")
        if self.weight is None:
            raise Exception("weight can not None")


class MazInfo(object):

    def __init__(self, master_id, az_name, option_id, ):
        """
        :param master_id: 主网卡
        :param az_name: 可用区
        :param option_id: 扩展网卡列表
        """
        self.master_id = master_id
        self.az_name = az_name
        self.option_id = option_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.master_id is not None:
            obj_dict["masterId"] = self.master_id
        if self.az_name is not None:
            obj_dict["azName"] = self.az_name
        if self.option_id is not None:
            obj_dict["optionId"] = self.option_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.master_id is None:
            raise Exception("master_id can not None")
        if self.az_name is None:
            raise Exception("az_name can not None")
        if self.option_id is None:
            raise Exception("option_id can not None")


class GroupUpdateRequestParam(object):

    def __init__(self, group_id, region_id, name=None, max_count=None, min_count=None, vpc_id=None, use_lb=None, move_out_strategy=None, recovery_mode=None, health_mode=None, health_period=None, lb_list=None, config_id=None, subnet_id_list=None, maz_info=None, expected_count=None, security_group_id_list=None):
        """
        :param group_id: 伸缩组ID
        :param region_id: 资源池ID
        :param name: 伸缩组名称，长度为2-50个字符
        :param max_count: 最大实例数 不能小于最小实例数
        :param min_count: 最小实例数 不能小于零
        :param vpc_id: VPC ID
        :param use_lb: 是否使用负载均衡，是（1） 否（2）
        :param move_out_strategy: 移除策略 1、较早创建的配置较早创建的实例 2、较晚创建的配置较晚创建的实例 3、较早创建的实例 4、较晚创建的实例
        :param recovery_mode: 释放方式，释放模式（1） 停机回收模式（2）
        :param health_mode: 健康检查方式，云服务器健康检查（1） 弹性负载均衡健康检查（2），只有伸缩组使用负载均衡时支持2
        :param health_period: 健康检查间隔，单位：秒
        :param lb_list: 负载均衡列表，use_lb为1时必填，开启负载均衡的伸缩组负载均衡数量在1到10之间 注意:此参数为数组
        :param config_id: 伸缩配置ID 修改配置ID时必传，其他参数不传（v1伸缩配置与其他参数不能同时修改）(公有云和v2没有这个要求)
        :param subnet_id_list: 子网ID数组 注意:此参数为数组
        :param maz_info: 多 az 信息  暂不支持
        :param expected_count: 期望实例数，v2未实现
        :param security_group_id_list: 安全组ID列表，非多可用区资源池不使用该参数 注意:此参数为数组
        """
        self.group_id = group_id
        self.region_id = region_id
        self.name = name
        self.max_count = max_count
        self.min_count = min_count
        self.vpc_id = vpc_id
        self.use_lb = use_lb
        self.move_out_strategy = move_out_strategy
        self.recovery_mode = recovery_mode
        self.health_mode = health_mode
        self.health_period = health_period
        self.lb_list = lb_list
        self.config_id = config_id
        self.subnet_id_list = subnet_id_list
        self.maz_info = maz_info
        self.expected_count = expected_count
        self.security_group_id_list = security_group_id_list

    def set_name(self, name):
        """
        :param name: 伸缩组名称，长度为2-50个字符
        """
        self.name = name

    def set_max_count(self, max_count):
        """
        :param max_count: 最大实例数 不能小于最小实例数
        """
        self.max_count = max_count

    def set_min_count(self, min_count):
        """
        :param min_count: 最小实例数 不能小于零
        """
        self.min_count = min_count

    def set_vpc_id(self, vpc_id):
        """
        :param vpc_id: VPC ID
        """
        self.vpc_id = vpc_id

    def set_use_lb(self, use_lb):
        """
        :param use_lb: 是否使用负载均衡，是（1） 否（2）
        """
        self.use_lb = use_lb

    def set_move_out_strategy(self, move_out_strategy):
        """
        :param move_out_strategy: 移除策略 1、较早创建的配置较早创建的实例 2、较晚创建的配置较晚创建的实例 3、较早创建的实例 4、较晚创建的实例
        """
        self.move_out_strategy = move_out_strategy

    def set_recovery_mode(self, recovery_mode):
        """
        :param recovery_mode: 释放方式，释放模式（1） 停机回收模式（2）
        """
        self.recovery_mode = recovery_mode

    def set_health_mode(self, health_mode):
        """
        :param health_mode: 健康检查方式，云服务器健康检查（1） 弹性负载均衡健康检查（2），只有伸缩组使用负载均衡时支持2
        """
        self.health_mode = health_mode

    def set_health_period(self, health_period):
        """
        :param health_period: 健康检查间隔，单位：秒
        """
        self.health_period = health_period

    def set_lb_list(self, lb_list):
        """
        :param lb_list: 负载均衡列表，use_lb为1时必填，开启负载均衡的伸缩组负载均衡数量在1到10之间
        """
        self.lb_list = lb_list

    def set_config_id(self, config_id):
        """
        :param config_id: 伸缩配置ID 修改配置ID时必传，其他参数不传（v1伸缩配置与其他参数不能同时修改）(公有云和v2没有这个要求)
        """
        self.config_id = config_id

    def set_subnet_id_list(self, subnet_id_list):
        """
        :param subnet_id_list: 子网ID数组
        """
        self.subnet_id_list = subnet_id_list

    def set_maz_info(self, maz_info):
        """
        :param maz_info: 多 az 信息  暂不支持
        """
        self.maz_info = maz_info

    def set_expected_count(self, expected_count):
        """
        :param expected_count: 期望实例数，v2未实现
        """
        self.expected_count = expected_count

    def set_security_group_id_list(self, security_group_id_list):
        """
        :param security_group_id_list: 安全组ID列表，非多可用区资源池不使用该参数
        """
        self.security_group_id_list = security_group_id_list

    def check_param(self):
        """
        the param required check
        """
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")

