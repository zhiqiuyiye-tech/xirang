# Control Panel NFS、Worker、Notebook 元数据与端口映射改进设计

- 状态：已确认
- 日期：2026-09-25
- 范围：`control_panel`

## 1. 背景与目标

当前控制面板存在以下问题：

1. 每次进入 NFS 页面都会同步 SSH 探测全部 Worker，导致页面加载缓慢。
2. 物理盘角色判断不准确，普通数据盘经常被显示为系统盘，剩余容量显示为 0；虚拟盘未按底层物理数据盘归组；挂载到 `/data01` 的 Kubernetes 保留盘未被特殊保护。
3. 安全可用的未挂载整盘或分区无法稳定识别为 NFS 初始化候选。
4. Worker 状态长期停留在 `unknown`；安装 NFS/LVM 依赖在 `detect_pm` 阶段失败。
5. Notebook Pod 的端口映射页面缺少使用人与备注信息；创建映射还要求管理员理解并填写 Service 中间端口，输入格式复杂，且本面板创建的多端口 Service 不能逐条维护端口。

本设计面向控制面板管理员，在不改变现有主要技术栈的前提下，提高页面响应速度、磁盘识别正确性、远程运维可靠性和 Notebook 使用归属的可见性。

## 2. 已确认需求

- NFS 页面进入后应在 1 秒内展示最近缓存，不再同步等待所有 Worker 的 SSH 探测。
- NFS 存储清单默认每 5 分钟后台刷新，支持刷新全部 Worker 或单个 Worker。
- Worker 默认每 60 秒执行轻量 SSH 心跳。
- 采集失败时保留最近一次成功数据，同时显示采集时间、过期状态和本次错误。
- 缓存跨控制面板重启保留。
- 磁盘需要区分系统盘、普通数据盘、LVM 数据盘、未使用设备和 Kubernetes 保留盘。
- 只要物理盘本身或任一后代设备挂载到 `/data01` 或其子目录，整块物理盘均禁止用于 NFS。
- 可用裸设备包括完全空白的整盘，以及未挂载、无文件系统、无已知签名、非 PV 的独立分区。
- NFS 虚拟盘按“物理盘 → 分区/PV → VG → LV”展示；跨盘 VG/LV 单独分组。
- Worker 状态使用 `online/offline/unknown`，手动测试必须立即回写状态。
- 依赖安装兼容 RHEL 系和 Debian/Ubuntu，并支持 `root` 与免密 `sudo` 普通账号。
- Notebook 提供“使用人”和“备注”两个字段，同时记录修改人和修改时间。
- 端口映射创建仅支持 NodePort/TCP，每条规则只填写 Pod 内部端口和可选的外部 NodePort。
- Service 中间端口自动等于 Pod 内部端口；外部 NodePort 留空时由 Kubernetes 自动分配。
- 一次可通过动态行提交多条映射，并可原地新增、修改或删除本面板创建的多端口 Service 中的端口。
- 备注仅供已登录管理员查看和修改。
- 预期规模为 20–100 个 Worker、100–1000 个 Notebook。
- 心跳周期、清单刷新周期、SSH 超时、并发数和保留挂载点列表均可配置。

## 3. 非目标

- 不重构现有管理员认证为完整的多角色权限系统。
- 不自动擦除已有文件系统、PV、分区表或无法确认用途的设备。
- 不修改 `/data01` 上的数据、挂载或 Kubernetes 工作负载。
- 不自动拆分已有的跨盘 VG。
- 不改变 Notebook 调度、创建或销毁机制。
- 不将备注写入 Pod Annotation，避免扩大 Kubernetes Pod 写权限。
- 端口映射不支持 UDP、ClusterIP 或自定义 Service 中间端口。
- 控制面板不自行随机选择 NodePort；留空时始终由 Kubernetes API Server 分配。

## 4. 假设

- 控制面板继续以单实例运行；当前部署与 Helm Chart 均为单副本。
- 使用现有 SQLite 数据库存储快照与 Notebook 元数据。
- Worker 可通过现有 SSH 凭证访问，并具备 `lsblk`、`findmnt`、`df` 等基础工具。
- 控制面板新建 VG 继续遵循“一块物理盘一个 VG”；已有跨盘 VG 只进行正确识别与展示。
- Notebook 的 `workspace_id`、`project_id` 标签在存在时具有业务稳定性。
- 缺少稳定标签时，备注仅绑定当前 Pod UID，不跨重建继承。
- 备注只允许填写业务识别信息，不用于保存密码、密钥或令牌。

## 5. 当前根因

### 5.1 NFS 页面慢

NFS 页面进入时调用 NFS 主机接口；该接口同步枚举 Worker，并为每个 Worker 发起完整 SSH 存储探测。虽然节点之间并发执行，但 HTTP 响应仍需等待最慢节点完成或超时，且结果没有持久化缓存。

### 5.2 磁盘角色和容量错误

现有逻辑只有 `lvm`、`unused`、`system` 三种角色。任何不是 PV、又不满足“完全无子设备的空盘”条件的磁盘都会落入 `system`，因此已有普通分区的数据盘被误判为系统盘。

物理盘剩余容量主要依赖 `pvs` 的 PV 可用空间；非 LVM 数据盘没有合适的容量口径，因此经常显示 0。虚拟盘与物理盘的关联依赖不可靠的简化关系，没有完整使用 LVM segment/device 信息。

### 5.3 裸盘漏检

现有候选规则只接受完全没有任何子设备的 `TYPE=disk`。已经创建但仍为空白、未挂载的分区会导致父盘被整体排除，分区自身也不会成为候选。

### 5.4 Worker 一直为 unknown

Worker 创建时状态默认为 `unknown`。手动连接测试只返回成功或失败，不调用数据库状态更新；系统也没有周期性健康检查。

### 5.5 detect_pm 误判

现有包管理器探测依次执行 `yum`、`dnf`、`apt` 检查，但整条 Shell 命令的最终退出码由最后一个 `apt` 检查决定。在 RHEL 系节点上，即使已经输出 `yum` 或 `dnf`，只要没有 `apt`，最终退出码仍为 1，任务便被错误标记为 `detect_pm failed`。

### 5.6 Notebook 无持久备注

当前 Kubernetes Service 与 Pod 视图没有备注字段，也没有本地 Notebook 元数据模型。Pod UID 会在重建后变化，不能单独作为需要继承备注时的稳定键。

### 5.7 端口映射创建与维护复杂

当前页面要求使用逗号和冒号组合输入 `Service.port`、`targetPort` 与 `nodePort`，并要求管理员理解 Kubernetes Service 的中间端口。创建接口也直接接受这些可相互矛盾的底层字段。多条映射会进入同一个 Service，但后续只能删除整个 Service，不能原地维护其中的单条端口。

## 6. 总体方案

采用“内置后台采集器 + SQLite 最近成功快照”。

### 6.1 职责划分

- `Collector`：执行 Worker 心跳和存储清单采集，负责调度、并发限制、错峰与同节点请求合并。
- 存储快照仓储：持久化每个 Worker 最近一次成功清单和最近一次尝试结果。
- Worker 服务：维护在线状态、最近检查时间、最近成功时间和错误摘要。
- 现有任务引擎：继续负责安装依赖、创建 VG/LV、导出 NFS 等会改变远端状态的操作。
- Notebook 元数据仓储：保存使用人、备注和稳定关联键。

### 6.2 数据流

1. 服务启动后立即开放 HTTP，并从 SQLite 返回已有快照。
2. `Collector` 启动后错峰安排 Worker 心跳与存储采集。
3. 页面读取缓存接口，不直接触发同步 SSH。
4. 手动刷新请求进入有界队列；同一 Worker 已排队或执行中时合并请求。
5. 完整采集成功后，在事务中替换成功快照并清除错误。
6. 完整采集失败时，只更新最近尝试时间和错误，不覆盖成功快照。
7. 变更类任务成功后，主动请求刷新目标 Worker。

## 7. 数据模型

### 7.1 `storage_inventory_snapshots`

建议字段：

- `worker_id`：主键并关联 Worker。
- `schema_version`：快照 JSON 结构版本。
- `payload_json`：最近一次成功的完整清单。
- `collected_at`：最近成功采集时间。
- `last_attempted_at`：最近尝试时间。
- `last_error`：最近失败的安全错误摘要，可为空。
- `updated_at`：记录更新时间。

`refreshing` 属于进程内瞬时状态，不持久化。服务重启后所有刷新状态重新进入正常调度，避免遗留永久“刷新中”。

### 7.2 `worker_nodes` 扩展

保留现有 `status` 与 `last_seen_at`，新增：

- `last_checked_at`：最近一次心跳检查时间。
- `status_error`：最近心跳错误摘要。
- `health_failures`：连续失败次数，用于防抖。

语义：

- `unknown`：从未完成心跳。
- `online`：最近心跳成功。
- `offline`：连续两次心跳失败。
- `last_seen_at`：只在成功时更新。

### 7.3 `notebook_metadata`

建议字段：

- `stable_key`：主键，包含键版本。
- `key_kind`：`business_labels` 或 `pod_uid`。
- `namespace`。
- `workspace_id`、`project_id`，可为空。
- `last_pod_uid`。
- `owner_name`：使用人，最多 100 字。
- `note`：备注，最多 1000 字。
- `updated_by`。
- `created_at`、`updated_at`。

两个业务字段同时为空时删除记录。

## 8. 采集器设计

### 8.1 调度

- Worker 心跳默认周期：60 秒。
- 存储清单默认周期：5 分钟。
- 默认并发数：8。
- 心跳默认超时：5 秒。
- 完整存储探测使用独立、可配置的较长超时。
- 节点按稳定哈希分散到周期窗口，避免同一时刻集中发起 SSH。
- 每个 Worker、每类探测最多允许一个排队或执行中的请求。

### 8.2 启停与失败

- 启动时不清空快照。
- Collector 使用服务生命周期 Context，关停时停止接收新请求并取消在途探测。
- 单节点失败不影响其他节点。
- 删除 Worker 时同步删除其快照，并取消尚未执行的请求。
- 当前为单实例设计；未来增加多副本前，需要增加数据库租约或主节点选举。

### 8.3 可观测性

记录结构化日志：探测类型、Worker ID、排队耗时、执行耗时、结果和安全错误分类。不得记录密码、私钥、命令输入或完整敏感环境变量。

## 9. 磁盘拓扑与分类

### 9.1 数据来源

单次完整采集应尽量合并 SSH 往返，并获取：

- `lsblk`：设备路径、类型、父设备、容量、文件系统、挂载点、型号、序列号和 WWN。
- `findmnt`：挂载源与挂载目标。
- `df`：已挂载文件系统的总量、已用、可用和使用率。
- `pvs`：PV 路径、容量、可用 extents 和 VG。
- `vgs`：VG 总量和可用空间。
- `lvs --segments`：LV、路径、容量和实际 devices。
- `wipefs` 的只读探测：确认候选设备不存在已知签名。
- NFS 服务状态与导出配置。

命令应使用机器可解析格式；对版本差异提供兼容回退和明确的“能力缺失”错误。

### 9.2 拓扑构建

1. 建立所有块设备的父子图。
2. 将分区、device-mapper、LVM、RAID 等节点追溯到顶层物理盘。
3. 根据 mount source 解析实际设备，再向上标记所有祖先物理盘。
4. 将 PV 映射到分区或整盘，再映射到物理盘。
5. 使用 LVM segment devices 将 LV 映射到一个或多个 PV/物理盘。

拓扑无法唯一解析的 RAID、多路径或异常 device-mapper 设备默认不可自动初始化，但仍可只读展示。

### 9.3 系统盘与保留盘

- 承载 `/`、`/boot`、`/boot/efi` 的物理盘标记 `is_system=true`。
- 承载 `/data01` 或其子目录的物理盘标记 `is_reserved=true`。
- 保留挂载点列表可配置，路径比较需要清理重复斜杠并按目录边界判断，不能把 `/data010` 误判为 `/data01` 子目录。
- 同一物理盘可以同时带多个标志；任一系统或保留标志都会使该盘及其后代设备失去 NFS 初始化资格。

### 9.4 设备角色

建议向前端返回明确角色和独立标志，而不是只返回单一互斥字符串：

- 系统盘。
- Kubernetes 保留盘。
- 普通数据盘。
- LVM 数据盘。
- 可初始化整盘。
- 可初始化分区。
- 不可识别或禁止操作。

每个不可操作设备返回 `blocked_reasons[]`，例如 `system_disk`、`reserved_mount:/data01`、`has_filesystem`、`already_pv`、`has_children` 或 `ambiguous_topology`。

### 9.5 裸设备候选规则

整盘候选必须：

- 类型为物理磁盘。
- 没有子分区或映射。
- 未挂载。
- 无文件系统或已知签名。
- 不是 PV。
- 不属于系统盘或保留盘。

分区候选必须：

- 类型为普通分区。
- 未挂载。
- 无文件系统或已知签名。
- 不是 PV。
- 没有依赖它的映射设备。
- 所属物理盘不是系统盘或保留盘。

创建 PV/VG 前必须重新实时执行同一套校验，并比对设备路径、类型、容量、序列号/WWN。缓存只用于展示，不能作为破坏性操作的唯一依据。

## 10. 容量口径

不再用一个含义不明的 `free_gb` 表示所有设备：

- `filesystem_available_bytes`：来自 `df`，仅适用于已挂载文件系统。
- `pv_free_bytes`：来自 `pvs`，表示单个 PV 可分配 extents。
- `vg_free_bytes`：来自 `vgs`，表示 VG 可分配容量。
- `candidate_bytes`：空白整盘或分区可用于初始化的容量。
- `lv_filesystem_available_bytes`：已挂载 LV 的文件系统可用量。

未挂载 LV 无法通过通用、安全方式获得文件系统内部剩余量时返回 `null`，前端显示“未知”，不得显示为 0，也不得假设等于 LV 总容量。

跨多个 PV 的 VG，其 VG 可用容量只显示一次；各 PV 显示自身 `pv_free_bytes`。LV 通过 segment devices 列出全部底层物理盘。

## 11. NFS 页面设计

### 11.1 页面加载

页面进入时并行读取 Worker 基础列表和存储快照，立即渲染已有数据。每个 Worker 独立显示：

- 新鲜：最近成功采集在新鲜度阈值内。
- 较旧：存在成功快照但已超过阈值。
- 刷新中。
- 采集失败：显示旧数据、失败时间和原因。
- 尚无数据：从未成功采集。

默认新鲜度阈值建议为两个采集周期，即 10 分钟，并允许配置。

### 11.2 分组展示

按物理盘卡片展示：

1. 物理盘身份、型号、容量和角色标志。
2. 分区或整盘 PV。
3. 对应 VG 及可分配容量。
4. LV、挂载点、文件系统容量、NFS 导出状态和操作。

跨盘 VG/LV 放入“跨盘存储池”区域，列出全部成员物理盘，避免在多个盘卡片中重复显示并造成误解。

### 11.3 刷新

- 页面提供“刷新全部”。
- 每个 Worker 提供“刷新此节点”。
- 请求立即返回，不阻塞 HTTP 到 SSH 完成。
- 前端轮询缓存状态，仅替换完成的节点卡片。
- 重复请求被后端合并。

## 12. Worker 健康检查

- 心跳只验证 SSH 建连、认证和简单固定命令执行，不执行包管理或磁盘命令。
- 单次失败先累计失败次数；连续两次失败后置为 `offline`。
- 任一次成功立即置为 `online`，清空错误和失败计数，并更新 `last_seen_at`。
- 手动“测试连接”复用同一状态更新函数并立即回写。
- 远程任务若已明确成功建立 SSH，可更新最近成功时间；远程命令自身退出码非零不等同于 Worker 离线。
- Worker 列表接口只读数据库状态，不现场探测。

## 13. NFS/LVM 依赖安装

### 13.1 预检

1. 读取 `/etc/os-release`，识别系统家族和版本。
2. 执行 `id -u`。
3. UID 为 0 时直接执行；否则验证 `sudo -n true`。
4. sudo 不可用时立即失败，并显示“需要 root 或免密 sudo”。

### 13.2 包管理器探测

使用单一条件链，找到后显式成功退出：

```sh
if command -v dnf >/dev/null 2>&1; then
  echo dnf
elif command -v yum >/dev/null 2>&1; then
  echo yum
elif command -v apt-get >/dev/null 2>&1; then
  echo apt
else
  exit 1
fi
```

该结构修复当前由最后一个 `apt` 检查决定整条命令退出码的问题。

### 13.3 安装与验证

- RHEL 系安装 `lvm2`、`nfs-utils`。
- Debian/Ubuntu 安装 `lvm2`、`nfs-kernel-server`，使用非交互模式。
- 安装前分别检查关键命令，已满足的依赖不重复安装。
- 对包管理器锁进行有限次数、带退避的重试；网络、DNS、仓库配置错误不盲目无限重试。
- 所有特权命令统一通过经过验证的 root/sudo 执行器调用。
- 幂等更新 `/etc/nfs.conf`，保留无关配置。
- 根据系统实际存在的 systemd unit 选择 `nfs-server` 或 `nfs-kernel-server`。
- 最终验证 `lvcreate`、`exportfs` 和 NFS 服务状态。
- 任务步骤保存安全的 stdout/stderr 摘要、退出码和错误分类。
- 成功后触发 Worker 心跳和存储清单刷新。

## 14. Notebook 使用人与备注

### 14.1 稳定键

后端实时读取目标 Pod 并生成稳定键，前端不得直接提交稳定键：

- 同时存在稳定业务标签时：`v1:namespace:<ns>:workspace:<workspace_id>:project:<project_id>`。
- 标签不足时：`v1:pod_uid:<uid>`。

使用业务标签的记录可在 Pod UID 变化后继续匹配；使用 UID 的记录只匹配当前实例，并在界面提示不会跨重建继承。

### 14.2 接口与界面

Pod 列表接口批量关联元数据并返回使用人、备注摘要、关联类型、修改人和修改时间。端口映射主列表增加“使用人”与备注摘要；现有 Pod 端口映射弹窗增加编辑区域。

保存接口建议为：

- `PUT /api/v1/k8s/notebooks/:namespace/:pod/metadata`

请求只包含 `owner_name` 与 `note`。后端重新获取 Pod、计算稳定键并验证 Pod 仍存在；Pod 已被替换时返回冲突，提示用户刷新页面后重试。

### 14.3 安全与审计

- 使用人最多 100 字，备注最多 1000 字。
- 仅接受纯文本，拒绝不允许的控制字符。
- 前端统一 HTML 转义。
- 只有现有已登录管理员可以读取和修改。
- 新增、修改、清空均写审计日志；审计日志不复制备注全文，只记录动作、目标、操作者与结果。

## 15. NodePort 映射简化与原地编辑

### 15.1 简化模型

创建和更新接口只接受业务所需字段：

```json
{
  "mappings": [
    { "pod_port": 8888, "node_port": 31088 },
    { "pod_port": 6006 }
  ]
}
```

后端固定派生：

- Service 类型为 `NodePort`。
- 协议为 `TCP`。
- `Service.port = Service.targetPort = pod_port`。
- `node_port` 缺省或为 `0` 时保留为 0，由 Kubernetes API Server 分配。

控制面板不得自行查询空闲端口后随机选择，以避免检查与创建之间的竞态。创建完成后，从 Kubernetes 实际返回的 Service 读取最终 NodePort。

### 15.2 校验

- `pod_port` 必须为 `1–65535`。
- 手动填写的 `node_port` 按当前集群默认范围校验为 `30000–32767`。
- 同一次提交中不得重复 Pod 内部端口。
- 同一次提交中不得重复非零 NodePort。
- 指定 NodePort 已占用时，保留 Kubernetes 返回的冲突原因并展示为可操作错误。
- 至少需要一条映射；编辑时删除最后一条属于资源删除流程。

### 15.3 动态行界面

新增映射区域使用结构化动态行，不再解析逗号/冒号文本：

- 每行包含“Pod 内部端口”和“外部 NodePort（可选）”。
- 提供“添加一行”和删除行操作。
- NodePort 留空提示“由 Kubernetes 自动分配”。
- 协议固定 TCP，不显示协议选择。
- 已有映射统一展示为“NodePort → Pod 内部端口”。

一次提交生成一个包含多条端口的 Service 和一个对应 NetworkPolicy。本面板创建的 Service 提供“编辑映射”入口；外部 Service 保持只读。

### 15.4 原地更新

更新请求提交完整期望端口集合，并携带 Service 的 Kubernetes `resourceVersion`：

- 保持原值的 NodePort 会被保留。
- 新增行的 NodePort 留空时由 Kubernetes 分配。
- 已有行清空 NodePort 表示请求重新自动分配。
- 修改 Pod 内部端口按删除旧端口并增加新端口处理。
- 删除最后一行并经用户确认后，删除 Service 和对应 NetworkPolicy。

后端仅允许更新带 `managed-by=control-panel` 且归属目标 Pod 的 Service。更新采用 Kubernetes 乐观并发控制；`resourceVersion` 冲突时不覆盖外部变化，提示管理员刷新后重试。

### 15.5 Service 与 NetworkPolicy 一致性

NetworkPolicy 放行的是 Pod 内部端口，而不是 NodePort。更新任务先读取两个资源并保存旧状态，再计算期望状态：

1. 更新 NetworkPolicy 的内部端口集合。
2. 原地更新 Service 端口集合，保留 ClusterIP 和无关元数据。
3. 若第二步失败，尝试将 NetworkPolicy 回滚到旧状态。
4. 回滚也失败时，将任务标记为失败并明确记录“不一致、需要重试修复”，不得误报成功。

更新任务必须幂等；重试时根据期望端口集合收敛两个资源。资源被删除或 Pod UID 已变化时停止更新并返回冲突。

### 15.6 端口映射测试

覆盖以下场景：

- 单条和多条动态行创建。
- 指定 NodePort 与 Kubernetes 自动分配。
- 非法范围、重复内部端口、重复 NodePort 和已占用 NodePort。
- 原地增加、修改和删除端口。
- 清空已有 NodePort 后重新自动分配。
- `resourceVersion` 并发冲突。
- 删除最后一行后删除 Service 与 NetworkPolicy。
- NetworkPolicy 内部端口同步。
- Service 更新失败时的 NetworkPolicy 回滚，以及回滚失败的诊断。
- 外部 Service 无编辑入口且后端拒绝更新。

## 16. API 调整

建议接口：

- `GET /api/v1/storage/nfs-hosts`：读取快照并返回主机摘要，不执行 SSH。
- `GET /api/v1/storage/inventory?worker_id=`：读取指定 Worker 快照和新鲜度元数据。
- `POST /api/v1/storage/refresh`：请求刷新全部或指定 Worker，返回 `202`。
- `POST /api/v1/workers/:id/test`：执行心跳并持久化状态。
- `GET /api/v1/k8s/pods`：在现有 Pod 数据上增加批量关联的 Notebook 元数据。
- `PUT /api/v1/k8s/notebooks/:namespace/:pod/metadata`：更新使用人与备注。
- `POST /api/v1/k8s/services`：仅接受 NodePort/TCP 的简化 `mappings[]`，后端派生 Service 字段。
- `PUT /api/v1/k8s/services/:name?namespace=`：携带 `resourceVersion`，原地替换本面板 Service 的期望端口集合并同步 NetworkPolicy。
- `DELETE /api/v1/k8s/services/:name?namespace=`：继续负责整组删除，也用于删除最后一条映射后的资源清理。

快照响应需要包含：

- `data`：最近成功清单，可为空。
- `collected_at`。
- `last_attempted_at`。
- `stale`。
- `refreshing`。
- `last_error`。

对现有字段尽量保持向后兼容；新增字段采用可选或增量方式。前端与后端在同一版本发布。

## 17. 配置项

建议加入统一配置：

- Worker 心跳周期，默认 60 秒。
- Worker 心跳超时，默认 5 秒。
- 存储刷新周期，默认 5 分钟。
- 存储探测超时。
- 采集并发数，默认 8。
- 快照新鲜度阈值，默认 10 分钟。
- 保留挂载点列表，默认包含 `/data01`。
- 包管理器锁重试次数和退避时间。

配置解析需要范围校验；非法配置应在启动时明确报错，而不是静默回退。

## 18. 错误处理与安全边界

- 单个 Worker 的失败不得使 NFS 列表接口整体失败。
- 快照错误只保存经过清理和长度限制的摘要。
- 首次无快照时返回明确空状态，不阻塞到探测完成。
- 所有磁盘变更操作执行前必须实时复检。
- 系统盘、保留盘、已有签名设备、拓扑不明确设备默认拒绝自动初始化。
- SSH 密码、私钥、sudo 信息和敏感环境变量不得进入日志、快照、任务参数明文或审计日志。
- 备注以纯文本存储和显示，避免 XSS。
- 所有写接口继续使用现有认证、CSRF 与审计机制。

## 19. 测试策略

### 19.1 磁盘解析

使用表驱动固定样例覆盖：

- SATA 与 NVMe。
- 整盘 PV 与分区 PV。
- 根目录位于普通分区或 LVM。
- `/data01` 位于整盘、分区或 LVM。
- 空白整盘与空白分区。
- 已有文件系统签名但未挂载的设备。
- 单 PV VG、多 PV VG、跨盘 LV。
- 未挂载 LV。
- LVM 名称包含连字符。
- RAID、多路径或无法唯一追溯的拓扑。

断言设备角色、祖先物理盘、候选资格、阻断原因和所有容量口径。

### 19.2 Worker 与依赖安装

伪 SSH Runner 覆盖：

- `dnf`、`yum`、`apt-get`。
- root、免密 sudo、无 sudo 权限。
- “有 yum/dnf、无 apt”的回归场景。
- 已安装依赖。
- 包管理器锁。
- DNS、仓库或网络失败。
- systemd unit 不存在或启动失败。
- 安装成功但验证失败。

### 19.3 Collector

验证并发上限、错峰、请求合并、成功替换、失败保留、重启读取、上下文取消、删除 Worker 清理和变更任务完成后的联动刷新。

### 19.4 API 与数据库

覆盖迁移、缓存读取、首次无数据、过期标识、单节点与全量刷新、认证、CSRF 和错误隔离。

### 19.5 Notebook 元数据

覆盖稳定标签跨 UID 继承、缺少标签时不继承、Pod 已删除或替换、清空记录、长度限制、控制字符、HTML 转义和审计。

### 19.6 界面与性能

- NFS 页面先显示缓存，再局部更新。
- 磁盘树形分组和跨盘区域正确。
- `/data01` 相关设备无可执行初始化入口。
- Worker 测试后状态立即变化。
- Notebook 使用人与备注可新增、修改和清空。
- 端口映射使用动态行，只展示 Pod 内部端口和可选 NodePort。
- 本面板创建的多端口 Service 可原地增删改端口，外部 Service 保持只读。
- 100 个 Worker 有缓存时，NFS 列表接口和页面首屏均在 1 秒内完成。

## 20. 验收标准

1. 重复进入 NFS 页面不会触发同步全节点 SSH，且有缓存时 1 秒内展示。
2. 后台每 5 分钟刷新清单，手动刷新可用，失败节点不影响其他节点。
3. 系统盘、普通数据盘、LVM 数据盘、裸设备和 `/data01` 保留盘分类正确。
4. `/data01` 所属整块物理盘在任何 NFS 初始化入口都被禁止。
5. 安全的空白整盘和分区能够成为候选，已有签名或用途不明设备不能成为候选。
6. NFS LV 能显示其底层物理盘；跨盘 LV/VG 显示全部成员盘。
7. 各容量字段来源明确，不再把未知值展示为 0。
8. Worker 心跳与手动测试能维护 `online/offline/unknown`，不再长期停留在 `unknown`。
9. RHEL 系节点不再因不存在 `apt` 而触发 `detect_pm failed`。
10. root 和免密 sudo 场景均可执行依赖安装，失败时能看到明确步骤和原因。
11. Notebook 端口映射页面可编辑使用人与备注，并按稳定标签规则正确继承或隔离。
12. 创建端口映射时只需填写 Pod 内部端口和可选 NodePort；留空 NodePort 后能展示 Kubernetes 实际分配值。
13. 一次可通过动态行创建多条 TCP 映射，Service 中间端口始终等于 Pod 内部端口。
14. 本面板创建的多端口 Service 可原地增删改端口，并与 NetworkPolicy 保持一致；外部 Service 不可编辑。
15. 删除最后一条映射时能确认并删除 Service 与配套 NetworkPolicy。
16. 所有新增逻辑通过单元测试、API 测试、静态检查和关键页面浏览器回归。

## 21. 决策日志

| 决策 | 采用方案 | 备选方案 | 原因 |
|---|---|---|---|
| NFS 页面刷新 | 缓存即时展示、手动刷新、后台定时刷新 | 每次进入实时探测；仅手动刷新 | 同时满足速度与数据新鲜度 |
| 状态采集架构 | 内置 Collector + SQLite 快照 | 全部走任务引擎；独立采集服务 | 适合当前单实例和中等规模，避免高频任务污染 |
| 缓存失败策略 | 保留最近成功数据并显示错误 | 用失败覆盖；仅内存缓存 | 提高可用性并支持重启恢复 |
| `/data01` 保护 | 任一后代挂载命中即排除整盘 | 只排除分区；仅精确路径 | 防止误用 Kubernetes 保留盘 |
| 裸设备范围 | 空白整盘和安全空白分区 | 仅整盘；仅分区 | 兼容实际环境和现有 NFS 操作文档 |
| 虚拟盘展示 | 按物理盘层级展示，跨盘单列 | 按 VG；平铺增加列 | 直接回答 LV 实际落在哪些数据盘 |
| Worker 状态 | 60 秒 SSH 心跳，连续两次失败判离线 | 仅手动；使用 K8s Ready | 状态表示控制面板实际远程运维能力 |
| 依赖权限 | root 或免密 sudo | 仅 root；交互式 sudo 密码 | 覆盖常见安全运维方式且避免存储 sudo 明文 |
| Linux 范围 | RHEL 系与 Debian/Ubuntu | 仅 RHEL | 满足异构 Worker 环境 |
| Notebook 备注 | 本地数据库中的使用人和备注 | Pod Annotation；仅单文本 | 可审计、无需扩大 K8s 权限、支持稳定键 |
| 备注继承 | 有稳定标签时继承；否则绑定 UID | 总按命名空间；解析 Pod 名称 | 避免错误关联到其他 Notebook |
| 权限 | 现有管理员可读写 | 新增角色权限 | 当前需求不需要权限系统重构 |
| 运维参数 | 全部配置化并提供安全默认值 | 固定值 | 便于不同规模和网络环境调优 |
| 端口映射模式 | 仅 NodePort/TCP | 保留 ClusterIP；支持 UDP | 符合当前只需外部 TCP 暴露的使用方式 |
| 端口输入模型 | Pod 内部端口 + 可选 NodePort | 继续填写 Service 中间端口 | 消除不必要的 Kubernetes 实现细节 |
| NodePort 分配 | 留空时由 Kubernetes 分配 | 控制面板自行随机选择 | 避免端口检查与创建之间的竞态 |
| 多端口资源组织 | 一次提交一个多端口 Service | 每条映射一个 Service | 减少资源数量并保持现有组织方式 |
| 映射维护 | 简化 API + 原地整体更新端口集合 | 删除重建 Service | 保留既有 NodePort，避免中断和重建失败导致映射丢失 |
| 空端口集合 | 删除 Service 与配套 NetworkPolicy | 禁止删除最后一行 | 行为符合“无映射即无资源”的直觉 |
