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


class QueryQuotaUsedRequest(CTYunRequest):
    """
    获取配额详情接口
    """

    def __init__(self, request_param):
        super(QueryQuotaUsedRequest, self).__init__("/v1/quota/queryQuotaUsed", "POST", "iam", "application/json")
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
        if self.parameters.query_user_list is not None:
            query_user_list = []
            if isinstance(self.parameters.query_user_list, list):
                for item in self.parameters.query_user_list:
                    if type(item) is dict:
                        query_user_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        query_user_list.append(item_dict_value)
            else:
                query_user_list.append(self.parameters.query_user_list.get_dic())
            body_param["queryUserList"] = query_user_list
        if self.parameters.user_quota_list is not None:
            user_quota_list = []
            if isinstance(self.parameters.user_quota_list, list):
                for item in self.parameters.user_quota_list:
                    if type(item) is dict:
                        user_quota_list.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        user_quota_list.append(item_dict_value)
            else:
                user_quota_list.append(self.parameters.user_quota_list.get_dic())
            body_param["userQuotaList"] = user_quota_list
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


class QueryUser(object):

    def __init__(self, account_id, region_id, quota_used_list, user_id=None, project_id=None):
        """
        :param user_id: 用户ID，暂时不启用，也不生效，可以忽略
        :param account_id: VDC的主账号ID
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        :param quota_used_list: 需要查询的配额ID列表
        """
        self.user_id = user_id
        self.account_id = account_id
        self.region_id = region_id
        self.project_id = project_id
        self.quota_used_list = quota_used_list
        self.check_param()

    def set_user_id(self, user_id):
        """
        :param user_id: 用户ID，暂时不启用，也不生效，可以忽略
        """
        self.user_id = user_id

    def set_project_id(self, project_id):
        """
        :param project_id: 企业项目ID
        """
        self.project_id = project_id

    def get_dic(self):
        obj_dict = dict()
        if self.user_id is not None:
            obj_dict["userId"] = self.user_id
        if self.account_id is not None:
            obj_dict["accountId"] = self.account_id
        if self.region_id is not None:
            obj_dict["regionId"] = self.region_id
        if self.project_id is not None:
            obj_dict["projectId"] = self.project_id
        if self.quota_used_list is not None:
            quota_used_list_array = []
            for item in self.quota_used_list:
                if type(item) is dict:
                    quota_used_list_array.append(item)
                else:
                    quota_used_list_array.append(item.get_dic())
            obj_dict["quotaUsedList"] = quota_used_list_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.account_id is None:
            raise Exception("account_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.quota_used_list is None:
            raise Exception("quota_used_list can not None")


class QuotaUsed(object):

    def __init__(self, quota_id, ):
        """
        :param quota_id: 配额ID
        """
        self.quota_id = quota_id
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.quota_id is not None:
            obj_dict["quotaId"] = self.quota_id
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.quota_id is None:
            raise Exception("quota_id can not None")


class UserQuota(object):

    def __init__(self, user_id, account_id, region_id, project_id, quota_used_list, ):
        """
        :param user_id: 用户ID，暂时不启用，也不生效，可以忽略
        :param account_id: VDC的主账号ID
        :param region_id: 资源池ID
        :param project_id: 企业项目ID
        :param quota_used_list: 需要查询的配额ID列表
        """
        self.user_id = user_id
        self.account_id = account_id
        self.region_id = region_id
        self.project_id = project_id
        self.quota_used_list = quota_used_list
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.user_id is not None:
            obj_dict["userId"] = self.user_id
        if self.account_id is not None:
            obj_dict["accountId"] = self.account_id
        if self.region_id is not None:
            obj_dict["regionId"] = self.region_id
        if self.project_id is not None:
            obj_dict["projectId"] = self.project_id
        if self.quota_used_list is not None:
            quota_used_list_array = []
            for item in self.quota_used_list:
                if type(item) is dict:
                    quota_used_list_array.append(item)
                else:
                    quota_used_list_array.append(item.get_dic())
            obj_dict["quotaUsedList"] = quota_used_list_array
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.user_id is None:
            raise Exception("user_id can not None")
        if self.account_id is None:
            raise Exception("account_id can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.project_id is None:
            raise Exception("project_id can not None")
        if self.quota_used_list is None:
            raise Exception("quota_used_list can not None")


class QueryQuotaUsedRequestParam(object):

    def __init__(self, query_user_list, user_quota_list, ):
        """
        :param query_user_list: 【废弃此字段，请用userQuotaList】配额查询详情 注意:此参数为数组
        :param user_quota_list: 配额查询详情(此接口与queryUserList，一摸一样，为兼容之前定义错误的接口) 注意:此参数为数组
        """
        self.query_user_list = query_user_list
        self.user_quota_list = user_quota_list

    def check_param(self):
        """
        the param required check
        """
        if self.query_user_list is None:
            raise Exception("query_user_list can not None")
        if self.user_quota_list is None:
            raise Exception("user_quota_list can not None")

