# Control Panel NFS Notebook 挂载与用量可见性设计

- 状态：设计已确认，尚未实施
- 日期：2026-09-28
- 范围：`control_panel`

## 1. 背景

现有 NFS 存储页从 Worker 的存储快照展示逻辑卷（LV）、导出路径及容量；Notebook Pod 列表已从 Kubernetes 读取 Pod，并通过 SQLite 展示使用人和备注。端口映射页也能查看 Pod 备注，但现有接口没有关联 Pod 声明的 PVC、PVC 绑定的 PV 与 Worker 上的 NFS 导出，因此管理员无法直接判断哪个客户正在使用哪个 NFS 虚拟盘。

Kubernetes 权限目前允许控制面板读取 Pod 和 Node，不允许读取 PersistentVolumeClaim（PVC）和 PersistentVolume（PV）。本需求只增加 NFS 使用关系展示，不改变 Kubernetes 工作负载或卷配置。

## 2. 已确认需求

- 在 NFS 虚拟盘信息中显示关联的 Notebook Pod、使用人和备注。
- 挂载关系按 `Pod → PVC → PV → NFS 服务地址与导出路径` 追溯。
- 在端口映射页的 Pod 列表展示简要 NFS 使用情况；打开 Pod 配置弹窗后展示完整挂载信息。
- 支持一对多、多对多关系：一个虚拟盘可由多个 Pod 使用，一个 Pod 也可使用多个虚拟盘。
- 完整信息包括虚拟盘/导出路径、PVC/PV、Pod 内容器挂载路径和虚拟盘整体容量用量。
- 容量显示总量、已用、可用和采集时间；这些是整个虚拟盘/文件系统的卷级数据，不表示某个 Pod 或 PVC 的独立占用。
- 只纳入现有 Notebook Pod 列表中的 Pod，即名称包含 `notebook` 的 Pod；继续复用其现有使用人和备注。
- 关系随当前 Kubernetes Pod/PVC/PV 资源变化更新；容量使用最近的 NFS 存储快照。
- 对未绑定、未匹配、有歧义或不可用的数据明确标记；单个关联失败不得阻断其他页面数据。
- 仅给控制面板 Kubernetes 服务账号增加 PVC/PV 的只读 `get/list` 权限。

## 3. 目标与非目标

### 目标

1. NFS 存储页可从虚拟盘直接识别关联客户及其 Notebook Pod。
2. 端口映射页可按 Pod 查看其 NFS 卷、容器挂载路径和卷级容量状态。
3. 用唯一、可解释的匹配规则避免错误归属，并在无法确认时显示状态而非猜测。
4. 继续使用当前 API、SQLite 快照、Pod 元数据和前端实现，不引入额外维护数据。

### 非目标

- 不统计或推算每个 Pod/PVC 的独立目录用量或配额。
- 不修改 Pod、PVC、PV、NFS 导出、挂载、Service 或 NetworkPolicy。
- 不增加人工维护的 Pod—NFS 关联表，也不增加新的后台采集服务。
- 不展示非 Notebook Pod 的挂载或为其增加使用人/备注功能。
- 不解析 Pod 直接声明的 `spec.volumes[].nfs` 卷；本功能限定在 Pod→PVC→PV 的关联链。
- 不根据部分匹配、名称相似或模糊路径推测虚拟盘归属。

## 4. 假设与约束

- Notebook Pod 仍按现有名称过滤规则识别；备注沿用现有稳定键和元数据仓储。
- 容量使用现有 Worker inventory 快照中的 LV/文件系统数据；快照缺失或过期时标示未知或较旧，并显示采集时间。
- 服务地址通过规范化后与已登记 Worker 的主机地址匹配。若 NFS PV 使用未登记的 VIP、别名或不同网络地址，不自动推测归属，显示未匹配。
- 标准 Kubernetes NFS PV 从 `spec.nfs.server/path` 取地址和路径。常见 `nfs.csi.k8s.io` PV 可从已知的 `server/share` 属性提取；无法识别的 CSI 格式显示未支持/未匹配，不猜测。
- PVC/PV 只读取 Kubernetes 元数据，不读取卷内文件内容。
- 规模沿用现有设计假设：20–100 个 Worker、100–1000 个 Notebook。

## 5. 总体方案

### 5.1 接口组织与响应形状

复用现有接口并由后端统一计算关联，不新增路由或数据库表：

- `GET /api/v1/storage/nfs-hosts`：每个 Worker 的 `virtual_disks[]` 增加 `mounted_pods[]`；Worker 对象另带 `mount_association_status` 和 `unmatched_mounts[]`。
- `GET /api/v1/storage/inventory?worker_id=...`：指定 Worker 的 `lvs[]` 增加 `mounted_pods[]`；响应另带同名汇总状态和未匹配 NFS 挂载。
- `GET /api/v1/k8s/pods`：Pod 增加 `nfs_mounts[]` 和 `nfs_mounts_status`。

`mounted_pods[]` 只包含已唯一关联到该 LV 的关系，每项包含 namespace、pod_name、pod_uid、owner_name、note、pvc_name、pv_name、export_path 和 `container_mounts[]`。同一 Pod 对同一 PVC/PV 的多个 volumeMount 合并为一个关系项，挂载路径全部放入 `container_mounts[]`；不同 PVC/PV 保留为独立关系。未匹配或有歧义的关系不会塞入某个虚拟盘，而是在 Pod 的 `nfs_mounts[]` 中保留状态；若 NFS 服务地址已匹配到 Worker 候选，则同时放入该 Worker 的 `unmatched_mounts[]`，字段包括 Pod 身份、PVC/PV、NFS server/path、`status` 和可安全展示的 `reason`。服务地址未匹配到任何 Worker 时只出现在 Pod 侧。

Pod 侧每个 `nfs_mounts[]` 项包含 `status`、`reason`、`nfs_source_confirmed`、PVC/PV、容器挂载路径；仅在已匹配时包含 Worker/虚拟盘身份和容量，其他状态的容量为 null。`nfs_mounts_status` 是所有挂载项的汇总状态。Worker 侧 `mount_association_status` 按该 Worker 已解析到的 NFS PV 关联汇总；`unmatched_mounts[]` 用于展示无法安全放入某个 LV 的记录。

PVC/PV 批量查询失败时不能构造逐 claim 的失败项，因为 NFS 类型无法确认；`nfs_mounts` / `unmatched_mounts` 返回空数组，并设置 `nfs_mounts_status` / `mount_association_status` 为 `lookup_failed`，同时设置分类错误码 `nfs_mounts_error` / `mount_association_error`（如 `pvc_list_failed`、`pv_list_failed`、`pod_list_failed` 或 `k8s_client_unavailable`）。对于 `/storage/nfs-hosts` 和 `/storage/inventory`，若关联所需的 Pod 列表失败，也沿用该 lookup_failed 处理；基础存储数据仍返回。前端必须根据汇总状态显示“关联查询暂不可用”，不可把空数组解释为没有挂载。

容量来源与新鲜度口径固定为：`lv_size_gb` 保留现有 LV `size_gb`（由 LVM `lv_size`/`--units g` 得到）的数值和项目现有 GB 展示约定，不再重新换算；`filesystem_used_gb`、`filesystem_free_gb` 和 `filesystem_use_pct` 来自该 LV 挂载点的 `df` 结果，其中字节按现有 `bytesToGB` 使用十进制 GB（1 GB = 1,000,000,000 bytes）换算。LV 总量与文件系统已用/可用量可能因文件系统预留空间或元数据而不相等；不得由其中两项反算第三项。每个容量字段独立判断有效性：有效字段照常返回，无效/缺失字段为 null；`capacity.known=true` 仅当 LV 总量和所有文件系统用量字段均有效，`false` 表示至少一项未知。`known` 表示数据在最近一次采集中完整，不表示新鲜；快照过期时可以 `known=true` 且 `stale=true`。无快照时 `collected_at=null`、`stale=true`、容量字段均为 null 且 `known=false`。过期状态复用现有 `storageHandlers.staleAfter` / `STORAGE_STALE_AFTER` 配置，默认 10 分钟；`now-collected_at` 超过阈值时保留最近成功值并设 `stale=true`。容量过期不改变挂载关系状态。

Pod 侧示例：

```json
{
  "nfs_mounts": [
    {
      "status": "matched",
      "worker_id": 12,
      "worker_name": "worker-a",
      "vg_name": "vg_data",
      "lv_name": "lv_nb_200g",
      "export_path": "/data02/nfs_lv_nb_200g",
      "pvc_name": "notebook-data",
      "pv_name": "pv-notebook-data",
      "container_mounts": [
        { "container_name": "notebook", "mount_path": "/workspace/data", "read_only": false }
      ],
      "capacity": {
        "lv_size_gb": 200,
        "filesystem_used_gb": 83.5,
        "filesystem_free_gb": 116.5,
        "filesystem_use_pct": "42%",
        "known": true,
        "collected_at": "2026-09-28T02:00:00Z",
        "stale": false,
        "scope": "volume"
      }
    }
  ],
  "nfs_mounts_status": "available"
}
```

实际字段按现有 Go DTO 命名和时间格式实现；两端接口表达相同的匹配关系，未匹配记录和汇总状态也使用一致的状态枚举。新增字段为增量字段，保持现有字段及旧版前端兼容。

### 5.2 数据流

1. `/k8s/pods` 使用现有 Pod 列表并批量读取关联需要的 PVC/PV；`/storage/nfs-hosts` 与 `/storage/inventory` 读取已有 SQLite Worker 快照，并批量读取当前 Notebook Pod、PVC/PV。
2. 通过 Pod 的 `spec.volumes[].persistentVolumeClaim.claimName`，以命名空间和 Claim 名定位 PVC，再以 PVC 绑定的 PV 名定位 PV。
3. 从 Pod 常规容器和 Init Container 的 `volumeMounts` 收集该卷对应的容器名、容器挂载路径和只读状态。
4. 从 PV 提取 NFS 服务地址和导出路径，关联到 Worker inventory 中的导出与 LV；从 SQLite 批量读取相关 Pod 的使用人和备注。
5. 返回双向关联字段；网页直接渲染，不自行实现存储匹配规则。

### 5.3 批量与性能

- 不执行逐 Pod 的 PVC/PV 请求；按页面 API 请求批量读取 Kubernetes 资源并建立内存索引。
- Kubernetes 列表读取使用 API Server watch cache（`ResourceVersion=0`），并遵循请求 Context 取消。
- 容量不触发额外 SSH 探测，继续读取持久化的最近成功 inventory 快照。
- 关联结果在 API 请求中计算，不持久化；新请求反映当前 Kubernetes 状态。
- 保持既有 NFS 首屏性能验收：100 个 Worker 均有缓存、最多 1000 个 Notebook Pod 时，`/storage/nfs-hosts` 接口和 NFS 页首屏目标均小于 1 秒。新增加的 K8s 查询必须保持批量读取，不增加每 Pod/PVC 的网络往返；以集成压测验证，不满足时需回到方案讨论，不默默降低目标或引入未确认的持久化缓存。

## 6. 关联与歧义处理

### 6.1 PVC/PV 追溯

- PVC 必须按 Pod 所在命名空间与 claimName 定位。
- PVC 已绑定后才继续追踪其 `spec.volumeName` 对应的 PV。
- Pod 常规容器及 Init Container 的挂载路径按 Pod Volume 名与 VolumeMount 名关联；同一个 PVC 在多个容器中挂载时全部展示。
- 标准 NFS PV 从 `spec.nfs.server/path` 解析；仅当 CSI Driver 明确为 `nfs.csi.k8s.io` 时才视为已确认的 NFS CSI 来源，并读取 `volumeAttributes.server/share`。
- 已确认的 NFS CSI PV 缺少 server/share 或格式无法解析时，保留为 `unsupported` 项并设 `nfs_source_confirmed=true`，避免静默漏报。
- 未绑定 PVC、引用但列表中不存在的 PVC、以及 PVC 已 Bound 但其 `spec.volumeName` 在成功读取的 PV 列表中不存在，分别保留为 `pending`、`missing_claim`、`missing_pv`，并设 `nfs_source_confirmed=false`。
- 已确认是非 NFS 的 PV，以及 Driver 未明确标识为 NFS 的其他 CSI PV 不进入 `nfs_mounts[]`；若集群使用自定义 NFS CSI Driver，必须先明确加入支持列表，不能按未识别 Driver 猜测。

### 6.2 Worker、导出路径与虚拟盘匹配

1. PV 的 NFS `server` 与 `db.WorkerNode.Host` 匹配；DNS 名忽略大小写并去除尾随点，IP 使用规范化表示。使用 Go POSIX `path.Clean` 规范绝对路径；空值或相对路径无效。不把 Worker 名称、Pod 所在节点名或字符串相似性当作地址别名，也不执行 DNS 解析。
2. 标准 PV 从 `spec.nfs.server/path` 取值；受支持的 CSI PV 从 `volumeAttributes.server/share` 取值，`share` 是 NFS 导出路径根。按规范化 server 找 Worker 候选，不匹配 Worker 时仅在 Pod 侧保留 `unmatched`/`unsupported` 状态。
3. 对唯一 Worker 的快照 `NFS.Exports` 路径去重并规范化。PV path 必须等于或位于 export 目录下（路径段边界）；有嵌套 export 时选择最具体匹配路径。
4. 将选定 export 映射到包含它的 LV 挂载点；多个 LV 挂载点都可包含时选择路径最长、最具体者。
5. 完成 server 候选唯一性检查，并对嵌套 export/LV 应用“最具体路径”规则后，仍有多个 Worker/export/LV 候选才标记 `ambiguous`；不挑选第一个候选。

候选归属按“先确认来源字段，再解析 Worker”处理：NFS 来源已确认但 server/path 缺失或无效时，Pod 项优先标为 `unsupported` 并说明 `reason`。若 server 可解析且只有一个 Worker 候选，该 Worker 收到 `unmatched_mounts[]` 中的 `unsupported` 告警；若有多个 Worker 候选，Pod 项仍为 `unsupported`，每个候选 Worker 收到 `status=ambiguous`、`source_status=unsupported`、`candidate_worker=true` 的告警，不关联到 LV；若无 Worker 候选则只保留 Pod 侧记录。来源字段完整时，server 无 Worker 候选标为 `unmatched`；唯一 Worker 继续匹配 export/LV；多个 Worker 候选标为 `ambiguous`，并在每个候选 Worker 上放置候选告警，不关联到任何 LV。Worker 告警表示候选或问题，不代表已确定数据实际落在该 Worker 上。


### 6.3 状态和部分失败

`nfs_mounts[]` 表示已确认的 NFS 关系，以及需要管理员识别的未决 Pod PVC 引用。每项包含 `status`、`reason` 和 `nfs_source_confirmed`：

- `matched`：NFS 服务地址、导出路径和 LV 均唯一匹配；`nfs_source_confirmed=true`。
- `pending`：Pod 引用的 PVC 存在但尚未绑定 PV；`nfs_source_confirmed=false`，界面写明“NFS 用途尚无法确认”。
- `missing_claim`：Pod 引用的 PVC 在成功读取的批量列表中不存在，通常是资源变化竞态；`nfs_source_confirmed=false`，`reason=pvc_not_found`。
- `missing_pv`：PVC 已 Bound 且设置 `spec.volumeName`，但 PV 在成功读取的批量列表中不存在；`nfs_source_confirmed=false`，`reason=pv_not_found`。
- `unmatched`：NFS 来源已确认（标准 `spec.nfs` 或已识别的 `nfs.csi.k8s.io`），但没有对应的已登记 Worker/export/LV；`nfs_source_confirmed=true`。
- `ambiguous`：NFS 来源已确认，但存在多个 Worker/export/LV 候选；`nfs_source_confirmed=true`。
- `unsupported`：NFS 来源已确认，但标准字段缺失/格式无效，或 `nfs.csi.k8s.io` 缺少 `server/share`；`nfs_source_confirmed=true`，`reason` 标明缺失字段/格式类别。未识别为 NFS 的其他 CSI Driver 和已确认的非 NFS PV 不进入 `nfs_mounts[]`。

`reason` 使用稳定的安全代码，不返回原始 PV/NFS 配置或错误文本：缺失 PVC/PV 引用分别为 `pvc_not_found`、`pv_not_found`；Pending PVC 为 `pvc_not_bound`；未匹配使用 `worker_not_found`、`export_not_found` 或 `lv_not_found`；歧义使用 `multiple_workers`、`multiple_exports` 或 `multiple_lvs`；不支持的 NFS 来源使用 `missing_nfs_server`、`missing_nfs_path`、`missing_csi_share` 或 `unsupported_nfs_format`。`nfs_source_confirmed=true` 仅用于已知 NFS 来源（`spec.nfs` 或明确的 `nfs.csi.k8s.io` Driver），不能根据未知 CSI Driver 推断。

Pod 的 `nfs_mounts_status` 汇总规则：

1. `lookup_failed`：PVC 或 PV 批量列表请求失败，无法计算关系；`nfs_mounts=[]`，设置安全错误码 `nfs_mounts_error`（如 `pvc_list_failed`、`pv_list_failed`、`k8s_client_unavailable`），已有 Pod 和备注仍返回。不得构造逐 claim 的失败项，因为此时 NFS 类型无法确认。
2. `none`：PVC/PV 读取成功，且没有 NFS 关系或未决 claim。
3. `pending`：至少有一个 `pending` claim，且没有其他已解析关系或异常项。
4. `available`：至少一项 `matched`，且所有 NFS 项均已唯一匹配。
5. `partial`：存在 `missing_claim`、`missing_pv`、`unmatched`、`ambiguous` 或 `unsupported`，或 `matched` 与 `pending` 同时出现。每项的详细状态保留在 `nfs_mounts[]`。

Worker 的 `mount_association_status` 使用 `lookup_failed`、`none`、`available`、`partial`：查询整体失败时为 `lookup_failed`；没有 NFS PV server 候选时为 `none`；至少一项关系匹配且该 Worker 的全部关联唯一成功时为 `available`；有未匹配、歧义候选或可归属该 Worker 的 unsupported 项时为 `partial`。Pending、missing_claim、missing_pv 和无法解析 server 的 unsupported 项没有 Worker 归属，不计入 Worker 状态。多个 Worker server 候选时，对每个候选 Worker 写入带 `candidate_worker=true` 的歧义告警，但不关联到任何 LV。NFS host/inventory 查询失败时 `unmatched_mounts=[]`、各 LV 的 `mounted_pods=[]`，设置 `mount_association_error` 为安全错误码；基础存储数据仍返回。

容量状态独立于关系状态：关系可以是 `matched`，同时容量 `known=false` 或 `stale=true`。过期时保留最近成功值和采集时间；无快照时 `collected_at=null`、`stale=true`，容量字段为 null。容量未知不输出为 0；不因过期改变挂载关系状态。

PVC/PV 列表请求是批量请求；任一请求失败均为 `lookup_failed`，不使用 `partial` 代替读取失败。对 `/storage/nfs-hosts` 和 `/storage/inventory`，Notebook Pod 列表失败也按 `lookup_failed` 处理，并以 `pod_list_failed` 返回安全错误码；存储快照和基础磁盘列表仍正常返回。对 `/k8s/pods`，Pod 列表本身是主数据，Pod API 请求失败沿用该端点现有错误响应；仅 PVC/PV 查询失败时保留 Pod 和备注。`partial` 只用于查询成功但关系图中存在未解决项。已有 Service 信息和 NFS 快照不得因 PVC/PV 查询失败而整体失败。错误只返回上述安全错误码，不记录凭证或卷内数据。

## 7. 页面设计

### 7.1 NFS 存储页

- NFS 主机概览的虚拟盘列表增加“挂载 Pod / 使用人”列。
- 每个关联展示命名空间、Pod 名称、使用人和备注；多 Pod 逐项列出。
- 选定 Worker 的虚拟盘明细显示同一关联信息。
- 未匹配、有歧义或查询失败时显示状态，不隐藏为“无使用人”。

### 7.2 端口映射页

- Notebook Pod 表格增加“NFS 挂载”摘要列，显示挂载卷名和数量。
- 现有端口映射与备注弹窗增加“NFS 挂载”标签页。
- 标签页按卷展示 Worker、虚拟盘和导出路径、PVC/PV、容器及 Pod 内挂载路径、容量总量/已用/可用、使用率和采集时间。
- 多卷、多容器挂载全部可查看；卷级容量需清楚标注，不误导为 Pod 专属用量。
- 使用现有 HTML 转义与登录保护，备注按纯文本显示。

## 8. Kubernetes 权限与安全

在以下两份部署 RBAC 配置中新增 PVC/PV 的只读权限：

- `control_panel/charts/control-panel/templates/rbac.yaml`
- `control_panel/deploy/rbac.yaml`

对 `persistentvolumeclaims`、`persistentvolumes` 仅增加 `get/list`，不增加 `watch/create/update/patch/delete`。PV 是集群级资源；当前使用 ClusterRoleBinding，因此 PVC 的读取权限也覆盖所有命名空间。API 仅为 Notebook Pod 构造并返回本功能所需的关联，不把其他命名空间的 PVC 列表暴露给网页。此范围已经确认接受。

## 9. 测试与验收

### 自动化测试

- Kubernetes 关联单元测试：PVC/PV 绑定链、命名空间隔离、多个 Pod 使用同一 PVC、Pod 多 PVC、多容器及 Init Container 挂载、PVC Pending/missing claim、Bound PVC 的 missing PV、非 NFS PV、标准 NFS PV、受支持的 `nfs.csi.k8s.io` 属性及缺属性/未知 Driver 的过滤规则。
- 匹配测试：Worker Host DNS/IP 规范化但不做 DNS 解析、POSIX 路径规范化、导出目录内子路径、嵌套 export/LV 选择最具体路径、`/share` 与 `/share2` 边界、VIP/别名地址不匹配、无 Worker/多 Worker 候选、缺 server/share 和未匹配场景。
- 容量测试：LV 总量保留现有 `size_gb`/`--units g` 值；文件系统已用/可用/使用率来自 `df` 和现有十进制 GB 转换；`known=true` 仅当 LV 总量和所有 `df` 指标均有效，部分有效数据保留有效值并将缺失值设 null/known=false；stale 不改变 known；未知快照的 `stale=true`、`collected_at=null`；默认 10 分钟及自定义 `STORAGE_STALE_AFTER` 边界。
- API 测试：三个接口正反向关系字段一致，`mounted_pods[]` 只包含唯一匹配，重复 volumeMount 按 Pod/PVC/PV 合并；未匹配和候选 Worker 告警字段正确；状态汇总覆盖 none/pending/missing claim/missing PV/matched/mixed/unsupported/lookup-failed；来源字段不完整时 Pod 与 Worker 告警优先级符合规则；PVC/PV 批量查询失败返回空关联数组与 `lookup_failed`/安全错误码，存储侧 Pod 列表失败保留基础存储数据，而非伪装为 `none`。
- RBAC 验证：Helm 模板和部署 YAML 只新增 PVC/PV 的 `get/list` 权限。
- 页面回归：NFS 主机虚拟盘及 Worker 明细展示使用人；Pod 表格显示摘要；弹窗展示多卷详细信息和异常状态；备注文本安全转义。

### 验收标准

1. 管理员能从 NFS 虚拟盘看到所有匹配 Notebook Pod 的命名空间、名称、使用人和备注。
2. 端口映射 Pod 列表有 NFS 使用摘要，弹窗能查看 PVC/PV、容器挂载路径和虚拟盘级容量。
3. 多 Pod 共用卷、单 Pod 多卷和多容器挂载均完整展示。
4. 待绑定、未匹配、有歧义、查询失败、快照过期和容量未知有明确状态，不误显示为零或无挂载。
5. Kubernetes PVC/PV 权限仅为只读 `get/list`；无需数据库迁移，不改变现有卷或工作负载。
6. 对 100 个 Worker 的缓存数据和最多 1000 个 Notebook Pod，NFS 主机接口和 NFS 页首屏达到 1 秒目标；性能测试验证无逐 Pod/PVC 查询。
7. 自动化测试、RBAC 验证和关键页面回归通过。

## 10. 决策日志

| 决策 | 采用方案 | 备选方案 | 原因 |
|---|---|---|---|
| 关联来源 | Pod→PVC→PV→NFS 服务地址/导出路径 | 仅从 Pod 直接 NFS 卷推断；人工标签 | 使用 Kubernetes 声明的持久卷关系，避免手工维护 |
| 接口组织 | 扩展现有 `/storage/nfs-hosts`、`/storage/inventory` 和 `/k8s/pods`，共享后端关联逻辑 | 新聚合接口；前端合并 | NFS 主机概览、Worker 明细和 Pod 端口页复用同一关系，避免新增路由和重复匹配 |
| 关系持久化 | 请求时从 Kubernetes 与 SQLite 快照派生 | 新关联表或后台持久化 | 关系跟随当前 Pod/PVC/PV；避免额外状态与同步问题 |
| 多对多 | 双向完整列出所有关联 | 仅显示一个主要 Pod/卷 | 避免遗漏客户和挂载关系 |
| 容量口径 | 最近 inventory 中的卷级总量/已用/可用 | 推算每个 Pod/PVC 用量 | 当前采集粒度不能提供独立租户目录用量 |
| 匹配安全 | 主机与路径必须唯一匹配；不明确则标记 | 模糊匹配或优先选一个候选 | 防止把客户错误归属给其他存储盘 |
| 权限 | ClusterRole 只增加 PVC/PV `get/list` | 新增 watch 或写权限 | 页面读取关联所需的最小操作集合；不修改 Kubernetes 对象 |
| 失败策略 | 部分数据可用并标记异常 | 任一关联失败使整页失败 | 单条关系故障不应影响存储和端口映射主流程 |
| 状态模型 | 挂载项状态与 Pod/Worker 汇总状态分开；查询失败不伪装成空结果 | 单一布尔成功/失败状态 | 多对多和部分匹配时保留具体故障原因 |
| 容量新鲜度 | 沿用 `STORAGE_STALE_AFTER`，默认 10 分钟；无快照标为 stale 且数值未知 | 单独刷新 NFS Usage 或无期限显示缓存 | 复用已有快照新鲜度配置，不增加采集链路 |
| 页面位置 | NFS 虚拟盘明细显示客户/Pod；端口映射表显示摘要，弹窗显示详情 | 仅在单一页面显示 | 运维和客户归属场景都可直接查看 |
