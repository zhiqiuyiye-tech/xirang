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


class DssClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('dss-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(DssClient, self).__init__(credential, config, 'dss', '0.1.0', logger, signer)

    def update_dss_name(self, update_dss_name_request_param):
        """
        /v4/dss/rename
        修改块存储专属集群名称
        """
        return self.send(update_dss_name_request_param)

    def list_dss(self, list_dss_request_param):
        """
        /v4/dss/list
        查询块存储专属集群
        """
        return self.send(list_dss_request_param)

    def dss_cluster_remove_pool(self, dss_cluster_remove_pool_request_param):
        """
        /v4/dss/remove-pool
        添加存储池到块存储专属集群
        """
        return self.send(dss_cluster_remove_pool_request_param)

    def dss_cluster_add_pool(self, dss_cluster_add_pool_request_param):
        """
        /v4/dss/add-pool
        添加存储池到块存储专属集群
        """
        return self.send(dss_cluster_add_pool_request_param)

    def delete_dss_cluster(self, delete_dss_cluster_request_param):
        """
        /v4/dss/delete
        删除块存储专属云
        """
        return self.send(delete_dss_cluster_request_param)
