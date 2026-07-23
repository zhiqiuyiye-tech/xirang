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


class EbsInfoByNameRequest(CTYunRequest):
    """
    基于名字查询云硬盘详情
    """

    def __init__(self, request_param):
        super(EbsInfoByNameRequest, self).__init__("/v4/ebs/info-by-name", "GET", "ebs", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.name is not None:
            query_param["name"] = self.parameters.name
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class EbsInfoByNameRequestParam(object):

    def __init__(self, region_id, name, ):
        """
        :param region_id: 资源池id
        :param name: 云盘名
        """
        self.region_id = region_id
        self.name = name

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")

