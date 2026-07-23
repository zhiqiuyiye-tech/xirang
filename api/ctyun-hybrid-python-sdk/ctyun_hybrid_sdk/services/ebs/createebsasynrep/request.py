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


class CreateEbsAsynRepRequest(CTYunRequest):
    """
    底层暂不支持
    """

    def __init__(self, request_param):
        super(CreateEbsAsynRepRequest, self).__init__("/v4/async_rep/create", "POST", "ebs", "application/json")
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
        if self.parameters.master_ebs_uuid is not None:
            body_param["masterEbsUUID"] = self.parameters.master_ebs_uuid
        if self.parameters.replication_uuid is not None:
            body_param["replicationUUID"] = self.parameters.replication_uuid
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


class CreateEbsAsynRepRequestParam(object):

    def __init__(self, master_ebs_uuid, replication_uuid, ):
        """
        :param master_ebs_uuid: 主盘uuid
        :param replication_uuid: 异步复制uuid
        """
        self.master_ebs_uuid = master_ebs_uuid
        self.replication_uuid = replication_uuid

    def check_param(self):
        """
        the param required check
        """
        if self.master_ebs_uuid is None:
            raise Exception("master_ebs_uuid can not None")
        if self.replication_uuid is None:
            raise Exception("replication_uuid can not None")

