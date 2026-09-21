# 查询一个或多个云主机规格资源_paas

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /v4/ecs/flavor/list:
    post:
      summary: 查询一个或多个云主机规格资源_paas
      deprecated: false
      description: >
        该接口提供用户可用规格列表查询功能，可返回云主机规格的详细信息,并允许用户根据云主机规格的特殊字段进行筛选。用户可以根据此接口的返回值了解自己可使用的云主机规格有哪些。

        **注意**： 如果您传了flavorID 则azName 为必填。如果只传regionID 则可查询所有数据，azName不是必填的
      operationId: listFlavor
      tags:
        - 计算/云主机规格
        - 云主机规格
        - pass-new
        - '3.0'
        - '4.0'
      parameters:
        - name: userID
          in: header
          description: ''
          required: false
          example: ef378f73-1c52-435e-90f2-6a9cd2258c8e
          schema:
            type: string
        - name: x-ctyun-user-id
          in: header
          description: ''
          example: '{{userID}}'
          schema:
            type: string
        - name: Accept-Language
          in: header
          description: en-US
          example: zh-CN
          schema:
            type: string
        - name: userId
          in: header
          description: ''
          example: '257230714868618'
          schema:
            type: string
            default: '257230714868618'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                regionID:
                  type: string
                  description: 资源池ID
                azName:
                  type: string
                  description: 支持多az的资源池，可用区必填
                flavorType:
                  type: string
                  description: >-
                    规格类型
                    取值范围：[CPU、CPU_S6、CPU_C6、CPU_M6、CPU_S3、CPU_C3、CPU_M3、CPU_IP3、GPU_N_T4_V、GPU_N_V100、GPU_N_V100_V、GPU_N_P2V_RENMIN、GPU_N_PI7、GPU_N_G7_V、GPU_N_V100、GPU_N_T4_JX]，支持类型会随着功能升级增加
                flavorName:
                  type: string
                  description: '规格名称 '
                flavorCPU:
                  type: integer
                  description: VCPU个数
                  format: int32
                flavorRAM:
                  type: integer
                  description: 存大小，单位为G
                  format: int32
                flavorArch:
                  type: string
                  description: 指令集架构 (x86/arm/sw_64)
                flavorSeries:
                  type: string
                  description: >-
                    规格系列  
                    取值范围：s：通用型，c：计算增强型，m：内存优化型，hs：海光通用型，hc：海光计算增强型，hm：海光内存型，fs：飞腾通用型，fc：飞腾计算增强型，fm：飞腾内存优化型，ks：鲲鹏通用型，kc：鲲鹏计算增强型，km：鲲鹏内存优化型，g：GPU图形加速基础型，p：GPU计算加速型，ip3：超高IO型，kir3：鲲鹏超高IO型
                flavorID:
                  type: string
                  description: '规格ID  '
                nicCount:
                  type: integer
                  description: 网卡个数（暂不支持）
                decID:
                  type: string
                  title: 计算专属云ID
                  description: 查询指定专属云下关联的云主机规格
                instanceID:
                  type: string
                  title: 云主机ID
                  description: 支持过滤支持变配的规格
              required:
                - regionID
              x-apifox-orders:
                - regionID
                - azName
                - flavorID
                - flavorType
                - flavorName
                - flavorCPU
                - flavorRAM
                - flavorArch
                - flavorSeries
                - nicCount
                - decID
                - instanceID
            example: "{\r\n    \"regionID\": \"2022guizhou_syj\",\r\n    \"azName\": \"cn-xinan1-1A\",\r\n    \"instanceID\": \"141e11aa-768a-44ae-10e2-358d4d1fc0e2\"\r\n    // \"flavorName\": \"ks1.medium.2\",\r\n    // \"flavorType\": \"CPU\",\r\n    // \"flavorSeries\": \"s\",\r\n    // \"flavorArch\": \"\"\r\n}"
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  returnObj:
                    type: object
                    properties:
                      flavorList:
                        type: array
                        items:
                          type: object
                          properties:
                            flavorType:
                              type: string
                              description: >-
                                规格类型，取值范围：[CPU、CPU_S6、CPU_C6、CPU_M6、CPU_S3、CPU_C3、CPU_M3、CPU_IP3、GPU_N_T4_V、GPU_N_V100、GPU_N_V100_V、GPU_N_P2V_RENMIN、GPU_N_PI7、GPU_N_G7_V、GPU_N_V100、GPU_N_T4_JX]，支持类型会随着功能升级增加
                            cpuInfo:
                              type: string
                              description: cpu架构
                            pps:
                              type: integer
                              format: int32
                              description: 最大收发包限制
                            bandwidth:
                              type: integer
                              description: 宽带(不支持)
                              format: int32
                            gpuType:
                              type: string
                              description: >-
                                GPU类型，取值范围：T4、V100、V100S、A10、A100、atlas 300i
                                pro、mlu370-s4，支持类型会随着功能升级增加
                            gpuCount:
                              type: string
                              description: GPU设备数量
                            baseBandwidth:
                              type: integer
                              format: int32
                              description: 基准带宽
                            flavorName:
                              type: string
                              description: 云主机规格名称
                            flavorSeries:
                              type: string
                              description: >-
                                云主机规格系列，规格系列说明：<br />s（通用性），<br />c（计算增强型），<br
                                />m（内存优化型），<br />hs（海光通用型），<br />hc（海光计算增强型），<br
                                />hm（海光内存优化型），<br />fs（飞腾通用型），<br
                                />fc（飞腾计算增强型），<br />fm（飞腾内存优化型），<br
                                />ks（鲲鹏通用型），<br />kc（鲲鹏计算增强型），<br
                                />kc（鲲鹏内存优化型），<br />p（GPU计算加速型），<br
                                />g（GPU图像加速基础型），<br />ip3（超高IO型）
                            nicMultiQueue:
                              type: integer
                              format: int32
                              description: 网卡多队列数目
                            flavorCPU:
                              type: integer
                              format: int32
                              description: VCPU个数
                            flavorRAM:
                              type: integer
                              format: int32
                              description: 内存
                            flavorID:
                              type: string
                              description: 云主机规格ID
                            gpuVendor:
                              type: string
                              description: GPU厂商
                            videoMemSize:
                              type: string
                              description: GPU显存大小
                            available:
                              type: boolean
                              description: 是否可用（true：可用；false：不可用，已售罄）
                            azList:
                              type: array
                              items:
                                type: string
                              description: 多az名称列表(不支持)
                            flavorSeriesName:
                              type: string
                              description: 规格系列名称，参照参数flavorSeries说明
                            availableNum:
                              type: integer
                              description: 库存数量(非公有云协议)
                          x-apifox-orders:
                            - cpuInfo
                            - baseBandwidth
                            - flavorName
                            - flavorType
                            - flavorSeries
                            - nicMultiQueue
                            - pps
                            - flavorCPU
                            - flavorRAM
                            - bandwidth
                            - flavorID
                            - gpuVendor
                            - videoMemSize
                            - gpuType
                            - gpuCount
                            - available
                            - availableNum
                            - azList
                            - flavorSeriesName
                    required:
                      - flavorList
                    description: 返回参数
                    x-apifox-orders:
                      - flavorList
                  'statusCode ':
                    type: integer
                    description: 返回状态码(800为成功，900为失败)
                    format: int32
                  errorCode:
                    type: string
                    description: 具体错误码标志
                  message:
                    type: string
                    description: 失败时的错误信息
                  description:
                    type: string
                    title: ' '
                    description: '失败时的错误描述 '
                required:
                  - returnObj
                x-apifox-orders:
                  - returnObj
                  - 'statusCode '
                  - errorCode
                  - message
                  - description
              example:
                description: 成功
                errorCode: SUCCESS
                message: success
                returnObj:
                  flavorList:
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 96
                      flavorID: 091de317-593a-9247-53b5-c981aa46e65b
                      flavorName: ''
                      flavorRAM: 768
                      flavorSeries: m
                      flavorSeriesName: 内存优化型
                      flavorType: SERIES-8-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 16
                      flavorID: 01c3f5c2-ebcc-ffce-02e7-e85fcc9f990d
                      flavorName: 计算增强型(c3)
                      flavorRAM: 32
                      flavorSeries: c
                      flavorSeriesName: 计算增强型
                      flavorType: SERIES-3-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 16
                      flavorID: 0271a8c4-104e-c5dc-246c-c179940a0426
                      flavorName: 通用型(s2)
                      flavorRAM: 64
                      flavorSeries: s
                      flavorSeriesName: 通用性
                      flavorType: public
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 2
                      flavorID: 0779ddaa-2d48-7287-1e84-394610cf701b
                      flavorName: 计算增强型(c6)
                      flavorRAM: 0
                      flavorSeries: c
                      flavorSeriesName: 计算增强型
                      flavorType: public
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 2
                      flavorID: ed00cf9c-7fcc-8087-b94a-99264b165f74
                      flavorName: 通用型(s6)
                      flavorRAM: 4
                      flavorSeries: s
                      flavorSeriesName: 通用性
                      flavorType: OPTIMIZE-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 2
                      flavorID: 0490c977-79f8-c9f5-d53f-0b1a22f00b4a
                      flavorName: 计算增强型(c3)
                      flavorRAM: 4
                      flavorSeries: c
                      flavorSeriesName: 计算增强型
                      flavorType: SERIES-3-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 32
                      flavorID: 058725a1-fd7b-c324-0ef6-9e2f263ecd41
                      flavorName: 海光-计算增强型(hc1)
                      flavorRAM: 128
                      flavorSeries: hc
                      flavorSeriesName: 海光计算增强型
                      flavorType: HAIGUANG-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                    - available: null
                      azList: null
                      bandwidth: 0
                      baseBandwidth: 0
                      cpuInfo: x86
                      flavorCPU: 1
                      flavorID: 67371e90-ef95-904e-1f9b-f9ece3613f4b
                      flavorName: 通用型(s7)
                      flavorRAM: 2
                      flavorSeries: s
                      flavorSeriesName: 通用性
                      flavorType: SERIES-7-ZONE
                      gpuCount: null
                      gpuType: null
                      gpuVendor: null
                      nicMultiQueue: 0
                      pps: 0
                      videoMemSize: null
                statusCode: 800
          headers: {}
          x-apifox-name: successful operation
      security: []
      x-ctstackv2-id-path: ''
      x-ctstackv2-name-path: ''
      x-apifox-folder: 计算/云主机规格
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/4152543/apis/api-154988141-run
components:
  schemas: {}
  securitySchemes: {}
servers: []
security: []

```