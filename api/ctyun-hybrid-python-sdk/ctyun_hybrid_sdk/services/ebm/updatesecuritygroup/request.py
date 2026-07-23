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


class UpdateSecurityGroupRequest(CTYunRequest):
    """
    更新物理机安全组
    """

    def __init__(self, request_param):
        super(UpdateSecurityGroupRequest, self).__init__("/v4/ebm/update-security-group", "POST", "ebm", "application/json")
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
        if self.parameters.instance_uuid is not None:
            body_param["instanceUUID"] = self.parameters.instance_uuid
        if self.parameters.interface_uuid is not None:
            body_param["interfaceUUID"] = self.parameters.interface_uuid
        if self.parameters.add_security_group_id_list is not None:
            body_param["addSecurityGroupIDList"] = self.parameters.add_security_group_id_list
        if self.parameters.del_security_group_id_list is not None:
            body_param["delSecurityGroupIDList"] = self.parameters.del_security_group_id_list
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


class UpdateSecurityGroupRequestParam(object):

    def __init__(self, region_id, instance_uuid, interface_uuid, add_security_group_id_list, del_security_group_id_list, ):
        """
        :param region_id: 区域ID
        :param instance_uuid: 实例UUID 
        :param interface_uuid: 网卡uuid
        :param add_security_group_id_list: 增加安全组的ID用,分割(addSecurityGroupIDList,delSecurityGroupIDList必须有一项必填)
        :param del_security_group_id_list: 删除安全组的ID用,分割(addSecurityGroupIDList,delSecurityGroupIDList必须有一项必填)
        """
        self.region_id = region_id
        self.instance_uuid = instance_uuid
        self.interface_uuid = interface_uuid
        self.add_security_group_id_list = add_security_group_id_list
        self.del_security_group_id_list = del_security_group_id_list

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_uuid is None:
            raise Exception("instance_uuid can not None")
        if self.interface_uuid is None:
            raise Exception("interface_uuid can not None")
        if self.add_security_group_id_list is None:
            raise Exception("add_security_group_id_list can not None")
        if self.del_security_group_id_list is None:
            raise Exception("del_security_group_id_list can not None")

