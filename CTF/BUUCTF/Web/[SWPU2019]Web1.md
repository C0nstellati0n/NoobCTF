# [SWPU2019]Web1

[题目地址](https://buuoj.cn/challenges#[SWPU2019]Web1)

开局一个登录框。自然是没测出来什么东西，老老实实注册一个用户，登录发现是一个广告发布平台。看到这个我就想到sql二次注入。从广告下手，找找漏洞点。当广告名为`'")}]`时，报错：

- You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '")}]' limit 0,1' at line 1

首要测试union select，看看有多少列什么的。

- ' union select 1,2,3#
    > 标题含有敏感词汇

不好有过滤。手动测试了一下，空格和#被过滤了。这俩都不是问题，空格用注释/**/绕，注释用另一个'闭合。这题不按套路出牌，平时我习惯直接1，2，3，4这样打，order by基本不用，因为一般都不会太多。这题打到10列的时候怀疑人生，遂用order by，然后被ban。行吧，上group by加二分法，上限50，最后得到有22行。

```
'union/**/select/**/1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22'
```

回显在2和3。

现在就是爆数据了。问题在于重要的information_schema也被ban了。好的不懂了，看[wp](https://blog.csdn.net/shinygod/article/details/123681039)，发现这根本不是问题，甚至有两种方法绕：

```
mysql.innodb_table_stats
sys.schema_auto_increment_columns
```

开开心心构造payload。

```
'union/**/select/**/1,2,group_concat(table_name),4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22/**/from/**/mysql.innodb_table_stats/**/where/**/database_name="web1"'
```

这题比较奇怪，database_name必须是这种形式而不能是database()。不是大事，之前多花一步爆数据库名就好了。表有ads和users，现在终极问题来了，由于我们使用的不是information_schema，导致没发直接查列名，因为无论是mysql.innodb_table_stats还是sys.schema_auto_increment_columns，都没有记录列名。于是引入第二个技巧：[无列名注入](https://err0r.top/article/mardasctf/)。这个技巧可以让我们在不知道列名的情况下直接爆值。先看payload。

```
-1'union/**/select/**/1, (select/**/group_concat(b)/**/from(select/**/1,2,3/**/as/**/b/**/union/**/select * from/**/users)x),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,'22 
```

这里我们选择2的位置回显爆出的内容，把2处的查询语句分解来看。`select/**/group_concat(b)/**/from`是一部分，`(select/**/1,2,3/**/as/**/b/**/union/**/select * from/**/users)x`是另一部分。第一部分的b来自于第二部分`select 1,2,3 as b`这一小部分给第三号列取了个别名b，而第二部分括号里的内容，叫派生表，完全是无列名差值的公式，刚刚给的文章内有详细说明。x是这个派生表的名字，随便取一个就行。或者我们这么看，`(select/**/1,2,3/**/as/**/b/**/union/**/select * from/**/users)x`从users中展开一个名为x的派生表，里面有列1，2，b（3的别名）。就把这个表看作正常表，该怎么select怎么select，于是有了`select/**/group_concat(b)/**/from`。