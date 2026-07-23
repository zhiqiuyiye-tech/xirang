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


class QueryEbsByIDRequest(CTYunRequest):
    """
    基于磁盘ID查询云硬盘详情。   
    ** 注意**： 此接口原始接口支持GET body 请求模式 从1.14.28 版本 修改为支持GET Query模式并对老版本进行了兼容，公有云同步修改为GET Query模式。如您使用的版本低于1.14.28 请使用GET body 请求模式 进行请求   
    增加diskId兼容
    """

    def __init__(self, request_param):
        super(QueryEbsByIDRequest, self).__init__("/v4/ebs/info-ebs", "GET", "ebs", "application/json")
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
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        return body_param

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.disk_id is not None:
            query_param["diskID"] = self.parameters.disk_id
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryEbsByIDRequestParam(object):

    def __init__(self, disk_id, region_id=None):
        """
        :param disk_id: 
        :param region_id: 
        """
        self.disk_id = disk_id
        self.region_id = region_id

    def set_region_id(self, region_id):
        """
        :param region_id: 
        """
        self.region_id = region_id

    def check_param(self):
        """
        the param required check
        """
        if self.disk_id is None:
            raise Exception("disk_id can not None")

