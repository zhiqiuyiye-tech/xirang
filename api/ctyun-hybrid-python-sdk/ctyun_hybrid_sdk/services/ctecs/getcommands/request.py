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


class GetCommandsRequest(CTYunRequest):
    """
    调用此接口可以查询用户手动创建的云助手命令或者云助手公共命令
    """

    def __init__(self, request_param):
        super(GetCommandsRequest, self).__init__("/v4/cloud-assistant/get-commands", "POST", "ctecs", "application/json")
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
        if self.parameters.is_public is not None:
            body_param["isPublic"] = self.parameters.is_public
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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
        :param key: 过滤条件的字段名，支持commandID、commandName、commandType
        :param value: 过滤字段对应的值
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


class GetCommandsRequestParam(object):

    def __init__(self, region_id, is_public=None, page_no=None, page_size=None, filters=None):
        """
        :param region_id: 资源池ID
        :param is_public: 是否为公共市场命令
        :param page_no: 当前页码，不传默认值为1
        :param page_size: 分页查询时设置的每页行数，最大值为100，默认为10,超过100按100查询，小于0按10查询
        :param filters: 过滤条件，json形式数组 注意:此参数为数组
        """
        self.region_id = region_id
        self.is_public = is_public
        self.page_no = page_no
        self.page_size = page_size
        self.filters = filters

    def set_is_public(self, is_public):
        """
        :param is_public: 是否为公共市场命令
        """
        self.is_public = is_public

    def set_page_no(self, page_no):
        """
        :param page_no: 当前页码，不传默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时设置的每页行数，最大值为100，默认为10,超过100按100查询，小于0按10查询
        """
        self.page_size = page_size

    def set_filters(self, filters):
        """
        :param filters: 过滤条件，json形式数组
        """
        self.filters = filters

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

