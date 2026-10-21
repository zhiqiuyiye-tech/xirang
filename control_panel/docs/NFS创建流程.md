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

如果宿主机 `umount` 提示 `target is busy`，说明仍有进程在该挂载命名空间中使用这个目录。找到持有者进程的 PID 后，进入它的挂载命名空间再执行一次普通卸载，然后回到宿主机重新执行上面的 `umount`：

```bash
sudo nsenter -t 2478731 -m umount /data02/nfs_lv_nb_57fc4e9250ee4cadb6f43dff96c48d54
```

### 8.3 彻底删除 LVM 逻辑卷（回收空间）

确认要回收的卷在宿主机及持有者容器中均已卸载后，才能删除逻辑卷。**仅卸载目录不会把空间归还 VG**；删除对应 LV 后，卷组可用空间才会增加。如果 `lvremove` 仍报该卷正在使用，说明还有未卸载的持有者，回到 8.2 处理。

执行删除命令（系统会询问你是否确认删除，输入 `y` 并回车）：

```bash
sudo lvremove /dev/vg_data/lv_notebook_200g
sudo lvremove /dev/vg_data/lv_notebook_500g
```

删除后，你可以运行 `sudo vgs` 看一眼，你会发现 `vg_data` 的 `VFree`（可用空间）又变回满血的 3.5T 了！

### 8.4 清理开机自启配置（极其重要！）

如果你之前为了防止重启失效，把挂载信息写进了 `/etc/fstab` 文件里，**这一步千万不能忘！**

找到带有 `lv_notebook_200g` 和 `lv_notebook_500g` 的那两行，**把它们删掉**。


## 9 扩容、缩容lv

使用 lvextend -r 同时扩容逻辑卷和文件系统：
lvextend -r -L 200G /dev/vg_data1/lv_nb_001


这里 200G 是扩容后的总容量，不是增加 200GB。

如果要在原有容量基础上增加 100GB：
lvextend -r -L +100G /dev/vg_data1/lv_nb_001


-r 会尝试自动扩容文件系统，适用于常见的 ext4、XFS 文件系统。

然后根据文件系统类型执行：

ext4：
resize2fs /dev/vg_data1/lv_nb_001


XFS：
xfs_growfs /实际挂载目录