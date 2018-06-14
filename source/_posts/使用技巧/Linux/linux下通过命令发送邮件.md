---
title: linux下通过命令发送邮件
categories:
  - 使用技巧
  - Linux
abbrlink: 35296
date: 2018-05-03 13:53:26
tags:
---

# 下载安装msmtp

[msmtp](http://downloads.sourceforge.net/msmtp)
下载后，解压、``configure make make install``
  <!--more-->
  
# 配置账号信息

在用户目录下，新建文件.msmtprc，设置权限为0600
填写内容：

```
# Set default values for all following accounts.
defaults

logfile /usr/local/msmtp/msmtp.log
# The SMTP server of the provider.
account test

# SMTP邮件服务器地址
host smtp.qq.com

# 发送的邮件Email
from xiaobaichi@i0554.com
auth login

# 邮件服务器登录账号
user xiaobaichi@i0554.com

# 邮件服务器登陆密码
password 123456
# Set a default account
account default : test
```

# 测试账号信息

``msmtp youremail@test.com`` 看看能否收到信息

# 安装配置mutt

``yum install mutt``

vi /etc/Muttrc ，编辑mutt的总设置，修改以下几行

```
set from=”发送邮件地址”
set sendmail=”/usr/local/msmtp/bin/msmtp”
set use_from=yes
set realname=”发件人”
set editor=”vi”
```

发件地址最好与msmtp设置的账号相同，否则可能会出错。

# 发送邮件

``echo “test” |mutt -s “my_first_test” yangcheng@i0554.com``