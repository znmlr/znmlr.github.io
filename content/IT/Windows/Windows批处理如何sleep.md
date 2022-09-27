---
title: "Windows批处理如何sleep"
date: 2022-09-27T22:30:44+08:00
draft: false
weight: 4
---

在`windows`批处理中，没有`sleep`，可以变相实现 

```powershell
ping -n 3 127.0.0.1 > nul
timeout /t 3 /nobreak > nul
```

以上两种方式中的`3`都是需要`sleep`的秒数 
