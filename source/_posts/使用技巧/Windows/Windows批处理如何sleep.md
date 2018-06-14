---
title: Windows批处理如何sleep
categories:
  - 使用技巧
  - Windows
abbrlink: 43381
tags:
  - 批处理
date: 2018-05-03 13:04:37
---

在windows批处理中，没有sleep，可以变相实现 
  <!--more-->
  
```powershell
ping -n 3 127.0.0.1 > nul
timeout /t 3 /nobreak > nul
```

以上两种方式中的3都是需要sleep的秒数 