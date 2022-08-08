# warmup

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=efa8c010-c20a-4693-90e9-ded8f5bef486_2)

考的是对php中include的理解。

![warmup](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/warmup.png)

进来直接滑稽怼脸。开发者工具检查元素发现了一个叫source.php的文件。

```php
<?php
    highlight_file(__FILE__);
    class emmm
    {
        public static function checkFile(&$page)
        {
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"];
            if (! isset($page) || !is_string($page)) {
                echo "you can't see it";
                return false;
            }

            if (in_array($page, $whitelist)) {
                return true;
            }

            $_page = mb_substr(
                $page,
                0,
                mb_strpos($page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }

            $_page = urldecode($page);
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
        }
    }

    if (! empty($_REQUEST['file'])
        && is_string($_REQUEST['file'])
        && emmm::checkFile($_REQUEST['file'])
    ) {
        include $_REQUEST['file'];
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
?>
```

看来又要想法子包含flag文件。先看看hint.php里是啥，毕竟现成的提示不看白不看。

- flag not here, and flag in ffffllllaaaagggg

所以flag在ffffllllaaaagggg文件里。$_REQUEST可以理解为$_GET，$_POST 和 $_COOKIE的整合数组。这里为了方便可以用get方法传参。过滤函数在checkFile函数中。看看该怎么绕过。

首先$page不为空且是字符串。这个肯定的，继续往下看。第二个if要求$page在$whitelist中。这个我们目前没有办法做到，如果我们就乖乖传入白名单中的内容的话，什么也不会发生。接下来切割出?前的字符串并继续判断切割后的结果是不是在白名单里。

这里就有问题了。根据函数的调用我们可以发现，传入checkFile的实参是 ?file= 后的值，那么正常来说这个值里根本就不会有问号。现在代码刻意在后面加了1个问号来取出文件名，但是如果我们自己提前传一个？的话，会发生什么呢？这里先看两个函数

- ### mb_substr()
- > 返回字符串的一部分，中文字符也可以使用。substr() 只针对英文字符
- > 语法：mb_substr(字符串，起始，长度，编码)，其中长度和编码可选。
- ### mb_strpos()
- > 返回要查找的字符串在别一个字符串中首次出现的位置
- > 语法：mb_strpos (字符串,要搜索的字符串)

因为mb_strpos()只会返回首次出现的位置，所以如果我们传类似于 hint.php?想要查看的文件路径 这样的payload的话，切割的结果是hint.php，通过了过滤。问题是过滤通过了后这个paylaod根本就不是一个有效的文件名啊？

不急。include有一个很有趣的特性：

- 如果参数中包含../这样的路径，解析器则会忽略../之前的字符串而去在当前目录的父目录下寻找文件

这意味着我们只要在想要查看的文件路径中使用../这类路径，include就会自动忽略前面的内容，这样真正包含的文件名就是有效的了。一点一点试就可以得到正确的路径了。

- ?file=hint.php?../../../../../ffffllllaaaagggg

- ### Flag
- > flag{25e7bce6005c4e0c983fb97297ac6e5a}