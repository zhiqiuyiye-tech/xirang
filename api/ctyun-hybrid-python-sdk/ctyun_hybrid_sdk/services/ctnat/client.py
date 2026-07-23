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


class CtnatClient(CTYunClient):

    def __init__(self, credential, config=None, logger=None, signer=None):
        if config is None:
            config = Config('ctnat-global.ctapi.ctyun.local', scheme="http")
        if logger is None:
            logger = get_default_logger()
        super(CtnatClient, self).__init__(credential, config, 'ctnat', '0.1.0', logger, signer)

    def renew_private_nat_price(self, renew_private_nat_price_request_param):
        """
        /v4/privatenat/query-renew-price
        续订NAT网关询价
        """
        return self.send(renew_private_nat_price_request_param)

    def private_nat_api_list(self, private_nat_api_list_request_param):
        """
        /v4/privatenat/list
        查询私网NAT网关接口列表
        """
        return self.send(private_nat_api_list_request_param)

    def create_private_snat_api(self, create_private_snat_api_request_param):
        """
        /v4/privatenat/create-snat
        创建私网SNAT规则。snatIps需填入中转IP的地址。sourceSubnetID和sourceCIDR必须传一个，都传以子网ID为准。
        """
        return self.send(create_private_snat_api_request_param)

    def renew_private_nat_api_order(self, renew_private_nat_api_order_request_param):
        """
        /v4/privatenat/renew-privatenat
        续订NAT网关
        """
        return self.send(renew_private_nat_api_order_request_param)

    def update_private_dnat_api(self, update_private_dnat_api_request_param):
        """
        /v4/privatenat/modify-dnat
        修改私网DNAT
        """
        return self.send(update_private_dnat_api_request_param)

    def update_private_snat_api(self, update_private_snat_api_request_param):
        """
        /v4/privatenat/modify-snat
        修改私网SNAT规则，子网和自定义网段可二选其一，都填以子网ID为主。
        """
        return self.send(update_private_snat_api_request_param)

    def delete_private_nat_order(self, delete_private_nat_order_request_param):
        """
        /v4/privatenat/delete-privatenat
        删除NAT网关
        """
        return self.send(delete_private_nat_order_request_param)

    def update_private_nat_api_order(self, update_private_nat_api_order_request_param):
        """
        /v4/privatenat/modify-spec
        变配私网NAT网关
        """
        return self.send(update_private_nat_api_order_request_param)

    def delete_private_snat_api(self, delete_private_snat_api_request_param):
        """
        /v4/privatenat/delete-snat
        删除私网SNAT
        """
        return self.send(delete_private_snat_api_request_param)

    def delete_transfer_ip_api(self, delete_transfer_ip_api_request_param):
        """
        /v4/privatenat/delete-ip
        删除中转IP
        """
        return self.send(delete_transfer_ip_api_request_param)

    def create_transfer_ip_api(self, create_transfer_ip_api_request_param):
        """
        /v4/privatenat/create-ip
        创建中转IP
        """
        return self.send(create_transfer_ip_api_request_param)

    def transfer_ip_api_list(self, transfer_ip_api_list_request_param):
        """
        /v4/privatenat/list-ips
        查询中转IP列表
        """
        return self.send(transfer_ip_api_list_request_param)

    def transfer_cidr_api_list(self, transfer_cidr_api_list_request_param):
        """
        /v4/privatenat/list-cidrs
        获取中转地址段
        """
        return self.send(transfer_cidr_api_list_request_param)

    def delete_private_dnat_api(self, delete_private_dnat_api_request_param):
        """
        /v4/privatenat/delete-dnat
        删除私网DNAT
        """
        return self.send(delete_private_dnat_api_request_param)

    def create_private_nat_price(self, create_private_nat_price_request_param):
        """
        /v4/privatenat/query_create_price
        创建私网NAT网关的询价，传参与创建一致。不涉及价格的参数只校验是否必传（不为空），不校验实际内容的有效性，直接透传。
        """
        return self.send(create_private_nat_price_request_param)

    def update_private_nat_price(self, update_private_nat_price_request_param):
        """
        /v4/privatenat/query_modify_spec_price
        变配私网NAT的询价
        """
        return self.send(update_private_nat_price_request_param)

    def create_private_dnat_api(self, create_private_dnat_api_request_param):
        """
        /v4/privatenat/create-dnat
        创建私网DNAT
        """
        return self.send(create_private_dnat_api_request_param)

    def private_dnat_api_list(self, private_dnat_api_list_request_param):
        """
        /v4/privatenat/list-dnats
        查询私网DNAT列表
        """
        return self.send(private_dnat_api_list_request_param)

    def update_private_nat_api(self, update_private_nat_api_request_param):
        """
        /v4/privatenat/update
        修改私网NAT网关的名称和描述
        """
        return self.send(update_private_nat_api_request_param)

    def private_snat_api_list(self, private_snat_api_list_request_param):
        """
        /v4/privatenat/list-snats
        查询私网SNAT列表
        """
        return self.send(private_snat_api_list_request_param)
