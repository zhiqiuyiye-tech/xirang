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


class CreateUserHubRequest(CTYunRequest):
    """
    密码使用SM4-CBC算法加密,pcks5填充   
    key是登录名做sha256
    """

    def __init__(self, request_param):
        super(CreateUserHubRequest, self).__init__("/v4/user/hub/create", "POST", "user", "application/json")
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
        if self.parameters.type is not None:
            body_param["type"] = self.parameters.type
        if self.parameters.user_name is not None:
            body_param["userName"] = self.parameters.user_name
        if self.parameters.login_name is not None:
            body_param["loginName"] = self.parameters.login_name
        if self.parameters.password is not None:
            body_param["password"] = self.parameters.password
        if self.parameters.password_confirm is not None:
            body_param["passwordConfirm"] = self.parameters.password_confirm
        if self.parameters.email is not None:
            body_param["email"] = self.parameters.email
        if self.parameters.phone is not None:
            body_param["phone"] = self.parameters.phone
        if self.parameters.vdc_id is not None:
            body_param["vdcID"] = self.parameters.vdc_id
        if self.parameters.vdc_name is not None:
            body_param["vdcName"] = self.parameters.vdc_name
        if self.parameters.user_group_ids is not None:
            body_param["userGroupIDs"] = self.parameters.user_group_ids
        if self.parameters.oauth2_user_id is not None:
            body_param["oauth2UserID"] = self.parameters.oauth2_user_id
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


class CreateUserHubRequestParam(object):

    def __init__(self, type, user_name, login_name, password, password_confirm, oauth2_user_id, email=None, phone=None, vdc_id=None, vdc_name=None, user_group_ids=None):
        """
        :param type: 用户类型 1-系统 2-租户
        :param user_name: 用户名，长度为2-63字符   
         支持使用中文，英文字母，数字，点号 (.)，括号，下划线(_)，中划线 (-)，半角冒号 (:)   
         不能包含续连字符（--）
        :param login_name: 用户登陆名，长度为2-20字符   
         支持使用英文字母、数字、连字符（-）、下划线（_）   
         不支持特殊字符开头，不能包含连续字符(--)
        :param password: 密码，默认规则：长度为8-20字符   
         必须包含4项：大写字母+小写字母+数字+特殊字符，特殊字符仅支持~!@#$%&*()-_.，若系统管理登录安全中设置了密码规则，则以此规则为准，若系统管理登录安全中设置了密码规则，则以此规则为准
        :param password_confirm: 密码确认，默认规则：长度为8-20字符   
         必须包含4项：大写字母+小写字母+数字+特殊字符，特殊字符仅支持~!@#$%&*()-_.若系统管理登录安全中设置了密码规则，则以此规则为准，若系统管理登录安全中设置了密码规则，则以此规则为准
        :param email: 邮箱，校验邮箱格式
        :param phone: 手机号，校验11位手机号
        :param vdc_id: 租户时必填，用户所属vdcid
        :param vdc_name: 租户时必填，用户所属vdc名称，以vdcid对应名称为准，后端自动修正
        :param user_group_ids: 用户组id列表   
         平台系统管理员：需加入代维管理员用户组（37cd364c-9a70-4857-b891-eeff6a5f704b）、运营管理员用户组（e5ca2085-7fd8-465a-934a-267c95fb66e7）   
         智维管理员：需加入VDC管理员用户组（1205d992-d569-44c6-ab0c-c030d2e3ce4c），智维菜单用户组（bb213ce7-533e-42d0-b86e-3385086beda1）   
         VDC管理员：需加入VDC管理员用户组（1205d992-d569-44c6-ab0c-c030d2e3ce4c），没有创建产品服务用户组（1afb0b5c-7e1a-4f64-bc74-1874754b11f3）   
         VDC业务员：需加入VDC业务员用户组（0333b266-c33a-4a30-8b8d-bdcedf9dd70b），没有创建产品服务用户组（1afb0b5c-7e1a-4f64-bc74-1874754b11f3）   
         VDC只读员：需加入VDC只读管理员用户组（c40e61f1-67b8-4877-acbb-162319cfabb1） 注意:此参数为数组
        :param oauth2_user_id: 云聚平台对应用户id
        """
        self.type = type
        self.user_name = user_name
        self.login_name = login_name
        self.password = password
        self.password_confirm = password_confirm
        self.email = email
        self.phone = phone
        self.vdc_id = vdc_id
        self.vdc_name = vdc_name
        self.user_group_ids = user_group_ids
        self.oauth2_user_id = oauth2_user_id

    def set_email(self, email):
        """
        :param email: 邮箱，校验邮箱格式
        """
        self.email = email

    def set_phone(self, phone):
        """
        :param phone: 手机号，校验11位手机号
        """
        self.phone = phone

    def set_vdc_id(self, vdc_id):
        """
        :param vdc_id: 租户时必填，用户所属vdcid
        """
        self.vdc_id = vdc_id

    def set_vdc_name(self, vdc_name):
        """
        :param vdc_name: 租户时必填，用户所属vdc名称，以vdcid对应名称为准，后端自动修正
        """
        self.vdc_name = vdc_name

    def set_user_group_ids(self, user_group_ids):
        """
        :param user_group_ids: 用户组id列表   
         平台系统管理员：需加入代维管理员用户组（37cd364c-9a70-4857-b891-eeff6a5f704b）、运营管理员用户组（e5ca2085-7fd8-465a-934a-267c95fb66e7）   
         智维管理员：需加入VDC管理员用户组（1205d992-d569-44c6-ab0c-c030d2e3ce4c），智维菜单用户组（bb213ce7-533e-42d0-b86e-3385086beda1）   
         VDC管理员：需加入VDC管理员用户组（1205d992-d569-44c6-ab0c-c030d2e3ce4c），没有创建产品服务用户组（1afb0b5c-7e1a-4f64-bc74-1874754b11f3）   
         VDC业务员：需加入VDC业务员用户组（0333b266-c33a-4a30-8b8d-bdcedf9dd70b），没有创建产品服务用户组（1afb0b5c-7e1a-4f64-bc74-1874754b11f3）   
         VDC只读员：需加入VDC只读管理员用户组（c40e61f1-67b8-4877-acbb-162319cfabb1）
        """
        self.user_group_ids = user_group_ids

    def check_param(self):
        """
        the param required check
        """
        if self.type is None:
            raise Exception("type can not None")
        if self.user_name is None:
            raise Exception("user_name can not None")
        if self.login_name is None:
            raise Exception("login_name can not None")
        if self.password is None:
            raise Exception("password can not None")
        if self.password_confirm is None:
            raise Exception("password_confirm can not None")
        if self.oauth2_user_id is None:
            raise Exception("oauth2_user_id can not None")

