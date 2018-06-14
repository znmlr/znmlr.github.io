---
title: Hexo建站笔记
categories:
  - 建站笔记
tags:
  - hexo
abbrlink: '61245e5'
date: 2018-05-02 18:20:11
---

# 简介

- Hexo 是一个快速、简洁且高效的博客框架
- Hexo 使用 Markdown解析文章，在几秒内，即可利用靓丽的主题生成静态网页

# 安装

## 运行环境

- [Node.js](https://nodejs.org/en/)
- [git](https://git-scm.com/download/win)
  <!--more-->

## 安装hexo

```shell
npm install -g hexo-cli
```

## 建站

> 路径最好不要有中文

```shell
hexo init <folder>
cd <folder>
npm install
```

## 发布静态页面

> 即从md文件生成html文件

```shell
hexo g
```

## 调试环境

> 可以使用hexo自带的调试服务器``hexo s``
>
> 推荐使用http-server

- 安装http-server

  ```shell
  npm install http-server -g
  ```

- 默认运行

  > 默认是 http://localhost:8080

  ```shell
  http-server <path_of_project>
  ```

- 带参数运行

  ```shell
  http-server <path_of_project> -a 0.0.0.0 -p 8080
  ```

> 这个时候打开 http://localhost:8080 应该可以看到hexo自带的hello world 博文

# 部署

> hexo推荐部署在github上，github免费且高速
>
> 也可以部署在任何虚拟主机上，国内免费托管还有coding、码云

## 关联github

### 配置github

- 注册账号
- 新建仓库

### 关联

- 设置git信息

  在git的bash中，执行下面命令

  ```
  git config --global user.name "your-github-name"
  git config --global user.email "your-github-reg-email"
  ssh-keygen -t rsa
  ```

- 获取密钥

  本地会生成2个密钥文件，选择其中任何一个均可，用记事本打开，复制其中内容

  ![Hexo建站笔记](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/Hexo%E5%BB%BA%E7%AB%99%E7%AC%94%E8%AE%B0_1.png)

- 设置github密钥

  在仓库的setting页面

  ![Hexo建站笔记](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/Hexo%E5%BB%BA%E7%AB%99%E7%AC%94%E8%AE%B0_2.png)

  有.pub结尾填入上方，没有的填入下方，二者填一个即可

## 自动部署

> 需要``hexo-deployer-git``插件支持

```shell
hexo d
```

## 将工程放入github

## 绑定二级域名

# 常用插件

## 