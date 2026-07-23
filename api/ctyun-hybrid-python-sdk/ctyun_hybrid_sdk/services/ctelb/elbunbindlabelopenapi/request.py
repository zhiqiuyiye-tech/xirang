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


class ElbUnbindLabelOpenapiRequest(CTYunRequest):
    """
    负载均衡解绑标签
    """

    def __init__(self, request_param):
        super(ElbUnbindLabelOpenapiRequest, self).__init__("/v4/elb/unbind-label", "POST", "ctelb", "application/json")
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
        if self.parameters.elb_id is not None:
            body_param["elbID"] = self.parameters.elb_id
        if self.parameters.label_id is not None:
            body_param["labelID"] = self.parameters.label_id
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


class ElbUnbindLabelOpenapiRequestParam(object):

    def __init__(self, region_id, elb_id, label_id, ):
        """
        :param region_id: 资源id
        :param elb_id: 负载均衡id
        :param label_id: 标签id
        """
        self.region_id = region_id
        self.elb_id = elb_id
        self.label_id = label_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.elb_id is None:
            raise Exception("elb_id can not None")
        if self.label_id is None:
            raise Exception("label_id can not None")

