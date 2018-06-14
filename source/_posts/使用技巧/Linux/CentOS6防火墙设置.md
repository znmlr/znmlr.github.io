---
title: CentOS6防火墙设置
tags:
  - centos
  - 防火墙
categories:
  - 使用技巧
  - Linux
abbrlink: b3e37511
date: 2018-05-05 13:45:01
---

# 打开iptables的配置文件

```
vi /etc/sysconfig/iptables
```

  <!--more-->

# 全部修改完之后重启iptables

```
service iptables restart
```

- 增加注释，需要另起一行，以# 开头

- 附FTP设置

```
# 开启20,21端口
-A INPUT -p tcp -m multiport --dport 20,21  -m state --state NEW -j ACCEPT
# 开启21主动端口
-A INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT
# 开启被动端口   
-A INPUT -p tcp --dport 30000:31000 -j ACCEPT
```