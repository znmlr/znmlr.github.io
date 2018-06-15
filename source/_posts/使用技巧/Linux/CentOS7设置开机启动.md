---
title: CentOS7设置开机启动
tags:
  - centos
  - 自启动
categories:
  - 使用技巧
  - Linux
date: 2018-06-15 08:34:16
---

# 问题

> 在新安装的CentOS7系统中，发现即使在``/etc/rc.local``中写了脚本，重启后也无法正常执行

# 解决方法

- 必须把``/etc/rc.d/rc.local ``和``/etc/rc.local ``两个文件同时赋予可执行权限
- 实际上，后者只是前者的软链接

# 注意

- 这个文件是为兼容性而添加的
- 在开机过程中强烈建议创建自己的systemd服务或udev规则来运行脚本，而不是使用此文件