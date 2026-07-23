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


class CtvpcClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctvpc-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtvpcClient, self).__init__(credential, config, 'ctvpc', '0.1.0', logger, signer)

    def create_gateway_route_table(self, create_gateway_route_table_request_param):
        """
        /v4/vpc/route-table/create-gateway-routetable
        创建网关路由表   
    ## 公有云差别   
    * clientToken公有云必填字段，字段不影响接口功能，混合云不必填当作对齐。   此接口仅支持4.0
        """
        return self.send(create_gateway_route_table_request_param)

    def update_endpoint(self, update_endpoint_request_param):
        """
        /v4/vpce/update-endpoint
        更新终端节点
        """
        return self.send(update_endpoint_request_param)

    def query_create_nat_price(self, query_create_nat_price_request_param):
        """
        /v4/nat/query-create-price
        非询价必需字段不做校验，只透传
        """
        return self.send(query_create_nat_price_request_param)

    def vpc_list_vdc(self, vpc_list_vdc_request_param):
        """
        /v4/vpc/list-vdc
        查询VPC列表
        """
        return self.send(vpc_list_vdc_request_param)

    def new_subnet_list(self, new_subnet_list_request_param):
        """
        /v4/vpc/new-list-subnet
        具体详细信息，查看解绑HaVip接口（/v4/vpc/list-subnet）。
        """
        return self.send(new_subnet_list_request_param)

    def delete_havip(self, delete_havip_request_param):
        """
        /v4/vpc/havip/delete
        删除高可用虚IP   
    虚拟ip如果绑定了实例或者弹性ip，该接口会自动进行解绑
        """
        return self.send(delete_havip_request_param)

    def dns_get_label_openapi(self, dns_get_label_openapi_request_param):
        """
        /v4/private-zone/list-labels
        查询DNS绑定的标签列表
        """
        return self.send(dns_get_label_openapi_request_param)

    def show_vpc_peer_connection(self, show_vpc_peer_connection_request_param):
        """
        /v4/vpc/get-vpc-peer-connection-attribute
        查询对等连接详情
        """
        return self.send(show_vpc_peer_connection_request_param)

    def attach_port_vm(self, attach_port_vm_request_param):
        """
        /v4/eip/attach-port-vm
        EIP绑定云主机网卡
        """
        return self.send(attach_port_vm_request_param)

    def modify_ipv6_bandwidth_spec(self, modify_ipv6_bandwidth_spec_request_param):
        """
        /v4/ipv6_bandwidth/modify-spec
        修改ipv6带宽规格
        """
        return self.send(modify_ipv6_bandwidth_spec_request_param)

    def list_private_zone(self, list_private_zone_request_param):
        """
        /v4/private-zone/list
        内网DNS列表
        """
        return self.send(list_private_zone_request_param)

    def delete_route_table_rules(self, delete_route_table_rules_request_param):
        """
        /v4/vpc/route-table/delete-rules
        批量删除路由表规则   3.0底层不支持批量删除，由云管侧兼容，尽量数量控制在10个以内
        """
        return self.send(delete_route_table_rules_request_param)

    def create_bandwidth(self, create_bandwidth_request_param):
        """
        /v4/bandwidth/create
        创建共享带宽
        """
        return self.send(create_bandwidth_request_param)

    def batch_unassign_ipv6_from_port(self, batch_unassign_ipv6_from_port_request_param):
        """
        /v4/ports/batch-unassign-ipv6
        多个网卡解绑IPv6地址
        """
        return self.send(batch_unassign_ipv6_from_port_request_param)

    def show_endpoint_whitelist(self, show_endpoint_whitelist_request_param):
        """
        /v4/vpce/show-endpoint-whitelist
        查询终端节点白名单
        """
        return self.send(show_endpoint_whitelist_request_param)

    def create_endpoint_service_rule(self, create_endpoint_service_rule_request_param):
        """
        /v4/vpce/create-endpoint-service-rule
        终端节点服务规则创建接口
        """
        return self.send(create_endpoint_service_rule_request_param)

    def disassociate_eip_from_bandwidth(self, disassociate_eip_from_bandwidth_request_param):
        """
        /v4/bandwidth/disassociate-eip
        调用此接口可从共享带宽移出EIPs。
        """
        return self.send(disassociate_eip_from_bandwidth_request_param)

    def create_endpoint(self, create_endpoint_request_param):
        """
        /v4/vpce/create-endpoint
        创建终端节点服务
        """
        return self.send(create_endpoint_request_param)

    def create_eip_address_group_open_api(self, create_eip_address_group_open_api_request_param):
        """
        /v4/eipPool
        创建ip地址组
        """
        return self.send(create_eip_address_group_open_api_request_param)

    def delete_flow_session(self, delete_flow_session_request_param):
        """
        /v4/flowsession/delete
        删除流量会话
        """
        return self.send(delete_flow_session_request_param)

    def list_route_table(self, list_route_table_request_param):
        """
        /v4/vpc/route-table/list
        查询路由表列表
        """
        return self.send(list_route_table_request_param)

    def new_acl_list(self, new_acl_list_request_param):
        """
        /v4/acl/new-list
        查询acl列表
        """
        return self.send(new_acl_list_request_param)

    def show_dnat_entry(self, show_dnat_entry_request_param):
        """
        /v4/vpc/detail-dnat-entries
        查询DNAT详情
        """
        return self.send(show_dnat_entry_request_param)

    def modify_bandwidth_spec(self, modify_bandwidth_spec_request_param):
        """
        /v4/bandwidth/modify-spec
        修改共享带宽的数值
        """
        return self.send(modify_bandwidth_spec_request_param)

    def update_private_zone_record_attribute(self, update_private_zone_record_attribute_request_param):
        """
        /v4/private-zone-record/update
        修改内网 DNS 记录（公有云不支持name传参）
        """
        return self.send(update_private_zone_record_attribute_request_param)

    def api_order_renew_ipv6_bandwidth(self, api_order_renew_ipv6_bandwidth_request_param):
        """
        /v4/ipv6_bandwidth/renew
        续订 IPv6 带宽
        """
        return self.send(api_order_renew_ipv6_bandwidth_request_param)

    def batch_assign_ipv6_to_port(self, batch_assign_ipv6_to_port_request_param):
        """
        /v4/ports/batch-assign-ipv6
        1、该接口无法保证原子性，可能会出现部分网卡更新成功，部分网卡更新失败的情况，这种情况需要调用方进行处理。   
    2、返回结果是多条任务的job id，再分别通过job id查询每条任务的执行结果。
        """
        return self.send(batch_assign_ipv6_to_port_request_param)

    def create_security_group(self, create_security_group_request_param):
        """
        /v4/vpc/create-security-group
        创建安全组。   
    安全组名称不允许重复   
    3.0vpcID无用
        """
        return self.send(create_security_group_request_param)

    def bandwidth_query_modify_price(self, bandwidth_query_modify_price_request_param):
        """
        /v4/bandwidth/query-modify-price
        共享带宽变配询价
        """
        return self.send(bandwidth_query_modify_price_request_param)

    def list_nat_gateways_vdc(self, list_nat_gateways_vdc_request_param):
        """
        /v4/vpc/describe-nat-gateways-vdc
        查询NAT网关接口列表
        """
        return self.send(list_nat_gateways_vdc_request_param)

    def vpc_show_ipv6_enabled_string(self, vpc_show_ipv6_enabled_string_request_param):
        """
        /v4/vpc/query-ipv6Enabled-string
        查询用户专有网络
        """
        return self.send(vpc_show_ipv6_enabled_string_request_param)

    def create_private_zone(self, create_private_zone_request_param):
        """
        /v4/private-zone/create
        创建内网 DNS
        """
        return self.send(create_private_zone_request_param)

    def query_ctyun_service_openapi(self, query_ctyun_service_openapi_request_param):
        """
        /v4/vpce/query-ctyun-service
        查看天翼云终端节点公共服务
        """
        return self.send(query_ctyun_service_openapi_request_param)

    def show_havip(self, show_havip_request_param):
        """
        /v4/vpc/havip/show
        1.14.27将返回中的instanceInfo字段从对象改为了集合(改动原因：vip下可以绑定多个云主机，符合业务逻辑)，同时新增了networkInfo集合
        """
        return self.send(show_havip_request_param)

    def list_endpoint_service(self, list_endpoint_service_request_param):
        """
        /v4/vpce/list-endpoint-service
        查看终端节点服务列表
        """
        return self.send(list_endpoint_service_request_param)

    def get_group_vdc_list_open_api(self, get_group_vdc_list_open_api_request_param):
        """
        /v4/eipPool/vdcList
        查询ip地址组已绑定vdc列表
        """
        return self.send(get_group_vdc_list_open_api_request_param)

    def disassociate_ipv6_from_bandwidth(self, disassociate_ipv6_from_bandwidth_request_param):
        """
        /v4/bandwidth/disassociate-ipv6
        调用此接口可从共享带宽中移出IPv6s。
        """
        return self.send(disassociate_ipv6_from_bandwidth_request_param)

    def query_create_eip_price(self, query_create_eip_price_request_param):
        """
        /v4/eip/query-create-price
        调用此接口可查询创建弹性公网IP的价格，可以直接使用创建参数询价，对非询价所需字段不做校验，只做透传，混合云目前入参缺失bandwidthID，这个字段。非必填，暂不做调整。支持3.0   
    价格单位：按带宽 元/小时，按流量 元/GB
        """
        return self.send(query_create_eip_price_request_param)

    def list_havip(self, list_havip_request_param):
        """
        /v4/vpc/havip/list
        查询HaVip，从1.14.27将返回中的instanceInfo字段从对象改为了集合(改动原因：vip下可以绑定多个云主机，符合业务逻辑)，同时新增了networkInfo集合
        """
        return self.send(list_havip_request_param)

    def create_ipv6_bandwidth(self, create_ipv6_bandwidth_request_param):
        """
        /v4/ipv6_bandwidth/create
        创建IPV6带宽
        """
        return self.send(create_ipv6_bandwidth_request_param)

    def vpc_list(self, vpc_list_request_param):
        """
        /v4/vpc/list
        查询VPC列表
        """
        return self.send(vpc_list_request_param)

    def delete_mirror_flow_filter_rule(self, delete_mirror_flow_filter_rule_request_param):
        """
        /v4/mirrorflow/delete-filter-rule
        删除过滤规则
        """
        return self.send(delete_mirror_flow_filter_rule_request_param)

    def delete_endpoint_service_reverse_rule(self, delete_endpoint_service_reverse_rule_request_param):
        """
        /v4/vpce/delete-endpoint-service-reverse-rule
        删除终端节点服务中转规则(反向访问规则)
        """
        return self.send(delete_endpoint_service_reverse_rule_request_param)

    def list_endpoint_vdc(self, list_endpoint_vdc_request_param):
        """
        /v4/vpce/list-endpoint-vdc
        查看终端节点列表
        """
        return self.send(list_endpoint_vdc_request_param)

    def list_route_table_rules(self, list_route_table_rules_request_param):
        """
        /v4/vpc/route-table/list-rules
        查询路由表规则列表   
    
        """
        return self.send(list_route_table_rules_request_param)

    def create_route_table_rules(self, create_route_table_rules_request_param):
        """
        /v4/vpc/route-table/create-rules
        批量创建路由表规则   3.0底层不支持批量，由云管侧处理兼容，所以尽量数量控制在5个以内   
    
        """
        return self.send(create_route_table_rules_request_param)

    def list_dnat_entries(self, list_dnat_entries_request_param):
        """
        /v4/vpc/describe-dnat-entries
        查询DNAT列表
        """
        return self.send(list_dnat_entries_request_param)

    def update_acl_rule_attribute(self, update_acl_rule_attribute_request_param):
        """
        /v4/acl-rule/update
        只有用户创建的ACL规则才能修改，ACL默认创建的ACL规则不允许修改
        """
        return self.send(update_acl_rule_attribute_request_param)

    def create_ipv6_gateway(self, create_ipv6_gateway_request_param):
        """
        /v4/vpc/create-ipv6-gateway
        创建ipv6网关
        """
        return self.send(create_ipv6_gateway_request_param)

    def get_avaliable_cidr_hybrid(self, get_avaliable_cidr_hybrid_request_param):
        """
        /v4/eip/available-cidr
        查询资源池所有可用的网段cidr
        """
        return self.send(get_avaliable_cidr_hybrid_request_param)

    def new_vpc_list(self, new_vpc_list_request_param):
        """
        /v4/vpc/new-list
        查询用户专有网络列表   
    具体详细信息，查看解绑HaVip接口（/v4/vpc/list）。
        """
        return self.send(new_vpc_list_request_param)

    def associate_eips_to_snat(self, associate_eips_to_snat_request_param):
        """
        /v4/vpc/join-snat-for-eips
        SNAT添加EIP
        """
        return self.send(associate_eips_to_snat_request_param)

    def change_filte_rule_priority(self, change_filte_rule_priority_request_param):
        """
        /v4/mirrorflow/change-filter-rule-priority
        调整过滤规则优先级
        """
        return self.send(change_filte_rule_priority_request_param)

    def create_nat_gateway(self, create_nat_gateway_request_param):
        """
        /v4/vpc/create-nat-gateway
        创建NAT网关
        """
        return self.send(create_nat_gateway_request_param)

    def replace_subnet_route_table(self, replace_subnet_route_table_request_param):
        """
        /v4/vpc/replace-subnet-route-table
        子网更换路由表，子网必须关联一张路由表。创建VPC后会自动生成一张默认路由表，新建子网时，会关联到默认路由表，子网可以更换其他路由表。   
    ## 接口约束   
    公有云没有azName字段，非必填字段，暂不做调整
        """
        return self.send(replace_subnet_route_table_request_param)

    def update_acl_attribute(self, update_acl_attribute_request_param):
        """
        /v4/acl/update
        修改acl 属性
        """
        return self.send(update_acl_attribute_request_param)

    def stop_flow_session(self, stop_flow_session_request_param):
        """
        /v4/flowsession/stop
        暂停流量会话
        """
        return self.send(stop_flow_session_request_param)

    def update_vpc_attribute(self, update_vpc_attribute_request_param):
        """
        /v4/vpc/update
        修改专有网络VPC的属性：名称、描述。
        """
        return self.send(update_vpc_attribute_request_param)

    def iaas_network_route_table_create(self, iaas_network_route_table_create_request_param):
        """
        /v4/vpc/route-table/create
        创建路由表
        """
        return self.send(iaas_network_route_table_create_request_param)

    def get_segments_open_api(self, get_segments_open_api_request_param):
        """
        /v4/eipPool/segments
        获取可用地址范围
        """
        return self.send(get_segments_open_api_request_param)

    def update_ipv6_status_for_vpc(self, update_ipv6_status_for_vpc_request_param):
        """
        /v4/vpc/update-ipv6-status
        修改VPC的 IPv6 状态
        """
        return self.send(update_ipv6_status_for_vpc_request_param)

    def get_unbind_vdc_list_open_api(self, get_unbind_vdc_list_open_api_request_param):
        """
        /v4/eipPool/unbindVdcList
        查询可绑定的VDC列表
        """
        return self.send(get_unbind_vdc_list_open_api_request_param)

    def delete_endpoint_service_whitelist(self, delete_endpoint_service_whitelist_request_param):
        """
        /v4/vpce/delete-endpoint-service-whitelist
        删除终端节点服务白名单
        """
        return self.send(delete_endpoint_service_whitelist_request_param)

    def join_security_group(self, join_security_group_request_param):
        """
        /v4/vpc/join-security-group
        绑定安全组。主机和安全组需要在同一个VPC下才能够进行绑定（4.0）
        """
        return self.send(join_security_group_request_param)

    def delete_vpc_peering_route_hybrid(self, delete_vpc_peering_route_hybrid_request_param):
        """
        /v4/vpc/vpcpeer/delete-peering-route
        1.16.01版本以后支持该接口
        """
        return self.send(delete_vpc_peering_route_hybrid_request_param)

    def query_renew_eip_price(self, query_renew_eip_price_request_param):
        """
        /v4/eip/query-renew-price
        调用此接口可查询续订弹性公网IP的价格
        """
        return self.send(query_renew_eip_price_request_param)

    def list_e_ip_name_hybrid(self, list_e_ip_name_hybrid_request_param):
        """
        /v4/eip/EIPGateway/listEIPName/
        查询网关出口类型列表
        """
        return self.send(list_e_ip_name_hybrid_request_param)

    def create_snat_entry(self, create_snat_entry_request_param):
        """
        /v4/vpc/create-snat-entry
        创建SNAT规则。snatIps需填入弹性IP的ID
        """
        return self.send(create_snat_entry_request_param)

    def show_endpoint_service_connections(self, show_endpoint_service_connections_request_param):
        """
        /v4/vpce/show-endpoint-service-connections
        终端节点服务连接查询
        """
        return self.send(show_endpoint_service_connections_request_param)

    def new_endpoints_list_vdc(self, new_endpoints_list_vdc_request_param):
        """
        /v4/vpce/new-list-endpoint-vdc
        查看终端节点列表   
    
        """
        return self.send(new_endpoints_list_vdc_request_param)

    def check_eip_address(self, check_eip_address_request_param):
        """
        /v4/eip/check-address
        检查EIP地址是否被使用   
    1.15已修改为返回对象
        """
        return self.send(check_eip_address_request_param)

    def associate_eip(self, associate_eip_request_param):
        """
        /v4/eip/associate
        调用此接口可将弹性公网IP（Elastic IP Address，简称EIP）与相关云产品上绑定。   
    绑定之前必须确定EIP没有绑定别的实例，并且云主机也不能已经绑定EIP   
    ### 接口约束   
    - EIP 需为可用状态。   
    - EIP 可绑定到同区域的云主机、裸金属和高可用虚拟IP上。   
    
        """
        return self.send(associate_eip_request_param)

    def list_vpc_peer_connection_vdc(self, list_vpc_peer_connection_vdc_request_param):
        """
        /v4/vpc/list-vpc-peer-connection-vdc
        查询对等连接列表
        """
        return self.send(list_vpc_peer_connection_vdc_request_param)

    def show_route_table(self, show_route_table_request_param):
        """
        /v4/vpc/route-table/show
        查询路由表详情
        """
        return self.send(show_route_table_request_param)

    def vpc_update_subnet_ipv6_status(self, vpc_update_subnet_ipv6_status_request_param):
        """
        /v4/vpc/update-subnet-ipv6-status
        修改子网的 IPv6 状态；3.0 子网一旦开启 ipv6 就不能关闭了
        """
        return self.send(vpc_update_subnet_ipv6_status_request_param)

    def get_group_eip_list_open_api(self, get_group_eip_list_open_api_request_param):
        """
        /v4/eipPool/eipList
        查询ip地址组已用EIP列表
        """
        return self.send(get_group_eip_list_open_api_request_param)

    def new_endpoint_service_white_list(self, new_endpoint_service_white_list_request_param):
        """
        /v4/vpce/new-list-endpoint-service-whitelist
        查询终端节点服务白名单
        """
        return self.send(new_endpoint_service_white_list_request_param)

    def create_security_group_in_rules_openapi_new(self, create_security_group_in_rules_openapi_new_request_param):
        """
        /v4/vpc/create-security-group-ingress-new
        创建安全组入向规则。公有云入参缺clientToken字段，暂不修改
        """
        return self.send(create_security_group_in_rules_openapi_new_request_param)

    def show_acl(self, show_acl_request_param):
        """
        /v4/acl/query
        查询ACL详情
        """
        return self.send(show_acl_request_param)

    def check_mx_openapi(self, check_mx_openapi_request_param):
        """
        /v4/private-zone-record/check-mx
        检查MX记录集合法性
        """
        return self.send(check_mx_openapi_request_param)

    def dns_unbind_label_openapi(self, dns_unbind_label_openapi_request_param):
        """
        /v4/private-zone/unbind-label
        DNS解绑标签
        """
        return self.send(dns_unbind_label_openapi_request_param)

    def get_sg_bind_ports(self, get_sg_bind_ports_request_param):
        """
        /v4/vpc/get-sg-bind-ports
        获取安全组绑定网卡
        """
        return self.send(get_sg_bind_ports_request_param)

    def remove_ipv6_from_ipv6_bandwidth(self, remove_ipv6_from_ipv6_bandwidth_request_param):
        """
        /v4/ipv6_bandwidth/remove-ipv6
        IPV6带宽移除IPV6地址
        """
        return self.send(remove_ipv6_from_ipv6_bandwidth_request_param)

    def show_port(self, show_port_request_param):
        """
        /v4/ports/show
        查询网卡信息
        """
        return self.send(show_port_request_param)

    def new_endpoints_list(self, new_endpoints_list_request_param):
        """
        /v4/vpce/new-list-endpoint
        查看终端节点列表   
    
        """
        return self.send(new_endpoints_list_request_param)

    def disassociate_eips_from_snat(self, disassociate_eips_from_snat_request_param):
        """
        /v4/vpc/revoke-snat-for-eips
        SNAT移除EIP
        """
        return self.send(disassociate_eips_from_snat_request_param)

    def update_mirror_flow_filter(self, update_mirror_flow_filter_request_param):
        """
        /v4/mirrorflow/update-filter
        流量镜像过滤条件更新
        """
        return self.send(update_mirror_flow_filter_request_param)

    def attach_port(self, attach_port_request_param):
        """
        /v4/ports/attach
        网卡绑定实例   
    ### 接口约束
        """
        return self.send(attach_port_request_param)

    def update_route_table_rules_attribute(self, update_route_table_rules_attribute_request_param):
        """
        /v4/vpc/route-table/modify-rules
        批量修改路由表规则   3.0底层不支持批量修改，由云管做的兼容，先删除再创建，所以建议此接口批量个数尽量不超过5个
        """
        return self.send(update_route_table_rules_attribute_request_param)

    def batch_delete_zone_records(self, batch_delete_zone_records_request_param):
        """
        /v4/private-zone-record/batch-delete
        内网 DNS 记录集批量删除
        """
        return self.send(batch_delete_zone_records_request_param)

    def list_vpc_peer(self, list_vpc_peer_request_param):
        """
        /v4/vpc/vpcpeer/requests
        获取待处理对等连接请求列表接口查询
        """
        return self.send(list_vpc_peer_request_param)

    def assign_ipv6_to_port(self, assign_ipv6_to_port_request_param):
        """
        /v4/ports/assign-ipv6
        单个网卡关联多个IPv6地址
        """
        return self.send(assign_ipv6_to_port_request_param)

    def list_mirror_flow_filter_vdc(self, list_mirror_flow_filter_vdc_request_param):
        """
        /v4/mirrorflow/list-filter-vdc
        流量镜像过滤条件列表 Vdc
        """
        return self.send(list_mirror_flow_filter_vdc_request_param)

    def associate_ipv6_to_bandwidth(self, associate_ipv6_to_bandwidth_request_param):
        """
        /v4/bandwidth/associate-ipv6
        调用方式：   
    1.通过/v4/ipv6/ipv6-list查询 绑定实例的id（associationID）   
    2.通过/v4/bandwidth/list查询共享带宽列表获取共享带宽id   
    
        """
        return self.send(associate_ipv6_to_bandwidth_request_param)

    def create_dnat_entry(self, create_dnat_entry_request_param):
        """
        /v4/vpc/create-dnat-entry
        创建DNAT规则
        """
        return self.send(create_dnat_entry_request_param)

    def update_nat_gateway_attribute(self, update_nat_gateway_attribute_request_param):
        """
        /v4/vpc/modify-nat-gateway-attribute
        修改NAT网关
        """
        return self.send(update_nat_gateway_attribute_request_param)

    def check_port_status(self, check_port_status_request_param):
        """
        /v4/ports/check-status
        网卡状态查询接口
        """
        return self.send(check_port_status_request_param)

    def list_snats(self, list_snats_request_param):
        """
        /v4/vpc/list-snats
        获取SNAT规则列表
        """
        return self.send(list_snats_request_param)

    def check_txt_openapi(self, check_txt_openapi_request_param):
        """
        /v4/private-zone-record/check-txt
        检查TXT记录集合法性
        """
        return self.send(check_txt_openapi_request_param)

    def vpc_show(self, vpc_show_request_param):
        """
        /v4/vpc/query
        查询用户专有网络
        """
        return self.send(vpc_show_request_param)

    def update_endpoint_service(self, update_endpoint_service_request_param):
        """
        /v4/vpce/modify-endpoint-service
        修改终端节点服务
        """
        return self.send(update_endpoint_service_request_param)

    def eip_renew(self, eip_renew_request_param):
        """
        /v4/eip/renew
        续订EIP。涉及订单计费，只能操作当前用户下的所属资源
        """
        return self.send(eip_renew_request_param)

    def query_renew_ipv6_bandwidth_price(self, query_renew_ipv6_bandwidth_price_request_param):
        """
        /v4/ipv6_bandwidth/query-renew-price
        续订询价。
        """
        return self.send(query_renew_ipv6_bandwidth_price_request_param)

    def list_ipv4_gw(self, list_ipv4_gw_request_param):
        """
        /v4/vpc/ipv4-gw/list
        获取IPv4网关列表  只支持4.0, 3.0列表为空
        """
        return self.send(list_ipv4_gw_request_param)

    def create_sg_egress_rule(self, create_sg_egress_rule_request_param):
        """
        /v4/vpc/create-security-group-egress
        创建安全组出向规则。
        """
        return self.send(create_sg_egress_rule_request_param)

    def list_flow_sessions_vdc(self, list_flow_sessions_vdc_request_param):
        """
        /v4/flowsession/list-vdc
        查看流量会话列表 Vdc
        """
        return self.send(list_flow_sessions_vdc_request_param)

    def show_endpoint(self, show_endpoint_request_param):
        """
        /v4/vpce/show-endpoint
        查看终端节点详情
        """
        return self.send(show_endpoint_request_param)

    def delete_acl(self, delete_acl_request_param):
        """
        /v4/acl/delete
        删除acl
        """
        return self.send(delete_acl_request_param)

    def create_acl_rule(self, create_acl_rule_request_param):
        """
        /v4/acl-rule/create
        创建aclrules：支持批量创建   
    1.15版本支持新返回格式   
    如果批量有成功也有失败的，返回当前acl下所有的acl规则id   
    如果创建都不成功，则返回空对象
        """
        return self.send(create_acl_rule_request_param)

    def agree_vpc_peer(self, agree_vpc_peer_request_param):
        """
        /v4/vpc/vpcpeer/agree-request
        同意建立对等链接
        """
        return self.send(agree_vpc_peer_request_param)

    def vpc_update_subnet_ipv6_enable_status(self, vpc_update_subnet_ipv6_enable_status_request_param):
        """
        /v4/vpc/subnet-enable-ipv6
        修改子网的 IPv6 状态，该接口仅支持开启V6
        """
        return self.send(vpc_update_subnet_ipv6_enable_status_request_param)

    def list_endpoint_service_reverse_rule(self, list_endpoint_service_reverse_rule_request_param):
        """
        /v4/vpce/list-endpoint-service-reverse-rule
        列表终端节点服务中转规则(反向访问规则)
        """
        return self.send(list_endpoint_service_reverse_rule_request_param)

    def update_single_rtb_rule_openapi(self, update_single_rtb_rule_openapi_request_param):
        """
        /v4/vpc/route-table/modify-rule
        修改单条路由表规则   
    
        """
        return self.send(update_single_rtb_rule_openapi_request_param)

    def get_eip_address_groups_open_api(self, get_eip_address_groups_open_api_request_param):
        """
        /v4/eipPool
        查询ip地址组列表
        """
        return self.send(get_eip_address_groups_open_api_request_param)

    def create_in_filter_rule(self, create_in_filter_rule_request_param):
        """
        /v4/mirrorflow/create-filter-in-rule
        destPort与srcPort 起始端口必须小于结束端口 当协议为ALL/ICMP时，端口传'-'
        """
        return self.send(create_in_filter_rule_request_param)

    def delete_endpoint_service(self, delete_endpoint_service_request_param):
        """
        /v4/vpce/delete-endpoint-service
        删除终端节点服务
        """
        return self.send(delete_endpoint_service_request_param)

    def sg_batch_detach_ports(self, sg_batch_detach_ports_request_param):
        """
        /v4/vpc/batch-detach-security-group-ports
        安全组批量解绑网卡。clientToken公有云必填字段，字段不影响接口功能，混合云不必填当作对齐。
        """
        return self.send(sg_batch_detach_ports_request_param)

    def update_flow_session(self, update_flow_session_request_param):
        """
        /v4/flowsession/update
        更新流量会话
        """
        return self.send(update_flow_session_request_param)

    def update_route_table_attribute(self, update_route_table_attribute_request_param):
        """
        /v4/vpc/route-table/modify
        修改路由表属性
        """
        return self.send(update_route_table_attribute_request_param)

    def modify_sg_ingress_rule(self, modify_sg_ingress_rule_request_param):
        """
        /v4/vpc/modify-security-group-ingress
        修改安全组入方向规则的描述信息，该接口只能修改入方向描述信息。
        """
        return self.send(modify_sg_ingress_rule_request_param)

    def get_associated_dns_vpc_list_openapi(self, get_associated_dns_vpc_list_openapi_request_param):
        """
        /v4/private-zone/list-vpcs
        内网 DNS 关联 VPC列表
        """
        return self.send(get_associated_dns_vpc_list_openapi_request_param)

    def batch_check_eip_address(self, batch_check_eip_address_request_param):
        """
        /v4/eip/check-addresses
        批量检查EIP地址是否被使用
        """
        return self.send(batch_check_eip_address_request_param)

    def refuse_endpoint_apply(self, refuse_endpoint_apply_request_param):
        """
        /v4/vpce/reject-endpoint-apply
        拒绝终端节点连接申请
        """
        return self.send(refuse_endpoint_apply_request_param)

    def list_endpoint(self, list_endpoint_request_param):
        """
        /v4/vpce/list-endpoint
        查看终端节点列表
        """
        return self.send(list_endpoint_request_param)

    def modify_service_ip_version(self, modify_service_ip_version_request_param):
        """
        /v4/vpce/modify-endpoint-service-ip-version
        添加终端节点白名单
        """
        return self.send(modify_service_ip_version_request_param)

    def delete_single_route_rule_openapi(self, delete_single_route_rule_openapi_request_param):
        """
        /v4/vpc/route-table/delete-rule
        删除单条路由表规则   
    
        """
        return self.send(delete_single_route_rule_openapi_request_param)

    def create_sg_ingress_rule(self, create_sg_ingress_rule_request_param):
        """
        /v4/vpc/create-security-group-ingress
        创建安全组入向规则。公有云入参缺clientToken字段，暂不修改
        """
        return self.send(create_sg_ingress_rule_request_param)

    def new_query_security_groups(self, new_query_security_groups_request_param):
        """
        /v4/vpc/new-query-security-groups
        查询用户安全组列表。
        """
        return self.send(new_query_security_groups_request_param)

    def create_endpoint_service_transit_ip(self, create_endpoint_service_transit_ip_request_param):
        """
        /v4/vpce/create-endpoint-service-transit-ip
        创建节点服务中转ip
        """
        return self.send(create_endpoint_service_transit_ip_request_param)

    def new_ipv6_list(self, new_ipv6_list_request_param):
        """
        /v4/ipv6/new-ipv6-list
        新查询ipv6列表
        """
        return self.send(new_ipv6_list_request_param)

    def show_private_zone_record(self, show_private_zone_record_request_param):
        """
        /v4/private-zone-record/query
        内网 DNS 记录详情
        """
        return self.send(show_private_zone_record_request_param)

    def get_free_ip_hybrid_for_test(self, get_free_ip_hybrid_for_test_request_param):
        """
        /v4/eip/free-ip
        内部测试使用，查询可用eip网段地址
        """
        return self.send(get_free_ip_hybrid_for_test_request_param)

    def list_acl(self, list_acl_request_param):
        """
        /v4/acl/list
        查询acl列表
        """
        return self.send(list_acl_request_param)

    def create_endpoint_service(self, create_endpoint_service_request_param):
        """
        /v4/vpce/create-endpoint-service
        创建终端节点服务.当type为反向reverse时，自动创建不指定的中转ip。中转ip列表可产看详情信息。
        """
        return self.send(create_endpoint_service_request_param)

    def show_snat(self, show_snat_request_param):
        """
        /v4/vpc/show-snat
        获取SNAT规则详情
        """
        return self.send(show_snat_request_param)

    def port_replace_subnet(self, port_replace_subnet_request_param):
        """
        /v4/ports/change-private-ip
        网卡更换子网和IP地址
        """
        return self.send(port_replace_subnet_request_param)

    def show_eip(self, show_eip_request_param):
        """
        /v4/eip/show
        调用此接口可查看EIP详情。混合云返回参数缺失tags，description字段 非重要字段，暂不做调整
        """
        return self.send(show_eip_request_param)

    def renew_nat_gateway(self, renew_nat_gateway_request_param):
        """
        /v4/vpc/renew-nat-gateway
        续订NAT网关
        """
        return self.send(renew_nat_gateway_request_param)

    def create_vpc_peer_connection(self, create_vpc_peer_connection_request_param):
        """
        /v4/vpc/create-vpc-peer-connection
        - 创建非跨账户对等连接时，无需传acceptEmail字段。   
    - 创建跨账户对等连接时，虚拟私有云需要与发起方和接收方账户对应，接收方邮箱需要为真实用户邮箱。   
    - 适用于1.15.2版本以后
        """
        return self.send(create_vpc_peer_connection_request_param)

    def create_vpc_peering_route_hybrid(self, create_vpc_peering_route_hybrid_request_param):
        """
        /v4/vpc/vpcpeer/create-peering-route
        1.16.01版本以后支持该接口
        """
        return self.send(create_vpc_peering_route_hybrid_request_param)

    def delete_acl_rule(self, delete_acl_rule_request_param):
        """
        /v4/acl-rule/delete
        只有用户创建的ACL规则才能删除，ACL默认创建的ACL规则不允许删除   
    删除aclrules：支持批量删除   
    1.15版本：解决格式不对齐问题   
    
        """
        return self.send(delete_acl_rule_request_param)

    def new_private_zone_record_list(self, new_private_zone_record_list_request_param):
        """
        /v4/private-zone-record/new-list
        内网 DNS 记录列表
        """
        return self.send(new_private_zone_record_list_request_param)

    def create_flow_session(self, create_flow_session_request_param):
        """
        /v4/flowsession/create
        创建镜像会话
        """
        return self.send(create_flow_session_request_param)

    def get_free_ip_hybrid(self, get_free_ip_hybrid_request_param):
        """
        /v4/eip/get-free-ip
        查询资源池所有可用eip地址
        """
        return self.send(get_free_ip_hybrid_request_param)

    def list_mirror_flow_filter(self, list_mirror_flow_filter_request_param):
        """
        /v4/mirrorflow/list-filter
        流量镜像过滤条件列表
        """
        return self.send(list_mirror_flow_filter_request_param)

    def create_mirror_flow_filter(self, create_mirror_flow_filter_request_param):
        """
        /v4/mirrorflow/create-filter
        流量镜像过滤条件创建 ，返回参数未与公有云对齐。
        """
        return self.send(create_mirror_flow_filter_request_param)

    def create_endpoint_service_reverse_rule(self, create_endpoint_service_reverse_rule_request_param):
        """
        /v4/vpce/create-endpoint-service-reverse-rule
        创建终端节点服务中转规则(反向访问规则)   
    
        """
        return self.send(create_endpoint_service_reverse_rule_request_param)

    def bandwidth_renew(self, bandwidth_renew_request_param):
        """
        /v4/bandwidth/renew
        续订共享带宽 1.16.01版本以后支持该接口
        """
        return self.send(bandwidth_renew_request_param)

    def new_ports_list(self, new_ports_list_request_param):
        """
        /v4/ports/new-list
        新-查询弹性网卡列表
        """
        return self.send(new_ports_list_request_param)

    def show_security_group(self, show_security_group_request_param):
        """
        /v4/vpc/describe-security-group-attribute
        查询用户安全组详情。
        """
        return self.send(show_security_group_request_param)

    def show_mirror_flow_filter(self, show_mirror_flow_filter_request_param):
        """
        /v4/mirrorflow/show-filter
        流量镜像过滤条件详情
        """
        return self.send(show_mirror_flow_filter_request_param)

    def revoke_sg_engress_rule(self, revoke_sg_engress_rule_request_param):
        """
        /v4/vpc/revoke-security-group-ingress
        删除一条入方向安全组规则，撤销安全组出方向的权限设置。
        """
        return self.send(revoke_sg_engress_rule_request_param)

    def replace_subnet_acl(self, replace_subnet_acl_request_param):
        """
        /v4/vpc/replace-subnet-acl
        子网更换ACL
        """
        return self.send(replace_subnet_acl_request_param)

    def unassign_ipv6_from_port(self, unassign_ipv6_from_port_request_param):
        """
        /v4/ports/unassign-ipv6
        单个网卡解绑多个 IPv6 地址
        """
        return self.send(unassign_ipv6_from_port_request_param)

    def list_vpc_peer_connection(self, list_vpc_peer_connection_request_param):
        """
        /v4/vpc/list-vpc-peer-connection
        查询对等连接列表
        """
        return self.send(list_vpc_peer_connection_request_param)

    def get_sg_associate_vms_openapi(self, get_sg_associate_vms_openapi_request_param):
        """
        /v4/vpc/get-sg-associate-vms
        查询安全组关联的主机列表
        """
        return self.send(get_sg_associate_vms_openapi_request_param)

    def havip_unbind_for_paas(self, havip_unbind_for_paas_request_param):
        """
        /v4/vpc/havip/unbind-for-paas
        v2绑定为同步操作，若异常会直接报错   
    ## 接口约束   
    此接口只能在port绑定了havip并且port绑定了实例时使用，否则解绑时会返回失败。   
    当resourceType 为VM、PM时 instanceID不能为空，当类型为NETWORK 时floatingID 值不允许为空。
        """
        return self.send(havip_unbind_for_paas_request_param)

    def find_e_ip_name_hybrid(self, find_e_ip_name_hybrid_request_param):
        """
        /v4/eip/EIPGroup/findEIPName
        EIP网关列表查询
        """
        return self.send(find_e_ip_name_hybrid_request_param)

    def update_vpc_peer_connection_attribute(self, update_vpc_peer_connection_attribute_request_param):
        """
        /v4/vpc/modify-vpc-peer-connection
        修改对等连接
        """
        return self.send(update_vpc_peer_connection_attribute_request_param)

    def new_endpoint_services_list(self, new_endpoint_services_list_request_param):
        """
        /v4/vpce/new-list-endpoint-service
        查看终端节点服务列表
        """
        return self.send(new_endpoint_services_list_request_param)

    def group_unbind_vdc_open_api(self, group_unbind_vdc_open_api_request_param):
        """
        /v4/eipPool/unbindVdc
        ip地址组解绑vdc
        """
        return self.send(group_unbind_vdc_open_api_request_param)

    def create_endpoint_service_whitelist(self, create_endpoint_service_whitelist_request_param):
        """
        /v4/vpce/create-endpoint-service-whitelist
        添加终端节点服务白名单
        """
        return self.send(create_endpoint_service_whitelist_request_param)

    def create_out_filter_rule(self, create_out_filter_rule_request_param):
        """
        /v4/mirrorflow/create-filter-out-rule
        destPort与srcPort 起始端口必须小于结束端口 当协议为ALL/ICMP时，端口传'-'
        """
        return self.send(create_out_filter_rule_request_param)

    def query_create_v_p_c_e_price(self, query_create_v_p_c_e_price_request_param):
        """
        /v4/vpce/query-create-endpoint-price
        创建终端节点服务.当type为反向reverse时，自动创建不指定的中转ip。中转ip列表可产看详情信息。
        """
        return self.send(query_create_v_p_c_e_price_request_param)

    def list_acl_rule(self, list_acl_rule_request_param):
        """
        /v4/acl-rule/list
        查询acl rules列表
        """
        return self.send(list_acl_rule_request_param)

    def delete_bandwidth(self, delete_bandwidth_request_param):
        """
        /v4/bandwidth/delete
        删除共享带宽
        """
        return self.send(delete_bandwidth_request_param)

    def new_eip_list(self, new_eip_list_request_param):
        """
        /v4/eip/new-list
        查询指定地域已创建的EIP。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。混合云入参缺失ipType和eipType两个字段，非必填字段，暂不做调整
        """
        return self.send(new_eip_list_request_param)

    def list_security_groups(self, list_security_groups_request_param):
        """
        /v4/vpc/query-security-groups
        查询用户安全组列表
        """
        return self.send(list_security_groups_request_param)

    def iaas_network_eip_disassociate(self, iaas_network_eip_disassociate_request_param):
        """
        /v4/eip/disassociate
        调用此接口可将弹性公网IP从绑定的云产品上解绑。   
       
    ### 接口约束   
    解绑的云产品需与 EIP 在同一区域下。
        """
        return self.send(iaas_network_eip_disassociate_request_param)

    def vpc_delete(self, vpc_delete_request_param):
        """
        /v4/vpc/delete
        删除专有网络   
    删除专有网络之前，需要先删除所有子网，且需要删除子网内所有的云资源，包括ECS、弹性裸金属服务器、弹性负载均衡、NAT网关、高可用虚拟 IP 等，需要将子网内的占用IP的资源全部释放。
        """
        return self.send(vpc_delete_request_param)

    def query_security_groups_vdc(self, query_security_groups_vdc_request_param):
        """
        /v4/vpc/query-security-groups-vdc
        查询用户安全组列表。
        """
        return self.send(query_security_groups_vdc_request_param)

    def delete_dnat_entry(self, delete_dnat_entry_request_param):
        """
        /v4/vpc/delete-dnat-entry
        删除指定的DNAT条目
        """
        return self.send(delete_dnat_entry_request_param)

    def delete_endpoint_whitelist(self, delete_endpoint_whitelist_request_param):
        """
        /v4/vpce/delete-endpoint-whitelist
        删除终端节点白名单
        """
        return self.send(delete_endpoint_whitelist_request_param)

    def list_eip_vdc(self, list_eip_vdc_request_param):
        """
        /v4/eip/list-vdc
        查询指定地域已创建的EIP。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。混合云入参缺失ipType和eipType两个字段，非必填字段，暂不做调整
        """
        return self.send(list_eip_vdc_request_param)

    def list_endpoint_service_vdc(self, list_endpoint_service_vdc_request_param):
        """
        /v4/vpce/list-endpoint-service-vdc
        查看终端节点服务列表VDC
        """
        return self.send(list_endpoint_service_vdc_request_param)

    def bind_havip(self, bind_havip_request_param):
        """
        /v4/vpc/havip/bind
        v2绑定为同步操作，绑定成功为done的状态，若异常会直接报错
        """
        return self.send(bind_havip_request_param)

    def list_eip(self, list_eip_request_param):
        """
        /v4/eip/list
        查询指定地域已创建的EIP。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。混合云入参缺失ipType和eipType两个字段，非必填字段，暂不做调整
        """
        return self.send(list_eip_request_param)

    def list_endpoint_service_transit_ip_new(self, list_endpoint_service_transit_ip_new_request_param):
        """
        /v4/vpce/list-endpoint-service-transit-ip-new
        终端节点服务中转IP列表
        """
        return self.send(list_endpoint_service_transit_ip_new_request_param)

    def attach_eip_to_port(self, attach_eip_to_port_request_param):
        """
        /v4/eip/attach-port
        网卡需要绑定虚机才可以调用此接口做绑定。
        """
        return self.send(attach_eip_to_port_request_param)

    def add_endpoint_whitelist(self, add_endpoint_whitelist_request_param):
        """
        /v4/vpce/add-endpoint-whitelist
        添加终端节点白名单，acs类型资源池反向终端节点不支持白名单功能
        """
        return self.send(add_endpoint_whitelist_request_param)

    def delete_security_group(self, delete_security_group_request_param):
        """
        /v4/vpc/delete-security-group
        删除安全组。删除安全组之前，请确保安全组内不存在实例。
        """
        return self.send(delete_security_group_request_param)

    def update_security_group_attribute(self, update_security_group_attribute_request_param):
        """
        /v4/vpc/modify-security-group-attribute
        修改安全组
        """
        return self.send(update_security_group_attribute_request_param)

    def ipv4_gw_bind_route_table(self, ipv4_gw_bind_route_table_request_param):
        """
        /v4/vpc/ipv4-gw/add-route-table-binding
        IPv4网关绑定网关路由表 只支持4.0   
       
    ### 接口约束   
       
    1 个 ipv4 网关只能绑定一个路由表，每次调用该接口的效果是进行 update 操作。
        """
        return self.send(ipv4_gw_bind_route_table_request_param)

    def port_replace_v_p_c(self, port_replace_v_p_c_request_param):
        """
        /v4/ports/change-vpc
        网卡更换网络和IP地址
        """
        return self.send(port_replace_v_p_c_request_param)

    def unbind_havip(self, unbind_havip_request_param):
        """
        /v4/vpc/havip/unbind
        v2绑定为同步操作，若异常会直接报错   
       
    ### 接口约束   
    此接口只能在port绑定了havip并且port绑定了实例时使用，否则解绑时会返回失败。   
    当resourceType 为VM、PM时 instanceID不能为空，当类型为NETWORK 时floatingID 值不允许为空。
        """
        return self.send(unbind_havip_request_param)

    def new_eip_list_audit(self, new_eip_list_audit_request_param):
        """
        /v4/eip/new-list-audit
        查询指定地域已创建的EIP。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。混合云入参缺失ipType非必填字段，暂不做调整
        """
        return self.send(new_eip_list_audit_request_param)

    def list_nat_gateways(self, list_nat_gateways_request_param):
        """
        /v4/vpc/describe-nat-gateways
        查询NAT网关接口列表
        """
        return self.send(list_nat_gateways_request_param)

    def update_mirror_flow_filter_rule(self, update_mirror_flow_filter_rule_request_param):
        """
        /v4/mirrorflow/update-filter-rule
        destPort与srcPort 起始端口必须小于结束端口 当协议为ALL/ICMP时，端口传'-'
        """
        return self.send(update_mirror_flow_filter_rule_request_param)

    def disassociate_secondary_cidrs_from_vpc(self, disassociate_secondary_cidrs_from_vpc_request_param):
        """
        /v4/vpc/disassociate-secondary-cidrs
        VPC 解绑扩展网段
        """
        return self.send(disassociate_secondary_cidrs_from_vpc_request_param)

    def disassociate_private_zone_from_vpc(self, disassociate_private_zone_from_vpc_request_param):
        """
        /v4/private-zone/disassociate-vpc
        内网取消 DNS 关联 VPC
        """
        return self.send(disassociate_private_zone_from_vpc_request_param)

    def create_subnet_acl(self, create_subnet_acl_request_param):
        """
        /v4/vpc/create-subnet-acl
        创建acl，ACL的名称不能重名；4.0场景下只能创建后绑定对应的VPC
        """
        return self.send(create_subnet_acl_request_param)

    def batch_check_port_status(self, batch_check_port_status_request_param):
        """
        /v4/ports/check-status-batch
        网卡状态批量查询接口
        """
        return self.send(batch_check_port_status_request_param)

    def unassign_secondary_private_ips_from_port(self, unassign_secondary_private_ips_from_port_request_param):
        """
        /v4/ports/unassign-secondary-private-ips
        网卡解绑辅助私网IP
        """
        return self.send(unassign_secondary_private_ips_from_port_request_param)

    def list_flow_sessions(self, list_flow_sessions_request_param):
        """
        /v4/flowsession/list
        查看流量会话列表
        """
        return self.send(list_flow_sessions_request_param)

    def check_ip_available(self, check_ip_available_request_param):
        """
        /v4/vpc/check-ip-avaliable
        检查子网IP是否可用
        """
        return self.send(check_ip_available_request_param)

    def delete_private_zone_record(self, delete_private_zone_record_request_param):
        """
        /v4/private-zone-record/delete
        删除内网 DNS 记录(公有云不支持azName和projectID传参)
        """
        return self.send(delete_private_zone_record_request_param)

    def create_havip(self, create_havip_request_param):
        """
        /v4/vpc/havip/create
        创建高可用虚IP   
    混合云入参多projectID字段，非必填，传入正确的uuid形式的projectID会校验企业项目；clientToken字段不影响业务混合云补充为非必填。
        """
        return self.send(create_havip_request_param)

    def assign_secondary_private_ips_to_port(self, assign_secondary_private_ips_to_port_request_param):
        """
        /v4/ports/assign-secondary-private-ips
        网卡关联辅助私网IP   
       
    ### 接口约束   
    secondaryPrivateIps 和 secondaryPrivateIpCount 在同一次请求中，同时只能传入一个。
        """
        return self.send(assign_secondary_private_ips_to_port_request_param)

    def group_bind_vdc_open_api(self, group_bind_vdc_open_api_request_param):
        """
        /v4/eipPool/bindVdc
        ip地址组绑定vdc
        """
        return self.send(group_bind_vdc_open_api_request_param)

    def new_private_zone_list(self, new_private_zone_list_request_param):
        """
        /v4/private-zone/new-list
        内网 DNS 列表
        """
        return self.send(new_private_zone_list_request_param)

    def route_table_new_list(self, route_table_new_list_request_param):
        """
        /v4/vpc/route-table/new-list
        新查询路由表列表
        """
        return self.send(route_table_new_list_request_param)

    def create_eip(self, create_eip_request_param):
        """
        /v4/eip/create
        调用此接口可创建弹性公网IP（Elastic IP Address，简称EIP）。混合云目前入参缺失bandwidthID，demandBillingType这两个字段。非必填，暂不做调整   
    3.0provider只支持ext-net，区分资源类型做校验
        """
        return self.send(create_eip_request_param)

    def create_acl(self, create_acl_request_param):
        """
        /v4/acl/create
        创建acl，ACL的名称不能重名
        """
        return self.send(create_acl_request_param)

    def show_bandwidth(self, show_bandwidth_request_param):
        """
        /v4/bandwidth/describe
        查询共享带宽详情
        """
        return self.send(show_bandwidth_request_param)

    def list_subnet_used_ips(self, list_subnet_used_ips_request_param):
        """
        /v4/vpc/list-used-ips
        查看某个子网已使用IP
        """
        return self.send(list_subnet_used_ips_request_param)

    def delete_eip_address_group_open_api(self, delete_eip_address_group_open_api_request_param):
        """
        /v4/eipPool/delete
        删除ip地址组
        """
        return self.send(delete_eip_address_group_open_api_request_param)

    def start_flow_session(self, start_flow_session_request_param):
        """
        /v4/flowsession/start
        启动流量会话
        """
        return self.send(start_flow_session_request_param)

    def get_new_route_rule_list_openapi(self, get_new_route_rule_list_openapi_request_param):
        """
        /v4/vpc/route-table/new-list-rules
        新查询路由表规则列表   
    
        """
        return self.send(get_new_route_rule_list_openapi_request_param)

    def delete_snat_entry(self, delete_snat_entry_request_param):
        """
        /v4/vpc/delete-snat-entry
        删除SNAT规则
        """
        return self.send(delete_snat_entry_request_param)

    def s_nat_list_v1_openapi(self, s_nat_list_v1_openapi_request_param):
        """
        /v4/vpc/describe-snat-entries
        获取SNAT规则列表-对齐V1接口
        """
        return self.send(s_nat_list_v1_openapi_request_param)

    def associate_eip_to_bandwidth(self, associate_eip_to_bandwidth_request_param):
        """
        /v4/bandwidth/associate-eip
        ipv4调用方式：   
    1.通过/v4/eip/list_for_manage或者/v4/eip/list接口查询 eipId   
    2.通过/v4/bandwidth/list查询共享带宽列表获取共享带宽id   
    注意：eip需为按需计费模式的
        """
        return self.send(associate_eip_to_bandwidth_request_param)

    def list_private_zone_record(self, list_private_zone_record_request_param):
        """
        /v4/private-zone-record/list
        内网dns记录列表
        """
        return self.send(list_private_zone_record_request_param)

    def list_endpoint_service_transit_ip(self, list_endpoint_service_transit_ip_request_param):
        """
        /v4/vpce/list-endpoint-service-transit-ip
        终端节点服务中转IP列表
        """
        return self.send(list_endpoint_service_transit_ip_request_param)

    def query_renew_nat_price(self, query_renew_nat_price_request_param):
        """
        /v4/nat/query-renew-price
        续订nat网关 询价
        """
        return self.send(query_renew_nat_price_request_param)

    def show_private_zone(self, show_private_zone_request_param):
        """
        /v4/private-zone/query
        内网DNS详情
        """
        return self.send(show_private_zone_request_param)

    def show_nat_gateway(self, show_nat_gateway_request_param):
        """
        /v4/vpc/get-nat-gateway-attribute
        查询NAT网关详情
        """
        return self.send(show_nat_gateway_request_param)

    def get_bandwidth_new_list(self, get_bandwidth_new_list_request_param):
        """
        /v4/bandwidth/new-list
        查询共享带宽列表   
    eips里的eipID（弹性IP的ID） 暂不支持。
        """
        return self.send(get_bandwidth_new_list_request_param)

    def list_private_zone_vdc(self, list_private_zone_vdc_request_param):
        """
        /v4/private-zone/list-vdc
        内网DNS列表
        """
        return self.send(list_private_zone_vdc_request_param)

    def bandwidth_query_renew_price(self, bandwidth_query_renew_price_request_param):
        """
        /v4/bandwidth/query-renew-price
        共享带宽续订询价
        """
        return self.send(bandwidth_query_renew_price_request_param)

    def delete_subnet(self, delete_subnet_request_param):
        """
        /v4/vpc/delete-subnet
        删除子网   
    ## 接口约束   
    公有云没有azName字段，非必填字段，暂不做调整
        """
        return self.send(delete_subnet_request_param)

    def delete_ipv6_gateway(self, delete_ipv6_gateway_request_param):
        """
        /v4/vpc/delete-ipv6-gateway
        删除ipv6网关
        """
        return self.send(delete_ipv6_gateway_request_param)

    def delete_mirror_flow_filter(self, delete_mirror_flow_filter_request_param):
        """
        /v4/mirrorflow/delete-filter
        流量镜像过滤条件删除
        """
        return self.send(delete_mirror_flow_filter_request_param)

    def create_security_group_out_rules_openapi_new(self, create_security_group_out_rules_openapi_new_request_param):
        """
        /v4/vpc/create-security-group-egress-new
        创建安全组出向规则。
        """
        return self.send(create_security_group_out_rules_openapi_new_request_param)

    def accept_endpoint_apply(self, accept_endpoint_apply_request_param):
        """
        /v4/vpce/accept-endpoint-apply
        通过终端节点连接申请
        """
        return self.send(accept_endpoint_apply_request_param)

    def delete_endpoint_service_transit_ip(self, delete_endpoint_service_transit_ip_request_param):
        """
        /v4/vpce/delete-endpoint-service-transit-ip
        删除节点服务中转ip
        """
        return self.send(delete_endpoint_service_transit_ip_request_param)

    def delete_nat_gateway(self, delete_nat_gateway_request_param):
        """
        /v4/vpc/delete-nat-gateway
        删除NAT网关
        """
        return self.send(delete_nat_gateway_request_param)

    def update_subnet(self, update_subnet_request_param):
        """
        /v4/vpc/update-subnet
        修改子网的属性：名称、描述。
        """
        return self.send(update_subnet_request_param)

    def modify_endpoint_ip_version(self, modify_endpoint_ip_version_request_param):
        """
        /v4/vpce/modify-endpoint-ip-version
        修改终端节点IP地址类型
        """
        return self.send(modify_endpoint_ip_version_request_param)

    def list_bandwidth_vdc(self, list_bandwidth_vdc_request_param):
        """
        /v4/bandwidth/list-vdc
        返回体中的creator已废弃勿用，值为空
        """
        return self.send(list_bandwidth_vdc_request_param)

    def show_ipv6_bandwidth_v1(self, show_ipv6_bandwidth_v1_request_param):
        """
        /v4/ipv6_bandwidth/v1_show
        查看 IPv6 带宽详情
        """
        return self.send(show_ipv6_bandwidth_v1_request_param)

    def modify_sg_engress_rule(self, modify_sg_engress_rule_request_param):
        """
        /v4/vpc/modify-security-group-egress
        修改安全组出方向规则的描述信息，该接口只能修改出方向描述信息。
        """
        return self.send(modify_sg_engress_rule_request_param)

    def update_bandwidth_attribute(self, update_bandwidth_attribute_request_param):
        """
        /v4/bandwidth/modify-attribute
        修改共享带宽的名称描述
        """
        return self.send(update_bandwidth_attribute_request_param)

    def change_eip_name(self, change_eip_name_request_param):
        """
        /v4/eip/change-name
        修改EIP名字。**注意**：EIP的名称不允许重名！
        """
        return self.send(change_eip_name_request_param)

    def check_name_openapi(self, check_name_openapi_request_param):
        """
        /v4/private-zone/check-name
        修改内网DNS
        """
        return self.send(check_name_openapi_request_param)

    def eip_list_for_manage(self, eip_list_for_manage_request_param):
        """
        /v4/eip/list_for_manage
        获取弹性IP列表管理用。调用此接口可查询指定地域已创建的弹性公网IP（Elastic IP Address，简称EIP）。
        """
        return self.send(eip_list_for_manage_request_param)

    def ipv4_gw_unbind_route_table(self, ipv4_gw_unbind_route_table_request_param):
        """
        /v4/vpc/ipv4-gw/remove-route-table-binding
        IPv4网关解绑网关路由表。clientToken私有云文档标记未非必填参数，可传但是不进行校验 只支持4.0
        """
        return self.send(ipv4_gw_unbind_route_table_request_param)

    def show_ipv4_gw(self, show_ipv4_gw_request_param):
        """
        /v4/vpc/ipv4-gw/show
        查看IPv4网关详情 只支持4.0   
    
        """
        return self.send(show_ipv4_gw_request_param)

    def revoke_sg_ingress_rule(self, revoke_sg_ingress_rule_request_param):
        """
        /v4/vpc/revoke-security-group-egress
        删除一条出方向安全组规则，撤销安全组出方向的权限设置。公有云入参缺clientToken字段，必填。暂不修改
        """
        return self.send(revoke_sg_ingress_rule_request_param)

    def sg_batch_attach_ports(self, sg_batch_attach_ports_request_param):
        """
        /v4/vpc/batch-attach-security-group-ports
        安全组批量绑定网卡。clientToken公有云必填字段，字段不影响接口功能，混合云不必填当作对齐。
        """
        return self.send(sg_batch_attach_ports_request_param)

    def query_modify_nat_price(self, query_modify_nat_price_request_param):
        """
        /v4/nat/query-modify-price
        变配nat网关 询价 
        """
        return self.send(query_modify_nat_price_request_param)

    def leave_security_group(self, leave_security_group_request_param):
        """
        /v4/vpc/leave-security-group
        解绑安全组。当主机只有一个安全组绑定着的时候，该安全组不支持解绑
        """
        return self.send(leave_security_group_request_param)

    def delete_port(self, delete_port_request_param):
        """
        /v4/ports/delete
        删除弹性网卡
        """
        return self.send(delete_port_request_param)

    def iaas_network_route_table_delete(self, iaas_network_route_table_delete_request_param):
        """
        /v4/vpc/route-table/delete
        删除路由表，其中自定义路由表可以删除，默认路由表随 VPC 删除时一起删除。
        """
        return self.send(iaas_network_route_table_delete_request_param)

    def share_vpc_to_project_openapi(self, share_vpc_to_project_openapi_request_param):
        """
        /v4/vpc/share-to-project
        共享vpc到企业项目
        """
        return self.send(share_vpc_to_project_openapi_request_param)

    def query_vpc_peering_route(self, query_vpc_peering_route_request_param):
        """
        /v4/vpc/vpcpeer/query-peering-route
        1.16.01版本以后支持该接口
        """
        return self.send(query_vpc_peering_route_request_param)

    def get_vpc_shared_projects_openapi(self, get_vpc_shared_projects_openapi_request_param):
        """
        /v4/vpc/shared-project-list
        查询vpc共享的企业项目列表
        """
        return self.send(get_vpc_shared_projects_openapi_request_param)

    def update_snat_entry_attribute(self, update_snat_entry_attribute_request_param):
        """
        /v4/vpc/modify-snat-entry
        修改SNAT规则
        """
        return self.send(update_snat_entry_attribute_request_param)

    def reject_vpc_peer(self, reject_vpc_peer_request_param):
        """
        /v4/vpc/vpcpeer/reject-request
        拒绝建立对等链接
        """
        return self.send(reject_vpc_peer_request_param)

    def port_create(self, port_create_request_param):
        """
        /v4/ports/create
        创建弹性网卡
        """
        return self.send(port_create_request_param)

    def create_single_route_rule_openapi(self, create_single_route_rule_openapi_request_param):
        """
        /v4/vpc/route-table/create-rule
        创建单条路由表规则   
    
        """
        return self.send(create_single_route_rule_openapi_request_param)

    def associate_secondary_cidrs_to_vpc(self, associate_secondary_cidrs_to_vpc_request_param):
        """
        /v4/vpc/associate-secondary-cidrs
        VPC 绑定扩展网段
        """
        return self.send(associate_secondary_cidrs_to_vpc_request_param)

    def delete_endpoint(self, delete_endpoint_request_param):
        """
        /v4/vpce/delete-endpoint
        删除终端节点
        """
        return self.send(delete_endpoint_request_param)

    def update_private_zone_attribute(self, update_private_zone_attribute_request_param):
        """
        /v4/private-zone/update
        修改内网DNS
        """
        return self.send(update_private_zone_attribute_request_param)

    def delete_private_zone(self, delete_private_zone_request_param):
        """
        /v4/private-zone/delete
        删除内网 DNS。clientToken非必填，并且此字段在私有云不具有实际意义
        """
        return self.send(delete_private_zone_request_param)

    def get_eip_filling_status(self, get_eip_filling_status_request_param):
        """
        /v4/eip/get-filing-status
        查询弹性ip是否开启端口备案
        """
        return self.send(get_eip_filling_status_request_param)

    def list_subnet(self, list_subnet_request_param):
        """
        /v4/vpc/list-subnet
        查询用户专有网络下子网列表
        """
        return self.send(list_subnet_request_param)

    def update_port(self, update_port_request_param):
        """
        /v4/ports/update
        修改网卡属性
        """
        return self.send(update_port_request_param)

    def vpc_create(self, vpc_create_request_param):
        """
        /v4/vpc/create
        创建一个专有网络VPC。   
       
    ### 接口约束   
       
    调用该接口创建 VPC 时，请注意：   
       
    - 一个 VPC 只能指定一个网段。   
       
    - VPC 创建后无法修改网段，但可以添加附加 IPv4 网段。   
       
    - 创建 VPC 后，会自动创建一个路由器和一个路由表。   
       
    - 创建VPC时若开启ipv6，默认创建ipv6网关   
       
    - enableIpv6参数仅支持4.0资源池
        """
        return self.send(vpc_create_request_param)

    def modify_eip_spec(self, modify_eip_spec_request_param):
        """
        /v4/eip/modify-spec
        修改EIP带宽，相当于变配。
        """
        return self.send(modify_eip_spec_request_param)

    def get_multicast_domain_list_openapi(self, get_multicast_domain_list_openapi_request_param):
        """
        /v4/multicast/list-domain
        查询组播域列表
        """
        return self.send(get_multicast_domain_list_openapi_request_param)

    def delete_ipv6_bandwidth(self, delete_ipv6_bandwidth_request_param):
        """
        /v4/ipv6_bandwidth/delete
        删除IPV6带宽
        """
        return self.send(delete_ipv6_bandwidth_request_param)

    def query_modify_ipv6_bandwidth_price(self, query_modify_ipv6_bandwidth_price_request_param):
        """
        /v4/ipv6_bandwidth/query-modify-price
        IPv6带宽变配询价
        """
        return self.send(query_modify_ipv6_bandwidth_price_request_param)

    def list_mirror_flow_filter_rule(self, list_mirror_flow_filter_rule_request_param):
        """
        /v4/mirrorflow/list-filter-rule
        查看过滤规则列表
        """
        return self.send(list_mirror_flow_filter_rule_request_param)

    def check_cname_openapi(self, check_cname_openapi_request_param):
        """
        /v4/private-zone-record/check-cname
        检查CNAME记录集合法性
        """
        return self.send(check_cname_openapi_request_param)

    def query_subnet(self, query_subnet_request_param):
        """
        /v4/vpc/query-subnet
        查询用户专有网络 VPC 下子网详情。   
    ## 接口约束   
    * 公有云没有azName字段，非必填字段，暂不做调整
        """
        return self.send(query_subnet_request_param)

    def query_modify_eip_price(self, query_modify_eip_price_request_param):
        """
        /v4/eip/query-modify-price
        调用此接口可查询变配弹性公网IP的价格，可以直接使用变配参数询价，对非询价所需字段不做校验，只做透传，混合云目前入参缺失bandwidthID，这个字段。非必填，暂不做调整   
    价格单位：按带宽 元/小时，按流量 元/GB，包年包月 元/月
        """
        return self.send(query_modify_eip_price_request_param)

    def update_dnat_entry_attribute(self, update_dnat_entry_attribute_request_param):
        """
        /v4/vpc/modify-dnat-entry
        修改DNAT规则
        """
        return self.send(update_dnat_entry_attribute_request_param)

    def detach_port(self, detach_port_request_param):
        """
        /v4/ports/detach
        网卡解绑实例   
    ### 接口约束   
    当前仅支持虚拟机
        """
        return self.send(detach_port_request_param)

    def update_eip_address_group_open_api(self, update_eip_address_group_open_api_request_param):
        """
        /v4/eipPool
        修改ip地址组
        """
        return self.send(update_eip_address_group_open_api_request_param)

    def query_create_ipv6_bandwidth_price(self, query_create_ipv6_bandwidth_price_request_param):
        """
        /v4/ipv6_bandwidth/query-create-price
        非必需询价字段不做校验，只透传
        """
        return self.send(query_create_ipv6_bandwidth_price_request_param)

    def create_subnet(self, create_subnet_request_param):
        """
        /v4/vpc/create-subnet
        创建子网。   
       
    ## 接口约束   
       
    调用该接口创建 Subnet 时，请注意：   
       
    - 一个 Subnet 只能指定一个网段，创建后无法修改网段。   
    - 共享vpc在共享企业项目下创建子网时需要指定共享企业项目的路由表   
       
    ## 接口差别   
    混合云入参多azName，非必填字段；缺clientToken字段，必填字段，字段不影响接口功能，混合云不必填当作对齐。
        """
        return self.send(create_subnet_request_param)

    def delete_endpoint_service_rule(self, delete_endpoint_service_rule_request_param):
        """
        /v4/vpce/delete-endpoint-service-rule
        终端节点服务规则删除接口
        """
        return self.send(delete_endpoint_service_rule_request_param)

    def dns_bind_label_openapi(self, dns_bind_label_openapi_request_param):
        """
        /v4/private-zone/bind-label
        DNS绑定标签
        """
        return self.send(dns_bind_label_openapi_request_param)

    def list_port(self, list_port_request_param):
        """
        /v4/ports/list
        查询网卡列表
        """
        return self.send(list_port_request_param)

    def batch_join_security_group(self, batch_join_security_group_request_param):
        """
        /v4/vpc/batch-join-security-group
        批量绑定安全组 
        """
        return self.send(batch_join_security_group_request_param)

    def nat_gateway_add_subnet(self, nat_gateway_add_subnet_request_param):
        """
        /v4/vpc/nat-gateway-add-subnet
        修改NAT网关
        """
        return self.send(nat_gateway_add_subnet_request_param)

    def add_ipv6_to_ipv6_bandwidth(self, add_ipv6_to_ipv6_bandwidth_request_param):
        """
        /v4/ipv6_bandwidth/add-ipv6
        IPv6带宽添加IPv6地址
        """
        return self.send(add_ipv6_to_ipv6_bandwidth_request_param)

    def list_endpoint_service_whitelist(self, list_endpoint_service_whitelist_request_param):
        """
        /v4/vpce/list-endpoint-service-whitelist
         查询终端节点服务白名单
        """
        return self.send(list_endpoint_service_whitelist_request_param)

    def disassociate_subnet_acl(self, disassociate_subnet_acl_request_param):
        """
        /v4/vpc/disassociate-subnet-acl
        子网解绑ACL
        """
        return self.send(disassociate_subnet_acl_request_param)

    def bandwidth_query_create_price(self, bandwidth_query_create_price_request_param):
        """
        /v4/bandwidth/query-create-price
        共享带宽创建询价
        """
        return self.send(bandwidth_query_create_price_request_param)

    def create_eip_with_ip_address(self, create_eip_with_ip_address_request_param):
        """
        /v4/eip/create-with-ipaddress
        创建指定地址的EIP，EIP的名称不允许重名！
        """
        return self.send(create_eip_with_ip_address_request_param)

    def update_endpoint_service_connections(self, update_endpoint_service_connections_request_param):
        """
        /v4/vpce/update-endpoint-service-connections
        终端节点服务连接修改
        """
        return self.send(update_endpoint_service_connections_request_param)

    def associate_private_zone_to_vpc(self, associate_private_zone_to_vpc_request_param):
        """
        /v4/private-zone/associate-vpc
        内网 DNS 关联 VPC
        """
        return self.send(associate_private_zone_to_vpc_request_param)

    def list_bandwidth(self, list_bandwidth_request_param):
        """
        /v4/bandwidth/list
        返回体中的creator已废弃勿用，值为空
        """
        return self.send(list_bandwidth_request_param)

    def delete_vpc_peer_connection(self, delete_vpc_peer_connection_request_param):
        """
        /v4/vpc/delete-vpc-peer-connection
        删除对等连接   
    不支持批量删除
        """
        return self.send(delete_vpc_peer_connection_request_param)

    def list_subnet_vdc(self, list_subnet_vdc_request_param):
        """
        /v4/vpc/list-subnet-vdc
        查询用户专有网络下子网列表
        """
        return self.send(list_subnet_vdc_request_param)

    def update_ipv6_bandwidth_openapi(self, update_ipv6_bandwidth_openapi_request_param):
        """
        /v4/ipv6_bandwidth/update
        修改ipv6带宽名称
        """
        return self.send(update_ipv6_bandwidth_openapi_request_param)

    def create_private_zone_record(self, create_private_zone_record_request_param):
        """
        /v4/private-zone-record/create
        创建内网 DNS 记录(公有云传参没有azName和projectID字段)
        """
        return self.send(create_private_zone_record_request_param)

    def show_flow_session(self, show_flow_session_request_param):
        """
        /v4/flowsession/show
        查看流量会话详情
        """
        return self.send(show_flow_session_request_param)

    def delete_eip(self, delete_eip_request_param):
        """
        /v4/eip/delete
        调用此接口可删除 EIP。   
       
    ### 接口约束   
    待删除的EIP需未绑定任何云产品实例。   
    涉及订单计费，当前用户只能操作归属自己的EIP资源，不可跨VDC操作
        """
        return self.send(delete_eip_request_param)

    def attach_port_bm(self, attach_port_bm_request_param):
        """
        /v4/eip/attach-port-bm
        EIP绑定裸金属网卡
        """
        return self.send(attach_port_bm_request_param)

    def api_order_resize_nat(self, api_order_resize_nat_request_param):
        """
        /v4/vpc/modify-nat-gateway-spec
        变配NAT网关走订单
        """
        return self.send(api_order_resize_nat_request_param)

    def v4_vpc_havip_bind_for_pass(self, v4_vpc_havip_bind_for_pass_request_param):
        """
        /v4/vpc/havip/bind-for-pass
        v2绑定为同步操作，绑定成功为done的状态，若异常会直接报错
        """
        return self.send(v4_vpc_havip_bind_for_pass_request_param)

    def modify_private_zone_record_desc(self, modify_private_zone_record_desc_request_param):
        """
        /v4/private-zone-record/modify-desc
        修改内网 DNS 记录描述信息
        """
        return self.send(modify_private_zone_record_desc_request_param)
