---
title: xampp初次使用可能遇到的问题
tags:
  - xampp
  - centos
  - apache
  - mysql
  - phpmyadmin
categories:
  - 使用技巧
  - Linux
abbrlink: 97776a9f
date: 2018-06-15 08:39:21
---

# 安装完成后，只能本机访问

- 原因：centos的防火墙没有关闭

- 解决办法

  > 查看防火墙状态 

  ```shell
  firewall-cmd    --state
  ```

  > 关闭防火墙 

  ```shell
  systemctl  stop   firewalld.service
  ```

  > 开启防火墙 

  ```shell
  systemctl  start   firewalld.service
  ```

  > 禁止开机启动启动防火墙 

  ```shell
  systemctl   disable   firewalld.service
  ```

# xampp安装后，无法使用phpmyadmin

- 原因，默认设置只能从本机访问

- 修改配置文件``/opt/lampp/etc/extra/http-xampp.conf``

  ```shell
  <Directory "/opt/lampp/phpmyadmin">
      AllowOverride AuthConfig Limit
      #Require local   #原来的
      Require all granted  #新的
      ErrorDocument 403 /error/XAMPP_FORBIDDEN.html.var
  </Directory>
  
  ```

# xampp安装后，mysql密码为空

- 在phpmyadmin中执行以下命令即可

  ```sql
  use mysql;
  update user set host = '%' where user = 'root';
  FLUSH PRIVILEGES;
  ```

  > 如果第二步报错，无须理会

# mysql配置密码后，phpmyadmin无法使用

- 修改phpmyadmin的配置文件``/opt/lampp/phpmyadmin/config.inc.php``

  ```shell
  $cfg['Servers'][$i]['password'] = 'yourpasswd';
  ```

