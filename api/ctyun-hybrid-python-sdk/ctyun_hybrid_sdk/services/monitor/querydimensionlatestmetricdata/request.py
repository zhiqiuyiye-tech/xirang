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


class QueryDimensionLatestMetricDataRequest(CTYunRequest):
    """
    宿主机disk_free指标为二次计算指标，可通过查询disk_total,disk_used指标相减进行获取
    """

    def __init__(self, request_param):
        super(QueryDimensionLatestMetricDataRequest, self).__init__("/v4.2/monitor/query-latest-metric-data", "POST", "monitor", "application/json")
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
         1.vm-云主机uuid 2.pushgateway_hpfs-并行文件uuid 3.disk-云硬盘uuid前20位 4.bare_metal-裸金属id 5.elb-负载均衡uuid(例:lb-f8lo6ya6mt) 6.eip-ip地址(例:100.127.176.100) 7.traffic-共享带宽id(例:bandwidth-zzvlrnorne) 8.listener-监听器uuid(例:listener-005oxpybzk) 9.scaling-弹性伸缩组uuid 10.cstor_sfs-弹性文件uuid(例:01v1aj2as5bg34uq)  11.ph-宿主机name
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


class QueryDimensionLatestMetricDataRequestParam(object):

    def __init__(self, region_id, service, dimension, item_name_list, dimensions, ):
        """
        :param region_id: 资源池ID
        :param service: vm-云主机；   
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
         nat-公网NAT网关；（2.2.1版本支持）   
         private_nat-私网NAT网关；（暂不支持）   
         zos_user-对象存储-用户维度；（暂不支持）   
         zos_bucket-对象存储-bucket维度；（2.2.3版本支持）   
         vnet_vpc_peer_stats-对等连接；（2.2.4版本支持）   
         vnet_monitor_endpoint_statistic-终端节点（2.2.4版本支持）   
         vnet_endpoint_service_statistic-终端节点服务（2.2.4版本支持）
        :param dimension: 云监控维度
        :param item_name_list: 具体设备对应监控项参见[监控项列表：查询/v4/monitor/query-monitor-items] 注意:此参数为数组
        :param dimensions: 用于定位目标设备，多标签查询取交集 注意:此参数为数组
        """
        self.region_id = region_id
        self.service = service
        self.dimension = dimension
        self.item_name_list = item_name_list
        self.dimensions = dimensions

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
        if self.dimensions is None:
            raise Exception("dimensions can not None")

