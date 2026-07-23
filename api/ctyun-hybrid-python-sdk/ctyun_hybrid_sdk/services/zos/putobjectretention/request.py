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


class PutObjectRetentionRequest(CTYunRequest):
    """
    设置对象合规保留配置
    """

    def __init__(self, request_param):
        super(PutObjectRetentionRequest, self).__init__("/v4/oss/put-object-retention", "POST", "zos", "application/json")
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
        if self.parameters.key is not None:
            body_param["key"] = self.parameters.key
        if self.parameters.version_id is not None:
            body_param["versionID"] = self.parameters.version_id
        if self.parameters.bypass_governance_retention is not None:
            body_param["bypassGovernanceRetention"] = self.parameters.bypass_governance_retention
        if self.parameters.retention_mode is not None:
            body_param["retentionMode"] = self.parameters.retention_mode
        if self.parameters.retain_until_date is not None:
            body_param["retainUntilDate"] = self.parameters.retain_until_date
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


class PutObjectRetentionRequestParam(object):

    def __init__(self, bucket, region_id, key, bypass_governance_retention, retention_mode, retain_until_date, version_id=None):
        """
        :param bucket: 桶名	
        :param region_id: 区域 ID	
        :param key: 对象名称	
        :param version_id: 版本ID，在开启多版本时可使用	
        :param bypass_governance_retention: 指示此操作是否应绕过Governance模式限制	
        :param retention_mode: 保留模式，必须为 COMPLIANCE 或 GOVERNANCE	
        :param retain_until_date: 保留截止日期, utc 时间戳，单位秒，距当前时刻不超过 70 年（按1年365天计）	
        """
        self.bucket = bucket
        self.region_id = region_id
        self.key = key
        self.version_id = version_id
        self.bypass_governance_retention = bypass_governance_retention
        self.retention_mode = retention_mode
        self.retain_until_date = retain_until_date

    def set_version_id(self, version_id):
        """
        :param version_id: 版本ID，在开启多版本时可使用	
        """
        self.version_id = version_id

    def check_param(self):
        """
        the param required check
        """
        if self.bucket is None:
            raise Exception("bucket can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.key is None:
            raise Exception("key can not None")
        if self.bypass_governance_retention is None:
            raise Exception("bypass_governance_retention can not None")
        if self.retention_mode is None:
            raise Exception("retention_mode can not None")
        if self.retain_until_date is None:
            raise Exception("retain_until_date can not None")

