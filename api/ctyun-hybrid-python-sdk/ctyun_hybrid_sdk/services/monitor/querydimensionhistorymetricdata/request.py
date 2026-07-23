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


class QueryDimensionHistoryMetricDataRequest(CTYunRequest):
    """
    宿主机disk_free指标为二次计算指标，可通过查询disk_total,disk_used指标相减进行获取
    """

    def __init__(self, request_param):
        super(QueryDimensionHistoryMetricDataRequest, self).__init__("/v4.2/monitor/query-history-metric-data", "POST", "monitor", "application/json")
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
        if self.parameters.service is not None:
            body_param["service"] = self.parameters.service
        if self.parameters.dimension is not None:
            body_param["dimension"] = self.parameters.dimension
        if self.parameters.item_name_list is not None:
            body_param["itemNameList"] = self.parameters.item_name_list
        if self.parameters.start_time is not None:
            body_param["startTime"] = self.parameters.start_time
        if self.parameters.end_time is not None:
            body_param["endTime"] = self.parameters.end_time
        if self.parameters.fun is not None:
            body_param["fun"] = self.parameters.fun
        if self.parameters.period is not None:
            body_param["period"] = self.parameters.period
        if self.parameters.dimensions is not None:
            dimensions = []
            if isinstance(self.parameters.dimensions, list):
                for item in self.parameters.dimensions:
                    if type(item) is dict:
                        dimensions.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        dimensions.append(item_dict_value)
            else:
                dimensions.append(self.parameters.dimensions.get_dic())
            body_param["dimensions"] = dimensions
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


class Dimension(object):

    def __init__(self, name, value, ):
        """
        :param name: 支持uuid（除了孤岛环境查宿主机需要传host）
        :param value: 设备标签键所对应的值   
         1.vm-云主机uuid 2.pushgateway_hpfs-并行文件uuid 3.disk-云硬盘uuid前20位 4.bare_metal-裸金属id 5.elb-负载均衡uuid(例:lb-f8lo6ya6mt) 6.eip-ip地址(例:100.127.176.100) 7.traffic-共享带宽id(例:bandwidth-zzvlrnorne) 8.listener-监听器uuid(例:listener-005oxpybzk) 9.scaling-弹性伸缩组uuid 10.cstor_sfs-弹性文件uuid(例:01v1aj2as5bg34uq) 
        """
        self.name = name
        self.value = value
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.name is not None:
            obj_dict["name"] = self.name
        if self.value is not None:
            obj_dict["value"] = self.value
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.name is None:
            raise Exception("name can not None")
        if self.value is None:
            raise Exception("value can not None")


class QueryDimensionHistoryMetricDataRequestParam(object):

    def __init__(self, region_id, service, dimension, item_name_list, start_time, end_time, fun, dimensions, period=None):
        """
        :param region_id: 资源池ID
        :param service: 云监控服务   
         vm-云主机；   
         disk-云硬盘；   
         bare_metal-裸金属；   
         elb-负载均衡 ；   
         eip-弹性ip；   
         traffic-共享带宽；   
         listener-监听器；   
         scaling-弹性伸缩组；   
         cstor_sfs-弹性文件；   
         pushgateway_hpfs-并行文件;（2.2.0版本支持）   
         oceanfs-海量文件；（2.2.1版本支持）   
         nat-公网NAT网关；（暂不支持）   
         private_nat-私网NAT网关；（暂不支持）   
         vnet_vpc_peer_stats-对等连接；（2.2.4版本支持）   
         vnet_monitor_endpoint_statistic-终端节点（2.2.4版本支持）   
         vnet_endpoint_service_statistic-终端节点服务（2.2.4版本支持）
        :param dimension: 云监控维度
        :param item_name_list: 具体设备对应监控项参见[监控项列表：查询/v4/monitor/query-monitor-items] 注意:此参数为数组
        :param start_time: 查询起始Unix时间戳，秒级
        :param end_time: 查询结束Unix时间戳，秒级
        :param fun: 常用值为avg。取值范围:raw：原始值。avg：平均值。min：最小值。max：最大值。variance：方差。sum：求和。根据以上范围取
        :param period: 单位：秒，默认300，需不小于60，推荐使用60的整倍数。当fun为raw时本参数无效。 
        :param dimensions: 用于定位目标设备，多标签查询取交集 注意:此参数为数组
        """
        self.region_id = region_id
        self.service = service
        self.dimension = dimension
        self.item_name_list = item_name_list
        self.start_time = start_time
        self.end_time = end_time
        self.fun = fun
        self.period = period
        self.dimensions = dimensions

    def set_period(self, period):
        """
        :param period: 单位：秒，默认300，需不小于60，推荐使用60的整倍数。当fun为raw时本参数无效。 
        """
        self.period = period

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.service is None:
            raise Exception("service can not None")
        if self.dimension is None:
            raise Exception("dimension can not None")
        if self.item_name_list is None:
            raise Exception("item_name_list can not None")
        if self.start_time is None:
            raise Exception("start_time can not None")
        if self.end_time is None:
            raise Exception("end_time can not None")
        if self.fun is None:
            raise Exception("fun can not None")
        if self.dimensions is None:
            raise Exception("dimensions can not None")

