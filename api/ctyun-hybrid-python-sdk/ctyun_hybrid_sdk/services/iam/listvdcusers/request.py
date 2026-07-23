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


class ListVdcUsersRequest(CTYunRequest):
    """
    VDC用户列表查询
    """

    def __init__(self, request_param):
        super(ListVdcUsersRequest, self).__init__("/v1/vdc/list-users", "GET", "iam", "")
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
        if self.parameters.vdc_id is not None:
            query_param["vdcID"] = self.parameters.vdc_id
        if self.parameters.page is not None:
            query_param["page"] = self.parameters.page
        if self.parameters.page_size is not None:
            query_param["pageSize"] = self.parameters.page_size
        if self.parameters.login_name is not None:
            query_param["loginName"] = self.parameters.login_name
        if self.parameters.hmac_verify_status is not None:
            query_param["hmacVerifyStatus"] = self.parameters.hmac_verify_status
        if self.parameters.user_name is not None:
            query_param["userName"] = self.parameters.user_name
        if self.parameters.cert_status is not None:
            query_param["certStatus"] = self.parameters.cert_status
        if self.parameters.status is not None:
            query_param["status"] = self.parameters.status
        if self.parameters.user_from is not None:
            query_param["userFrom"] = self.parameters.user_from
        return query_param

    def get_path_param(self):
        """
        http path param get
        """
        return dict()


class ListVdcUsersRequestParam(object):

    def __init__(self, vdc_id, page, page_size, login_name=None, hmac_verify_status=None, user_name=None, cert_status=None, status=None, user_from=None):
        """
        :param vdc_id: vdc的id
        :param page: 页数，最小值为1   
         
        :param page_size: 每页显示条数，最大为100
        :param login_name: 登录名，支持模糊查询
        :param hmac_verify_status: 完整性校验状态 1-未验证 3-验证成功 4-验证失败 2-验证中
        :param user_name: 用户名，支持模糊匹配
        :param cert_status: 用户UKey证书状态 1-未上传 2-未激活 3-已激活 4-已到期
        :param status: 1正常  0锁定
        :param user_from: 创建方式，1-平台创建，2-手动导入。可多选，多个逗号分割
        """
        self.vdc_id = vdc_id
        self.page = page
        self.page_size = page_size
        self.login_name = login_name
        self.hmac_verify_status = hmac_verify_status
        self.user_name = user_name
        self.cert_status = cert_status
        self.status = status
        self.user_from = user_from

    def set_login_name(self, login_name):
        """
        :param login_name: 登录名，支持模糊查询
        """
        self.login_name = login_name

    def set_hmac_verify_status(self, hmac_verify_status):
        """
        :param hmac_verify_status: 完整性校验状态 1-未验证 3-验证成功 4-验证失败 2-验证中
        """
        self.hmac_verify_status = hmac_verify_status

    def set_user_name(self, user_name):
        """
        :param user_name: 用户名，支持模糊匹配
        """
        self.user_name = user_name

    def set_cert_status(self, cert_status):
        """
        :param cert_status: 用户UKey证书状态 1-未上传 2-未激活 3-已激活 4-已到期
        """
        self.cert_status = cert_status

    def set_status(self, status):
        """
        :param status: 1正常  0锁定
        """
        self.status = status

    def set_user_from(self, user_from):
        """
        :param user_from: 创建方式，1-平台创建，2-手动导入。可多选，多个逗号分割
        """
        self.user_from = user_from

    def check_param(self):
        """
        the param required check
        """
        if self.vdc_id is None:
            raise Exception("vdc_id can not None")
        if self.page is None:
            raise Exception("page can not None")
        if self.page_size is None:
            raise Exception("page_size can not None")

