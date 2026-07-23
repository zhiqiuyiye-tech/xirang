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


class V4PaasEbsSnapshotCreateEbsSnapRequest(CTYunRequest):
    """
    本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。查询接口为/v4/job/info；保留策略暂不支持
    """

    def __init__(self, request_param):
        super(V4PaasEbsSnapshotCreateEbsSnapRequest, self).__init__("/v4/paas/ebs_snapshot/create-ebs-snap", "POST", "ct", "application/json")
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
        if self.parameters.snapshot_name is not None:
            body_param["snapshotName"] = self.parameters.snapshot_name
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
        if self.parameters.retention_policy is not None:
            body_param["retentionPolicy"] = self.parameters.retention_policy
        if self.parameters.retention_time is not None:
            body_param["retentionTime"] = self.parameters.retention_time
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

    def __init__(self, paas_resource_id=None, paas_account_id=None, master_order_id=None, tags=None, metas=None):
        """
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        :param tags: 自定义map结构
        :param metas: 自定义map结构
        """
        self.paas_resource_id = paas_resource_id
        self.paas_account_id = paas_account_id
        self.master_order_id = master_order_id
        self.tags = tags
        self.metas = metas

    def set_paas_resource_id(self, paas_resource_id):
        """
        :param paas_resource_id: 变配或删除时，使用和创建资源相同的paasResourceID
        """
        self.paas_resource_id = paas_resource_id

    def set_paas_account_id(self, paas_account_id):
        """
        :param paas_account_id: 资源的付费账号，通过上送IT用于内部结算，和channel无关
        """
        self.paas_account_id = paas_account_id

    def set_master_order_id(self, master_order_id):
        """
        :param master_order_id: IaaS记入话单，用来关联订单和资源
        """
        self.master_order_id = master_order_id

    def set_tags(self, tags):
        """
        :param tags: 自定义map结构
        """
        self.tags = tags

    def set_metas(self, metas):
        """
        :param metas: 自定义map结构
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


class V4PaasEbsSnapshotCreateEbsSnapRequestParam(object):

    def __init__(self, client_token, region_id, snapshot_name, disk_id, retention_policy, channel_info=None, retention_time=None):
        """
        :param channel_info: 当前并未处理。应是必填
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 您可以调用[regionID](https://www.ctyun.cn/document/10026730/10040588)查看最新的天翼云资源池列表
        :param snapshot_name: 快照名称
        :param disk_id: 云硬盘ID
        :param retention_policy: 取值范围：[/forever]，custom：自定义保留天数，forever：永久保留
        :param retention_time: 取值范围：1-65535。当快照保留策略为custom时该参数为必填，当快照保留策略为forever时，自动设置为65535
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.snapshot_name = snapshot_name
        self.disk_id = disk_id
        self.retention_policy = retention_policy
        self.retention_time = retention_time

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 当前并未处理。应是必填
        """
        self.channel_info = channel_info

    def set_retention_time(self, retention_time):
        """
        :param retention_time: 取值范围：1-65535。当快照保留策略为custom时该参数为必填，当快照保留策略为forever时，自动设置为65535
        """
        self.retention_time = retention_time

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_name is None:
            raise Exception("snapshot_name can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")
        if self.retention_policy is None:
            raise Exception("retention_policy can not None")

