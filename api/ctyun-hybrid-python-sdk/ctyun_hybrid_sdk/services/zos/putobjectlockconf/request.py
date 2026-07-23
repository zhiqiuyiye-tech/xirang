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


class PutObjectLockConfRequest(CTYunRequest):
    """
    要测试该接口，在创建桶时，需要设置ObjectLockEnabledForBucket为true
    """

    def __init__(self, request_param):
        super(PutObjectLockConfRequest, self).__init__("/v4/oss/put-object-lock-conf", "POST", "zos", "application/json")
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
        if self.parameters.bucket is not None:
            body_param["bucket"] = self.parameters.bucket
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.retention_mode is not None:
            body_param["retentionMode"] = self.parameters.retention_mode
        if self.parameters.days is not None:
            body_param["days"] = self.parameters.days
        if self.parameters.years is not None:
            body_param["years"] = self.parameters.years
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


class PutObjectLockConfRequestParam(object):

    def __init__(self, bucket, region_id, retention_mode, days=None, years=None):
        """
        :param bucket: 存储空间名
        :param region_id: 资源池ID
        :param retention_mode: 保留模式，必须为COMPLIANCE 或GOVERNANCE
        :param days: 天数（days 与 years 参数必须存在其一，但不能同时存在）最大1000天
        :param years: 天数（days 与 years 参数必须存在其一，但不能同时存在）最大70年
        """
        self.bucket = bucket
        self.region_id = region_id
        self.retention_mode = retention_mode
        self.days = days
        self.years = years

    def set_days(self, days):
        """
        :param days: 天数（days 与 years 参数必须存在其一，但不能同时存在）最大1000天
        """
        self.days = days

    def set_years(self, years):
        """
        :param years: 天数（days 与 years 参数必须存在其一，但不能同时存在）最大70年
        """
        self.years = years

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.retention_mode is None:
            raise Exception("retention_mode can not None")

