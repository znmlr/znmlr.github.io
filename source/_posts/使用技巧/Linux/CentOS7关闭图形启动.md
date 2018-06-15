---
title: CentOS7关闭图形启动
tags:
  - centos
  - 启动
categories:
  - 使用技巧
  - Linux
abbrlink: 1d5ae2d7
date: 2018-06-15 08:37:37
---

# 起因

- 利用淘宝购买的二手的瘦客户机充当家用服务器，性能较差
- 更新操作系统为最新的CentOS 7 1804，发现``gnome shell ``进程占用大量CPU资源

# 解决方案

- 查看当前运行级别

  ```shell
  [root@znmlr ~]# systemctl get-default
  graphical.target
  ```

  发现是图形界面启动，实际使用中并不需要图形界面，只需要文字界面启动即可

- 通过命令关闭图形启动

  ```shell
  [root@znmlr ~]# systemctl set-default multi-user.target
  Removed symlink /etc/systemd/system/default.target.
  Created symlink from /etc/systemd/system/default.target to /usr/lib/systemd/system/multi-user.target.
  
  
  [root@znmlr ~]# systemctl get-default
  multi-user.target
  ```

- 再次确认已经设置好