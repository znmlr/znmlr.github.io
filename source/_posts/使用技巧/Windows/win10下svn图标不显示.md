---
title: win10下svn图标不显示
tags:
  - svn
categories:
  - 使用技巧
  - Windows
abbrlink: 11fd2e3b
date: 2018-05-04 14:12:00
---

- ``window+R``调用运行，输入``regedit``打开 注册表
- ``ctrl+F``，搜``ShellIconOverlayIdentifiers``项
- 在``1TortoiseNormal``、``2TortoiseModified``等貌似9个svn相关的项，前面增加3个空格
- 修改完成后重启电脑，即可显示图标。

