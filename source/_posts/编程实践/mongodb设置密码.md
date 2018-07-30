---
title: mongodb设置密码
tags:
  - mongodb
categories:
  - 编程实践
date: 2018-07-30 16:25:23
---

> 默认mongod是不带密码的，非常不安全
>
> 要么使用阿里云等提供的云数据库，要么自建数据库时加上密码设置

- 选择`admin`数据库

- > `use admin`

- 创建用户名密码

  > `db.createUser({ user: "useradmin", pwd: "adminpassword", roles: [{ role: "userAdminAnyDatabase", db: "admin" }] })`  

- 验证是否成功

  > `db.auth("useradmin", "adminpassword")`  

- 修改启动配置

  > 在启动命令后加上`-- auth`

