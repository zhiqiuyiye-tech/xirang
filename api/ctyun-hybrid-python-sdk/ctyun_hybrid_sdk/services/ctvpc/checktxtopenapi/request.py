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


class CheckTxtOpenapiRequest(CTYunRequest):
    """
    检查TXT记录集合法性
    """

    def __init__(self, request_param):
        super(CheckTxtOpenapiRequest, self).__init__("/v4/private-zone-record/check-txt", "POST", "ctvpc", "application/json")
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
        if self.parameters.txt_records is not None:
            body_param["txtRecords"] = self.parameters.txt_records
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


class CheckTxtOpenapiRequestParam(object):

    def __init__(self, txt_records, ):
        """
        :param txt_records: 待检查的 txt数组，数组长度最大支持 10 注意:此参数为数组
        """
        self.txt_records = txt_records

    def check_param(self):
        """
        the param required check
        """
        if self.txt_records is None:
            raise Exception("txt_records can not None")

