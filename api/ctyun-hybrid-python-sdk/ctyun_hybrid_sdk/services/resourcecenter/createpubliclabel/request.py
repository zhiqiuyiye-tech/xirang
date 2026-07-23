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


class CreatePublicLabelRequest(CTYunRequest):
    """
    创建自定义（公共）标签
    """

    def __init__(self, request_param):
        super(CreatePublicLabelRequest, self).__init__("/v4/resource-center/label/create/public", "POST", "resourcecenter", "application/json")
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
        if self.parameters.labels is not None:
            labels = []
            if isinstance(self.parameters.labels, list):
                for item in self.parameters.labels:
                    if type(item) is dict:
                        labels.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        labels.append(item_dict_value)
            else:
                labels.append(self.parameters.labels.get_dic())
            body_param["labels"] = labels
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


class Label(object):

    def __init__(self, label_key, label_value, ):
        """
        :param label_key: 长度为1~32字符，支持使用中文、英文字母、数字、下划线（_）、中划线（-）
        :param label_value: 长度为1~32字符，支持使用中文、英文字母、数字、下划线（_）、中划线（-）、点号（.）
        """
        self.label_key = label_key
        self.label_value = label_value
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.label_key is not None:
            obj_dict["labelKey"] = self.label_key
        if self.label_value is not None:
            obj_dict["labelValue"] = self.label_value
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.label_key is None:
            raise Exception("label_key can not None")
        if self.label_value is None:
            raise Exception("label_value can not None")


class CreatePublicLabelRequestParam(object):

    def __init__(self, labels, ):
        """
        :param labels: 标签对象数组 注意:此参数为数组
        """
        self.labels = labels

    def check_param(self):
        """
        the param required check
        """
        if self.labels is None:
            raise Exception("labels can not None")

