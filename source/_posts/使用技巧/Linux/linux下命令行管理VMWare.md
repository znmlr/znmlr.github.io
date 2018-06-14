---
title: linux下命令行管理VMWare
categories:
  - 使用技巧
  - Linux
abbrlink: 602bd5b4
date: 2018-05-04 13:07:58
tags:
---

# 虚拟机管理

- 关机 

  ```
  vmrun stop "/opt/VMware/win2k8r2.vmx" hard | soft
  // 强制关闭虚拟机(相当于直接关电源) | 正常关闭虚拟机
  ```
  <!--more-->

- 重启 

  ```
  vmrun reset "/opt/VMware/win2k8r2.vmx" hard | soft
  // 冷重启虚拟机 | 热重启虚拟机
  ```

- 挂起 

  ```
  vmrun suspend  "/opt/VMware/win2k8r2.vmx" hard | soft
  // 挂起虚拟机（可能相当于休眠）
  ```

- 查询 

  ```
   vmrun list 
   // 列出正在运行的虚拟机
  ```

- 图形化开机 

  ```
  vmrun start "/opt/VMware/win2k8r2.vmx" 
  // gui启动带图形界面虚拟机
  ```

- 无图形化开机 

  ```
  vmrun -T ws start "/opt/VMware/win2k8r2.vmx" nogui
  // 启动无图形界面虚拟机  （-T 是区分宿主机的类型，ws|server|server1|fusion|esx|vc|player，可能比较常用的是ws、esx和player，不过我没有加-T在Workstation也能正常运行, 可能esx和server就需要了）
  ```

# 快照管理

- 创建快照 

  ```
  vmrun -T ws snapshot "/opt/VMware/win2k8r2.vmx" snapshotName
  // 创建一个快照
  ```

- 列出快照 

  ```
  vmrun -T ws listSnapshots "/opt/VMware/win2k8r2.vmx"
  // 列出虚拟机快照数量及名称
  ```

- 从快照恢复 

  ```
  vmrun -T ws reverToSnapshot "/opt/VMware/win2k8r2.vmx" snapshotName 
  // 从一个快照中恢复虚拟机
  ```

- 删除快照 

  ```
  vmrun -T ws deleteSnapshot1 "/opt/VMware/win2k8r2.vmx" snapshotName 
  // 删除一个快照
  ```

  