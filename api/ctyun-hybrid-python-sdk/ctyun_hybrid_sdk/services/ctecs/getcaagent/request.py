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


class GetCaAgentRequest(CTYunRequest):
    """
    调用此接口可以查询一台或多台弹性云主机、物理机内是否安装了云助手agent   
    说明：仅支持批量查询弹性云主机或物理机是否安装了云助手agent，不支持混合查询
    """

    def __init__(self, request_param):
        super(GetCaAgentRequest, self).__init__("/v4/cloud-assistant/get-ca-agent", "POST", "ctecs", "application/json")
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
        if self.parameters.instance_ids is not None:
            body_param["instanceIDs"] = self.parameters.instance_ids
        if self.parameters.page_no is not None:
            body_param["pageNo"] = self.parameters.page_no
        if self.parameters.page_size is not None:
            body_param["pageSize"] = self.parameters.page_size
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


class GetCaAgentRequestParam(object):

    def __init__(self, region_id, instance_ids, page_no=None, page_size=None):
        """
        :param region_id: 资源池ID
        :param instance_ids: 待执行命令的云主机、物理机ID列表, 使用英文 , 分割
        :param page_no: 当前页码，不传默认值为1
        :param page_size: 分页查询时设置的每页行数，不传默认值为10，最大值为100，传超过100按100查询，小于0按10查询
        """
        self.region_id = region_id
        self.instance_ids = instance_ids
        self.page_no = page_no
        self.page_size = page_size

    def set_page_no(self, page_no):
        """
        :param page_no: 当前页码，不传默认值为1
        """
        self.page_no = page_no

    def set_page_size(self, page_size):
        """
        :param page_size: 分页查询时设置的每页行数，不传默认值为10，最大值为100，传超过100按100查询，小于0按10查询
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_ids is None:
            raise Exception("instance_ids can not None")

