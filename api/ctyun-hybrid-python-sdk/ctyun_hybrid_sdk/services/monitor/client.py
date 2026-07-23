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

from ctyun_hybrid_sdk.core.ctyunclient import CTYunClient
from ctyun_hybrid_sdk.core.config import Config
from ctyun_hybrid_sdk.core.logger import get_default_logger


class MonitorClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('monitor-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(MonitorClient, self).__init__(credential, config, 'monitor', '0.1.0', logger, signer)

    def query_vm_disk_top_hybrid(self, query_vm_disk_top_hybrid_request_param):
        """
        /v4/monitor/query-disk-top
        调用此接口可查询用户在指定资源池云主机监控中磁盘使用率Top-N。
        """
        return self.send(query_vm_disk_top_hybrid_request_param)

    def update_shield_rule_status_hybrid(self, update_shield_rule_status_hybrid_request_param):
        """
        /v4/monitor/update-shield-rule-status
        修改告警屏蔽规则状态
        """
        return self.send(update_shield_rule_status_hybrid_request_param)

    def query_metric_data_avg_hybrid(self, query_metric_data_avg_hybrid_request_param):
        """
        /v4/monitor/query-metricdata-avg
        查询某个设备的历史数据，以period为周期，返回每个周期内的平均值
        """
        return self.send(query_metric_data_avg_hybrid_request_param)

    def update_resource_group(self, update_resource_group_request_param):
        """
        /v4.1/monitor/update-resource-group
        调用此接口可更新资源分组，支持全量字段修改。   
       
    接口约束   
    1. 资源分组名称不可重复。2. 资源分组创建类型不能修改。3. 其他参见请求参数说明。
        """
        return self.send(update_resource_group_request_param)

    def update_group_contacts_hybrid(self, update_group_contacts_hybrid_request_param):
        """
        /v4/monitor/update-group-contacts
        调用此接口可变更告警联系组内的告警联系人列表。
        """
        return self.send(update_group_contacts_hybrid_request_param)

    def delete_resource_groups(self, delete_resource_groups_request_param):
        """
        /v4.1/monitor/delete-resource-groups
        调用此接口可删除指定资源分组。
        """
        return self.send(delete_resource_groups_request_param)

    def get_platform_statistics_hybrid(self, get_platform_statistics_hybrid_request_param):
        """
        /v4/monitor/get-platform-statistics
        查询平台监控聚合监控
        """
        return self.send(get_platform_statistics_hybrid_request_param)

    def create_contact_hybrid(self, create_contact_hybrid_request_param):
        """
        /v4/monitor/create-contact
        调用此接口可创建告警联系人，用于告警通知。
        """
        return self.send(create_contact_hybrid_request_param)

    def query_items_hybrid(self, query_items_hybrid_request_param):
        """
        /v4/monitor/query-items
        2.2.7.2提供   
    当前事件告警只支持弹性云主机vm
        """
        return self.send(query_items_hybrid_request_param)

    def cloud_monitor_get_alarm_event_hybrid(self, cloud_monitor_get_alarm_event_hybrid_request_param):
        """
        /v4/alarm/cloudMonitor/get-alarm-event
        （2.2.6版本支持）
        """
        return self.send(cloud_monitor_get_alarm_event_hybrid_request_param)

    def query_alarm_rules_v41(self, query_alarm_rules_v41_request_param):
        """
        /v4.1/monitor/query-alarm-rules
        根据筛选项查询告警规则列表。   
    2.2.5版本支持
        """
        return self.send(query_alarm_rules_v41_request_param)

    def delete_contacts_hybrid(self, delete_contacts_hybrid_request_param):
        """
        /v4/monitor/delete-contacts
        告警联系人：批量删除
        """
        return self.send(delete_contacts_hybrid_request_param)

    def update_alarm_rule_info_hybrid(self, update_alarm_rule_info_hybrid_request_param):
        """
        /v4/monitor/update-alarm-rule-info
        调用此接口可修改指定告警规则基本信息，支持全量字段修改。
        """
        return self.send(update_alarm_rule_info_hybrid_request_param)

    def query_metric_data_variance_hybrid(self, query_metric_data_variance_hybrid_request_param):
        """
        /v4/monitor/query-metricdata-variance
        查询某个设备的历史数据，以period为周期，返回每个周期内的方差
        """
        return self.send(query_metric_data_variance_hybrid_request_param)

    def update_alarm_rule_conditions_hybrid(self, update_alarm_rule_conditions_hybrid_request_param):
        """
        /v4/monitor/update-alarm-rule-conditions
        告警规则：修改告警规则条件
        """
        return self.send(update_alarm_rule_conditions_hybrid_request_param)

    def v41describe_baremetal_history_metric_data(self, v41describe_baremetal_history_metric_data_request_param):
        """
        /v4.1/monitor/query-baremetal-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |内存使用率|mem_util|%|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|
        """
        return self.send(v41describe_baremetal_history_metric_data_request_param)

    def v41describe_disk_history_metric_data(self, v41describe_disk_history_metric_data_request_param):
        """
        /v4.1/monitor/query-disk-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|
        """
        return self.send(v41describe_disk_history_metric_data_request_param)

    def describe_contact_hybrid(self, describe_contact_hybrid_request_param):
        """
        /v4/monitor/describe-contact
        告警联系人：查看详情
        """
        return self.send(describe_contact_hybrid_request_param)

    def describe_alarm_rules_hybrid(self, describe_alarm_rules_hybrid_request_param):
        """
        /v4/monitor/describe-alarm-rule
        查看告警规则的详情信息。   
    因与公有云底层逻辑区别，返回格式与公有云不同。
        """
        return self.send(describe_alarm_rules_hybrid_request_param)

    def query_dimension_latest_metric_data(self, query_dimension_latest_metric_data_request_param):
        """
        /v4.2/monitor/query-latest-metric-data
        宿主机disk_free指标为二次计算指标，可通过查询disk_total,disk_used指标相减进行获取
        """
        return self.send(query_dimension_latest_metric_data_request_param)

    def disable_alarm_rules_hybrid(self, disable_alarm_rules_hybrid_request_param):
        """
        /v4/monitor/disable-alarm-rules
        调用此接口可批量禁用多个告警规则
        """
        return self.send(disable_alarm_rules_hybrid_request_param)

    def v41describe_vm_latest_metric_data(self, v41describe_vm_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-vm-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |CPU空闲时间占比|cpu_idle_time|%|   
    |CPU中断时间占比|cpu_interrupt_time|%|   
    |内核空间CPU使用率|cpu_system_time|%|   
    |用户空间CPU使用率|cpu_user_time|%|   
    |15分钟平均负载|processor_load_15_min_average_per_core|%|   
    |1分钟平均负载|processor_load_1_min_average_per_core|%|   
    |5分钟平均负载|processor_load_5_min_average_per_core|%|   
    |内存使用率|mem_util|%|   
    |已用内存量|used_memory|GB|   
    |可用内存|free_memory|GB|   
    |睡眠进程数|sleep_num|个|   
    |僵死进程数|zomb_num|个|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读操作速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写操作速率|disk_write_requests_rate|请求/秒|   
    |挂载点剩余量|free_disk_space_on|GB|   
    |挂载点使用率|pused_disk_space_on|%|   
    |挂载点总量|total_disk_space_on|GB|   
    |挂载点使用量|used_disk_space_on|GB|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|
        """
        return self.send(v41describe_vm_latest_metric_data_request_param)

    def v41describe_listener_latest_metric_data(self, v41describe_listener_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-listener-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ls_lbin|bit/s|   
    |网络流出速率|ls_lbout|bit/s|   
    |流入包个数|ls_inpkts|count/s|   
    |流出包个数|ls_outpkts|count/s|   
    |活跃连接数|ls_actconn|count|   
    |新建连接数|ls_newcreate|count/s|   
    |并发连接数|ls_scur|count|   
    |7层查询速率|ls_req_rate|count/s|   
    |7层协议返回码2XX个数|ls_hrsp_2xx|count/s|   
    |7层协议返回码3XX个数|ls_hrsp_3xx|count/s|   
    |7层协议返回码4XX个数|ls_hrsp_4xx|count/s|   
    |7层协议返回码5XX个数|ls_hrsp_5xx|count/s|   
    |7层协议返回码Others个数|ls_hrsp_other|count/s|
        """
        return self.send(v41describe_listener_latest_metric_data_request_param)

    def update_contact_groups_hybrid(self, update_contact_groups_hybrid_request_param):
        """
        /v4.1/monitor/update-contact-groups
        告警联系人：变更所属告警联系人组列表
        """
        return self.send(update_contact_groups_hybrid_request_param)

    def query_alarm_trend_hybrid(self, query_alarm_trend_hybrid_request_param):
        """
        /v4.1/monitor/query-alarm-trend
        调用此接口可根据时间范围查询指定资源池告警次数的变化趋势。
        """
        return self.send(query_alarm_trend_hybrid_request_param)

    def query_total_ebm_trend_hybrid(self, query_total_ebm_trend_hybrid_request_param):
        """
        /v4/monitor/query-baremetal-trend
        资源池下所有裸金属统计出总的时序指标性能数据。
        """
        return self.send(query_total_ebm_trend_hybrid_request_param)

    def v41describe_e_l_b_latest_metric_data(self, v41describe_e_l_b_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-elb-latestmetricdata
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
        return self.send(v41describe_e_l_b_latest_metric_data_request_param)

    def delete_shield_rule_hybrid(self, delete_shield_rule_hybrid_request_param):
        """
        /v4/monitor/delete-shield-rule
        删除告警屏蔽规则
        """
        return self.send(delete_shield_rule_hybrid_request_param)

    def delete_alarm_rules_v41(self, delete_alarm_rules_v41_request_param):
        """
        /v4.1/monitor/delete-alarm-rules
        调用此接口可批量删除多个创建告警规则
        """
        return self.send(delete_alarm_rules_v41_request_param)

    def push_alert_issue_hybrid(self, push_alert_issue_hybrid_request_param):
        """
        /v4/monitor/push-alert-issue
        用户可以自行推送的告警事件，非系统自动产生，可以在告警历史中查询到。
        """
        return self.send(push_alert_issue_hybrid_request_param)

    def query_monitor_resource_total_hybrid(self, query_monitor_resource_total_hybrid_request_param):
        """
        /v4/monitor/query-item-total
        调用此接口可查询指定资源池下所有资源总数量。
        """
        return self.send(query_monitor_resource_total_hybrid_request_param)

    def create_contact_group_hybrid(self, create_contact_group_hybrid_request_param):
        """
        /v4/monitor/create-contact-group
        调用此接口可创建告警联系组。
        """
        return self.send(create_contact_group_hybrid_request_param)

    def query_ebm_disk_top_hybrid(self, query_ebm_disk_top_hybrid_request_param):
        """
        /v4/monitor/query-baremetal-disk-top
        调用此接口可查询用户在指定资源池裸金属监控中磁盘使用率Top-N。
        """
        return self.send(query_ebm_disk_top_hybrid_request_param)

    def query_metric_data_hybrid(self, query_metric_data_hybrid_request_param):
        """
        /v4/ops/monitor/query-metricdata
        查询最新宿主机时序指标性能数据   
    监控项itemNameList支持：cpu_til（cpu利用率）、disk_util（系统盘利用率）、mem_util（内存利用率）   
    注：mem_util会返回mem_util（包含大页得）、real_mem_util（和页面一致的）   
    
        """
        return self.send(query_metric_data_hybrid_request_param)

    def v41describe_s_f_s_latest_metric_data(self, v41describe_s_f_s_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-sfs-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |单个文件系统写IOPS|fs_write_iops|次|   
    |单个文件系统写带宽|fs_write_bw|KB/s|   
    |单个文件系统读IOPS|fs_read_iops|次|   
    |单个文件系统读带宽|fs_read_bw|KB/s|   
    |单个文件系统开通总容量|fs_capacity_total|GB|   
    |单个文件系统已使用容量|fs_capacity_used|GB|
        """
        return self.send(v41describe_s_f_s_latest_metric_data_request_param)

    def update_shield_rule_hybrid(self, update_shield_rule_hybrid_request_param):
        """
        /v4/monitor/update-shield-rule
        修改告警屏蔽规则
        """
        return self.send(update_shield_rule_hybrid_request_param)

    def query_monitor_items(self, query_monitor_items_request_param):
        """
        /v4/monitor/query-monitor-items
        查询监控项列表
        """
        return self.send(query_monitor_items_request_param)

    def v41describe_vm_history_metric_data(self, v41describe_vm_history_metric_data_request_param):
        """
        /v4.1/monitor/query-vm-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |CPU空闲时间占比|cpu_idle_time|%|   
    |CPU中断时间占比|cpu_interrupt_time|%|   
    |内核空间CPU使用率|cpu_system_time|%|   
    |用户空间CPU使用率|cpu_user_time|%|   
    |15分钟平均负载|processor_load_15_min_average_per_core|%|   
    |1分钟平均负载|processor_load_1_min_average_per_core|%|   
    |5分钟平均负载|processor_load_5_min_average_per_core|%|   
    |内存使用率|mem_util|%|   
    |已用内存量|used_memory|GB|   
    |可用内存|free_memory|GB|   
    |睡眠进程数|sleep_num|个|   
    |僵死进程数|zomb_num|个|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读操作速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写操作速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|
        """
        return self.send(v41describe_vm_history_metric_data_request_param)

    def get_platform_aggregation_hybrid(self, get_platform_aggregation_hybrid_request_param):
        """
        /v4/monitor/get-platform-aggregation
        查询平台监控聚合图表信息
        """
        return self.send(get_platform_aggregation_hybrid_request_param)

    def query_dimension_history_metric_data(self, query_dimension_history_metric_data_request_param):
        """
        /v4.2/monitor/query-history-metric-data
        宿主机disk_free指标为二次计算指标，可通过查询disk_total,disk_used指标相减进行获取
        """
        return self.send(query_dimension_history_metric_data_request_param)

    def query_contact_groups_hybrid(self, query_contact_groups_hybrid_request_param):
        """
        /v4.1/monitor/query-contact-groups
        调用此接口可查询告警联系人组的列表。
        """
        return self.send(query_contact_groups_hybrid_request_param)

    def export_alert_history_hybrid(self, export_alert_history_hybrid_request_param):
        """
        /v4/monitor/export-alert-history
        导出告警历史   
    返回字段：   
    监控对象、首次告警触发条件、告警ID、产品类型、告警级别、通知对象、所属用户、告警规则、发生时间、持续时间、状态、确认用户、清除用户（当前告警不返回此字段）
        """
        return self.send(export_alert_history_hybrid_request_param)

    def query_total_vm_trend_hybrid(self, query_total_vm_trend_hybrid_request_param):
        """
        /v4/monitor/query-vm-trend
        资源池下所有云主机统计出总的时序指标性能数据。
        """
        return self.send(query_total_vm_trend_hybrid_request_param)

    def v41describe_e_ip_history_metric_data(self, v41describe_e_ip_history_metric_data_request_param):
        """
        /v4.1/monitor/query-eip-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ingress_throughput|MB/min|   
    |网络流出速率|egress_throughput|MB/min|   
    |网络流入带宽|ingress_bandwidth|Mb/s|   
    |网络流出带宽|egress_bandwidth|Mb/s|
        """
        return self.send(v41describe_e_ip_history_metric_data_request_param)

    def get_pools_count(self, get_pools_count_request_param):
        """
        /v4/stats/pools-count
        多云资源池数目统计(vdc绑定的资源池)
        """
        return self.send(get_pools_count_request_param)

    def delete_contact_hybrid(self, delete_contact_hybrid_request_param):
        """
        /v4/monitor/delete-contact
        调用此接口可删除告警联系人。
        """
        return self.send(delete_contact_hybrid_request_param)

    def query_metric_data_max_hybrid(self, query_metric_data_max_hybrid_request_param):
        """
        /v4/monitor/query-metricdata-max
        查询某个设备的历史数据，以period为周期，返回每个周期内的最大值
        """
        return self.send(query_metric_data_max_hybrid_request_param)

    def query_alarm_top_event_hybrid(self, query_alarm_top_event_hybrid_request_param):
        """
        /v4/monitor/query-alarm-top-event
        调用此接口可查询指定资源池下告警Top事件。
        """
        return self.send(query_alarm_top_event_hybrid_request_param)

    def get_alarm_event_hybrid(self, get_alarm_event_hybrid_request_param):
        """
        /v4/alarm/get-alarm-event
        告警事件查询 开发未对齐原因：公有云无此接口，按照upms接口开发   
    （2.2.4版本支持）
        """
        return self.send(get_alarm_event_hybrid_request_param)

    def query_vm_host_disk_top_hybrid(self, query_vm_host_disk_top_hybrid_request_param):
        """
        /v4/monitor/query-ph-disk-top
        调用此接口可查询用户在指定资源池宿主机监控中磁盘使用率Top-N。
        """
        return self.send(query_vm_host_disk_top_hybrid_request_param)

    def create_alarm_rule_v41(self, create_alarm_rule_v41_request_param):
        """
        /v4.1/monitor/create-alarm-rule
        创建一个告警规则。
        """
        return self.send(create_alarm_rule_v41_request_param)

    def query_alert_top_overview_hybrid(self, query_alert_top_overview_hybrid_request_param):
        """
        /v4/monitor/query-alert-top-overview
        查询告警历史告警数TOP细分图表
        """
        return self.send(query_alert_top_overview_hybrid_request_param)

    def get_cluster_threshold_hybrid(self, get_cluster_threshold_hybrid_request_param):
        """
        /v4/monitor/get-cluster-threshold
        查询集群容量阈值
        """
        return self.send(get_cluster_threshold_hybrid_request_param)

    def query_alert_history_info_hybrid(self, query_alert_history_info_hybrid_request_param):
        """
        /v4/monitor/query-alert-history-info
        查询单条告警历史详情
        """
        return self.send(query_alert_history_info_hybrid_request_param)

    def set_alarm_rule_contact_hybrid(self, set_alarm_rule_contact_hybrid_request_param):
        """
        /v4/monitor/set-alarm-rule-contact
        调用此接口可设置指定告警规则的告警联系人及通知方式。
        """
        return self.send(set_alarm_rule_contact_hybrid_request_param)

    def query_ebm_cpu_top_hybrid(self, query_ebm_cpu_top_hybrid_request_param):
        """
        /v4/monitor/query-baremetal-cpu-top
        调用此接口可查询用户在指定资源池裸金属监控中cpu使用率Top-N。
        """
        return self.send(query_ebm_cpu_top_hybrid_request_param)

    def v41describe_s_f_s_history_metric_data(self, v41describe_s_f_s_history_metric_data_request_param):
        """
        /v4.1/monitor/query-sfs-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |单个文件系统写IOPS|fs_write_iops|次|   
    |单个文件系统写带宽|fs_write_bw|KB/s|   
    |单个文件系统读IOPS|fs_read_iops|次|   
    |单个文件系统读带宽|fs_read_bw|KB/s|   
    |单个文件系统开通总容量|fs_capacity_total|GB|   
    |单个文件系统已使用容量|fs_capacity_used|GB|
        """
        return self.send(v41describe_s_f_s_history_metric_data_request_param)

    def query_ebm_mem_top_hybrid(self, query_ebm_mem_top_hybrid_request_param):
        """
        /v4/monitor/query-baremetal-mem-top
        调用此接口可查询用户在指定资源池裸金属监控中内存使用率Top-N。
        """
        return self.send(query_ebm_mem_top_hybrid_request_param)

    def delete_contact_group_hybrid(self, delete_contact_group_hybrid_request_param):
        """
        /v4/monitor/delete-contact-group
        调用此接口可删除告警联系人组。
        """
        return self.send(delete_contact_group_hybrid_request_param)

    def get_cloud_platform_top(self, get_cloud_platform_top_request_param):
        """
        /v4/stats/cloudPlatform-top
        多云资源池实例数目Top(云主机和云硬盘)
        """
        return self.send(get_cloud_platform_top_request_param)

    def enable_alarm_rules_hybrid(self, enable_alarm_rules_hybrid_request_param):
        """
        /v4/monitor/enable-alarm-rules
        调用此接口可批量启用多个告警规则
        """
        return self.send(enable_alarm_rules_hybrid_request_param)

    def list_shield_rule_hybrid(self, list_shield_rule_hybrid_request_param):
        """
        /v4/monitor/list-shield-rule
        查询告警屏蔽规则列表
        """
        return self.send(list_shield_rule_hybrid_request_param)

    def query_metric_data_min_hybrid(self, query_metric_data_min_hybrid_request_param):
        """
        /v4/monitor/query-metricdata-min
        查询某个设备的历史数据，以period为周期，返回每个周期内的最小值
        """
        return self.send(query_metric_data_min_hybrid_request_param)

    def query_alarm_services_hybrid(self, query_alarm_services_hybrid_request_param):
        """
        /v4/monitor/query-alarm-services
        告警规则：获取告警服务列表
        """
        return self.send(query_alarm_services_hybrid_request_param)

    def change_custom_alarm_rules_status_hybrid(self, change_custom_alarm_rules_status_hybrid_request_param):
        """
        /v4/monitor/change-custom-alarm-rules-status
        批量更新告警规则状态为禁用或启用
        """
        return self.send(change_custom_alarm_rules_status_hybrid_request_param)

    def update_contacts_hybrid(self, update_contacts_hybrid_request_param):
        """
        /v4/monitor/update-contacts
        调用此接口可修改告警联系人配置，支持全量字段修改。
        """
        return self.send(update_contacts_hybrid_request_param)

    def set_alarm_rule_notify_time_hybrid(self, set_alarm_rule_notify_time_hybrid_request_param):
        """
        /v4/monitor/set-alarm-rule-notify-time
        调用此接口可设置指定告警规则的通知周期。
        """
        return self.send(set_alarm_rule_notify_time_hybrid_request_param)

    def query_id_c_metric_data_hybrid(self, query_id_c_metric_data_hybrid_request_param):
        """
        /v4/ops/monitor/query-idc-metricdata
        查询资源池使用率。监控项itemNameList支持：cpu_til（cpu利用率）、disk_util（系统盘利用率）、mem_util（内存利用率）   
    
        """
        return self.send(query_id_c_metric_data_hybrid_request_param)

    def query_vm_mem_top_hybrid(self, query_vm_mem_top_hybrid_request_param):
        """
        /v4/monitor/query-mem-top
        调用此接口可查询用户在指定资源池云主机监控中内存使用率Top-N。
        """
        return self.send(query_vm_mem_top_hybrid_request_param)

    def update_cluster_threshold_hybrid(self, update_cluster_threshold_hybrid_request_param):
        """
        /v4/monitor/update-cluster-threshold
        修改集群容量阈值
        """
        return self.send(update_cluster_threshold_hybrid_request_param)

    def query_alarm_top_resource_hybrid(self, query_alarm_top_resource_hybrid_request_param):
        """
        /v4/monitor/query-alarm-top-resource
        调用此接口可查询指定资源池下告警Top实例。
        """
        return self.send(query_alarm_top_resource_hybrid_request_param)

    def v41describe_traffic_history_metric_data(self, v41describe_traffic_history_metric_data_request_param):
        """
        /v4.1/monitor/query-traffic-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ingress_throughput|MB/min|   
    |网络流出速率|egress_throughput|MB/min|   
    |网络流入带宽|ingress_bandwidth|Mb/s|   
    |网络流出带宽|egress_bandwidth|Mb/s|
        """
        return self.send(v41describe_traffic_history_metric_data_request_param)

    def query_alarm_data_hybrid(self, query_alarm_data_hybrid_request_param):
        """
        /v4/ops/monitor/query-alarmdata
        查询宿主机告警数据   
    注：返回数据中的ip是宿主机名称、云主机名称-->原因：混合云创建告警规则使用name和id创建，查询告警数据需关联规则进行查询，因此ip返回的实际是名称   
    告警数据有权限控制，超管查询全部数据   
    
        """
        return self.send(query_alarm_data_hybrid_request_param)

    def v41describe_e_ip_latest_metric_data(self, v41describe_e_ip_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-eip-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ingress_throughput|MB/min|   
    |网络流出速率|egress_throughput|MB/min|   
    |网络流入带宽|ingress_bandwidth|Mb/s|   
    |网络流出带宽|egress_bandwidth|Mb/s|
        """
        return self.send(v41describe_e_ip_latest_metric_data_request_param)

    def delete_alarm_rules_hybrid(self, delete_alarm_rules_hybrid_request_param):
        """
        /v4/monitor/delete-alarm-rules
        调用此接口可批量删除多个创建告警规则
        """
        return self.send(delete_alarm_rules_hybrid_request_param)

    def v41describe_scaling_latest_metric_data(self, v41describe_scaling_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-scaling-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |内存使用率|mem_util|%|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|   
    |实例个数|instance_count|个|
        """
        return self.send(v41describe_scaling_latest_metric_data_request_param)

    def ph_info_idc_hybrid(self, ph_info_idc_hybrid_request_param):
        """
        /v4/ops/cmdb/ph-info-idc
        查询宿主机基本信息：资源池级别(该资源池下所有用户查询结果相同)   
    注：目前返回结果仅支持主结构中的ip、hostName、hostID字段；cpuInfo对象中的cpuLcoreCount、cpuModelName字段；memInfo对象中的memVirtualTotal字段；diskInfo对象中的diskSize；hostInfo对象中的hostID、hostName字段   
       
    返回参数cpuInfo.cpuLcoreCount，v1是包含了预留核数，而v2是扣除了预留核数（之前v1中化学项目客户质疑过云管前端展示和接口返回对不上，原因就是云管前端展示的不带预留，而v2接口因为扣除了预留，所以不存在该问题）
        """
        return self.send(ph_info_idc_hybrid_request_param)

    def query_alert_history_hybrid(self, query_alert_history_hybrid_request_param):
        """
        /v4/monitor/query-alert-history
        查询告警历史   
    建议使用：/v4/alarm/get-alarm-event
        """
        return self.send(query_alert_history_hybrid_request_param)

    def query_resource_groups(self, query_resource_groups_request_param):
        """
        /v4.1/monitor/query-resource-groups
        调用此接口可查询用户资源分组列表。
        """
        return self.send(query_resource_groups_request_param)

    def update_alarm_event_hybrid(self, update_alarm_event_hybrid_request_param):
        """
        /v4/monitor/update-alarm-event
        告警事件：确认/清除
        """
        return self.send(update_alarm_event_hybrid_request_param)

    def v41describe_e_l_b_history_metric_data(self, v41describe_e_l_b_history_metric_data_request_param):
        """
        /v4.1/monitor/query-elb-historymetricdata
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
        return self.send(v41describe_e_l_b_history_metric_data_request_param)

    def query_vm_host_cpu_top_hybrid(self, query_vm_host_cpu_top_hybrid_request_param):
        """
        /v4/monitor/query-ph-cpu-top
        调用此接口可查询用户在指定资源池宿主机监控中cpu使用率Top-N。
        """
        return self.send(query_vm_host_cpu_top_hybrid_request_param)

    def get_pool_threshold_hybrid(self, get_pool_threshold_hybrid_request_param):
        """
        /v4/monitor/get-pool-threshold
        查询资源池容量阈值
        """
        return self.send(get_pool_threshold_hybrid_request_param)

    def query_vm_host_mem_top_hybrid(self, query_vm_host_mem_top_hybrid_request_param):
        """
        /v4/monitor/query-ph-mem-top
        调用此接口可查询用户在指定资源池宿主机监控中内存使用率Top-N。
        """
        return self.send(query_vm_host_mem_top_hybrid_request_param)

    def v41describe_listener_history_metric_data(self, v41describe_listener_history_metric_data_request_param):
        """
        /v4.1/monitor/query-listener-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ls_lbin|bit/s|   
    |网络流出速率|ls_lbout|bit/s|   
    |流入包个数|ls_inpkts|count/s|   
    |流出包个数|ls_outpkts|count/s|   
    |活跃连接数|ls_actconn|count|   
    |新建连接数|ls_newcreate|count/s|   
    |并发连接数|ls_scur|count|   
    |7层查询速率|ls_req_rate|count/s|   
    |7层协议返回码2XX个数|ls_hrsp_2xx|count/s|   
    |7层协议返回码3XX个数|ls_hrsp_3xx|count/s|   
    |7层协议返回码4XX个数|ls_hrsp_4xx|count/s|   
    |7层协议返回码5XX个数|ls_hrsp_5xx|count/s|   
    |7层协议返回码Others个数|ls_hrsp_other|count/s|
        """
        return self.send(v41describe_listener_history_metric_data_request_param)

    def delete_alarm_rule_hybrid(self, delete_alarm_rule_hybrid_request_param):
        """
        /v4/monitor/delete-alarm-rule
        调用此接口可删除创建告警规则
        """
        return self.send(delete_alarm_rule_hybrid_request_param)

    def update_contact_group_hybrid(self, update_contact_group_hybrid_request_param):
        """
        /v4/monitor/update-contact-group
        调用此接口可修改告警联系组基本信息， 支持全量字段修改。
        """
        return self.send(update_contact_group_hybrid_request_param)

    def set_alarm_rule_notify_strategy_hybrid(self, set_alarm_rule_notify_strategy_hybrid_request_param):
        """
        /v4/monitor/set-alarm-rule-notify-strategy
        调用此接口可设置指定告警规则的通知策略（重复通知，静默时间，告警恢复是否通知）。
        """
        return self.send(set_alarm_rule_notify_strategy_hybrid_request_param)

    def create_shield_rule_hybrid(self, create_shield_rule_hybrid_request_param):
        """
        /v4/monitor/create-shield-rule
        创建告警屏蔽规则
        """
        return self.send(create_shield_rule_hybrid_request_param)

    def query_total_host_trend_hybrid(self, query_total_host_trend_hybrid_request_param):
        """
        /v4/monitor/query-ph-trend
        资源池下所有宿主机统计出总的时序指标性能数据。
        """
        return self.send(query_total_host_trend_hybrid_request_param)

    def v41describe_disk_latest_metric_data(self, v41describe_disk_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-disk-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|
        """
        return self.send(v41describe_disk_latest_metric_data_request_param)

    def v41describe_scaling_history_metric_data(self, v41describe_scaling_history_metric_data_request_param):
        """
        /v4.1/monitor/query-scaling-historymetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |内存使用率|mem_util|%|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|   
    |实例个数|instance_count|个|
        """
        return self.send(v41describe_scaling_history_metric_data_request_param)

    def query_alarm_top_dimension_hybrid(self, query_alarm_top_dimension_hybrid_request_param):
        """
        /v4/monitor/query-alarm-top-dimension
        调用此接口可查询指定资源池下告警Top产品。
        """
        return self.send(query_alarm_top_dimension_hybrid_request_param)

    def update_alarm_rule_info_v41(self, update_alarm_rule_info_v41_request_param):
        """
        /v4.1/monitor/update-alarm-rule
        调用此接口可修改指定告警规则基本信息，支持全量字段修改。
        """
        return self.send(update_alarm_rule_info_v41_request_param)

    def query_alarm_rules_hybrid(self, query_alarm_rules_hybrid_request_param):
        """
        /v4/monitor/query-alarm-rules
        根据筛选项查询告警规则列表。   
    因与公有云底层逻辑区别，返回格式与公有云不同。
        """
        return self.send(query_alarm_rules_hybrid_request_param)

    def query_alarm_top_metric_hybrid(self, query_alarm_top_metric_hybrid_request_param):
        """
        /v4/monitor/query-alarm-top-metric
        调用此接口可查询指定资源池下告警Top指标。
        """
        return self.send(query_alarm_top_metric_hybrid_request_param)

    def v41describe_traffic_latest_metric_data(self, v41describe_traffic_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-traffic-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |网络流入速率|ingress_throughput|MB/min|   
    |网络流出速率|egress_throughput|MB/min|   
    |网络流入带宽|ingress_bandwidth|Mb/s|   
    |网络流出带宽|egress_bandwidth|Mb/s|
        """
        return self.send(v41describe_traffic_latest_metric_data_request_param)

    def create_resource_group(self, create_resource_group_request_param):
        """
        /v4.1/monitor/create-resource-group
        1. 资源分组名称不可重复。2. 可创建的资源分组数量不能超出配额数量。3. 其他参见请求参数说明。
        """
        return self.send(create_resource_group_request_param)

    def create_alarm_rule_hybrid(self, create_alarm_rule_hybrid_request_param):
        """
        /v4/monitor/create-alarm-rule
        创建一个告警规则。
        """
        return self.send(create_alarm_rule_hybrid_request_param)

    def describe_contact_group_hybrid(self, describe_contact_group_hybrid_request_param):
        """
        /v4/monitor/describe-contact-group
        调用此接口可查询告警联系人组的配置详情。
        """
        return self.send(describe_contact_group_hybrid_request_param)

    def query_alarm_total_hybrid(self, query_alarm_total_hybrid_request_param):
        """
        /v4.1/monitor/query-alarm-total
        调用此接口可查询指定资源池告警数量统计。
        """
        return self.send(query_alarm_total_hybrid_request_param)

    def v41describe_bare_metal_latest_metric_data(self, v41describe_bare_metal_latest_metric_data_request_param):
        """
        /v4.1/monitor/query-baremetal-latestmetricdata
        具体资源池具体指标通过[监控项列表：查询]-->/v4/monitor/query-monitor-items查询所得。常用监控指标如下：   
    |指标描述|指标名|指标单位|   
    |---|---|---|   
    |CPU使用率|cpu_util|%|   
    |内存使用率|mem_util|%|   
    |系统盘使用率|disk_util|%|   
    |磁盘读速率|disk_read_bytes_rate|KB/s|   
    |磁盘读请求速率|disk_read_requests_rate|请求/秒|   
    |磁盘写速率|disk_write_bytes_rate|KB/s|   
    |磁盘写请求速率|disk_write_requests_rate|请求/秒|   
    |网络流入速率|net_in_bytes_rate|B/s|   
    |网络流出速率|net_out_bytes_rate|B/s|
        """
        return self.send(v41describe_bare_metal_latest_metric_data_request_param)

    def get_resource_by_pool(self, get_resource_by_pool_request_param):
        """
        /v4/stats/resource-by-pool
        资源池维度资源分配率
        """
        return self.send(get_resource_by_pool_request_param)

    def query_vm_cpu_top_hybrid(self, query_vm_cpu_top_hybrid_request_param):
        """
        /v4/monitor/query-cpu-top
        调用此接口可查询用户在指定资源池云主机监控中cpu使用率Top-N。
        """
        return self.send(query_vm_cpu_top_hybrid_request_param)
