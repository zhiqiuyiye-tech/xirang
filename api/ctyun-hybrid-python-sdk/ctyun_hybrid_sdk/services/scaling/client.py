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


class ScalingClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('scaling-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(ScalingClient, self).__init__(credential, config, 'scaling', '0.1.0', logger, signer)

    def group_update_health_period(self, group_update_health_period_request_param):
        """
        /v4/scaling/group/update-health-period
        修改弹性伸缩组的健康检查间隔
        """
        return self.send(group_update_health_period_request_param)

    def group_update_instance_move_out_strategy(self, group_update_instance_move_out_strategy_request_param):
        """
        /v4/scaling/group/update-instance-move-out-strategy
        设置实例移出规则
        """
        return self.send(group_update_instance_move_out_strategy_request_param)

    def group_update_attach_load_balancers(self, group_update_attach_load_balancers_request_param):
        """
        /v4/scaling/group/update-attach-load-balancers
        添加一个或多个负载均衡，伸缩组本质上绑定的是主机组，所以主机组ID不能重复   
    添加的负载均衡和主机组需要与伸缩组同一资源池，同一vdc，并且开启健康检查功能
        """
        return self.send(group_update_attach_load_balancers_request_param)

    def group_disable(self, group_disable_request_param):
        """
        /v4/scaling/group/disable
        停用一个伸缩组
        """
        return self.send(group_disable_request_param)

    def group_query_activities(self, group_query_activities_request_param):
        """
        /v4/scaling/group/query-activities
        查询伸缩活动id列表
        """
        return self.send(group_query_activities_request_param)

    def group_query_instance_list(self, group_query_instance_list_request_param):
        """
        /v4/scaling/group/query-instance-list
        查询伸缩组内云主机的列表，并列出云主机的信息
        """
        return self.send(group_query_instance_list_request_param)

    def rule_query_scheduled(self, rule_query_scheduled_request_param):
        """
        /v4/scaling/rule/query-scheduled
        查询定时任务信息
        """
        return self.send(rule_query_scheduled_request_param)

    def rule_stop(self, rule_stop_request_param):
        """
        /v4/scaling/rule/stop
        停用伸缩组中指定策略
        """
        return self.send(rule_stop_request_param)

    def group_instance_move_in(self, group_instance_move_in_request_param):
        """
        /v4/scaling/group/instance-move-in
        手动添加云主机
        """
        return self.send(group_instance_move_in_request_param)

    def group_delete(self, group_delete_request_param):
        """
        /v4/scaling/group/delete
        删除一个伸缩组，有伸缩活动正在进行时无法删除
        """
        return self.send(group_delete_request_param)

    def group_instance_monitor(self, group_instance_monitor_request_param):
        """
        /v4/scaling/group/instance-monitor
        获取弹性伸缩实例数量监控数据
        """
        return self.send(group_instance_monitor_request_param)

    def quota(self, quota_request_param):
        """
        /v4/scaling/quota
        查询用户弹性伸缩资源配额，**注意**：1.12版本后不支持该功能。
        """
        return self.send(quota_request_param)

    def group_instance_move_out(self, group_instance_move_out_request_param):
        """
        /v4/scaling/group/instance-move-out
        从一个伸缩组移出一台或多台ECS实例
        """
        return self.send(group_instance_move_out_request_param)

    def group_update_detach_load_balancers(self, group_update_detach_load_balancers_request_param):
        """
        /v4/scaling/group/update-detach-load-balancers
        删除一个或多个负载均衡
        """
        return self.send(group_update_detach_load_balancers_request_param)

    def group_check(self, group_check_request_param):
        """
        /v4/scaling/group/check
        检查伸缩组是否可修改
        """
        return self.send(group_check_request_param)

    def rule_list(self, rule_list_request_param):
        """
        /v4/scaling/rule/list
        查询弹性伸缩组内的策略列表
        """
        return self.send(rule_list_request_param)

    def group_protect_enable(self, group_protect_enable_request_param):
        """
        /v4/scaling/group/protect-enable
        开启云主机保护
        """
        return self.send(group_protect_enable_request_param)

    def group_instance_az(self, group_instance_az_request_param):
        """
        /v4/scaling/group/instance-az
        查询伸缩组内的云主机的可用区分布
        """
        return self.send(group_instance_az_request_param)

    def query_activities_list(self, query_activities_list_request_param):
        """
        /v4/scaling/group/query-activities-list
        查询伸缩活动列表
        """
        return self.send(query_activities_list_request_param)

    def rule_start(self, rule_start_request_param):
        """
        /v4/scaling/rule/start
        启用伸缩组中指定策略
        """
        return self.send(rule_start_request_param)

    def group_update_health_mode(self, group_update_health_mode_request_param):
        """
        /v4/scaling/group/update-health-mode
        修改弹性伸缩组的健康检查方式
        """
        return self.send(group_update_health_mode_request_param)

    def rule_start_alarm(self, rule_start_alarm_request_param):
        """
        /v4/scaling/rule/start-alarm
        启用一条报警策略
        """
        return self.send(rule_start_alarm_request_param)

    def rule_delete_alarm(self, rule_delete_alarm_request_param):
        """
        /v4/scaling/rule/delete-alarm
        删除一个告警策略
        """
        return self.send(rule_delete_alarm_request_param)

    def rule_delete_scheduled(self, rule_delete_scheduled_request_param):
        """
        /v4/scaling/rule/delete-scheduled
        删除一个定时任务
        """
        return self.send(rule_delete_scheduled_request_param)

    def config_security_groups_check(self, config_security_groups_check_request_param):
        """
        /v4/scaling/config/securitygroups-check
        用于检查该账户下，哪些安全组被伸缩配置所使用
        """
        return self.send(config_security_groups_check_request_param)

    def group_update(self, group_update_request_param):
        """
        /v4/scaling/group/update
        修改一个弹性伸缩组
        """
        return self.send(group_update_request_param)

    def group_update_recovery_mode(self, group_update_recovery_mode_request_param):
        """
        /v4/scaling/group/update-recovery-mode
        修改弹性伸缩组的云主机回收方式
        """
        return self.send(group_update_recovery_mode_request_param)

    def group_instance_move_out_release(self, group_instance_move_out_release_request_param):
        """
        /v4/scaling/group/instance-move-out-release
        移出一台实例并释放
        """
        return self.send(group_instance_move_out_release_request_param)

    def group_query_load_balancer_list(self, group_query_load_balancer_list_request_param):
        """
        /v4/scaling/group/query-load-balancer-list
        查询伸缩组的负载均衡器
        """
        return self.send(group_query_load_balancer_list_request_param)

    def is_open(self, is_open_request_param):
        """
        /v4/scaling/is-open
        验证用户是否已开通弹性伸缩服务
        """
        return self.send(is_open_request_param)

    def rule_create(self, rule_create_request_param):
        """
        /v4/scaling/rule/create
        创建一条伸缩策略
        """
        return self.send(rule_create_request_param)

    def rule_create_cycle(self, rule_create_cycle_request_param):
        """
        /v4/scaling/rule/create-cycle
        创建一个周期策略   
    **注意**：cycle=2时，day取值范围为0~6，0代表周天(底层设计如此)
        """
        return self.send(rule_create_cycle_request_param)

    def group_protect_disable(self, group_protect_disable_request_param):
        """
        /v4/scaling/group/protect-disable
        关闭云主机保护
        """
        return self.send(group_protect_disable_request_param)

    def rule_update_scheduled(self, rule_update_scheduled_request_param):
        """
        /v4/scaling/rule/update-scheduled
        修改一个定时任务的信息
        """
        return self.send(rule_update_scheduled_request_param)

    def rule_update_alarm(self, rule_update_alarm_request_param):
        """
        /v4/scaling/rule/update-alarm
        修改一个报警策略
        """
        return self.send(rule_update_alarm_request_param)

    def group_set_instances_protection(self, group_set_instances_protection_request_param):
        """
        /v4/scaling/group/set-instances-protection
        设置云主机保护
        """
        return self.send(group_set_instances_protection_request_param)

    def group_unhealthy_instance_list(self, group_unhealthy_instance_list_request_param):
        """
        /v4/scaling/group/unhealthy-instance-list
        查询伸缩组不健康主机
        """
        return self.send(group_unhealthy_instance_list_request_param)

    def rule_stop_alarm(self, rule_stop_alarm_request_param):
        """
        /v4/scaling/rule/stop-alarm
        停用一条报警策略
        """
        return self.send(rule_stop_alarm_request_param)

    def rule_create_alarm(self, rule_create_alarm_request_param):
        """
        /v4/scaling/rule/create-alarm
        创建一个告警策略
        """
        return self.send(rule_create_alarm_request_param)

    def group_update_instance_min_num(self, group_update_instance_min_num_request_param):
        """
        /v4/scaling/group/update-instance-min-num
        修改伸缩组最小实例数
        """
        return self.send(group_update_instance_min_num_request_param)

    def group_list(self, group_list_request_param):
        """
        /v4/scaling/group/list
        查询伸缩组列表
        """
        return self.send(group_list_request_param)

    def config_create(self, config_create_request_param):
        """
        /v4/scaling/config-create
        创建一个弹性伸缩配置
        """
        return self.send(config_create_request_param)

    def rule_execute(self, rule_execute_request_param):
        """
        /v4/scaling/rule/execute
        请求示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"regionID"</span><span class="colour" style="color:rgb(0, 0, 0)">:</span><span class="colour" style="color:rgb(4, 81, 165)">"nm8"</span><span class="colour" style="color:rgb(0, 0, 0)">,</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"ruleID"</span><span class="colour" style="color:rgb(0, 0, 0)">:</span><span class="colour" style="color:rgb(4, 81, 165)">"8e6883a0-5b63-11ed-a71c-0242ac130010"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>   
       
    返回示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    </span><span class="colour" style="color:rgb(163, 21, 21)">"returnObj"</span><span class="colour" style="color:rgb(0, 0, 0)">: {</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">        </span><span class="colour" style="color:rgb(163, 21, 21)">"ruleID"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"8e6883a0-5b63-11ed-a71c-0242ac130010"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    },</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">    </span><span class="colour" style="color:rgb(163, 21, 21)">"statusCode"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(9, 134, 88)">800</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>
        """
        return self.send(rule_execute_request_param)

    def config_delete(self, config_delete_request_param):
        """
        /v4/scaling/config-delete
        删除一个弹性伸缩配置
        """
        return self.send(config_delete_request_param)

    def config_list(self, config_list_request_param):
        """
        /v4/scaling/config-list
        查询弹性伸缩配置
        """
        return self.send(config_list_request_param)

    def rule_delete(self, rule_delete_request_param):
        """
        /v4/scaling/rule/delete
        删除一条伸缩策略
        """
        return self.send(rule_delete_request_param)

    def group_update_instance_max_num(self, group_update_instance_max_num_request_param):
        """
        /v4/scaling/group/update-instance-max-num
        修改伸缩组最大实例数
        """
        return self.send(group_update_instance_max_num_request_param)

    def group_query_activity_detail(self, group_query_activity_detail_request_param):
        """
        /v4/scaling/group/query-activity-detail
        查询伸缩活动详情
        """
        return self.send(group_query_activity_detail_request_param)

    def group_create(self, group_create_request_param):
        """
        /v4/scaling/group/create
        创建一个弹性伸缩组，注意伸缩组名称不能重复
        """
        return self.send(group_create_request_param)

    def config_update(self, config_update_request_param):
        """
        /v4/scaling/config-update
        修改一个弹性伸缩配置
        """
        return self.send(config_update_request_param)

    def rule_query_alarm(self, rule_query_alarm_request_param):
        """
        /v4/scaling/rule/query-alarm
        查询报警任务的信息
        """
        return self.send(rule_query_alarm_request_param)

    def group_enable(self, group_enable_request_param):
        """
        /v4/scaling/group/enable
        启用一个伸缩组
        """
        return self.send(group_enable_request_param)

    def rule_create_scheduled(self, rule_create_scheduled_request_param):
        """
        /v4/scaling/rule/create-scheduled
        创建一个定时任务
        """
        return self.send(rule_create_scheduled_request_param)

    def rule_update(self, rule_update_request_param):
        """
        /v4/scaling/rule/update
        修改一条伸缩策略   
    混合云管2.2.4版本及之前不支持修改告警策略已绑定的告警规则参数，仅支持ruleID更换其他已有规则，或者triggerObj新建其他告警规则，二选一。   
    2.2.4版本支持可修改告警策略已绑定的告警规则
        """
        return self.send(rule_update_request_param)
