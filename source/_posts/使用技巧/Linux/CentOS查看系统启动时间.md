---
title: CentOS查看系统启动时间
categories:
  - 使用技巧
  - Linux
abbrlink: 35977
tags:
  - centos
date: 2018-05-03 14:00:37
---

# 查看/proc/uptime文件  

```
cat /proc/uptime  
73064.44 276161.85
```
  <!--more-->

第一数字即是系统已运行的时间73064.44 秒，运用系统工具date即可算出系统启动时间  

```
date -d "$(awk -F. '{print $1}' /proc/uptime) second ago" +"%Y-%m-%d %H:%M:%S"  
2015-12-02 13:00:59
```

# 计算系统运行时间  

```
cat /proc/uptime| awk -F. '{run_days=$1 / 86400;run_hour=($1 % 86400)/3600;run_minute=($1 % 3600)/60;run_second=$1 % 60;printf("系统已运行：%d天%d时%d分%d秒",run_days,run_hour,run_minute,run_second)}'  
 
系统已运行：0天20时19分26秒
```

