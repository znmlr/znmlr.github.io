---
title: 关闭wps后台驻留进程
tags:
  - wps
  - office
categories:
  - 使用技巧
  - Windows
abbrlink: 49e263f5
date: 2018-06-14 20:54:32
---

# 起因

- wps是一款非常优秀的国产办公软件，但是迫于各种压力，也开始耍流氓了：开机自启动，不能完全退出进程……，让人很烦恼
- 用wps而不是office的原因：1、wps对个人用户免费；2、wps小巧轻便

## 现象

启动wps相关软件后，即使把软件关闭，后台也会有进程驻留

- wpsnotify.exe
- wpscenter.exe
- wpscloudsvr.exe

  <!--more-->

# 解决方案

## 方案一

- 改造上述3个可执行程序，自己编译一个空程序来代替。原理非常简单

  ```c
  int main(int argc, char ** argv)
  {
      return 0;
  }
  ```

- 直接把编译出来的可执行程序，重命名后覆盖上述3个exe即可

> 这样做有一个缺陷：很多wps的云服务无法使用

## 方案二

- 思路：后台起一个服务，定时检测wps软件是否存在，如果存在则不处理；如果不存在则强制关闭上述3个进程

- 步骤1：在任务计划中，制定一个周期性任务，从早上9点开始，每5分钟执行一个vbs脚本

- 步骤2：vbs脚本，执行一个bat

  ```vbscript
  set ws=wscript.createobject("wscript.shell")
  ws.run "D:\ProgramData\bat\wps.bat /start",0
  ```

  > 如果在任务计划中直接执行bat的话，会有dos窗口弹出，不优雅

- 步骤3：在bat脚本中检查wps是否退出，并执行关闭操作

  ```bash
  @echo off
  
  set app1=wps.exe
  set app2=et.exe
  set app3=wpp.exe
  
  set Pr=0
  for /f "tokens=1 delims= " %%a in ('tasklist ^| findstr /i "%app1% %app2% %app3%"') do (
      set APP=%%~a
      set /a Pr+=1
  )
  
  if %Pr% equ 0 (
  taskkill /im wpsnotify.exe /f
  taskkill /im wpscenter.exe /f
  taskkill /im wpscloudsvr.exe /f
  taskkill /im wpsoffice.exe /f
  )
  ```

  > wps.exe：类似于word
  >
  > et.exe：类似于excel
  >
  > wpp.exe：类似于ppt