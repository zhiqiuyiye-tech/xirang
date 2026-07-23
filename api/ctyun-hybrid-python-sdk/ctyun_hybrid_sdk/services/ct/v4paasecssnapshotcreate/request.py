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


class V4PaasEcsSnapshotCreateRequest(CTYunRequest):
    """
    1.云主机快照目前不计费，快照信息创建的时候，不需要登记Paas订单，无需生成话单   
    2.本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。   
    3.查询接口为/v4/job/info
    """

    def __init__(self, request_param):
        super(V4PaasEcsSnapshotCreateRequest, self).__init__("/v4/paas/ecs/snapshot/create", "POST", "ct", "application/json")
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
        if self.parameters.channel_info is not None:
            if type(self.parameters.channel_info) is dict:
                channel_info_dict_value = self.parameters.channel_info
            else:
                channel_info_dict_value = self.parameters.channel_info.get_dic()
            body_param["channelInfo"] = channel_info_dict_value
        if self.parameters.client_token is not None:
            body_param["clientToken"] = self.parameters.client_token
        if self.parameters.region_id is not None:
            body_param["regionID"] = self.parameters.region_id
        if self.parameters.instance_id is not None:
            body_param["instanceID"] = self.parameters.instance_id
        if self.parameters.snapshot_name is not None:
            body_param["snapshotName"] = self.parameters.snapshot_name
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


class ChannelInfo(object):

    def __init__(self, paas_resource_id, paas_account_id, master_order_id, tags=None, metas=None):
        """
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        :param tags: 自定义map结构（v2没有）
        :param metas: 自定义map结构（v2没有）
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas
        self.check_param()

    def set_tags(self, tags):
        """
        :param tags: 自定义map结构（v2没有）
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 自定义map结构（v2没有）
        """
        self.metas = metas

    def get_dic(self):
        obj_dict = dict()
        if self.paas_resource_id is not None:
            obj_dict["paasResourceID"] = self.paas_resource_id
        if self.paas_account_id is not None:
            obj_dict["paasAccountID"] = self.paas_account_id
        if self.master_order_id is not None:
            obj_dict["masterOrderID"] = self.master_order_id
        if self.tags is not None:
            obj_dict["tags"] = self.tags
        if self.metas is not None:
            obj_dict["metas"] = self.metas
        return obj_dict

    def check_param(self):
        """
        the param required check
        """
        if self.paas_resource_id is None:
            raise Exception("paas_resource_id can not None")
        if self.paas_account_id is None:
            raise Exception("paas_account_id can not None")
        if self.master_order_id is None:
            raise Exception("master_order_id can not None")


class V4PaasEcsSnapshotCreateRequestParam(object):

    def __init__(self, channel_info, client_token, region_id, instance_id, snapshot_name, ):
        """
        :param channel_info: 当前并未处理。应是必填(v2改为必传)
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 您可以调用[regionID](https://www.ctyun.cn/document/10026730/10040588)查看最新的天翼云资源池列表
        :param instance_id: 云主机ID
        :param snapshot_name: 满足以下规则：长度在2～63个字符,包含字母（区分大小写）、数字和特殊字符（~!@#$%^*_-+{[]}:,.?）的组合   
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.instance_id = instance_id
        self.snapshot_name = snapshot_name

    def check_param(self):
        """
        the param required check
        """
        if self.channel_info is None:
            raise Exception("channel_info can not None")
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.instance_id is None:
            raise Exception("instance_id can not None")
        if self.snapshot_name is None:
            raise Exception("snapshot_name can not None")

