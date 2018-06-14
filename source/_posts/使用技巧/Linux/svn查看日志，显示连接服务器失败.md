---
title: svn查看日志，显示连接服务器失败
categories:
  - 使用技巧
  - Linux
abbrlink: 62801
tags:
  - svn
date: 2018-05-03 14:02:11
---

# 问题描述：

> svn查看日志显示连接服务器失败。你想使用缓存中的数据吗？后面还有三个选项“立即离线、永远离线、取消“
  <!--more-->
  
# 解决方案：

> 将svnserve.conf里的anon-access=read 改为anon-access=none

