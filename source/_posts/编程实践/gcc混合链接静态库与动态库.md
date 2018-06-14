---
title: gcc混合链接静态库与动态库
tags:
  - gcc
  - 链接
categories:
  - 编程实践
abbrlink: ddcdb5c5
date: 2018-05-05 13:40:27
---

```
-Wl,-Bstatic  -levent_core
-Wl,-Bdynamic -llog4cplus
```

- 链接libevent_core.a
- 链接liblog4cplus.so