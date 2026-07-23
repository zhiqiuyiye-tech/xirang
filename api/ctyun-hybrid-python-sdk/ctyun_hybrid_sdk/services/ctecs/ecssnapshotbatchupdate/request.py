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


class EcsSnapshotBatchUpdateRequest(CTYunRequest):
    """
    批量更改云主机快照名称和描述
    """

    def __init__(self, request_param):
        super(EcsSnapshotBatchUpdateRequest, self).__init__("/v4/ecs/snapshot-batch-update", "POST", "ctecs", "application/json")
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
        if self.parameters.update_info is not None:
            update_info = []
            if isinstance(self.parameters.update_info, list):
                for item in self.parameters.update_info:
                    if type(item) is dict:
                        update_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        update_info.append(item_dict_value)
            else:
                update_info.append(self.parameters.update_info.get_dic())
            body_param["updateInfo"] = update_info
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


class UpdateInfo(object):

    def __init__(self, name, snapshot_id, description=None):
        """
        :param name: 云主机快照名称，不允许与已有的重复（长度为2～63字符，不支持中文）
        :param snapshot_id: 云主机快照ID
        :param description: 云主机快照描述，长度不超过256
        """
        self.name = name
        self.snapshot_id = snapshot_id
        self.description = description
        self.check_param()

    def set_description(self, description):
        """
        :param description: 云主机快照描述，长度不超过256
        """
        self.description = description

    def get_dic(self):
        obj_dict = dict()
        if self.name is not None:
            obj_dict["name"] = self.name
        if self.snapshot_id is not None:
            obj_dict["snapshotID"] = self.snapshot_id
        if self.description is not None:
            obj_dict["description"] = self.description
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")


class EcsSnapshotBatchUpdateRequestParam(object):

    def __init__(self, region_id, update_info, ):
        """
        :param region_id: 资源池ID
        :param update_info: 云主机备份更新信息 注意:此参数为数组
        """
        self.region_id = region_id
        self.update_info = update_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.update_info is None:
            raise Exception("update_info can not None")

