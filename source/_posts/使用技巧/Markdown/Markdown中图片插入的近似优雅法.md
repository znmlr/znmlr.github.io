---
title: Markdown中图片插入的近似优雅法
tags:
  - markdown
abbrlink: 4cabcca1
categories:
  - 使用技巧
  - Markdown
date: 2018-05-06 08:19:03
---

# 最终实现效果

- 在图片上右键上传，自动生成markdown``图片链接格式``到剪切板中，任意地方``Ctrl+v``均可粘贴
- 在文件上右键上传，自动生成markdown``超链接格式``到剪切板中，任意地方``Ctrl+v``均可粘贴

 <!--more-->

# markdown介绍

- Markdown是一种可以使用普通文本编辑器编写的标记语言，通过简单的标记语法，它可以使普通文本内容具有一定的格式。 
- Markdown的语法简洁明了、学习容易，10分钟即可完全学会掌握。Markdown 的语法全由一些符号所组成，这些符号经过精挑细选，其作用一目了然。 即使没有渲染器，以纯文本方式阅读，也毫无障碍。
- 对于开发人员还有一个特别棒的优点：得益于其纯文本属性，用markdown编写的文档、表格等，存放与svn/git/perforce以后，可以非常方便的使用比较工具，对比历史版本！这个word、excel……所不能或者不易办到的。

# markdown的痛点

## 图片保存现状

成也萧何败也萧何，由于markdown的纯文本属性，决定了它不可能优雅的存储图片，在实践中有2种图形表示法

- markdown标准

  ```
  ![Alt text](/path/to/img.jpg)
  ```

  > 这样实际是存放的图片地址，而非图片本身

- html转义

  ```
  ![](data:image/*;base64,iVBORw0KGgoAAAANSUhEUgAAAJgAAADZCAIAAABTpG6/AAANaklEQVR4Ae2de1BU1x3H97ILC8gCRh5RjC9sEozPaQc7TiCO02o6+aMZp8M/plOn/8TEtv/V/OMM5Z9OdPJPk5ohbWfazNSJ0o6dSf6IEkubYlLt1PgAwReagK7A4gPEFVjY7Xf3wOYII=)
  ```

  > 以上是base64编码以后的二进制数据

上述2种方法，在书写markdown的过程中，都很不方便

## 便利的编辑器

- typora

  在windows下最好的markdown编辑器，没有之一

  拖动图片到文档中，会自动拷贝图片到硬盘的指定位置，算是半自动化解决了问题

  但是依然存在问题：分享为博客后，这些图片的路径很难正确处理

# 理想中的解决方案

- 在“我的电脑”中任意位置找到图片，右键点击“上传”，
- 自动生成markdown格式``![Alt text](http://***.***.***/***.jpg)``或者``[filedes](http://****.*****.***/***.zip) ``在剪切板中
- 在任何文本/markdown编辑器中，直接``Ctrl+V``即可完成编写

## 准备工作

### COS

> 对象存储（Cloud Object Storage，COS）

我们需要一个空间，用于存放图片或者文件，这里推荐使用腾讯云或者七牛云

他们提供的免费额度足够普通用户使用了

#### 腾讯云的免费额度

| 资源类型 | 资源子类型          | 每月免费额度 |
| -------- | ------------------- | ------------ |
| 存储空间 | 存储空间            | 50 GB        |
| 流量     | 外网下行流量        | 10 GB        |
| 流量     | 腾讯云 CDN 回源流量 | 10 GB        |
| 请求     | 读请求              | 100 万次     |
| 请求     | 写请求              | 100 万次     |

#### 七牛云的免费额度

| 资源类型                        | 免费额度   |
| ------------------------------- | ---------- |
| 标准存储空间                    | 0-10 GB    |
| 每月上传流量                    | 无上限     |
| 标准存储每月写请求 Put / Delete | 0-10 万次  |
| 标准存储每月读请求 Get          | 0-100 万次 |

### 本地环境

这里以腾讯云接口为例，本地需要``nodejs``运行环境

- [nodejs](https://nodejs.org/en/download/)
- [腾讯云SDK](https://github.com/tencentyun/cos-nodejs-sdk-v5)
### 环境变量配置

- 在``windows环境变量``中增加一项``NODE_PATH ``，最好同时指向2处，例如：``C:\Users\ZNMLR\node_modules``和``C:\Users\ZNMLR\AppData\Roaming\npm\node_modules``
- 前者对应npm的本地安装，后者对应npm的全局安装

# 开始优雅之旅

## 实现右键调用某bat

> 目标：在任意格式文件上单击右键，弹出菜单“上传”，然后调用指定bat
>

- 打开注册表编辑器

  ``WIN+R``调用运行库，输入``regedit``，会打开注册表编辑器

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_1.png)

- 找到``计算机\HKEY_CLASSES_ROOT\*\shell``

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_2.png)

- 新建项，名字随意

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_3.png)

- 再新建``command``子项，并修改右侧默认值

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_4.png)

  图中的D:\1.bat是我测试用的，其存放于某合理的地方

- 修改批处理内容，测试是否工作

  ```bat
  @echo off
  echo %1%
  pause
  exit
  ```

  该批处理暂时只获取输入参数，并打印出来

  然后等待用户敲个``Enter``就自动退出了

- 右键点击任意文件

  ![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_5.png)

- 查看运行效果

![](https://znmlr-1251254271.cos.ap-shanghai.myqcloud.com/2018/05/markdwon%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87_6.png)

## 不那么严肃的声明

今天是我用nodejs的第二天，代码可能写不那么符合标准不那么优雅，见谅

如果发现有更好的优化方法，请发邮件通知我，谢谢 yangyunzhao#qq.com

## 安装腾讯云SDK

- 安装nodejs运行环境

  这个没什么好说的，双击下一步就好了

- 安装sdk

  ```bat
  C:\Users\ZNMLR>npm i cos-nodejs-sdk-v5 --save -g
  + cos-nodejs-sdk-v5@2.4.0
  added 68 packages in 10.082s
  ```

- 再次安装sdk

  > 不要问我为何有这一步，腾讯云文档这样写的  
  >
  > 先下载[腾讯云SDK](https://github.com/tencentyun/cos-nodejs-sdk-v5)，解压，到指定目录执行命令

  ```
  C:\Users\ZNMLR>d:
  D:\>cd cos-nodejs-sdk-v5-master
  D:\cos-nodejs-sdk-v5-master>npm install -g
  + cos-nodejs-sdk-v5@2.4.0
  updated 1 package in 6.33s
  ```


## 获取腾讯云上传鉴权码

- 请到[腾讯云](https://cloud.tencent.com/product/cos)注册账号并实名认证，

- 新建存储桶

- 获取APPID、SecretId、SecretKey、存储桶名称、所属地域 

  以上步骤请自行阅读腾讯云文档，这里不做说明

## 编写上传脚本

### 官方示例

```
// 引入模块
var COS = require('cos-nodejs-sdk-v5');
// 创建实例
var cos = new COS({
    AppId: '1250000000',   // 修改为自己的appid
    SecretId: 'AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', // 修改为自己的SecretId
    SecretKey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', // 修改为自己的SecretKey
});
// 分片上传
cos.sliceUploadFile({
    Bucket: 'test', // 修改为自己的存储桶名称，由英文、数字和标点符号组成
    Region: 'ap-guangzhou', // 修改为自己的所属地域，应该是纯英文的部分
    Key: '1.zip', // 这个是远端的地址
    FilePath: './1.zip' // 这个是本地地址
}, function (err, data) {
    console.log(err, data);
});
```

执行js文件

```
D:\>node 2.js
warning: AppId has been deprecated, Please put it at the end of parameter Bucket(E.g: "test-1250000000").
(node:11824) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
null { Location: '**********.cos.ap-shanghai.myqcloud.com/1.png',
  Bucket: '*****',
  Key: '1.png',
  ETag: '"*******************-1"',
  statusCode: 200,
  headers:
   { 'content-type': 'application/xml',
     'transfer-encoding': 'chunked',
     connection: 'close',
     date: 'Sun, 06 May 2018 03:38:13 GMT',
     server: 'tencent-cos',
     'x-cos-request-id': '************************' } }
```

> 上传成功了
>
> 敏感信息用*号代替了
>
> 但是文件在根目录下

###优化：上传到指定路径

```
var filepath='D:/135.png';
var filename = filepath.substring(filepath.lastIndexOf("/")+1); 
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth() + 1;
var urlkey=year+"/"+(month<10?'0'+month:month)+"/"+filename;


// 引入模块
var COS = require('cos-nodejs-sdk-v5');
// 创建实例
var cos = new COS({
    AppId: '*',
    SecretId: '*',
    SecretKey: '*',
});
// 分片上传
cos.sliceUploadFile({
    Bucket: '*',
    Region: '*',
    Key: urlkey,
    FilePath: filepath
}, function (err, data) {
    console.log(err, data);
});
```

执行脚本

```
D:\>node 2.js
warning: AppId has been deprecated, Please put it at the end of parameter Bucket(E.g: "test-1250000000").
(node:7620) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
null { Location: '*.cos.*.myqcloud.com/2018/05/135.png',
  Bucket: '*',
  Key: '2018/05/135.png',
  ETag: '"*-1"',
  statusCode: 200,
  headers:
   { 'content-type': 'application/xml',
     'transfer-encoding': 'chunked',
     connection: 'close',
     date: 'Sun, 06 May 2018 04:16:42 GMT',
     server: 'tencent-cos',
     'x-cos-request-id': '*=' } }
```

查看返回值Location生成路径已经有年月了

### 优化：上传后自动存放在剪切板

略

### 优化：生成markdown格式

```
var picsuffix=new Array(".jpg", ".png", ".bmp", ".jpeg");
function contains(arr, obj) {
  var i = arr.length;
  while (i--) {
    if (arr[i] === obj) {
      return true;
    }
  }
  return false;
}

var filepath='D:/tk.db';
var filename = filepath.substring(filepath.lastIndexOf("/")+1); 
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth() + 1;
var urlkey=year+"/"+(month<10?'0'+month:month)+"/"+filename;
var suffix=filename.substring(filename.lastIndexOf("."), filename.length);

// 引入模块
var COS = require('cos-nodejs-sdk-v5');
// 创建实例
var cos = new COS({
    AppId: '*',
    SecretId: '*',
    SecretKey: '*',
});
// 分片上传
cos.sliceUploadFile({
    Bucket: '*',
    Region: '*',
    Key: urlkey,
    FilePath: filepath
}, function (err, data) {
    console.log(err, data);
	const util = require('util');
	var url='';
	if (contains(picsuffix, suffix)) {
		url='![](https://'+data.Location+')';
	}
	else {
		url='[](https://'+data.Location+')';
	}
	require('child_process').spawn('clip').stdin.end(url);
});
```

- 这次定义了数组picsuffix，实现了图片与文件生成不同的字符串
- 实现了自动拷贝到剪切板的功能

## 关联bat与上传脚本

- 修改之前的bat批处理文件

  ```
  @echo off
  node D:\2.js %1%
  exit
  ```

- 修改js脚本

  ```
  var picsuffix=new Array(".jpg", ".png", ".bmp", ".jpeg");
  function contains(arr, obj) {
    var i = arr.length;
    while (i--) {
      if (arr[i] === obj) {
        return true;
      }
    }
    return false;
  }
  
  var filepath=process.argv.splice(2).toString();
  var filename = filepath.substring(filepath.lastIndexOf("\\")+1); 
  var today = new Date();
  var year = today.getFullYear();
  var month = today.getMonth() + 1;
  var urlkey=year+"/"+(month<10?'0'+month:month)+"/"+filename;
  var suffix=filename.substring(filename.lastIndexOf("."), filename.length);
  
  // 引入模块
  var COS = require('cos-nodejs-sdk-v5');
  // 创建实例
  var cos = new COS({
      AppId: '*',
      SecretId: '*',
      SecretKey: '*',
  });
  // 分片上传
  cos.sliceUploadFile({
      Bucket: '*',
      Region: '*',
      Key: urlkey,
      FilePath: filepath
  }, function (err, data) {
  	if(err){
  		console.log(err);
  	}
  	else{
  		console.log(data);
  		const util = require('util');
  		var url='';
  		if (contains(picsuffix, suffix)) {
  			url='![](https://'+data.Location+')';
  		}
  		else {
  			url='[](https://'+data.Location+')';
  		}
  		require('child_process').spawn('clip').stdin.end(url);
  	}
  });
  ```

- 大功告成