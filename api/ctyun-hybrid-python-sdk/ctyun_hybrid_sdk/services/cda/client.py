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


class CdaClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('cda-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CdaClient, self).__init__(credential, config, 'cda', '0.1.0', logger, signer)

    def cda_static_route_list(self, cda_static_route_list_request_param):
        """
        /v4/cda/static-route/list
        请求参数请用JSON格式
        """
        return self.send(cda_static_route_list_request_param)

    def cda_static_route_add(self, cda_static_route_add_request_param):
        """
        /v4/cda/static-route/add
        专线网关需要先绑定物理专线且没有绑定动态路由
        """
        return self.send(cda_static_route_add_request_param)

    def cda_gateway_count(self, cda_gateway_count_request_param):
        """
        /v4/cda/gateway/count
        注：入参需要使用JSON格式
        """
        return self.send(cda_gateway_count_request_param)

    def cda_static_route_update(self, cda_static_route_update_request_param):
        """
        /v4/cda/static-route/update
        底层不支持修改ipVersion
        """
        return self.send(cda_static_route_update_request_param)

    def get_cda_or_vpn_gateway_openapi(self, get_cda_or_vpn_gateway_openapi_request_param):
        """
        /v4/l2gw/gw_query
        查询云专线或VPN网关
        """
        return self.send(get_cda_or_vpn_gateway_openapi_request_param)

    def delete_l2_connection_openapi(self, delete_l2_connection_openapi_request_param):
        """
        /v4/l2gw_connection/delete
        删除二层连接
        """
        return self.send(delete_l2_connection_openapi_request_param)

    def cda_physical_line_list(self, cda_physical_line_list_request_param):
        """
        /v4/cda/physical-line/list
        请求参数需要使用JSON格式
        """
        return self.send(cda_physical_line_list_request_param)

    def l2_gateway_query_renew_price_openapi(self, l2_gateway_query_renew_price_openapi_request_param):
        """
        /v4/l2gw/query-renew-price
        企业交换机续订询价
        """
        return self.send(l2_gateway_query_renew_price_openapi_request_param)

    def check_tunnel_openapi(self, check_tunnel_openapi_request_param):
        """
        /v4/l2gw_connection/tunnel_check
        校验tunnel（暂不使用）
        """
        return self.send(check_tunnel_openapi_request_param)

    def cda_physical_line_update(self, cda_physical_line_update_request_param):
        """
        /v4/cda/physical-line/update
        物理专线未绑定专线网关时，可修改本端对端互联ip和专线类型   
    如单栈变双栈，双栈变单栈等.如果物理专线已经绑定了专线网关，只能修改带宽和物理专线名称。
        """
        return self.send(cda_physical_line_update_request_param)

    def cloudvpn_user_add(self, cloudvpn_user_add_request_param):
        """
        /v4/cloudvpn/user/add
        客户信息增加
        """
        return self.send(cloudvpn_user_add_request_param)

    def cda_bgp_route_add(self, cda_bgp_route_add_request_param):
        """
        /v4/cda/bgp-route/add
         BGP路由添加
        """
        return self.send(cda_bgp_route_add_request_param)

    def cloudvpn_user_query(self, cloudvpn_user_query_request_param):
        """
        /v4/cloudvpn/user/query
        客户信息查询
        """
        return self.send(cloudvpn_user_query_request_param)

    def cda_physical_line_count(self, cda_physical_line_count_request_param):
        """
        /v4/cda/physical-line/count
        请求参数请用JSON格式
        """
        return self.send(cda_physical_line_count_request_param)

    def cda_physical_line_add(self, cda_physical_line_add_request_param):
        """
        /v4/cda/physical-line/add
        物理专线创建
        """
        return self.send(cda_physical_line_add_request_param)

    def update_l2_gateway_openapi(self, update_l2_gateway_openapi_request_param):
        """
        /v4/l2gw/update
        更新企业交换机
        """
        return self.send(update_l2_gateway_openapi_request_param)

    def cda_switch_switch_ports(self, cda_switch_switch_ports_request_param):
        """
        /v4/cda/switch/switch-ports
        交换机端口信息查询
        """
        return self.send(cda_switch_switch_ports_request_param)

    def cda_bgp_route_delete(self, cda_bgp_route_delete_request_param):
        """
        /v4/cda/bgp-route/delete
         BGP路由删除
        """
        return self.send(cda_bgp_route_delete_request_param)

    def update_l2_connection_openapi(self, update_l2_connection_openapi_request_param):
        """
        /v4/l2gw_connection/update
        更新二层连接
        """
        return self.send(update_l2_connection_openapi_request_param)

    def delete_l2_gateway_openapi(self, delete_l2_gateway_openapi_request_param):
        """
        /v4/l2gw/delete
        删除企业交换机
        """
        return self.send(delete_l2_gateway_openapi_request_param)

    def cda_shared_physical_line_list(self, cda_shared_physical_line_list_request_param):
        """
        /v4/cda/shared-physical-line/list
        请求参数需要使用JSON格式
        """
        return self.send(cda_shared_physical_line_list_request_param)

    def get_l2_gateway_list_openapi(self, get_l2_gateway_list_openapi_request_param):
        """
        /v4/l2gw/query
        查询企业交换机列表
        """
        return self.send(get_l2_gateway_list_openapi_request_param)

    def cda_bgp_route_list(self, cda_bgp_route_list_request_param):
        """
        /v4/cda/bgp-route/list
        请求参数请用JSON格式
        """
        return self.send(cda_bgp_route_list_request_param)

    def cda_bgp_route_update(self, cda_bgp_route_update_request_param):
        """
        /v4/cda/bgp-route/update
        底层不支持修改ipVersion
        """
        return self.send(cda_bgp_route_update_request_param)

    def cda_vpc_update(self, cda_vpc_update_request_param):
        """
        /v4/cda/vpc/update
        仅支持修改子网
        """
        return self.send(cda_vpc_update_request_param)

    def l2_gateway_renew_openapi(self, l2_gateway_renew_openapi_request_param):
        """
        /v4/l2gw/renew
        企业交换机续订
        """
        return self.send(l2_gateway_renew_openapi_request_param)

    def cda_static_route_delete(self, cda_static_route_delete_request_param):
        """
        /v4/cda/static-route/delete
        静态路由删除
        """
        return self.send(cda_static_route_delete_request_param)

    def create_l2_connection_openapi(self, create_l2_connection_openapi_request_param):
        """
        /v4/l2gw_connection/create
        创建二层连接
        """
        return self.send(create_l2_connection_openapi_request_param)

    def cda_gateway_list(self, cda_gateway_list_request_param):
        """
        /v4/cda/gateway/list
        请求参数需要使用JSON格式
        """
        return self.send(cda_gateway_list_request_param)

    def l2_gateway_query_new_price_openapi(self, l2_gateway_query_new_price_openapi_request_param):
        """
        /v4/l2gw/query-create-price
        企业交换机订购询价
        """
        return self.send(l2_gateway_query_new_price_openapi_request_param)

    def cda_physical_line_access_point_list(self, cda_physical_line_access_point_list_request_param):
        """
        /v4/cda/physical-line/access-point-list
        物理专线接入点查询,请求参数请用JSON格式
        """
        return self.send(cda_physical_line_access_point_list_request_param)

    def cda_switch_delete(self, cda_switch_delete_request_param):
        """
        /v4/cda/switch/delete
        专线交换机删除
        """
        return self.send(cda_switch_delete_request_param)

    def cda_vpc_count(self, cda_vpc_count_request_param):
        """
        /v4/cda/vpc/count
        请求参数需要使用JSON格式
        """
        return self.send(cda_vpc_count_request_param)

    def cda_gateway_add(self, cda_gateway_add_request_param):
        """
        /v4/cda/gateway/add
        专线网关创建
        """
        return self.send(cda_gateway_add_request_param)

    def get_l2_connection_list_openapi(self, get_l2_connection_list_openapi_request_param):
        """
        /v4/l2gw_connection/query
        查询二层连接列表
        """
        return self.send(get_l2_connection_list_openapi_request_param)

    def cda_switch_add(self, cda_switch_add_request_param):
        """
        /v4/cda/switch/add
        专线交换机创建
        """
        return self.send(cda_switch_add_request_param)

    def create_l2_gateway_openapi(self, create_l2_gateway_openapi_request_param):
        """
        /v4/l2gw/create
        创建企业交换机
        """
        return self.send(create_l2_gateway_openapi_request_param)

    def cloudvpn_user_delete(self, cloudvpn_user_delete_request_param):
        """
        /v4/cloudvpn/user/delete
        客户信息删除
        """
        return self.send(cloudvpn_user_delete_request_param)

    def cda_gateway_delete(self, cda_gateway_delete_request_param):
        """
        /v4/cda/gateway/delete
        入参示例:   
    <span class="colour" style="color:rgb(0, 0, 0)">{</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"regionID"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"nm8",</span>   
    <span class="colour" style="color:rgb(163, 21, 21)">"gatewayName"</span><span class="colour" style="color:rgb(0, 0, 0)">: </span><span class="colour" style="color:rgb(4, 81, 165)">"d5hrh7wcbzgx1107testzz"</span>   
    <span class="colour" style="color:rgb(0, 0, 0)">}</span>   
       
    <span class="colour" style="color:rgb(0, 0, 0)">返回参数示例：</span>   
    <span class="colour" style="color:rgb(0, 0, 0)"></span>{   
        "returnObj": {   
            "data": null,   
            "errorMsg": null,   
            "result": "1"   
        },   
        "statusCode": 800   
    }<span class="colour" style="color:rgb(0, 0, 0)"></span>
        """
        return self.send(cda_gateway_delete_request_param)

    def cda_vpc_list(self, cda_vpc_list_request_param):
        """
        /v4/cda/vpc/list
        专线网关VPC查询,请求参数需要使用JSON格式
        """
        return self.send(cda_vpc_list_request_param)

    def cda_physical_line_delete(self, cda_physical_line_delete_request_param):
        """
        /v4/cda/physical-line/delete
        物理专线删除
        """
        return self.send(cda_physical_line_delete_request_param)

    def cda_physical_line_bind(self, cda_physical_line_bind_request_param):
        """
        /v4/cda/physical-line/bind
        专线网关绑定物理专线
        """
        return self.send(cda_physical_line_bind_request_param)

    def cda_physical_line_unbind(self, cda_physical_line_unbind_request_param):
        """
        /v4/cda/physical-line/unbind
        专线网关解绑物理专线
        """
        return self.send(cda_physical_line_unbind_request_param)

    def cda_switch_list(self, cda_switch_list_request_param):
        """
        /v4/cda/switch/list
        专线交换机查询
        """
        return self.send(cda_switch_list_request_param)

    def cloudvpn_user_update(self, cloudvpn_user_update_request_param):
        """
        /v4/cloudvpn/user/update
        客户信息修改
        """
        return self.send(cloudvpn_user_update_request_param)

    def cda_gateway_physical_line_list(self, cda_gateway_physical_line_list_request_param):
        """
        /v4/cda/gateway/physical-line-list
        请求参数需要使用JSON格式
        """
        return self.send(cda_gateway_physical_line_list_request_param)

    def cda_vpc_add(self, cda_vpc_add_request_param):
        """
        /v4/cda/vpc/add
        专线网关添加VPC
        """
        return self.send(cda_vpc_add_request_param)

    def cda_vpc_delete(self, cda_vpc_delete_request_param):
        """
        /v4/cda/vpc/delete
        专线网关删除VPC
        """
        return self.send(cda_vpc_delete_request_param)
