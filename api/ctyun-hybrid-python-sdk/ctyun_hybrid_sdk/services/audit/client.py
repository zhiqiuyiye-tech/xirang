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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class AuditClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('audit-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(AuditClient, self).__init__(credential, config, 'audit', '0.1.0', logger, signer)

    def describe_ecs_auditlogs(self, describe_ecs_auditlogs_request_param):
        """
        /v1/audit/ecs-audit-logs
        云主机控制台（OpenAPI）操作审计日志查询，注意请求的开始时间结束时间为UnixMilli 时间戳 或者Unix时间戳，开始时间结束时间必填，最长可以获取7天的日志，C端调用获取的是当前用户的日志，如果是B端调用可以获取用户权限下的日志（用户及下级vdc，传超管用户id 能查询所有的），
        """
        return self.send(describe_ecs_auditlogs_request_param)

    def describe_audit_log(self, describe_audit_log_request_param):
        """
        /v1/audit/logDetail
        查询审计日志详情，包含请求返回值和校验信息
        """
        return self.send(describe_audit_log_request_param)

    def describe_auditlogs(self, describe_auditlogs_request_param):
        """
        /v1/audit/auditlogs
        审计日志查询，注意请求的开始时间结束时间为UnixMilli 时间戳 或者Unix时间戳，开始时间结束时间必填，最长可以获取7天的日志，获取的是当前用户的日志，如需获取更大范围权限可以联系运维获取方案
        """
        return self.send(describe_auditlogs_request_param)
