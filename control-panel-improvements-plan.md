# Control Panel 存储、Worker 与端口映射改进实施计划

## 目标

按 `control_panel/docs/design-nfs-worker-notebook-improvements.md` 实现持久化存储快照、正确磁盘拓扑、Worker 健康检查与依赖安装、Notebook 元数据，以及简化且可编辑的 NodePort 映射。全程遵循测试先行：每项先增加会因缺失行为而失败的测试，再写最小实现并保持全套测试通过。

## 任务

- [x] **1. 数据库与配置基础**：先在 `internal/db/*_test.go`、`internal/config/config_test.go` 增加失败用例，再扩展 `migrations.go`、`models.go`、`workers.go`，新增存储快照和 Notebook 元数据仓储，并在 `config.go` 加入心跳、采集、超时、并发、新鲜度和保留挂载点配置。→ 验证：迁移可从现有库升级且重复执行安全，非法配置明确失败，`go test ./internal/db ./internal/config` 通过。

- [x] **2. 修复依赖安装与 Worker 状态**：先在 `internal/storage/deps_test.go`、`handlers_test.go`、`internal/workers/service_test.go` 重现 `yum/dnf` 存在但 `apt` 缺失、root/免密 sudo、状态不回写等场景；再修改 `deps.go`、`storage/handlers.go`、`workers/service.go` 和 API handler，实现权限预检、条件式包管理器探测、服务验证及手动测试状态更新。→ 验证：回归用例从红转绿，错误步骤和 stderr 可诊断。

- [x] **3. 重建磁盘拓扑与安全候选识别**：先扩充 `internal/storage/inventory_test.go`，覆盖 SATA/NVMe、整盘/分区 PV、系统 LVM、`/data01`、空白分区、签名设备、多 PV VG 和跨盘 LV；再重构 `inventory.go`，解析父子设备、LVM segment、挂载和容量口径，并为候选返回阻断原因与操作前实时复检。→ 验证：所有夹具正确归类，任何 `/data01` 所属整盘均不可初始化，未知容量不再输出为 0。

- [x] **4. 实现后台 Collector 与持久化快照**：先新增采集器测试，验证并发上限、错峰、请求合并、成功替换、失败保留和关闭取消；再新增 `internal/collector`（或等价包），接入 `cmd/server/main.go`，实现 60 秒心跳、5 分钟存储采集和变更任务后的目标刷新。→ 验证：测试中单节点失败不影响其余节点，重启后可读取最近成功快照。

- [x] **5. 将存储 API 和 NFS 页面切换为缓存模式**：先在 `internal/api/handlers_storage_test.go` 增加无同步 SSH、首次无数据、过期、失败保留及刷新入队测试；再修改 `handlers_storage.go`、`router.go`、`web/app.js` 和 `styles.css`，增加刷新接口、快照状态和“物理盘→PV/VG→LV”分组界面。→ 验证：缓存接口不调用 Runner，页面可显示新鲜/较旧/刷新中/失败状态及跨盘存储池。

- [x] **6. 实现 Notebook 使用人与备注**：先在 DB、Kubernetes Pod 和 API 测试中覆盖稳定标签继承、UID 回退、Pod 替换、清空、权限和审计；再扩展 `internal/k8s/pods.go`、`internal/api/handlers_k8s.go`、`router.go` 与 `web/app.js`，批量关联并编辑使用人和备注。→ 验证：有稳定标签时跨 UID 继承，缺标签时不继承，备注按纯文本安全显示。

- [x] **7. 简化并支持原地编辑 NodePort**：先在 `internal/k8s/services_test.go`、`handlers_test.go`、`networkpolicies_test.go` 与 API 测试中覆盖简化 DTO、自动分配、指定端口、重复/冲突、乐观并发、增删改、最后一行删除和回滚；再修改 `services.go`、`handlers.go`、`handlers_k8s.go`、`router.go`，派生 `port=targetPort=pod_port`，新增多端口 Service/NetworkPolicy 原地更新任务。→ 验证：仅可更新本面板资源，`resourceVersion` 冲突不覆盖，Service 与 NetworkPolicy 最终一致。

- [x] **8. 完成端口映射动态行界面**：修改 `web/app.js` 与 `styles.css`，移除 ClusterIP、协议和冒号文本语法，加入可增删动态行、NodePort 留空提示、已有映射编辑、`NodePort → Pod 端口` 展示及删除最后一行确认。→ 验证：浏览器中可批量创建、自动分配、原地编辑和整组清理；外部 Service 仅只读。

- [x] **9. 最终验证与验收（最后执行）**：在 `control_panel/backend` 运行 `gofmt`、`go test ./...`、`go vet ./...`，启动 `control_panel/run_dev_server.ps1` 完成 Worker、NFS、Notebook 备注和 NodePort 关键流程浏览器回归，并用 100 个缓存 Worker 数据验证 NFS 首屏/接口小于 1 秒。→ 验证：命令零错误，设计文档第 20 节全部验收项通过。

## 依赖顺序

任务 1 是共同基础；任务 2、3、6、7 可在其后独立推进；任务 4 依赖任务 2、3；任务 5 依赖任务 4；任务 8 依赖任务 6、7；任务 9 必须最后执行。关键路径为 **1 → 3 → 4 → 5 → 9**。

## 完成条件

- [x] 已确认设计中的 16 条验收标准全部通过。
- [x] 每个新增或修复行为均有先失败、后通过的自动化测试。
- [x] 未扩大 Kubernetes 权限，未记录 SSH 凭证或敏感备注内容。
- [x] `/data01` 保护与磁盘变更前实时复检在后端强制执行。
