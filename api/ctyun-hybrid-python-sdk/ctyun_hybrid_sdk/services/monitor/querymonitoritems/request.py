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


class QueryMonitorItemsRequest(CTYunRequest):
    """
    查询监控项列表
    """

    def __init__(self, request_param):
        super(QueryMonitorItemsRequest, self).__init__("/v4/monitor/query-monitor-items", "GET", "monitor", "")
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
        if self.parameters.device_type is not None:
            query_param["deviceType"] = self.parameters.device_type
        if self.parameters.region_id is not None:
            query_param["regionID"] = self.parameters.region_id
        if self.parameters.uuid is not None:
            query_param["UUID"] = self.parameters.uuid
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class QueryMonitorItemsRequestParam(object):

    def __init__(self, region_id, device_type=None, uuid=None):
        """
        :param device_type: 本参数表示设备类型。默认值为所有类型。取值范围：<br>vm：云主机。<br>bare_metal：裸金属。<br>disk：云磁盘。<br>scaling：弹性伸缩。<br>traffic：共享带宽。<br>eip：弹性IP。<br>elb：负载均衡。<br>listener：监听器。<br>cstor_sfs：弹性文件。<br>ph：宿主机。<br>根据以上范围取值。
        :param region_id: 资源池id
        :param uuid: 资源uuid，当设备类型为云主机或裸金属时生效。
        """
        self.device_type = device_type
        self.region_id = region_id
        self.uuid = uuid

    def set_device_type(self, device_type):
        """
        :param device_type: 本参数表示设备类型。默认值为所有类型。取值范围：<br>vm：云主机。<br>bare_metal：裸金属。<br>disk：云磁盘。<br>scaling：弹性伸缩。<br>traffic：共享带宽。<br>eip：弹性IP。<br>elb：负载均衡。<br>listener：监听器。<br>cstor_sfs：弹性文件。<br>ph：宿主机。<br>根据以上范围取值。
        """
        self.device_type = device_type

    def set_uuid(self, uuid):
        """
        :param uuid: 资源uuid，当设备类型为云主机或裸金属时生效。
        """
        self.uuid = uuid

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")

