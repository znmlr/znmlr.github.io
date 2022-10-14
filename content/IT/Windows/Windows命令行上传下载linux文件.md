---
title: "Windows命令行上传下载linux文件"
date: 2022-09-27T22:25:13+08:00
draft: false
weight: 2
---

# 安装工具

使用psftp.exe来完成

[putty](https://www.putty.org/ )或者[putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html )

# 下载文件

```powershell
%~d0
cd %~dp0
echo get /home/%date:~0,4%-%date:~5,2%-%date:~8,2%.tar.bz2 E:\backup.tar.bz2 > E:\cmd.txt
psftp.exe root@192.168.2.31 -pw iampswd -b "cmd.txt" -bc
del E:\cmd.txt /F/S/Q
```

# 上传文件

```powershell
%~d0
cd %~dp0
echo put E:\1.txt /home/backup/1.txt > E:\cmd.txt
psftp.exe root@192.168.2.31 -pw iampswd -b "cmd.txt" -bc
del E:\cmd.txt /F/S/Q
```

