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


class LabelUnBindResourceRequest(CTYunRequest):
    """
    标签解绑资源
    """

    def __init__(self, request_param):
        super(LabelUnBindResourceRequest, self).__init__("/v4/resource-center/label/unbind", "POST", "resourcecenter", "application/json")
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
        if self.parameters.resources is not None:
            resources = []
            if isinstance(self.parameters.resources, list):
                for item in self.parameters.resources:
                    if type(item) is dict:
                        resources.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        resources.append(item_dict_value)
            else:
                resources.append(self.parameters.resources.get_dic())
            body_param["resources"] = resources
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


class Resource(object):

    def __init__(self, resource_id, label_ids, ):
        """
        :param resource_id: 解绑资源ID
        :param label_ids: 解绑标签ID数组
        """
        self.resource_id = resource_id
        self.label_ids = label_ids
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.resource_id is not None:
            obj_dict["resourceID"] = self.resource_id
        if self.label_ids is not None:
            obj_dict["labelIDs"] = self.label_ids
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.resource_id is None:
            raise Exception("resource_id can not None")
        if self.label_ids is None:
            raise Exception("label_ids can not None")


class LabelUnBindResourceRequestParam(object):

    def __init__(self, resources, ):
        """
        :param resources: 解绑资源对象数组 注意:此参数为数组
        """
        self.resources = resources

    def check_param(self):
        """
        the param required check
        """
        if self.resources is None:
            raise Exception("resources can not None")

