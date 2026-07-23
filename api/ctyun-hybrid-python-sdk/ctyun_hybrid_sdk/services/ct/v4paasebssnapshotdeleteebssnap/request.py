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


class V4PaasEbsSnapshotDeleteEbsSnapRequest(CTYunRequest):
    """
    1.本接口为异步接口，调用成功后会返回一个`jobID`，调用方通过`jobID`轮询任务执行结果。   
    2.该接口目前不支持多个删除 查询接口为/v4/job/info
    """

    def __init__(self, request_param):
        super(V4PaasEbsSnapshotDeleteEbsSnapRequest, self).__init__("/v4/paas/ebs_snapshot/delete-ebs-snap", "POST", "ct", "application/json")
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
        if self.parameters.snapshot_ids is not None:
            body_param["snapshotIDs"] = self.parameters.snapshot_ids
        if self.parameters.refund_order is not None:
            body_param["refundOrder"] = self.parameters.refund_order
        if self.parameters.disk_id is not None:
            body_param["diskID"] = self.parameters.disk_id
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


class V4PaasEbsSnapshotDeleteEbsSnapRequestParam(object):

    def __init__(self, client_token, region_id, snapshot_ids, disk_id, channel_info=None, refund_order=None):
        """
        :param channel_info: 当前并未处理。应是必填
        :param client_token: 用于保证订单幂等性。要求单个云平台账户内唯一
        :param region_id: 您可以调用[regionID](https://www.ctyun.cn/document/10026730/10040588)查看最新的天翼云资源池列表
        :param snapshot_ids: 请根据查询快照列表接口返回值进行传参，获取snapshotID参数，当refundOrder为True时不校验该字段，将删除所有的快照，该字段传空即可 注意:此参数为数组
        :param refund_order: 是否退订该硬盘下的所有的快照，True时将删除所有的快照并删除订单，False时只删除快照不删除订单 
        :param disk_id: 云硬盘ID
        """
        self.channel_info = channel_info
        self.client_token = client_token
        self.region_id = region_id
        self.snapshot_ids = snapshot_ids
        self.refund_order = refund_order
        self.disk_id = disk_id

    def set_channel_info(self, channel_info):
        """
        :param channel_info: 当前并未处理。应是必填
        """
        self.channel_info = channel_info

    def set_refund_order(self, refund_order):
        """
        :param refund_order: 是否退订该硬盘下的所有的快照，True时将删除所有的快照并删除订单，False时只删除快照不删除订单 
        """
        self.refund_order = refund_order

    def check_param(self):
        """
        the param required check
        """
        if self.client_token is None:
            raise Exception("client_token can not None")
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_ids is None:
            raise Exception("snapshot_ids can not None")
        if self.disk_id is None:
            raise Exception("disk_id can not None")

