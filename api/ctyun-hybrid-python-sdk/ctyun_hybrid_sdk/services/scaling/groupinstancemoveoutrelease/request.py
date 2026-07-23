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


class GroupInstanceMoveOutReleaseRequest(CTYunRequest):
    """
    移出一台实例并释放
    """

    def __init__(self, request_param):
        super(GroupInstanceMoveOutReleaseRequest, self).__init__("/v4/scaling/group/instance-move-out-release", "POST", "scaling", "application/json")
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
        if self.parameters.group_id is not None:
            body_param["groupID"] = self.parameters.group_id
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_id_list is not None:
            body_param["instanceIDList"] = self.parameters.instance_id_list
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


class GroupInstanceMoveOutReleaseRequestParam(object):

    def __init__(self, group_id, region_id, instance_id_list, ):
        """
        :param group_id: 伸缩组ID
        :param region_id: 资源池ID
        :param instance_id_list: 云主机id列表 注意:此参数为数组
        """
        self.group_id = group_id
        self.region_id = region_id
        self.instance_id_list = instance_id_list

    def check_param(self):
        """
        the param required check
        """
        if self.group_id is None:
            raise Exception("group_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id_list is None:
            raise Exception("instance_id_list can not None")

