---
title: SVN中使用钩子自动拷贝文件
tags:
  - svn
categories:
  - 使用技巧
  - Windows
abbrlink: 167cd7f6
date: 2018-06-19 15:26:16
---

# 什么是钩子

- 我们经常提到的svn hooks（钩子）是一组“外挂”脚本程序， 是svn提供的一组由svn事件触发的特别有用的程序
- 钩子可以调用批处理文件、可执行文件或者一些类似于perl、python等的脚本

# 钩子有哪些
  <!--more-->
> 懒得打字，直接上截图

![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/SVN%E9%92%A9%E5%AD%90-1.png)

# 应用实例

> 需求：希望A目录更新后，把固定的几个文件覆盖拷贝到B目录中

- 新建脚本

  ```powershell
  @echo off
  del D:\workspace\project\B\* /F/S/Q
  copy D:\workspace\project\A D:\workspace\project\B\ /Y
  ```

- 设置钩子

  1. 在本地SVN文件夹上单击右键，选择属性

  2. 点击“Subversion”选项卡

  3. 点击“属性”按钮

     ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/SVN%E9%92%A9%E5%AD%90-2.png)

  4. 点击“新建”---“本地钩子”

     ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/SVN%E9%92%A9%E5%AD%90-3.png)

  5. 选择合适的钩子，然后填入脚本（包括路径信息）

     ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/SVN%E9%92%A9%E5%AD%90-4.png)

- 初次激活钩子时，系统可能会提示