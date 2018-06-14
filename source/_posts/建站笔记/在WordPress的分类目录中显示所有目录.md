---
title: 在WordPress的分类目录中显示所有目录
categories:
  - 建站笔记
abbrlink: 21017
date: 2018-05-03 09:47:13
tags:
---

默认仅显示有文章的目录，没有文章的不显示
  <!--more-->
  
特殊需求下，可以修改主题的functions.php文件

文件路径``/htdocs/wp-content/themes/[主题名称]/functions.php``

在文件头部增加代码如下 

```php
add_filter( 'widget_categories_args', 'wpdx_show_empty_cats' );
function wpdx_show_empty_cats($cat_args) {
    $cat_args['hide_empty'] = 0;
    return $cat_args;
}
```

