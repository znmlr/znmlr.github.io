---
title: linux远程同步文件夹
categories:
  - 使用技巧
  - Linux
abbrlink: 42618
date: 2018-05-03 13:49:11
tags:
---

# 需求

A、B两台linux主机，平时主要在主机A上存取文件，需要在某些特定时间点把主机A上的文件夹同步到主机B 
  <!--more-->
  
```
rsync -rzP –delete /home/AAAAA/ root@info.znmlr.cn:/home/BBBBB/
```

- 需要运行在主机A，从主机A的/home/AAAAA/目录自动同步到主机B（info.znmlr.cn，域名或者IP均可）的/home/BBBBB/目录 
- 前置条件：已经设置到ssh免密码登陆 