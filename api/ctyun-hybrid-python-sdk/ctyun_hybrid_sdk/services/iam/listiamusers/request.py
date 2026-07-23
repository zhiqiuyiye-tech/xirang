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


class ListIAMUsersRequest(CTYunRequest):
    """
    IAM认证-用户列表查询 
    """

    def __init__(self, request_param):
        super(ListIAMUsersRequest, self).__init__("/v1/user/iam/list", "GET", "iam", "")
        if request_param is None:
            raise Exception("request_param can not None")
        self.parameters = request_param
        self.parameters.check_param()
        self.header = dict()

    def get_body_param(self):
        """
        http body param get
        """
        return dict()

    def get_query_param(self):
        """
        http query param get
        """
        query_param = dict()
        if self.parameters.user_name is not None:
            query_param["userName"] = self.parameters.user_name
        if self.parameters.login_name is not None:
            query_param["loginName"] = self.parameters.login_name
        if self.parameters.type is not None:
            query_param["type"] = self.parameters.type
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.cert_status is not None:
            query_param["certStatus"] = self.parameters.cert_status
        if self.parameters.user_from is not None:
            query_param["userFrom"] = self.parameters.user_from
        if self.parameters.ldap_dn is not None:
            query_param["ldapDn"] = self.parameters.ldap_dn
        if self.parameters.hmac_verify_status is not None:
            query_param["hmacVerifyStatus"] = self.parameters.hmac_verify_status
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListIAMUsersRequestParam(object):

    def __init__(self, user_name=None, login_name=None, type=None, status=None, cert_status=None, user_from=None, ldap_dn=None, hmac_verify_status=None, page=None, page_size=None):
        """
        :param user_name: 用户名
        :param login_name: 登录名
        :param type: 用户类型准确匹配，1-系统 2-租户 3-代维   
         
        :param status: 1未锁定 2锁定   
         
        :param cert_status: 证书状态 1-未上传 2-未激活 3-已激活 4-已过期   
         
        :param user_from: 用户来源：1. 平台创建、2. AD/LDAP手动导入   
         
        :param ldap_dn: 用户来源是ldap的dn信息   
         
        :param hmac_verify_status: 完整性校验状态 1-未验证 3-验证成功 4-验证失败 2-验证中   
         
        :param page: 页数，默认为1   
         
        :param page_size: 每页显示条数，默认为10
        """
        self.user_name = user_name
        self.login_name = login_name
        self.type = type
        self.status = status
        self.cert_status = cert_status
        self.user_from = user_from
        self.ldap_dn = ldap_dn
        self.hmac_verify_status = hmac_verify_status
        self.page = page
        self.page_size = page_size

    def set_user_name(self, user_name):
        """
        :param user_name: 用户名
        """
        self.user_name = user_name

    def set_login_name(self, login_name):
        """
        :param login_name: 登录名
        """
        self.login_name = login_name

    def set_type(self, type):
        """
        :param type: 用户类型准确匹配，1-系统 2-租户 3-代维   
         
        """
        self.type = type

    def set_status(self, status):
        """
        :param status: 1未锁定 2锁定   
         
        """
        self.status = status

    def set_cert_status(self, cert_status):
        """
        :param cert_status: 证书状态 1-未上传 2-未激活 3-已激活 4-已过期   
         
        """
        self.cert_status = cert_status

    def set_user_from(self, user_from):
        """
        :param user_from: 用户来源：1. 平台创建、2. AD/LDAP手动导入   
         
        """
        self.user_from = user_from

    def set_ldap_dn(self, ldap_dn):
        """
        :param ldap_dn: 用户来源是ldap的dn信息   
         
        """
        self.ldap_dn = ldap_dn

    def set_hmac_verify_status(self, hmac_verify_status):
        """
        :param hmac_verify_status: 完整性校验状态 1-未验证 3-验证成功 4-验证失败 2-验证中   
         
        """
        self.hmac_verify_status = hmac_verify_status

    def set_page(self, page):
        """
        :param page: 页数，默认为1   
         
        """
        self.page = page

    def set_page_size(self, page_size):
        """
        :param page_size: 每页显示条数，默认为10
        """
        self.page_size = page_size

    def check_param(self):
        """
        the param required check
        """
        pass

