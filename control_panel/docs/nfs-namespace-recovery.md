# NFS 虚拟盘残留挂载自动回收

## 行为

`storage_delete_lv` 和 `storage_reclaim_nfs` 共用删除流程。业务 Pod 仍引用卷，或者 Kubernetes 查询结果不确定时，保留逻辑卷。首次 `lvremove` 明确报文件系统占用后，扫描其他进程的挂载命名空间，核实全部持有者的工作负载身份。只有显式许可的日志采集容器才允许执行普通卸载；再次确认设备身份、残留挂载消失、Open Count=0，复查业务使用后，仅额外重试一次删除。

不自动重启 Promtail，不删除 Pod，不终止业务进程，不使用强制或延迟卸载。任务日志保留首次删除失败和最终恢复结果，清理失败不会显示成功。

## 启用条件

自动清理默认关闭，许可名单为空。Git 推送、Chart 升级或镜像更新不会自动给所有容器授权。

1. 使用单个 control_panel 后端实例，避免同一节点登记为多个 worker；回收期间不并行手工修改 LVM。
2. 所有虚拟盘删除的目标 worker 安装 `python3`（3.7及以上）、GNU `timeout`（coreutils）、`lvm2`，并具备读取完整 `/proc`、进入 mount namespace、chroot 及普通卸载所需权限。新工具前置条件不由旧版“安装依赖”按钮自动保证。
3. 控制面服务账号需要现有 Pods/PVC/PV/Nodes 只读权限和新增的 `apps/daemonsets get`。无需增加 Pod 或 DaemonSet 删除/修改权限。
4. 先在独立 Linux 测试环境验证 namespace/root 和普通卸载行为；Windows Go/Python 解析测试不等于 Linux 内核验证。
5. 核对真实的命名空间、DaemonSet 名称和容器名称，再配置精确的 `namespace/daemonset/container`。例如 `monitoring/promtail/promtail` 仅为示例，不能从某次 `promtail-xxxxx` Pod 名或 PID 推断永久身份。

许可名单中的工作负载应是受信任的日志采集程序；限制该命名空间中创建或修改 Pod/DaemonSet 的权限。许可意味着管理员允许移除已停用卷在该容器中的残留挂载，不保证日志采集完全无影响。

## 配置

| 环境变量 | Helm values | 默认值 |
| --- | --- | --- |
| `NAMESPACE_CLEANUP_ALLOWLIST` | `config.namespaceCleanupAllowlist`（字符串列表） | 空列表，关闭自动清理 |
| `NAMESPACE_CLEANUP_TIMEOUT` | `config.namespaceCleanupTimeout` | `60s` |
| `NAMESPACE_UNMOUNT_TIMEOUT` | `config.namespaceUnmountTimeout` | `10s` |

环境变量许可名单使用逗号分隔；不支持通配符。总恢复预算最多5分钟，单次卸载期限最多10秒，且单次期限不能超过总预算。配置错误阻止启动。

Helm 中可以配置 `config.namespaceCleanupAllowlist: ["monitoring/promtail/promtail"]`，替换为已经核对的实际名称。原生清单在 `deploy/deployment.yaml` 配置同名环境变量。清空名单并重启后端即可关闭自动恢复；已经完成的卸载不会因此自动恢复。

## 保守拒绝情形

首版只支持明确识别的独立普通 LV 与安全叶子挂载。未知持有者、未知导出路径、运行时身份不匹配、主机进程、复杂/层叠/子挂载、存在未核实的向外传播风险、保护目录、快照/薄池等复杂逻辑卷、缺少工具或权限，均停止自动操作并报告原因。

宿主机挂载与残留命名空间挂载均检查目标和父挂载传播属性。不会为了清理目标而修改传播设置或递归卸载其他设备。执行器使用可信宿主机解释器和普通卸载系统调用，不执行容器提供的 `umount`、动态加载器或辅助程序。

如果卷已经在宿主机卸载且无法证明当前导出路径，会采用保守业务检查，并拒绝不能授权的自动清理。历史任务参数和旧 fstab/exports 条目只作线索。

## 执行状态不明

远端恢复执行器在改变挂载前创建 `/run/control-panel-storage-recovery.uncertain`。只有确认执行器及其子进程结束时才清除标记。超时、连接丢失或退出情况不明时保留标记，阻止该节点后续存储命令，避免与尚在运行的执行器交错。后端同时将该 worker 加入进程内隔离名单，覆盖尚未确认远端标记创建的连接失败情况；仅在维护人员核实远端执行器已退出、挂载状态一致后，才可解除标记并重启后端以清除本地隔离。

出现该标记时由维护人员先只读确认恢复执行器已经结束、挂载和设备身份状态，再决定是否移除标记并重试。不能为了继续删除而直接清除标记；无法终止的内核等待需要节点维护处理。此标记不替代对外部管理员和控制器操作的协调。

## 已有现场证据与验收范围

用户已在 worker-1-10 验证普通 `nsenter -t PID -m umount` 后 Open Count归零，并成功删除对应LV。这验证了恢复顺序，但不是新执行器的隔离测试。

发布应分别报告 Go回归测试、Python纯解析/安全测试、Helm/RBAC验证和Linux隔离验证结果。没有Linux隔离验证时保持许可名单为空，不宣称自动恢复已验证生产可用。
