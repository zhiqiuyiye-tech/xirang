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


class CtelbClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctelb-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtelbClient, self).__init__(credential, config, 'ctelb', '0.1.0', logger, signer)

    def associate_eip_to_load_balancer(self, associate_eip_to_load_balancer_request_param):
        """
        /v4/elb/associate-eip-to
        内网负载均衡绑定弹性 IP，实现外网流量负载均衡能力。
        """
        return self.send(associate_eip_to_load_balancer_request_param)

    def update_rule(self, update_rule_request_param):
        """
        /v4/elb/update-rule
        更新转发规则
        """
        return self.send(update_rule_request_param)

    def list_vm_pool(self, list_vm_pool_request_param):
        """
        /v4/elb/list-vm-pool
        该接口为适配3.0资源池接口，可兼容4.0资源池
        """
        return self.send(list_vm_pool_request_param)

    def update_listener_response_timeout(self, update_listener_response_timeout_request_param):
        """
        /v4/elb/update-listener-response-timeout
        设置监听器响应超时时间 HTTP/HTTPS   
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(update_listener_response_timeout_request_param)

    def show_health_check_new(self, show_health_check_new_request_param):
        """
        /v4/elb/show-health-check-new
        查询健康检查详情   
    
        """
        return self.send(show_health_check_new_request_param)

    def create_listener(self, create_listener_request_param):
        """
        /v4/elb/create-listener
        创建监听器   
       
    #### 备注   
    * 3.0/acs已支持创建，但是不支持设置限速、全端口监听等高级配置。使用说明：foward类型不需要传defaultAction配合创建后端服务组使用，redirect类型使用defaultAction
        """
        return self.send(create_listener_request_param)

    def async_create_target(self, async_create_target_request_param):
        """
        /v4/elb/async-create-vm
        该接口为适配3.0资源池接口，可兼容4.0资源池   
    如果是批量创建多个，其中一个出错时会返回错误，可能出现部分创建成功，部分失败的场景
        """
        return self.send(async_create_target_request_param)

    def list_target_group(self, list_target_group_request_param):
        """
        /v4/elb/list-target-group
        查看后端服务组列表
        """
        return self.send(list_target_group_request_param)

    def renew_lb_openapi(self, renew_lb_openapi_request_param):
        """
        /v4/elb/renew-pgelb
        续订性能保障型负载均衡实例，仅支持性能保障型的续订
        """
        return self.send(renew_lb_openapi_request_param)

    def list_access_control(self, list_access_control_request_param):
        """
        /v4/elb/list-access-control
        查询策略地址组，访问控制采用黑、白名单方式实现，此接口为查询黑、白名单的地址组。   
    
        """
        return self.send(list_access_control_request_param)

    def create_load_balancer(self, create_load_balancer_request_param):
        """
        /v4/elb/create-loadbalancer
        创建负载均衡实例，创建elb时，eipID绑定失败会报错(eip已经被绑定/eip不存在)   
    
        """
        return self.send(create_load_balancer_request_param)

    def list_listener(self, list_listener_request_param):
        """
        /v4/elb/list-listener
        查看监听器列表   
    
        """
        return self.send(list_listener_request_param)

    def list_certificate(self, list_certificate_request_param):
        """
        /v4/elb/list-certificate
        获取证书列表
        """
        return self.send(list_certificate_request_param)

    def refund_paas_elb_hybrid(self, refund_paas_elb_hybrid_request_param):
        """
        /v4/elb/refund-pgelb
        退订性能保障型负载均衡实例，支持退订正常/错误状态下的资源；3,0底层性能保障型没有余量
        """
        return self.send(refund_paas_elb_hybrid_request_param)

    def show_access_control(self, show_access_control_request_param):
        """
        /v4/elb/show-access-control
        查询访问控制详情
        """
        return self.send(show_access_control_request_param)

    def delete_rule(self, delete_rule_request_param):
        """
        /v4/elb/delete-rule
        删除转发规则
        """
        return self.send(delete_rule_request_param)

    def disable_elb_ipv6(self, disable_elb_ipv6_request_param):
        """
        /v4/elb/disable-ipv6
        负载均衡关闭IPv6   
    3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的   
    #### 备注   
    * 不支持 3.0，因为 3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的
        """
        return self.send(disable_elb_ipv6_request_param)

    def resize_lb_order_openapi(self, resize_lb_order_openapi_request_param):
        """
        /v4/elb/modify-pgelb-spec
        性能保障型负载均衡变配；3,0底层性能保障型没有余量
        """
        return self.send(resize_lb_order_openapi_request_param)

    def update_listener(self, update_listener_request_param):
        """
        /v4/elb/update-listener
        更新监听器   
       
    #### 备注   
    * 不支持 3.0，因为 3.0 支持更新的参数与 4.0 不一致
        """
        return self.send(update_listener_request_param)

    def get_elb_label_openapi(self, get_elb_label_openapi_request_param):
        """
        /v4/elb/list-labels
        查询负载均衡实例绑定的标签列表
        """
        return self.send(get_elb_label_openapi_request_param)

    def enable_elb_ipv6(self, enable_elb_ipv6_request_param):
        """
        /v4/elb/enable-ipv6
        负载均衡开启IPv6   
    3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的   
    #### 备注   
    * 不支持 3.0，因为 3.0 的 elb ipv6 是靠 eip 是不是 v6 支持的
        """
        return self.send(enable_elb_ipv6_request_param)

    def query_sla(self, query_sla_request_param):
        """
        /v4/elb/query-sla
        查看规格列表
        """
        return self.send(query_sla_request_param)

    def show_load_balancer(self, show_load_balancer_request_param):
        """
        /v4/elb/show-loadbalancer
        查询负载均衡实例
        """
        return self.send(show_load_balancer_request_param)

    def update_listener_nat64(self, update_listener_nat64_request_param):
        """
        /v4/elb/update-listener-nat64
        设置监听器NAT64   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(update_listener_nat64_request_param)

    def show_rule(self, show_rule_request_param):
        """
        /v4/elb/show-rule
        <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
       
    ```   
       
        "errorCode": null,   
        "returnObj": {   
            "ID": "default_action",   
            "action": {   
                "forwardConfig": {   
                    "targetGroups": [   
                        {   
                            "targetGroupID": "tg-y49ma576s1",   
                            "weight": 100   
                        }   
                    ]   
                },   
                "type": "forward"   
            },   
            "azName": "az3",   
            "conditions": [   
                {   
                    "serverNameConfig": {},   
                    "urlPathConfig": {}   
                }   
            ],   
            "createdTime": "2022-12-21T10:58:18.840648Z",   
            "listenerID": "listener-6rfyd0m2w3",   
            "loadBalancerID": "",   
            "projectID": "",   
            "regionID": "nm8",   
            "updatedTime": "2022-12-21T10:58:18.840684Z"   
        },   
        "statusCode": 800   
    }   
    ```
        """
        return self.send(show_rule_request_param)

    def delete_target(self, delete_target_request_param):
        """
        /v4/elb/delete-target
        删除后端服务
        """
        return self.send(delete_target_request_param)

    def disassociate_eip_from_load_balancer(self, disassociate_eip_from_load_balancer_request_param):
        """
        /v4/elb/disassociate-eip-from
        解绑弹性 IP
        """
        return self.send(disassociate_eip_from_load_balancer_request_param)

    def list_l_b_domain_cert_links_openapi(self, list_l_b_domain_cert_links_openapi_request_param):
        """
        /v4/elb/list-domain-cert-links
        查看多证书列表
        """
        return self.send(list_l_b_domain_cert_links_openapi_request_param)

    def show_target_group(self, show_target_group_request_param):
        """
        /v4/elb/show-target-group
        查看后端服务组信息   
    
        """
        return self.send(show_target_group_request_param)

    def delete_load_balancer(self, delete_load_balancer_request_param):
        """
        /v4/elb/delete-loadbalancer
        删除负载均衡实例
        """
        return self.send(delete_load_balancer_request_param)

    def elb_bind_label_openapi(self, elb_bind_label_openapi_request_param):
        """
        /v4/elb/bind-label
        负载均衡绑定标签
        """
        return self.send(elb_bind_label_openapi_request_param)

    def delete_listener(self, delete_listener_request_param):
        """
        /v4/elb/delete-listener
        删除监听器
        """
        return self.send(delete_listener_request_param)

    def delete_certificate(self, delete_certificate_request_param):
        """
        /v4/elb/delete-certificate
        删除证书
        """
        return self.send(delete_certificate_request_param)

    def update_lb_listener_qps_openapi(self, update_lb_listener_qps_openapi_request_param):
        """
        /v4/elb/update-listener-qps
        设置监听器每秒查询数,HTTPS/HTTP类型   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(update_lb_listener_qps_openapi_request_param)

    def delete_l_b_domain_cert_links_openapi(self, delete_l_b_domain_cert_links_openapi_request_param):
        """
        /v4/elb/delete-domain-cert-links
        删除多证书
        """
        return self.send(delete_l_b_domain_cert_links_openapi_request_param)

    def creat_paas_elb_hybrid(self, creat_paas_elb_hybrid_request_param):
        """
        /v4/elb/create-pgelb
        创建性能保障型负载均衡实例；3,0底层性能保障型没有余量，无法创建
        """
        return self.send(creat_paas_elb_hybrid_request_param)

    def stop_listener(self, stop_listener_request_param):
        """
        /v4/elb/stop-listener
        停止监听器   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(stop_listener_request_param)

    def start_listener(self, start_listener_request_param):
        """
        /v4/elb/start-listener
        启动监听器   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(start_listener_request_param)

    def create_access_control(self, create_access_control_request_param):
        """
        /v4/elb/create-access-control
        创建策略地址组，策略地址组为被访问控制的黑白名单调用的地址组。
        """
        return self.send(create_access_control_request_param)

    def classic2_performance_optimized(self, classic2_performance_optimized_request_param):
        """
        /v4/elb/upgrade-to-pgelb
        经典型负载均衡实例升级为性能保障型；3,0底层性能保障型没有余量，无法升级
        """
        return self.send(classic2_performance_optimized_request_param)

    def create_l_b_domain_cert_links_openapi(self, create_l_b_domain_cert_links_openapi_request_param):
        """
        /v4/elb/create-domain-cert-links
        创建多证书
        """
        return self.send(create_l_b_domain_cert_links_openapi_request_param)

    def create_target(self, create_target_request_param):
        """
        /v4/elb/create-target
        创建后端服务   
    **注意**：   InstanceType参数在私有云是直接根据instanceId即可判断主机类型，默认云主机/裸金属不用传，但是当IP时必须要指定的。取值范围：VM、BM、ENIC（ENIC暂不支持）、IP   
    更新支持IP，开发中
        """
        return self.send(create_target_request_param)

    def async_create_certificate(self, async_create_certificate_request_param):
        """
        /v4/elb/async-create-certificate
        该接口为适配3.0资源池接口，可兼容4.0资源池
        """
        return self.send(async_create_certificate_request_param)

    def delete_target_group(self, delete_target_group_request_param):
        """
        /v4/elb/delete-target-group
        删除后端服务组
        """
        return self.send(delete_target_group_request_param)

    def show_certificate(self, show_certificate_request_param):
        """
        /v4/elb/show-certificate
        查看证书详情
        """
        return self.send(show_certificate_request_param)

    def async_create_loadbalance(self, async_create_loadbalance_request_param):
        """
        /v4/elb/async-create-loadbalance
        该接口为适配3.0资源池接口，可兼容创建4.0资源
        """
        return self.send(async_create_loadbalance_request_param)

    def update_lb_listener_establish_timeout(self, update_lb_listener_establish_timeout_request_param):
        """
        /v4/elb/update-listener-estab-timeout
        设置监听器建立连接超时时间   
    #### 备注   
    * 3.0 无此能力   
    TCP协议的监听器设置连接超时时间，范围10-1800；UDP/IPRAW设置请求超时时间，范围0-300
        """
        return self.send(update_lb_listener_establish_timeout_request_param)

    def update_target(self, update_target_request_param):
        """
        /v4/elb/update-target
        更新后端服务
        """
        return self.send(update_target_request_param)

    def show_health_check(self, show_health_check_request_param):
        """
        /v4/elb/show-health-check
        查询健康检查详情   
    
        """
        return self.send(show_health_check_request_param)

    def query_sla_new(self, query_sla_new_request_param):
        """
        /v4/elb/query-sla-new
        查看规格列表
        """
        return self.send(query_sla_new_request_param)

    def elb_unbind_label_openapi(self, elb_unbind_label_openapi_request_param):
        """
        /v4/elb/unbind-label
        负载均衡解绑标签
        """
        return self.send(elb_unbind_label_openapi_request_param)

    def update_rule_new(self, update_rule_new_request_param):
        """
        /v4/elb/update-rule-new
        更新转发规则，对齐公有云出入参
        """
        return self.send(update_rule_new_request_param)

    def query_create_lb_price(self, query_create_lb_price_request_param):
        """
        /v4/elb/query-create-price
        v2版本询价接口有效参数仅有regionID，slaName，cycleType，cycleCount参数，其余参数仅在必传性兼容公有云，不校验正确性
        """
        return self.send(query_create_lb_price_request_param)

    def async_create_listener(self, async_create_listener_request_param):
        """
        /v4/elb/async-create-listener
        该接口为适配3.0资源池接口，注意该接口不兼容创建4.0资源池资源
        """
        return self.send(async_create_listener_request_param)

    def update_certificate(self, update_certificate_request_param):
        """
        /v4/elb/update-certificate
        更新证书
        """
        return self.send(update_certificate_request_param)

    def list_query(self, list_query_request_param):
        """
        /v4/elb/list-rule
        转发规则列表
        """
        return self.send(list_query_request_param)

    def list_health_check(self, list_health_check_request_param):
        """
        /v4/elb/list-health-check
        获取健康检查列表
        """
        return self.send(list_health_check_request_param)

    def list_target(self, list_target_request_param):
        """
        /v4/elb/list-target
        查看后端服务列表
        """
        return self.send(list_target_request_param)

    def update_listener_attr(self, update_listener_attr_request_param):
        """
        /v4/elb/update-listener-attr
        该接口为适配3.0资源池接口，可兼容4.0资源池
        """
        return self.send(update_listener_attr_request_param)

    def delete_health_check(self, delete_health_check_request_param):
        """
        /v4/elb/delete-health-check
        删除健康检查需要先停止健康检查
        """
        return self.send(delete_health_check_request_param)

    def delete_access_control(self, delete_access_control_request_param):
        """
        /v4/elb/delete-access-control
        删除访问控制策略
        """
        return self.send(delete_access_control_request_param)

    def query_resize_lb_price(self, query_resize_lb_price_request_param):
        """
        /v4/elb/query-modify-price
        性能保障型负载均衡变配询价
        """
        return self.send(query_resize_lb_price_request_param)

    def update_health_check_new(self, update_health_check_new_request_param):
        """
        /v4/elb/update-health-check-new
        更新健康检查
        """
        return self.send(update_health_check_new_request_param)

    def update_health_check(self, update_health_check_request_param):
        """
        /v4/elb/update-health-check
        更新健康检查
        """
        return self.send(update_health_check_request_param)

    def list_load_balancer_vdc(self, list_load_balancer_vdc_request_param):
        """
        /v4/elb/list-loadbalancer-vdc
        查看负载均衡实例列表
        """
        return self.send(list_load_balancer_vdc_request_param)

    def update_listener_new(self, update_listener_new_request_param):
        """
        /v4/elb/update-listener-new
        更新监听器，对齐公有云返回   
       
    #### 备注   
    * 不支持 3.0，因为 3.0 支持更新的参数与 4.0 不一致
        """
        return self.send(update_listener_new_request_param)

    def update_lb_listener_cps(self, update_lb_listener_cps_request_param):
        """
        /v4/elb/update-listener-cps
        设置监听器每秒查询数,HTTPS/HTTP类型   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(update_lb_listener_cps_request_param)

    def show_listener(self, show_listener_request_param):
        """
        /v4/elb/show-listener
        查看监听器详情
        """
        return self.send(show_listener_request_param)

    def create_certificate(self, create_certificate_request_param):
        """
        /v4/elb/create-certificate
        创建证书   
       
    #### 备注   
    * 不支持3.0，因为3.0 是异步逻辑，4.0 是同步逻辑
        """
        return self.send(create_certificate_request_param)

    def update_access_control(self, update_access_control_request_param):
        """
        /v4/elb/update-access-control
        更新访问控制
        """
        return self.send(update_access_control_request_param)

    def list_target_new(self, list_target_new_request_param):
        """
        /v4/elb/list-target-new
        查看后端服务列表，对齐公有云
        """
        return self.send(list_target_new_request_param)

    def create_target_group(self, create_target_group_request_param):
        """
        /v4/elb/create-target-group
        创建后端服务组   
       
    #### 备注   
    * 3.0 已支持，需先创建监听器再创建后端服务组，不支持全端口监听
        """
        return self.send(create_target_group_request_param)

    def list_load_balancer(self, list_load_balancer_request_param):
        """
        /v4/elb/list-loadbalancer
        查看负载均衡实例列表
        """
        return self.send(list_load_balancer_request_param)

    def show_target(self, show_target_request_param):
        """
        /v4/elb/show-target
        查看后端服务详情
        """
        return self.send(show_target_request_param)

    def update_listener_idle_timeout(self, update_listener_idle_timeout_request_param):
        """
        /v4/elb/update-listener-idle-timeout
        设置监听器空闲超时时间 HTTP/HTTPS   
       
    #### 备注   
    * 3.0 无此能力
        """
        return self.send(update_listener_idle_timeout_request_param)

    def create_rule_new(self, create_rule_new_request_param):
        """
        /v4/elb/create-rule-new
        创建转发规则new，对齐公有云出入参数   
       
    #### 备注   
    * 不支持 3.0，因为 3.0 是异步逻辑，4.0 是同步逻辑
        """
        return self.send(create_rule_new_request_param)

    def create_health_check(self, create_health_check_request_param):
        """
        /v4/elb/create-health-check
        创建健康检查   
       
    #### 备注   
    * 3.0 已支持，需先创建主机组
        """
        return self.send(create_health_check_request_param)

    def query_renew_lb_price(self, query_renew_lb_price_request_param):
        """
        /v4/elb/query-renew-price
        性能保障型负载均衡实例续订询价
        """
        return self.send(query_renew_lb_price_request_param)

    def update_load_balancer(self, update_load_balancer_request_param):
        """
        /v4/elb/update-loadbalancer
        更新负载均衡实例
        """
        return self.send(update_load_balancer_request_param)

    def create_rule(self, create_rule_request_param):
        """
        /v4/elb/create-rule
        创建转发规则   
       
    #### 备注   
    * 不支持 3.0，因为 3.0 是异步逻辑，4.0 是同步逻辑
        """
        return self.send(create_rule_request_param)

    def update_target_group(self, update_target_group_request_param):
        """
        /v4/elb/update-target-group
        更新后端服务组   
       
    #### 备注   
    * 不支持3.0，因为无法兼容更换健康检查逻辑
        """
        return self.send(update_target_group_request_param)

    def list_vm(self, list_vm_request_param):
        """
        /v4/elb/list-vm
        该接口为适配3.0资源池接口，可兼容4.0资源池
        """
        return self.send(list_vm_request_param)

    def update_l_b_domain_cert_links_openapi(self, update_l_b_domain_cert_links_openapi_request_param):
        """
        /v4/elb/update-domain-cert-links
        修改扩展域名证书
        """
        return self.send(update_l_b_domain_cert_links_openapi_request_param)

    def remove_vm(self, remove_vm_request_param):
        """
        /v4/elb/remove-vm
        该接口为适配3.0资源池接口，可兼容4.0资源池   
    如果是批量删除多个，其中一个出错时会返回错误，可能出现部分删除成功，部分失败的场景
        """
        return self.send(remove_vm_request_param)
