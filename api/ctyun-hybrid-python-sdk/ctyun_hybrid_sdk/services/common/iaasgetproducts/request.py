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


class IaasGetProductsRequest(CTYunRequest):
    """
    查询一个资源池支持的云产品信息列表，以及云产品的产品特性信息。   
       
    ## 接口约束: 2.2.1 以下版本只支持云盘产品信息返回，2.2.1 版本以上支持返回云盘产品信息，oss，hpfs和sfs支持信息返回。   
    
    """

    def __init__(self, request_param):
        super(IaasGetProductsRequest, self).__init__("/v4/region/get-products", "GET", "common", "")
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
        if self.parameters.version is not None:
            query_param["version"] = self.parameters.version
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class IaasGetProductsRequestParam(object):

    def __init__(self, region_id, version=None):
        """
        :param region_id: 资源池ID
        :param version: 传任意值：不为空的时候返回底层透传磁盘类型；为空的时候返回和公有云匹配磁盘类型
        """
        self.region_id = region_id
        self.version = version

    def set_version(self, version):
        """
        :param version: 传任意值：不为空的时候返回底层透传磁盘类型；为空的时候返回和公有云匹配磁盘类型
        """
        self.version = version

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

