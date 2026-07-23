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


class QueryAvailableZoneRequest(CTYunRequest):
    """
    将废弃,原因：未匹配公有云 建议使用:/v4/region/get-zones   
    补充返回参数中id的说明：V2没有数字zoneId属性，目前是根据UUID，将uuid按照’-‘分隔，并且取前两个数据，组成的16进制字符串，转换成int64生成的。即，e334a588-260e-43dc-aa29-887a8e616328 转换成 e334a588260e， 然后将e334a588260e转成int64，请勿拿此id执行查询操作   
       
    
    """

    def __init__(self, request_param):
        super(QueryAvailableZoneRequest, self).__init__("/v4/resource/query-available-zone", "GET", "common", "")
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
        return dict()

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryAvailableZoneRequestParam(object):

    def __init__(self, ):
        """
        """

    def check_param(self):
        """
        the param required check
        """
        pass

