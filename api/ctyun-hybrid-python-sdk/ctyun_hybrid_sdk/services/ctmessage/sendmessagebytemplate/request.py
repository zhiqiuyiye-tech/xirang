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


class SendMessageByTemplateRequest(CTYunRequest):
    """
    注: 9901-其他消息暂时未定义模板   
    detailParam参数不同类型的消息对应参数不同，所有参数类型均使用字符串类型，具体如下：   
    产品消息，消息详细类型:1001,1002,1003,1004,1005:   
    regionID -- 资源池ID   
    productType -- 产品类型   
    productTypeName -- 产品类型名称   
    resourceID -- 资源ID   
    resourceUUID -- 资源UUID   
    resourceName -- 资源名称   
    resourceOwner -- 资源所属人用户名称   
    运维消息，消息详细类型:2001, 2002:   
    regionID -- 资源池ID   
    productType -- 产品类型   
    productTypeName -- 产品类型名称   
    resourceName -- 资源名称   
    resourceOwner -- 资源所属人用户名称   
    alarmLevel -- 告警级别,1-提示,2-一般,3-严重,4-灾难   
    alarmRuleID -- 告警规则ID   
    alarmRuleName -- 告警规则名称,   
    currentValue -- 当前告警值   
    resourceID -- 资源ID   
    resourceUUID -- 资源UUID   
    monitorType -- 监控类型   
    平台消息，详细消息类型：3001，3002，3011. 3012:   
    resourceID -- 资源ID   
    resourceName -- 资源名称   
    其中，产品类型productType和产品类型名称productTypeName枚举见产品资源中心产品编码与产品名称，固定值   
    工单消息，详细消息类型: 4001，4002：    
    regionID -- 资源池ID，   
    resourceID -- 工单ID,    
    resourceName -- 工单名称   
     resourceOwner -- 提单人，   
    workOrderType-工单类型；   
    4002:    
    approvalResult-工单审批结果
    """

    def __init__(self, request_param):
        super(SendMessageByTemplateRequest, self).__init__("/v4/message/send-message", "POST", "ctmessage", "application/json")
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
        if self.parameters.message_spec_type is not None:
            body_param["messageSpecType"] = self.parameters.message_spec_type
        if self.parameters.send_chan is not None:
            body_param["sendChan"] = self.parameters.send_chan
        if self.parameters.detail_param is not None:
            body_param["detailParam"] = self.parameters.detail_param
        if self.parameters.message_template_param is not None:
            body_param["messageTemplateParam"] = self.parameters.message_template_param
        if self.parameters.receive_users is not None:
            body_param["receiveUsers"] = self.parameters.receive_users
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


class SendMessageByTemplateRequestParam(object):

    def __init__(self, message_spec_type, send_chan, receive_users, detail_param=None, message_template_param=None):
        """
        :param message_spec_type: 1001-产品即将到期通知， 1002-产品到期通知，1003-产品即将销毁通知， 1004-产品销毁通知，1005-资源开通失败通知，2001-云监控告警， 2002-资源池容量告警，3001-许可证即将到期通知，3002-许可证到期通知，4001-工单待审批提醒，4002-工单已审批提醒，5001-预算额度告警，9901-其他消息
        :param send_chan: 可选值1,3,5,7，其中1-站内信/2-短信/4-邮件，多个渠道相加，站内信为必选项
        :param detail_param: 使用json格式序列化字符串，值类型要求均为字符串类型，参数值用于消息卡片展示，不同消息类型要求的参数不同，详见说明
        :param message_template_param: 使用json格式序列化字符串，值类型要求均为字符串类型，此参数中的内容会替换模板内容中的占位符如${ResourceID}
        :param receive_users: 用户ID数组 注意:此参数为数组
        """
        self.message_spec_type = message_spec_type
        self.send_chan = send_chan
        self.detail_param = detail_param
        self.message_template_param = message_template_param
        self.receive_users = receive_users

    def set_detail_param(self, detail_param):
        """
        :param detail_param: 使用json格式序列化字符串，值类型要求均为字符串类型，参数值用于消息卡片展示，不同消息类型要求的参数不同，详见说明
        """
        self.detail_param = detail_param

    def set_message_template_param(self, message_template_param):
        """
        :param message_template_param: 使用json格式序列化字符串，值类型要求均为字符串类型，此参数中的内容会替换模板内容中的占位符如${ResourceID}
        """
        self.message_template_param = message_template_param

    def check_param(self):
        """
        the param required check
        """
        if self.message_spec_type is None:
            raise Exception("message_spec_type can not None")
        if self.send_chan is None:
            raise Exception("send_chan can not None")
        if self.receive_users is None:
            raise Exception("receive_users can not None")

