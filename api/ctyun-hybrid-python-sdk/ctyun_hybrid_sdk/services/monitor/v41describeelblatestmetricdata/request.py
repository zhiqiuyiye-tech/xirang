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


class V41describeELBLatestMetricDataRequest(CTYunRequest):
    """
    具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|lb_lbin|kb/s|   
    |网络流出速率|lb_lbout|kb/s|   
    |网络流入包速率|lb_inpkts|pps|   
    |网络流出包速率|lb_outpkts|pps|   
    |活跃连接数|lb_actconn|个|   
    |新建连接数|lb_newcreate|个|   
    |并发连接数|lb_scur|个|   
    |7层查询速率|lb_req_rate|请求/秒|   
    |7层协议返回码（2XX）|lb_hrsp_2xx|个/秒|   
    |7层协议返回码（3XX）|lb_hrsp_3xx|个/秒|   
    |7层协议返回码（4XX）|lb_hrsp_4xx|个/秒|   
    |7层协议返回码（5XX）|lb_hrsp_5xx|个/秒|   
    |7层协议返回码（Others）|lb_hrsp_other|个/秒|
    """

    def __init__(self, request_param):
        super(V41describeELBLatestMetricDataRequest, self).__init__("/v4.1/monitor/query-elb-latestmetricdata", "POST", "monitor", "application/json")
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
        if self.parameters.device_uuid_list is not None:
            body_param["deviceUUIDList"] = self.parameters.device_uuid_list
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


class V41describeELBLatestMetricDataRequestParam(object):

    def __init__(self, region_id, device_uuid_list, ):
        """
        :param region_id: 资源池ID
        :param device_uuid_list: 查询设备ID列表(建议:设备数不大于20，可以重复) 注意:此参数为数组
        """
        self.region_id = region_id
        self.device_uuid_list = device_uuid_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.device_uuid_list is None:
            raise Exception("device_uuid_list can not None")

