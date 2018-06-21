---
title: 自建anki服务器
tags:
  - anki
  - 神器
categories:
  - 学习方法
abbrlink: 79bd6352
date: 2018-06-16 21:51:25
---

# 为什么要自建

- 官方服务器在境外，不太可靠
- 免费软件，尽量减轻开发者的负担
- 数据在自己手里，比较放心

# 需要哪些条件

- linux环境的主机
- 公网ip
- 路由器上设置端口映射

  <!--more-->
  
# 自建的步骤

## 前置条件

- 安装python和pip

```shell
yum install python-pip
```

> 我用的centos7，自带了python2.7，只需要安装pip即可

## 安装服务器

```shell
easy_install AnkiServer
```

> 时间比较久，请耐心等待

## 建立配置脚本

- 新建目录，用于存储anki相关数据

  ```shell
  cd /home/data
  mkdir anki
  ```

- 拷贝配置脚本

  ```
  cp /usr/lib/python2.7//site-packages/AnkiServer-2.0.6-py2.7.egg/examples/example.ini /home/data/anki/anki.ini
  ```

- 修改参数

  ```
  host= 10.XX.XX.XX  #自己服务器的地址也可是局域网IP
  allowed_hosts=0.0.0.0 #允许同步的客户端ip地址，使用0.0.0.0表示允许任何ip地址连接
  ```

## 创建用户

```
ankiserverctl.py adduser username #创建用户
ankiserverctl.py lsuser #验证
```

## 运行服务

```
ankiserverctl.py debug ./production.ini	#测试模式
ankiserverctl.py start ./production.ini #正常模式
```

# 配置桌面程序

- 打开插件文件夹

![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/%E8%87%AA%E5%BB%BAanki%E6%9C%8D%E5%8A%A1%E5%99%A8-1.jpg)

- 新建文本文件``mysyncserver.py ``

![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/%E8%87%AA%E5%BB%BAanki%E6%9C%8D%E5%8A%A1%E5%99%A8-2.jpg)

- 修改``mysyncserver.py ``内容

  ```python
  import anki.sync
  anki.sync.SYNC_BASE = 'http://192.168.0.100:27701/' # 注意修改IP和端口
  anki.sync.SYNC_MEDIA_BASE = 'http://192.168.0.100:27701/msync/' # 注意修改IP和端口
  ```

- 重启anki，点击界面同步按钮

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/06/%E8%87%AA%E5%BB%BAanki%E6%9C%8D%E5%8A%A1%E5%99%A8-3.jpg)

- 大功告成

  > 如果有问题，请在服务端运行debug模式，观察原因