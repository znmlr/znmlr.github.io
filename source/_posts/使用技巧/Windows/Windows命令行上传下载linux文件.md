---
title: Windows命令行上传下载linux文件
categories:
  - 使用技巧
  - Windows
abbrlink: 25846
date: 2018-05-03 11:27:26
tags:
---
# 安装工具

使用psftp.exe来完成

[putty](https://www.putty.org/ )或者[putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html )
  <!--more-->
  
# 下载文件

```
%~d0
cd %~dp0
echo get /home/%date:~0,4%-%date:~5,2%-%date:~8,2%.tar.bz2 E:\backup.tar.bz2 > E:\cmd.txt
psftp.exe root@192.168.2.31 -pw iampswd -b "cmd.txt" -bc
del E:\cmd.txt /F/S/Q
```

# 上传文件

```
%~d0
cd %~dp0
echo put E:\1.txt /home/backup/1.txt > E:\cmd.txt
psftp.exe root@192.168.2.31 -pw iampswd -b "cmd.txt" -bc
del E:\cmd.txt /F/S/Q
```

