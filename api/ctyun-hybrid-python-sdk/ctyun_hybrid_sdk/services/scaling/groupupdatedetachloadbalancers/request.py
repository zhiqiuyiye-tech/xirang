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


class GroupUpdateDetachLoadBalancersRequest(CTYunRequest):
    """
    删除一个或多个负载均衡
    """

    def __init__(self, request_param):
        super(GroupUpdateDetachLoadBalancersRequest, self).__init__("/v4/scaling/group/update-detach-load-balancers", "POST", "scaling", "application/json")
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

    def __init__(self, lb_id, host_group_id, ):
        """
        :param lb_id: 负载均衡ID
        :param host_group_id: 主机组ID
        """
        self.lb_id = lb_id
        self.host_group_id = host_group_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.lb_id is not None:
            obj_dict["lbID"] = self.lb_id
        if self.host_group_id is not None:
            obj_dict["hostGroupID"] = self.host_group_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.lb_id is None:
            raise Exception("lb_id can not None")
        if self.host_group_id is None:
            raise Exception("host_group_id can not None")


class GroupUpdateDetachLoadBalancersRequestParam(object):

    def __init__(self, group_id, region_id, lb_list, ):
        """
        :param group_id: 伸缩组ID
        :param region_id: 资源池ID
        :param lb_list: 负载均衡列表，删除的负载均衡需要和伸缩组有绑定关系，且当伸缩组开启负载均衡时，负载均衡数量不能小于1 注意:此参数为数组
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

