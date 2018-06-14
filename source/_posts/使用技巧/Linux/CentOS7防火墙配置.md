---
title: CentOS7防火墙配置
tags:
  - centos
  - 防火墙
abbrlink: 82587e7f
categories:
  - 使用技巧
  - Linux
date: 2018-06-14 21:28:43
---

> 最近在家部署CentOS7， 发现以前CentOS 6 系列中的 iptables 相关命令不能用了
>
> 查了下，发现Centos 7使用firewalld代替了原来的iptables

# 关闭防火墙

```shell
systemctl stop firewalld.service           #停止firewall
systemctl disable firewalld.service        #禁止firewall开机启动
```

# 开启端口

  <!--more-->

```shell
firewall-cmd --zone=public --add-port=80/tcp --permanent

命令含义：
--zone #作用域
--add-port=80/tcp #添加端口，格式为：端口/通讯协议
--permanent #永久生效，没有此参数重启后失效
```

# 重启防火墙

```shell
firewall-cmd --reload
```

# 常用命令

```shell
firewall-cmd --state                           ##查看防火墙状态，是否是running
firewall-cmd --reload                          ##重新载入配置，比如添加规则之后，需要执行此命令
firewall-cmd --get-zones                       ##列出支持的zone
firewall-cmd --get-services                    ##列出支持的服务，在列表中的服务是放行的
firewall-cmd --query-service ftp               ##查看ftp服务是否支持，返回yes或者no
firewall-cmd --add-service=ftp                 ##临时开放ftp服务
firewall-cmd --add-service=ftp --permanent     ##永久开放ftp服务
firewall-cmd --remove-service=ftp --permanent  ##永久移除ftp服务
firewall-cmd --add-port=80/tcp --permanent     ##永久添加80端口 

iptables -L -n                                 ##查看规则，这个命令是和iptables的相同的
man firewall-cmd                               ##查看帮助
```

