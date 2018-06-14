---
title: Win下SVN目录锁死的解决办法
categories:
  - 使用技巧
  - Windows
abbrlink: 41237
tags:
  - svn
date: 2018-05-03 17:14:34
---

# 现象

在windows下，如果上次更新SVN中断，下次执行别的操作时，偶尔会出现失败的提示，类似

```
svn cleanup failed–previous operation has not finished; run cleanup if it was interrupted
```

这个时候用任何命令都无法清理空间了

# 工具

[SQLite Expert Personal ](http://www.sqliteexpert.com/download.html)

# 方法

打开``.svn``目录下的``wc.db``文件，清空``WORK_QUEUE``表