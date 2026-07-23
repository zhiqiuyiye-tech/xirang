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


class DeletePublicLabelRequest(CTYunRequest):
    """
    删除标签同时`解绑`其关联的所有资源
    """

    def __init__(self, request_param):
        super(DeletePublicLabelRequest, self).__init__("/v4/resource-center/label/delete/public", "POST", "resourcecenter", "application/json")
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
        if self.parameters.label_ids is not None:
            body_param["labelIDs"] = self.parameters.label_ids
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


class DeletePublicLabelRequestParam(object):

    def __init__(self, label_ids, ):
        """
        :param label_ids: 请确保id正确，否则会报错 注意:此参数为数组
        """
        self.label_ids = label_ids

    def check_param(self):
        """
        the param required check
        """
        if self.label_ids is None:
            raise Exception("label_ids can not None")

