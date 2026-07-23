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


class VpcCreateRequest(CTYunRequest):
    """
    创建一个专有网络VPC。   
       
    ### 接口约束   
       
    调用该接口创建 VPC 时，请注意：   
       
    - 一个 VPC 只能指定一个网段。   
       
    - VPC 创建后无法修改网段，但可以添加附加 IPv4 网段。   
       
    - 创建 VPC 后，会自动创建一个路由器和一个路由表。   
       
    - 创建VPC时若开启ipv6，默认创建ipv6网关   
       
    - enableIpv6参数仅支持4.0资源池
    """

    def __init__(self, request_param):
        super(VpcCreateRequest, self).__init__("/v4/vpc/create", "POST", "ctvpc", "application/json")
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
        if self.parameters.name is not None:
            body_param["name"] = self.parameters.name
        if self.parameters.az_name is not None:
            body_param["azName"] = self.parameters.az_name
        if self.parameters.cidr is not None:
            body_param["CIDR"] = self.parameters.cidr
        if self.parameters.enable_ipv6 is not None:
            body_param["enableIpv6"] = self.parameters.enable_ipv6
        if self.parameters.description is not None:
            body_param["description"] = self.parameters.description
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
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


class VpcCreateRequestParam(object):

    def __init__(self, region_id, name, cidr, az_name=None, enable_ipv6=None, description=None, client_token=None):
        """
        :param region_id: 资源池 ID
        :param name: 支持英文字母、中文、数字，下划线，连字符，中文 / 英文字母开头，长度 2 - 32
        :param az_name: 可用区名称   
         （差异点说明：2.0对齐公有云文档，无此参数）
        :param cidr: VPC 的网段。建议您使用 192.168.0.0/16、172.16.0.0/12、10.0.0.0/8 三个 RFC 标准私网网段及其子网作为专有网络的主 IPv4 网段，网段掩码有效范围为 8~28 位
        :param enable_ipv6: 是否开启 IPv6 网段。取值：false（默认值）:不开启，true: 开启   
         （差异点说明：2.0已对齐公有云文档，该参数类型为bool类型; 1.0为string格式，若开启ipv6，默认创建ipv6网关）
        :param description: vpc 描述。内容限制：1、长度限制 128 2、支持汉字，大小写字母，数字 3、支持英文特殊字符：！@#￥%……&*（）——-+=《》？：”“{}，。、；‘'【】4、 不支持特殊字符 英文字符(反引号`)(反斜杠) 中英文空格
        :param client_token: 可传但是不进行校验, 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.region_id = region_id
        self.name = name
        self.az_name = az_name
        self.cidr = cidr
        self.enable_ipv6 = enable_ipv6
        self.description = description
        self.client_token = client_token

    def set_az_name(self, az_name):
        """
        :param az_name: 可用区名称   
         （差异点说明：2.0对齐公有云文档，无此参数）
        """
        self.az_name = az_name

    def set_enable_ipv6(self, enable_ipv6):
        """
        :param enable_ipv6: 是否开启 IPv6 网段。取值：false（默认值）:不开启，true: 开启   
         （差异点说明：2.0已对齐公有云文档，该参数类型为bool类型; 1.0为string格式，若开启ipv6，默认创建ipv6网关）
        """
        self.enable_ipv6 = enable_ipv6

    def set_description(self, description):
        """
        :param description: vpc 描述。内容限制：1、长度限制 128 2、支持汉字，大小写字母，数字 3、支持英文特殊字符：！@#￥%……&*（）——-+=《》？：”“{}，。、；‘'【】4、 不支持特殊字符 英文字符(反引号`)(反斜杠) 中英文空格
        """
        self.description = description

    def set_client_token(self, client_token):
        """
        :param client_token: 可传但是不进行校验, 客户端存根，用于保证订单幂等性。要求单个云平台账户内唯一
        """
        self.client_token = client_token

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.name is None:
            raise Exception("name can not None")
        if self.cidr is None:
            raise Exception("cidr can not None")

