# supersqli

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=279780af-0dcb-4a1c-b8d3-fd0410115df9_2)

sql注入还是要看知识面啊，因为你永远都不知道会遇到什么数据库，要用什么语句。

场景就是一个输入框，看来这就是我们的注入点了。

![inject](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/inject.png)

直接输入1'可以得到报错内容。(基础的sql注入一般都是输入引号进行测试)

- error 1064 : You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1''' at line 1

MariaDB又是什么数据库啊？

- ### MariaDB
- > MariaDB数据库管理系统是 MySQL 的一个分支，主要由开源社区在维护，采用GPL授权许可。MariaDB的目的是完全兼容MySQL，包括API和命令行，使之能轻松成为MySQL的替代品。 在MariaDB与MySQL几乎一模一样，它们有相同的命令、界面，以及库与API。

哦，跟MySQL差不多。那就把这个当成一个MySQL注入题得了。既然有报错，那就试一下联合注入(union select)。

- return preg_match("/select|update|delete|drop|insert|where|\./i",$inject);

没那么简单，这里把select过滤了。且有/i标志，意味着全局匹配且大小写不敏感。看来得考虑别的。既然我们不能在一条语句里注入，多来几条怎么样？这种方法就叫堆叠注入。主要原理就是MySQL数据库中用 ; 来表示一条语句的结束，所以我们也可以在payload中添加 ; 来一次注入多条语句。

- ?inject=1';show databases; #

我们要往inject传参数，payload中用'闭合前面的语句，;拼接下一条语句，show database在mysql中可以列出服务器上所有的数据库。#注释后面的内容。

![dataBases](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/showDatabases.png)

既然这个挑战叫supersqli，那就看看supersqli数据库里有啥。我们现在应该就在supersqli数据库里，所以可以直接使用show tables来列出当前数据库中所有的表。

- ?inject=1';show tables; #

![tables](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/showTables.png)

有两个表，都看看里面有啥。show columnns可以从显示指定表（用from指定）中的字段，表名要用反引号\``扩起来，因为当字符串为表名进行操作时要加反引号

- ?inject=1';show columns from \`words`; #

![words](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/words.png)

- ?inject=1';show columns from \`1919810931114514`; #

![flag](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/flagTable.png)

可以看见flag在1919810931114514这个表中。问题是我们的select不能用，该怎么看这个字段中的内容呢？我们可以利用预编译来构造一条查询语句。

- ### 预编译
- > 执行一条sql查询语句需要经过三个步骤：（1）词法和语义解析    （2）优化sql语句，制定执行计划  （3）执行并返回结果
- > 跟编程一样，有些常用的语句可能会被用很多次。但是如果每次用的时候都来这三步，语句量大的时候效率就不行了。一般常用的语句每次只会有查询的值有细微差别，所以我们可以将这类语句中查询的值用占位符替代，将sql语句模板化或者说参数化，就可以一次编译、多次运行，省去了解析优化等过程。

我们主要会用到三条命令

- ### set
- > 可以理解为设置变量或准备即将预编译的语句。
- > 语法：set @名称=值
- ### prepare
- > 预编译一条sql语句。
- > 语法：prepare 语句名 from 语句
- ### execute
- > 执行预编译语句
- > 语法：execute 语句名 \[变量]\(可选)

那么我们可以准备下面这个payload：

- ?inject=1';set @sql=concat('s','elect * from \`1919810931114514`');PREPARE pre FROM @sql;EXECUTE pre; #
- > 不能在直接拼接select，因为这样就是字符串而不是可以执行的语句了。

这条语句意为：set准备需要的select语句（用concat拼接字符串绕过过滤，prepare预编译语句，execute执行语句。

- ### Flag
- > flag{c168d583ed0d4d7196967b28cbd0b5e9}