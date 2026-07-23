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


class UpdateClusterThresholdHybridRequest(CTYunRequest):
    """
    修改集群容量阈值
    """

    def __init__(self, request_param):
        super(UpdateClusterThresholdHybridRequest, self).__init__("/v4/monitor/update-cluster-threshold", "POST", "monitor", "application/json")
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
        if self.parameters.cluster_id is not None:
            body_param["clusterID"] = self.parameters.cluster_id
        if self.parameters.item_name is not None:
            body_param["itemName"] = self.parameters.item_name
        if self.parameters.threshold is not None:
            if type(self.parameters.threshold) is dict:
                threshold_dict_value = self.parameters.threshold
            else:
                threshold_dict_value = self.parameters.threshold.get_dic()
            body_param["threshold"] = threshold_dict_value
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


class Threshold(object):

    def __init__(self, warning=None, average=None, high=None, disaster=None):
        """
        :param warning: 提示阈值
        :param average: 次要阈值
        :param high: 重要阈值
        :param disaster: 紧急阈值
        """
        self.warning = warning
        self.average = average
        self.high = high
        self.disaster = disaster

    def set_warning(self, warning):
        """
        :param warning: 提示阈值
        """
        self.warning = warning

    def set_average(self, average):
        """
        :param average: 次要阈值
        """
        self.average = average

    def set_high(self, high):
        """
        :param high: 重要阈值
        """
        self.high = high

    def set_disaster(self, disaster):
        """
        :param disaster: 紧急阈值
        """
        self.disaster = disaster

    def get_dic(self):
        obj_dict = dict()
        if self.warning is not None:
            obj_dict["warning"] = self.warning
        if self.average is not None:
            obj_dict["average"] = self.average
        if self.high is not None:
            obj_dict["high"] = self.high
        if self.disaster is not None:
            obj_dict["disaster"] = self.disaster
        return obj_dict


class UpdateClusterThresholdHybridRequestParam(object):

    def __init__(self, region_id, cluster_id, item_name, threshold=None):
        """
        :param region_id: 资源池ID
        :param cluster_id: 集群ID
        :param item_name: 集群指标 cpu_allocated_rate：CPU分配率，memory_allocated_rate内存分配率，alloc_rate存储分配率
        :param threshold: 阈值需要0-100     
         要求：提示阈值<次要阈值<重要阈值<紧急阈值
        """
        self.region_id = region_id
        self.cluster_id = cluster_id
        self.item_name = item_name
        self.threshold = threshold

    def set_threshold(self, threshold):
        """
        :param threshold: 阈值需要0-100     
         要求：提示阈值<次要阈值<重要阈值<紧急阈值
        """
        self.threshold = threshold

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.cluster_id is None:
            raise Exception("cluster_id can not None")
        if self.item_name is None:
            raise Exception("item_name can not None")

