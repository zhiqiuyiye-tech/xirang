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


class SfsModifySnapshotSfsRequest(CTYunRequest):
    """
    弹性文件修改快照   
    
    """

    def __init__(self, request_param):
        super(SfsModifySnapshotSfsRequest, self).__init__("/v4/sfs/snapshot/modify", "POST", "sfs", "application/json")
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
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
        if self.parameters.uid is not None:
            body_param["UID"] = self.parameters.uid
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
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


class SfsModifySnapshotSfsRequestParam(object):

    def __init__(self, region_id, snapshot_id, uid, name, description=None):
        """
        :param region_id: 资源池ID
        :param snapshot_id: 快照ID
        :param uid: 文件系统ID
        :param description: 最大128字符
        :param name: 2-63字符，必须以字母开头，支持含字母、数字、下划线
        """
        self.region_id = region_id
        self.snapshot_id = snapshot_id
        self.uid = uid
        self.description = description
        self.name = name

    def set_description(self, description):
        """
        :param description: 最大128字符
        """
        self.description = description

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")
        if self.uid is None:
            raise Exception("uid can not None")
        if self.name is None:
            raise Exception("name can not None")

