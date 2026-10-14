## 1、安装NFS

```sql
sudo yum update -y
sudo yum install -y nfs-utils
```

## 2、配置强制使用NFSv4

```sql
sudo vi /etc/nfs.conf
```

找到 `[nfsd]` 这一节（如果没有就自己加在文件末尾），配置如下：

```conf
[nfsd]
vers2=n
vers3=n
vers4=y
vers4.0=y
vers4.1=y
vers4.2=y
```

## 3、把物理盘做成 LVM 存储池 (Volume Group)

```bash
# 0. 安装依赖
dnf install -y lvm2

# 1. 创建物理卷 (PV)
pvcreate /dev/nvme1n1p1

# 2. 创建一个名为 "vg_data" 的存储池 (VG)，把刚才的 PV 加进去
vgcreate vg_data /dev/nvme1n1p1

# 可以运行 vgs 看看，你现在拥有了一个容量为 3.5T 的资源池！
vgs
```

## 4、按需“切出”你想要的空间 (Logical Volume)

现在，你要给某个 Notebook 切一个 200G 的盘，给另一个切 500G 的盘：

```bash
# 1. 从资源池里切出一个 200G 的卷，取名叫 lv_notebook_200g
lvcreate -L 200G -n lv_notebook_200g vg_data

# 2. 从资源池里切出一个 500G 的卷，取名叫 lv_notebook_500g
lvcreate -L 500G -n lv_notebook_500g vg_data

# 可以运行 lvs 查看你切出来的卷
lvs
```

## 5、格式化并挂载为独立的文件夹

```bash
# 1. 格式化这些逻辑卷 (推荐使用 ext4 或 xfs)
mkfs.ext4 /dev/vg_data/lv_notebook_200g
mkfs.ext4 /dev/vg_data/lv_notebook_500g

# 2. 在宿主机上创建专门用来跑 NFS 的挂载点
mkdir -p /data02/notebook_a_200g
mkdir -p /data02/notebook_b_500g

# 3. 将逻辑卷挂载到对应的文件夹
mount /dev/vg_data/lv_notebook_200g /data02/notebook_a_200g
mount /dev/vg_data/lv_notebook_500g /data02/notebook_b_500g
```

(注意：为了机器重启后不掉线，你需要把它们写入 `/etc/fstab`。)

```bash
/dev/vg_data/lv_notebook_200g   /data02/notebook_a_200g   ext4    defaults    0 2
/dev/vg_data/lv_notebook_500g   /data02/notebook_b_500g   ext4    defaults    0 2
```

请注意将 `ext4` 替换为真实格式

## 6、通过 NFS 暴露出去

现在，你再去修改 NFS 的配置文件 `/etc/exports`

```bash
vi /etc/exports
```

添加上下面的内容

```bash
/data02/notebook_a_200g *(rw,sync,no_root_squash,no_subtree_check)
/data02/notebook_b_500g *(rw,sync,no_root_squash,no_subtree_check)
```

## 7、启动服务并设置开机自启

```bash
# 使挂载配置生效
sudo exportfs -arv

# 启动并设置开机自启（注意名字是 nfs-server）
sudo systemctl enable --now nfs-server

# 查看服务状态确认有没有报错
sudo systemctl status nfs-server
```


## 8、回收LVM空间

### 8.1 停止 NFS 共享并清理配置

```bash
sudo vi /etc/exports
```

把里面关于 `/data02/notebook_a_200g` 和 `/data02/notebook_b_500g` 的那两行配置**删除**。

刷新NFS配置

```bash
sudo exportfs -arv
```

### 8.2 在宿主机上卸载（Unmount）目录

```bash
sudo umount /data02/notebook_a_200g
sudo umount /data02/notebook_b_500g
```

如果宿主机 `umount` 提示 `target is busy`，先用 `sudo lsof +D /data02/notebook_a_200g` 等只读检查确认当前使用者。经授权正常停止或释放使用该卷的业务后再试；不要直接杀掉未知进程，也不要使用强制或延迟卸载绕过占用。

### 8.2.1 解除 Promtail 等容器中的残留挂载（如有）

**宿主机卸载成功，不等于所有容器中的挂载副本都已消失。** Promtail 等日志采集容器可能通过父目录 `hostPath` 继承了此卷，并在自己的挂载命名空间中保留副本。此时 `lvremove` 仍可能提示 `contains a filesystem in use`。

少的这一步是：**在实际持有者容器的挂载命名空间内普通卸载该卷，再确认设备打开计数为 0，最后执行 8.3。** 这不是重启 Promtail、删除 Pod 或终止业务进程，也不需要 Linux 6.12 的命名空间枚举接口；Linux 5.10 支持这种手工操作。

1. 先确认没有 Notebook 或其他业务 Pod 使用该卷，并确认相关维护操作不会并发改变挂载或 LVM。下面以文档中的一个示例 LV 为例，实际操作须替换为要回收的准确设备：

   ```bash
   LV_DEV=/dev/vg_data/lv_notebook_200g
   MAJ_MIN=$(sudo lsblk -dn -o MAJ:MIN "$LV_DEV")
   printf 'target device: %s (%s)\n' "$LV_DEV" "$MAJ_MIN"
   ```

2. 在该 LV 所在的 worker 上按主次设备号查找仍持有挂载的进程。只有上一项设备查询成功且打印出唯一、有效的主次设备号时，才运行下面的只读检查：

   ```bash
   sudo awk -v dev="$MAJ_MIN" '$3 == dev { print FILENAME, "root=" $4, "mountpoint=" $5 }' /proc/[0-9]*/mountinfo
   ```

   输出中的 `/proc/<PID>/mountinfo` 给出宿主机 PID，`mountpoint` 是那个进程视图中的实际挂载路径。结合当前容器运行时信息、`/proc/<PID>/cgroup` 和 Pod 所在节点核实其容器/Pod 身份；可能是 Promtail，也可能是其他持有者，不能只凭进程名判断。多个 PID 可能属于同一个挂载命名空间。**不要照抄历史 PID、Pod 名或把宿主机路径当成必然正确的容器路径。**

3. 确认该持有者是获准释放此已停用卷的日志采集容器，而不是业务使用者后，从 worker 进入它的挂载命名空间和根目录，普通卸载核实过的容器路径：

   ```bash
   # 两个变量必须取自本次占用和容器身份检查，不能使用历史示例值。
   HOLDER_PID=''       # 填本次核实的宿主机 PID
   CONTAINER_MOUNT=''  # 填本次核实的容器内实际挂载路径
   if [ -n "$HOLDER_PID" ] && [ -n "$CONTAINER_MOUNT" ]; then
       sudo nsenter -t "$HOLDER_PID" --mount --root --wd -- umount -- "$CONTAINER_MOUNT"
   else
       echo '请先核实并填写 PID 和容器挂载路径，当前不会执行卸载。' >&2
   fi
   ```

   `--root` 和 `--wd` 使用该目标进程的根目录与工作目录，避免仅切换 mount namespace 却仍按不匹配的根目录解释路径。这种手工方式需要目标根目录中的 `umount` 工具可用，且操作者具备相应权限；目标工作目录若在待卸载卷内，也可能导致 busy。工具缺失、身份/路径无法确认或普通卸载失败时停止，改由维护人员使用正确根目录上下文的可信宿主机执行器处理，不猜路径、不临时强制卸载。多个独立持有者须逐一核实、授权和释放。

4. 重新检查宿主机及已核实容器视图中没有该卷挂载，并检查设备打开计数：

   ```bash
   sudo findmnt -rn -o TARGET --source "$LV_DEV"
   sudo dmsetup info -c -o name,major,minor,open "$LV_DEV"
   ```

   宿主机 `findmnt` 应无挂载输出；`dmsetup` 的 `Open` 列必须为 `0` 才进入 8.3。计数非零时仍可能有其他挂载、打开文件或其他设备引用，应继续排查并保留卷。只扫描进程列表不能证明完整的内核命名空间范围，手动流程依赖管理员核实维护范围，不能把“没找到 PID”当成可删除的证据。

### 8.3 彻底删除 LVM 逻辑卷（回收空间）

确认要回收的卷在宿主机及已核实的持有者容器中均已卸载、设备打开计数为 0 后，才能删除逻辑卷。**仅卸载目录不会把空间归还 VG**；删除对应 LV 后，卷组可用空间才会增加。

执行删除命令（系统会询问你是否确认删除，输入 `y` 并回车）：

```bash
sudo lvremove /dev/vg_data/lv_notebook_200g
sudo lvremove /dev/vg_data/lv_notebook_500g
```

删除后，你可以运行 `sudo vgs` 看一眼，你会发现 `vg_data` 的 `VFree`（可用空间）又变回满血的 3.5T 了！

### 8.4 清理开机自启配置（极其重要！）

如果你之前为了防止重启失效，把挂载信息写进了 `/etc/fstab` 文件里，**这一步千万不能忘！**

找到带有 `lv_notebook_200g` 和 `lv_notebook_500g` 的那两行，**把它们删掉**。


添加NFS到集群

登记 NFS 存储时，请通过获批的集群管理界面或内部运维流程操作，并按申请填写存储标识、名称、导出路径、服务地址、工作空间和存储类型。数据库连接参数或直接连接命令请填写为：[数据库连接信息占位符]；实际凭据和连接目标仅通过授权的受控配置或密钥管理渠道获取，不在本文档中记录。
