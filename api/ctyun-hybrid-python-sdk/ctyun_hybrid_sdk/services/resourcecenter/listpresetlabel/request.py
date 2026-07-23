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


class ListPresetLabelRequest(CTYunRequest):
    """
    查询预置标签列表
    """

    def __init__(self, request_param):
        super(ListPresetLabelRequest, self).__init__("/v4/resource-center/label/list/preset", "POST", "resourcecenter", "application/json")
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
        if self.parameters.vdc_id is not None:
            body_param["vdcID"] = self.parameters.vdc_id
        if self.parameters.label_keys is not None:
            body_param["labelKeys"] = self.parameters.label_keys
        if self.parameters.fuzzy_label_key is not None:
            body_param["fuzzyLabelKey"] = self.parameters.fuzzy_label_key
        if self.parameters.label_values is not None:
            body_param["labelValues"] = self.parameters.label_values
        if self.parameters.fuzzy_label_value is not None:
            body_param["fuzzyLabelValue"] = self.parameters.fuzzy_label_value
        if self.parameters.label_ids is not None:
            body_param["labelIDs"] = self.parameters.label_ids
        if self.parameters.fuzzy_label_id is not None:
            body_param["fuzzyLabelID"] = self.parameters.fuzzy_label_id
        if self.parameters.fuzzy_content is not None:
            body_param["fuzzyContent"] = self.parameters.fuzzy_content
        if self.parameters.sort is not None:
            body_param["sort"] = self.parameters.sort
        if self.parameters.asc is not None:
            body_param["asc"] = self.parameters.asc
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
        if self.parameters.page is not None:
            body_param["page"] = self.parameters.page
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


class ListPresetLabelRequestParam(object):

    def __init__(self, vdc_id, label_keys=None, fuzzy_label_key=None, label_values=None, fuzzy_label_value=None, label_ids=None, fuzzy_label_id=None, fuzzy_content=None, sort=None, asc=None, page_size=None, page=None):
        """
        :param vdc_id: 查询预置标签必传
        :param label_keys: (数组)批量精确搜索标签键 注意:此参数为数组
        :param fuzzy_label_key: 模糊搜索标签键
        :param label_values: (数组)批量精确搜索标签值 注意:此参数为数组
        :param fuzzy_label_value: 模糊搜索标签值
        :param label_ids: (数组)批量精确搜索标签ID 注意:此参数为数组
        :param fuzzy_label_id: 模糊搜索标签ID
        :param fuzzy_content: 模糊搜索范围：标签键，标签值
        :param sort: 指定排序字段
        :param asc: 与sort组合使用
        :param page_size: 分页大小
        :param page: -1 返回全量数据不分页
        """
        self.vdc_id = vdc_id
        self.label_keys = label_keys
        self.fuzzy_label_key = fuzzy_label_key
        self.label_values = label_values
        self.fuzzy_label_value = fuzzy_label_value
        self.label_ids = label_ids
        self.fuzzy_label_id = fuzzy_label_id
        self.fuzzy_content = fuzzy_content
        self.sort = sort
        self.asc = asc
        self.page_size = page_size
        self.page = page

    def set_label_keys(self, label_keys):
        """
        :param label_keys: (数组)批量精确搜索标签键
        """
        self.label_keys = label_keys

    def set_fuzzy_label_key(self, fuzzy_label_key):
        """
        :param fuzzy_label_key: 模糊搜索标签键
        """
        self.fuzzy_label_key = fuzzy_label_key

    def set_label_values(self, label_values):
        """
        :param label_values: (数组)批量精确搜索标签值
        """
        self.label_values = label_values

    def set_fuzzy_label_value(self, fuzzy_label_value):
        """
        :param fuzzy_label_value: 模糊搜索标签值
        """
        self.fuzzy_label_value = fuzzy_label_value

    def set_label_ids(self, label_ids):
        """
        :param label_ids: (数组)批量精确搜索标签ID
        """
        self.label_ids = label_ids

    def set_fuzzy_label_id(self, fuzzy_label_id):
        """
        :param fuzzy_label_id: 模糊搜索标签ID
        """
        self.fuzzy_label_id = fuzzy_label_id

    def set_fuzzy_content(self, fuzzy_content):
        """
        :param fuzzy_content: 模糊搜索范围：标签键，标签值
        """
        self.fuzzy_content = fuzzy_content

    def set_sort(self, sort):
        """
        :param sort: 指定排序字段
        """
        self.sort = sort

    def set_asc(self, asc):
        """
        :param asc: 与sort组合使用
        """
        self.asc = asc

    def set_page_size(self, page_size):
        """
        :param page_size: 分页大小
        """
        self.page_size = page_size

    def set_page(self, page):
        """
        :param page: -1 返回全量数据不分页
        """
        self.page = page

    def check_param(self):
        """
        the param required check
        """
        if self.vdc_id is None:
            raise Exception("vdc_id can not None")

