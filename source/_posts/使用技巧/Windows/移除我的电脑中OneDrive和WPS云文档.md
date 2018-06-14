---
title: 移除我的电脑中OneDrive和WPS云文档
categories:
  - 使用技巧
  - Windows
abbrlink: 51124
date: 2018-05-03 13:08:30
tags:
---

# 除去“我的电脑”中“WPS云文档”

- 强迫症患者福音
- 之前可以在配置工具中修改，但是现在不能了
  <!--more-->
  
- ``win+r``输入``regedit ``打开注册表，找到如下项目``\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace``点击浏览里面的项目，你就会找到有wps云文档的子项，删除就ok了
- 上面的方法可以去除“我的电脑”中的，但是左侧导航窗格里面还有，这里继续删除

``\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\``下面的项目

# Win10移除资源管理器中的OneDrive

国内OneDrive用处不大，可以通过修改注册表中删除资源管理器中的图标

- 使用Win+R打开运行对话框，输入regedit打开注册表编辑器
- 定位到``HKEY_CLASSES_ROOT\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}``，在右边双击``System.IsPinnedToNameSpaceTree``这个键，将``System.IsPinnedToNameSpaceTree``中的值从1改为0

