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


class EcsBatchUpdateInstancesRequest(CTYunRequest):
    """
    1. 确保当前请求资源池下，这些云主机存在（即instanceID真实存在且与regionID相对应）   
    2. 修改前后的displayName须不一样   
    3. 云主机只有在运行（running）、关机（stopped）或节省关机（shelve）状态才可执行该操作，您可以调用查询云主机列表或获取多台云主机的状态信息查询结果中的instanceStatus字段来确认当前云主机状态
    """

    def __init__(self, request_param):
        super(EcsBatchUpdateInstancesRequest, self).__init__("/v4/ecs/batch-update-instances", "POST", "ctecs", "application/json")
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
        if self.parameters.update_info is not None:
            update_info = []
            if isinstance(self.parameters.update_info, list):
                for item in self.parameters.update_info:
                    if type(item) is dict:
                        update_info.append(item)
                    else:
                        item_dict_value = item.get_dic()
                        update_info.append(item_dict_value)
            else:
                update_info.append(self.parameters.update_info.get_dic())
            body_param["updateInfo"] = update_info
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


class UpdateInfo(object):

    def __init__(self, instance_id, display_name, ):
        """
        :param instance_id: 云主机ID
        :param display_name: 云主机显示名称，长度为2-63字符
        """
        self.instance_id = instance_id
        self.display_name = display_name
        self.check_param()

    def get_dic(self):
        obj_dict = dict()
        if self.instance_id is not None:
            obj_dict["instanceID"] = self.instance_id
        if self.display_name is not None:
            obj_dict["displayName"] = self.display_name
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.display_name is None:
            raise Exception("display_name can not None")


class EcsBatchUpdateInstancesRequestParam(object):

    def __init__(self, region_id, update_info, ):
        """
        :param region_id: 资源池ID
        :param update_info: 批量更新信息列表 注意:此参数为数组
        """
        self.region_id = region_id
        self.update_info = update_info

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.update_info is None:
            raise Exception("update_info can not None")

