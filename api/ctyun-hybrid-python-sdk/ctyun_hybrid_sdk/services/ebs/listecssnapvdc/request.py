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


class ListEcsSnapVdcRequest(CTYunRequest):
    """
    查询快照列表-vdc   
    默认查询用户所在VDC资源，暂不支持返回所有下级VDC资源。
    """

    def __init__(self, request_param):
        super(ListEcsSnapVdcRequest, self).__init__("/v4/ebs_snapshot/list-vdc", "GET", "ebs", "")
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
        if self.parameters.volume_id is not None:
            query_param["volumeID"] = self.parameters.volume_id
        if self.parameters.org_id is not None:
            query_param["orgId"] = self.parameters.org_id
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListEcsSnapVdcRequestParam(object):

    def __init__(self, region_id, volume_id, org_id=None):
        """
        :param region_id: 资源池ID
        :param volume_id: 云硬盘ID
        :param org_id: 组织ID
        """
        self.region_id = region_id
        self.volume_id = volume_id
        self.org_id = org_id

    def set_org_id(self, org_id):
        """
        :param org_id: 组织ID
        """
        self.org_id = org_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.volume_id is None:
            raise Exception("volume_id can not None")

