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


class EcsSnapshotDetailsRequest(CTYunRequest):
    """
    查询云主机快照详情   
    1.14返回:   
    {   
    	"description": "成功",   
    	"errorCode": "SUCCESS",   
    	"message": "success",   
    	"returnObj": [   
    		{   
    			"azName": "az3",   
    			"createAt": "2023-04-10T09:39:16.444482Z",   
    			"customerID": 2065,   
    			"description": "",   
    			"instanceID": "e993eff4-12c3-23cf-6a5a-196bb235496a",   
    			"instanceSnapshotName": "ecs-snapshot-041001",   
    			"instanceStatus": "ACTIVE",   
    			"isMaz": false,   
    			"isPaas": false,   
    			"members": [   
    				{   
    					"isBootable": false,   
    					"isEncrypted": false,   
    					"snapshotID": "d2cfda04-dae6-40b0-9375-07a778cb0a92",   
    					"snapshotStatus": "available",   
    					"volumeID": "2ac4d787-3812-4818-a3ce-8fa0b58c47ec",   
    					"volumeName": "hytest-022801-data-1",   
    					"volumeSize": 20,   
    					"volumeTypeName": "SAS-public"   
    				},   
    				{   
    					"isBootable": true,   
    					"isEncrypted": false,   
    					"snapshotID": "a0505d41-b217-4372-8233-87e40e6fe51a",   
    					"snapshotStatus": "available",   
    					"volumeID": "0f8c9554-f762-4c50-8cb0-99af02a0c7fe",   
    					"volumeName": "hytest-022801-volume-000",   
    					"volumeSize": 40,   
    					"volumeTypeName": "SAS-public"   
    				}   
    			],   
    			"snapshotID": "04294618-c941-8ba7-dee7-c8d19f3bf14d",   
    			"status": "available",   
    			"updateAt": "2023-04-10T09:41:06.620707Z"   
    		}   
    	],   
    	"statusCode": 800   
    }   
    1.15版本返回:   
    {   
    	"description": "成功 X-Trace-ID-->a685899ccbbe2f37",   
    	"errorCode": "SUCCESS",   
    	"message": "success",   
    	"returnObj": {   
    		"totalPage": 1,   
    		"currentCount": 1,   
    		"totalCount": 1,   
    		"results": [   
    			{   
    				"azName": "az1",   
    				"createAt": "2024-01-01T07:00:02.515775Z",   
    				"customerID": 1000000957,   
    				"instanceID": "f4f7bf5d-f592-32df-92ec-0b417ef6f650",   
    				"instanceSnapshotName": "auto_vm_snap-87aa04fb-20240101070000-s814",   
    				"instanceStatus": "SHUTOFF",   
    				"isMaz": false,   
    				"isPaas": false,   
    				"members": [],   
    				"snapshotID": "3b6be2a8-3e47-e82b-cb22-daa78a20a6e7",   
    				"status": "available",   
    				"updateAt": "2024-01-02T02:46:21.953592Z"   
    			}   
    		]   
    	},   
    	"statusCode": 800   
    }
    """

    def __init__(self, request_param):
        super(EcsSnapshotDetailsRequest, self).__init__("/v4/ecs/snapshot-details", "POST", "ctecs", "application/json")
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
        if self.parameters.snapshot_id is not None:
            body_param["snapshotID"] = self.parameters.snapshot_id
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


class EcsSnapshotDetailsRequestParam(object):

    def __init__(self, region_id, snapshot_id, ):
        """
        :param region_id: 区域ID
        :param snapshot_id: 云主机快照实例ID
        """
        self.region_id = region_id
        self.snapshot_id = snapshot_id

    def check_param(self):
        """
        the param required check
        """
        if self.region_id is None:
            raise Exception("region_id can not None")
        if self.snapshot_id is None:
            raise Exception("snapshot_id can not None")

