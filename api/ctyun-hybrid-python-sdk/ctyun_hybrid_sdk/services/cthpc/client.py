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


class CthpcClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('cthpc-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CthpcClient, self).__init__(credential, config, 'cthpc', '0.1.0', logger, signer)

    def query_host_under_cluster(self, query_host_under_cluster_request_param):
        """
        /v4/cthpc/list-host
        查询集群下的宿主机列表
        """
        return self.send(query_host_under_cluster_request_param)

    def query_cluster_list(self, query_cluster_list_request_param):
        """
        /v4/cthpc/list-cluster
        查询集群列表
        """
        return self.send(query_cluster_list_request_param)

    def query_instance_under_cluster(self, query_instance_under_cluster_request_param):
        """
        /v4/cthpc/list-instance
        查询集群下的云主机列表
        """
        return self.send(query_instance_under_cluster_request_param)
