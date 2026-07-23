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


class ListHavipRequest(CTYunRequest):
    """
    查询HaVip，从1.14.27将返回中的instanceInfo字段从对象改为了集合(改动原因：vip下可以绑定多个云主机，符合业务逻辑)，同时新增了networkInfo集合
    """

    def __init__(self, request_param):
        super(ListHavipRequest, self).__init__("/v4/vpc/havip/list", "POST", "ctvpc", "application/json")
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
        if self.parameters.filters is not None:
            filters = []
            if isinstance(self.parameters.filters, list):
                for item in self.parameters.filters:
                    if type(item) is dict:
                        filters.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        filters.append(item_dict_value)
            else:
                filters.append(self.parameters.filters.get_dic())
            body_param["filters"] = filters
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.project_id is not None:
            body_param["projectID"] = self.parameters.project_id
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


class Filter(object):

    def __init__(self, key, value, ):
        """
        :param key: 筛选字段的key，支持：haVipID，vpcID，subnetID，其中vpcID和subnetID支持模糊筛选
        :param value: 筛选字段对应key的value
        """
        self.key = key
        self.value = value
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.key is not None:
            obj_dict["key"] = self.key
        if self.value is not None:
            obj_dict["value"] = self.value
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.key is None:
            raise Exception("key can not None")
        if self.value is None:
            raise Exception("value can not None")


class ListHavipRequestParam(object):

    def __init__(self, region_id, filters=None, az_name=None, project_id=None, client_token=None):
        """
        :param region_id: 资源池id
        :param filters: 筛选条件，不同字段组合筛选 注意:此参数为数组
        :param az_name: 可用区名称(暂没有用到)
        :param project_id: 企业项目ID
        :param client_token: 可传但是不进行校验, 客户端存根
        """
        self.region_id = region_id
        self.filters = filters
        self.az_name = az_name
        self.project_id = project_id
        self.client_token = client_token

    def set_filters(self, filters):
        """
        :param filters: 筛选条件，不同字段组合筛选
        """
        self.filters = filters

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称(暂没有用到)
        """
        self.az_name = az_name

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验, 客户端存根
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

