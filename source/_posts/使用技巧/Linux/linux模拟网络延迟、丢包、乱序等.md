---
title: linux模拟网络延迟、丢包、乱序等
categories:
  - 使用技巧
  - Linux
abbrlink: 8371
date: 2018-05-03 13:50:54
tags:
---

# 延时设置
  <!--more-->
  
设置延时：``tc qdisc add dev eth0 root netem delay 30ms``
显示延时设置：``tc qdisc show``
修改延时：``tc qdisc change dev eth0 root netem delay 40ms``
删除延时：``tc qdisc del dev eth0 root netem delay 40ms``
带波动延时：``tc qdisc add dev eth0 root netem delay 100ms 10ms``
带概率波动：``tc qdisc add dev eth0 root netem delay 100ms 10ms 30%``

# 模拟丢包

``tc qdisc add dev eth0 root netem loss 1%``
该命令将 eth0 网卡的传输设置为随机丢掉 1% 的数据包。
``tc qdisc add dev eth0 root netem loss 1% 30%``
该命令将 eth0 网卡的传输设置为随机丢掉 1% 的数据包，成功率为 30% 。

# 模拟包重复

``tc qdisc add dev eth0 root netem duplicate 1%``
该命令将 eth0 网卡的传输设置为随机产生 1% 的重复数据包 。

# 模拟包损坏

``tc qdisc add dev eth0 root netem corrupt 0.2%``
该命令将 eth0 网卡的传输设置为随机产生 0.2% 的损坏的数据包

# 模拟数据包乱序

``tc qdisc change dev eth0 root netem delay 10ms reorder 25% 50%``
该命令将 eth0 网卡的传输设置为:有 25% 的数据包（50%相关）会被立即发送，其他的延迟 10 秒