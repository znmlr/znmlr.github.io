---
title: Windows下创建一个没有窗口的控制台程序
categories:
  - 使用技巧
  - Windows
abbrlink: e4a7498c
date: 2018-05-04 12:48:09
tags:
---

```c++
#pragma comment( linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"")
int main(int argc, char **argv)
{
    return 0;
}
```

