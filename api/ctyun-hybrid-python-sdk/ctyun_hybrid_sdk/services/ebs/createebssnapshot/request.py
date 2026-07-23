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


class CreateEbsSnapshotRequest(CTYunRequest):
    """
    开发未对齐原因：混合云直接创建，公有云走工单创建
    """

    def __init__(self, request_param):
        super(CreateEbsSnapshotRequest, self).__init__("/v4/ebs_snapshot/create", "POST", "ebs", "application/json")
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
        if self.parameters.snapshot_name is not None:
            body_param["snapshotName"] = self.parameters.snapshot_name
        if self.parameters.volume_id is not None:
            body_param["volumeID"] = self.parameters.volume_id
        if self.parameters.retention_policy is not None:
            body_param["retentionPolicy"] = self.parameters.retention_policy
        if self.parameters.retention_time is not None:
            body_param["retentionTime"] = self.parameters.retention_time
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class CreateEbsSnapshotRequestParam(object):

    def __init__(self, region_id, snapshot_name, volume_id, retention_policy=None, retention_time=None, client_token=None):
        """
        :param region_id: 区域ID
        :param snapshot_name: 长度为2～63字符 支持以大小写字母开头，可包含数字, 字母，下划线（_）或中划线（-）
        :param volume_id: 云硬盘ID
        :param retention_policy: 快照保留策略 取值范围：[custom/forever]，custom：自定义保留天数，forever：永久保留  (公有云字段，混合云暂不匹配，忽略)
        :param retention_time: 自定义快照保留天数。取值范围：1-65535。当快照保留策略为custom时该参数为必填，否则不识别该参数  (公有云字段，混合云暂不匹配，忽略)
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一  (公有云字段，混合云暂不匹配，忽略)
        """
        self.region_id = region_id
        self.snapshot_name = snapshot_name
        self.volume_id = volume_id
        self.retention_policy = retention_policy
        self.retention_time = retention_time
        self.client_token = client_token

    def set_retention_policy(self, retention_policy):
        """
        :param retention_policy: 快照保留策略 取值范围：[custom/forever]，custom：自定义保留天数，forever：永久保留  (公有云字段，混合云暂不匹配，忽略)
        """
        self.retention_policy = retention_policy

    def set_retention_time(self, retention_time):
        """
        :param retention_time: 自定义快照保留天数。取值范围：1-65535。当快照保留策略为custom时该参数为必填，否则不识别该参数  (公有云字段，混合云暂不匹配，忽略)
        """
        self.retention_time = retention_time

    def set_client_token(self, client_token):
        """
        :param client_token: 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一  (公有云字段，混合云暂不匹配，忽略)
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_name is None:
            raise Exception("snapshot_name can not None")
        if self.volume_id is None:
            raise Exception("volume_id can not None")

