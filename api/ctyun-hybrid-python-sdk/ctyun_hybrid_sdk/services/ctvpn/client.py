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


class CtvpnClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctvpn-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtvpnClient, self).__init__(credential, config, 'ctvpn', '0.1.0', logger, signer)

    def ctvpn_connection_update(self, ctvpn_connection_update_request_param):
        """
        /v4/vpn/connection/update
        VPN连接修改
        """
        return self.send(ctvpn_connection_update_request_param)

    def ctvpn_gateway_upgrade_query_price(self, ctvpn_gateway_upgrade_query_price_request_param):
        """
        /v4/vpn/gateway/query-price-upgrade
        VPN网关升配询价
        """
        return self.send(ctvpn_gateway_upgrade_query_price_request_param)

    def ctvpn_gateway_list(self, ctvpn_gateway_list_request_param):
        """
        /v4/vpn/gateway/list
        GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
        """
        return self.send(ctvpn_gateway_list_request_param)

    def ctvpn_user_gateway_add(self, ctvpn_user_gateway_add_request_param):
        """
        /v4/vpn/user-gateway/add
        用户网关创建
        """
        return self.send(ctvpn_user_gateway_add_request_param)

    def ctvpn_gateway_new_query_price(self, ctvpn_gateway_new_query_price_request_param):
        """
        /v4/vpn/gateway/query-price-new
        VPN网关订购询价
        """
        return self.send(ctvpn_gateway_new_query_price_request_param)

    def ctvpn_user_gateway_delete(self, ctvpn_user_gateway_delete_request_param):
        """
        /v4/vpn/user-gateway/delete
        用户网关删除
        """
        return self.send(ctvpn_user_gateway_delete_request_param)

    def ctvpn_connection_delete(self, ctvpn_connection_delete_request_param):
        """
        /v4/vpn/connection/delete
        VPN连接删除
        """
        return self.send(ctvpn_connection_delete_request_param)

    def ctvpn_gateway_new(self, ctvpn_gateway_new_request_param):
        """
        /v4/vpn/gateway/new
        VPN网关订购
        """
        return self.send(ctvpn_gateway_new_request_param)

    def ctvpn_gateway_renew_query_price(self, ctvpn_gateway_renew_query_price_request_param):
        """
        /v4/vpn/gateway/query-price-renew
        VPN网关续订询价
        """
        return self.send(ctvpn_gateway_renew_query_price_request_param)

    def ctvpn_gateway_upgrade(self, ctvpn_gateway_upgrade_request_param):
        """
        /v4/vpn/gateway/upgrade
        VPN网关升配
        """
        return self.send(ctvpn_gateway_upgrade_request_param)

    def ctvpn_connection_add(self, ctvpn_connection_add_request_param):
        """
        /v4/vpn/connection/add
        VPN连接创建
        """
        return self.send(ctvpn_connection_add_request_param)

    def ctvpn_connection_list(self, ctvpn_connection_list_request_param):
        """
        /v4/vpn/connection/list
        GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
        """
        return self.send(ctvpn_connection_list_request_param)

    def ipsec_vpn_connection_query(self, ipsec_vpn_connection_query_request_param):
        """
        /v4/vpn/ipsec-vpn-connection/list
        GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
        """
        return self.send(ipsec_vpn_connection_query_request_param)

    def ctvpn_user_gateway_update(self, ctvpn_user_gateway_update_request_param):
        """
        /v4/vpn/user-gateway/update
        用户网关修改
        """
        return self.send(ctvpn_user_gateway_update_request_param)

    def ctvpn_gateway_renew(self, ctvpn_gateway_renew_request_param):
        """
        /v4/vpn/gateway/renew
        VPN网关续订
        """
        return self.send(ctvpn_gateway_renew_request_param)

    def ctvpn_gateway_refund(self, ctvpn_gateway_refund_request_param):
        """
        /v4/vpn/gateway/refund
        VPN网关退订
        """
        return self.send(ctvpn_gateway_refund_request_param)

    def ctvpn_user_gateway_list(self, ctvpn_user_gateway_list_request_param):
        """
        /v4/vpn/user-gateway/list
        GET请求规范格式是用query，body格式为广域云网历史遗留问题，确认中
        """
        return self.send(ctvpn_user_gateway_list_request_param)

    def ctvpn_gateway_update(self, ctvpn_gateway_update_request_param):
        """
        /v4/vpn/gateway/update
        VPN网关修改
        """
        return self.send(ctvpn_gateway_update_request_param)

    def ctvpn_connection_policy(self, ctvpn_connection_policy_request_param):
        """
        /v4/vpn/connection/policy
        VPN连接策略查询
        """
        return self.send(ctvpn_connection_policy_request_param)
