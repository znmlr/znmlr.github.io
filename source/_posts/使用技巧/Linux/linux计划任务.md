---
title: linux计划任务
categories:
  - 使用技巧
  - Linux
abbrlink: 41239
date: 2018-05-03 13:58:57
tags:
---

crond是比较简单易用的。

使用crontab -e编辑配置文件，格式如下：
  <!--more-->
  
| Minute | Hour | Day  | Month | Dayofweek | command |
| ------ | ---- | ---- | ----- | --------- | ------- |
| 分钟   | 小时 | 天   | 月    | 天每星期  | 命令    |

例如：
``50 15 * * * XXX``
表示每天15点50执行XXX命令

crontab文件的一些例子：
``30 21 * * * /usr/local/etc/rc.d/lighttpd restart``
上面的例子表示每晚的21:30重启apache。

``45 4 1,10,22 * * /usr/local/etc/rc.d/lighttpd restart``
上面的例子表示每月1、10、22日的4 : 45重启apache。

``10 1 * * 6,0 /usr/local/etc/rc.d/lighttpd restart``
上面的例子表示每周六、周日的1 : 10重启apache。

``0,30 18-23 * * * /usr/local/etc/rc.d/lighttpd restart``
上面的例子表示在每天18 : 00至23 : 00之间每隔30分钟重启apache。

``0 23 * * 6 /usr/local/etc/rc.d/lighttpd restart``
上面的例子表示每星期六的11 : 00 pm重启apache。

``* */1 * * * /usr/local/etc/rc.d/lighttpd restart``
每一小时重启apache

``* 23-7/1 * * * /usr/local/etc/rc.d/lighttpd restart``
晚上11点到早上7点之间，每隔一小时重启apache

``0 11 4 * mon-wed /usr/local/etc/rc.d/lighttpd restart``
每月的4号与每周一到周三的11点重启apache

``0 4 1 jan * /usr/local/etc/rc.d/lighttpd restart``
一月一号的4点重启apache