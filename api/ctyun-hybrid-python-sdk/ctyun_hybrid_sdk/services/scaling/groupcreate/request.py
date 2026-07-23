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


class GroupCreateRequest(CTYunRequest):
    """
    创建一个弹性伸缩组，注意伸缩组名称不能重复
    """

    def __init__(self, request_param):
        super(GroupCreateRequest, self).__init__("/v4/scaling/group/create", "POST", "scaling", "application/json")
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
        if self.parameters.config_id is not None:
            body_param["configID"] = self.parameters.config_id
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
        if self.parameters.max_count is not None:
            body_param["maxCount"] = self.parameters.max_count
        if self.parameters.min_count is not None:
            body_param["minCount"] = self.parameters.min_count
        if self.parameters.move_out_strategy is not None:
            body_param["moveOutStrategy"] = self.parameters.move_out_strategy
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.recovery_mode is not None:
            body_param["recoveryMode"] = self.parameters.recovery_mode
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.subnet_id_list is not None:
            body_param["subnetIDList"] = self.parameters.subnet_id_list
        if self.parameters.use_lb is not None:
            body_param["useLb"] = self.parameters.use_lb
        if self.parameters.vpc_id is not None:
            body_param["vpcID"] = self.parameters.vpc_id
        if self.parameters.security_group_id_list is not None:
            body_param["securityGroupIDList"] = self.parameters.security_group_id_list
        if self.parameters.expected_count is not None:
            body_param["expectedCount"] = self.parameters.expected_count
        if self.parameters.maz_info is not None:
            maz_info = []
            if isinstance(self.parameters.maz_info, list):
                for item in self.parameters.maz_info:
                    if type(item) is dict:
                        maz_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        maz_info.append(item_dict_value)
            else:
                maz_info.append(self.parameters.maz_info.get_dic())
            body_param["mazInfo"] = maz_info
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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

    def __init__(self, host_group_id, lb_id, port, weight, ):
        """
        :param host_group_id: 主机组ID，本质上绑定的是主机组
        :param lb_id: 负载均衡ID
        :param port: 端口号 取值范围1到65536
        :param weight: 权重取值 范围1到256
        """
        self.host_group_id = host_group_id
        self.lb_id = lb_id
        self.port = port
        self.weight = weight
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.host_group_id is not None:
            obj_dict["hostGroupID"] = self.host_group_id
        if self.lb_id is not None:
            obj_dict["lbID"] = self.lb_id
        if self.port is not None:
            obj_dict["port"] = self.port
        if self.weight is not None:
            obj_dict["weight"] = self.weight
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.host_group_id is None:
            raise Exception("host_group_id can not None")
        if self.lb_id is None:
            raise Exception("lb_id can not None")
        if self.port is None:
            raise Exception("port can not None")
        if self.weight is None:
            raise Exception("weight can not None")


class MazInfo(object):

    def __init__(self, master_id, az_name, option_id=None):
        """
        :param master_id: 主网卡，子网可跨可用区
        :param az_name: 云主机的可用区
        :param option_id: 扩展网卡列表
        """
        self.master_id = master_id
        self.az_name = az_name
        self.option_id = option_id
        self.check_param()

    def set_option_id(self, option_id):
        """
        :param option_id: 扩展网卡列表
        """
        self.option_id = option_id

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


class GroupCreateRequestParam(object):

    def __init__(self, config_id, health_mode, health_period, max_count, min_count, move_out_strategy, name, recovery_mode, region_id, subnet_id_list, use_lb, vpc_id, security_group_id_list, lb_list=None, expected_count=None, maz_info=None, project_id=None):
        """
        :param config_id: 伸缩配置ID
        :param health_mode: 健康检查方式，云服务器健康检查（1） 弹性负载均衡健康检查（2）
        :param health_period: 健康检查间隔，单位：秒
        :param lb_list: 负载均衡列表，use_lb为1时必填 注意:此参数为数组
        :param max_count: 最大实例数，大于等于0，且大于等于最小实例数
        :param min_count: 最小实例数，大于等于0，且小于等于最小实例数
        :param move_out_strategy: 移除策略 1、较早创建的配置较早创建的实例 2、较晚创建的配置较晚创建的实例 3、较早创建的实例 4、较晚创建的实例
        :param name: 伸缩组名称，长度2-50个字符
        :param recovery_mode: 释放方式，释放模式（1） 停机回收模式（2）
        :param region_id: 区域id
        :param subnet_id_list: 子网ID列表  由于mazInfo暂不支持，所以必传 注意:此参数为数组
        :param use_lb: 是否使用负载均衡，是（1） 否（2）
        :param vpc_id: VPC ID
        :param security_group_id_list: 安全组ID列表，公有云必传，由于新建伸缩配置暂不支持，所以必传
        :param expected_count: 期望实例数，v2未实现
        :param maz_info: 多可用区资源池的实例可用区及子网信息。暂不支持 注意:此参数为数组
        :param project_id: 项目ID
        """
        self.config_id = config_id
        self.health_mode = health_mode
        self.health_period = health_period
        self.lb_list = lb_list
        self.max_count = max_count
        self.min_count = min_count
        self.move_out_strategy = move_out_strategy
        self.name = name
        self.recovery_mode = recovery_mode
        self.region_id = region_id
        self.subnet_id_list = subnet_id_list
        self.use_lb = use_lb
        self.vpc_id = vpc_id
        self.security_group_id_list = security_group_id_list
        self.expected_count = expected_count
        self.maz_info = maz_info
        self.project_id = project_id

    def set_lb_list(self, lb_list):
        """
        :param lb_list: 负载均衡列表，use_lb为1时必填
        """
        self.lb_list = lb_list

    def set_expected_count(self, expected_count):
        """
        :param expected_count: 期望实例数，v2未实现
        """
        self.expected_count = expected_count

    def set_maz_info(self, maz_info):
        """
        :param maz_info: 多可用区资源池的实例可用区及子网信息。暂不支持
        """
        self.maz_info = maz_info

    def set_project_id(self, project_id):
        """
        :param project_id: 项目ID
        """
        self.project_id = project_id

    def check_param(self):
        """
        the param required check
        """
        if self.config_id is None:
            raise Exception("config_id can not None")
        if self.health_mode is None:
            raise Exception("health_mode can not None")
        if self.health_period is None:
            raise Exception("health_period can not None")
        if self.max_count is None:
            raise Exception("max_count can not None")
        if self.min_count is None:
            raise Exception("min_count can not None")
        if self.move_out_strategy is None:
            raise Exception("move_out_strategy can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.recovery_mode is None:
            raise Exception("recovery_mode can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.subnet_id_list is None:
            raise Exception("subnet_id_list can not None")
        if self.use_lb is None:
            raise Exception("use_lb can not None")
        if self.vpc_id is None:
            raise Exception("vpc_id can not None")
        if self.security_group_id_list is None:
            raise Exception("security_group_id_list can not None")

