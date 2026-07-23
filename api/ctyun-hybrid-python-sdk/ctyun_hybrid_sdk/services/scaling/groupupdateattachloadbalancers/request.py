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


class GroupUpdateAttachLoadBalancersRequest(CTYunRequest):
    """
    添加一个或多个负载均衡，伸缩组本质上绑定的是主机组，所以主机组ID不能重复   
    添加的负载均衡和主机组需要与伸缩组同一资源池，同一vdc，并且开启健康检查功能
    """

    def __init__(self, request_param):
        super(GroupUpdateAttachLoadBalancersRequest, self).__init__("/v4/scaling/group/update-attach-load-balancers", "POST", "scaling", "application/json")
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

    def __init__(self, lb_id, host_group_id, port, weight, ):
        """
        :param lb_id: 负载均衡ID
        :param host_group_id: 主机组ID，本质上绑定的是主机组
        :param port: 端口号 取值范围0到65536
        :param weight: 权重取值 范围1到256
        """
        self.lb_id = lb_id
        self.host_group_id = host_group_id
        self.port = port
        self.weight = weight
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.lb_id is not None:
            obj_dict["lbID"] = self.lb_id
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
        if self.lb_id is None:
            raise Exception("lb_id can not None")
        if self.host_group_id is None:
            raise Exception("host_group_id can not None")
        if self.port is None:
            raise Exception("port can not None")
        if self.weight is None:
            raise Exception("weight can not None")


class GroupUpdateAttachLoadBalancersRequestParam(object):

    def __init__(self, group_id, region_id, lb_list, ):
        """
        :param group_id: 伸缩组ID
        :param region_id: 资源池ID
        :param lb_list: 负载均衡列表，只有开启了负载均衡的伸缩组可以绑定负载均衡，总数不能超过十个 注意:此参数为数组
        """
        self.group_id = group_id
        self.region_id = region_id
        self.lb_list = lb_list

    def check_param(self):
        """
        the param required check
        """
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.lb_list is None:
            raise Exception("lb_list can not None")

