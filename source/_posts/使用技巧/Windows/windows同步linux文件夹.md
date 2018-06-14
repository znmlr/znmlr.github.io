---
title: windows同步linux文件夹
categories:
  - 使用技巧
  - Windows
abbrlink: 20726
date: 2018-05-03 13:36:50
tags:
---

# 需求

有一台centos主机，上面运行了SVN服务。但是这个主机硬盘比较陈旧，担心硬盘损坏，所以得定期把服务器上的文件夹备份到本地磁盘上，避免数据丢失 
  <!--more-->
  
# 工具

[winscp ](https://winscp.net/eng/download.php )

- 安装winscp并配置好登陆信息 
- 编写脚本 

## 启动脚本

```
C:
cd "C:\Program Files (x86)\WinSCP"
winscp.exe /console /script=D:\backup.bat
```

> 进入安装目录，以命令行模式启动，并且指定命令脚本 

## 命令脚本

```
open root:password@192.168.1.144
cd /home/data/backup
lcd D:\ProgramData\backup
option transfer binary
option synchdelete on
synchronize local
close
exit
```

> 打开连接，进入远程目录和本地目录，设定同步参数，执行同步命令(local是从远端到本地，remote是从本地到远端) 