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


class RemoveVmRequest(CTYunRequest):
    """
    该接口为适配3.0资源池接口，可兼容4.0资源池   
    如果是批量删除多个，其中一个出错时会返回错误，可能出现部分删除成功，部分失败的场景
    """

    def __init__(self, request_param):
        super(RemoveVmRequest, self).__init__("/v4/elb/remove-vm", "POST", "ctelb", "application/json")
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
        if self.parameters.target_group_id is not None:
            body_param["targetGroupID"] = self.parameters.target_group_id
        if self.parameters.target_ids is not None:
            body_param["targetIDs"] = self.parameters.target_ids
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


class RemoveVmRequestParam(object):

    def __init__(self, region_id, target_group_id, target_ids, ):
        """
        :param region_id: 资源池id
        :param target_group_id: 服务组id
        :param target_ids: 后端服务id列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.target_group_id = target_group_id
        self.target_ids = target_ids

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.target_group_id is None:
            raise Exception("target_group_id can not None")
        if self.target_ids is None:
            raise Exception("target_ids can not None")

