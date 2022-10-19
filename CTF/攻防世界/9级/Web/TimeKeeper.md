# TimeKeeper

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=8bd4b5cb-8924-41c7-b27d-e73595840933_2)

这题是出了非预期解吗？

进入网站，一个购物的。这个模板怎么这么眼熟呢？原来是我之前做过同样模板的题。登录注册界面统统搞一遍sql，没东西。看robots.txt和www.zip找找有没有泄露的，没有。抓个包看看，日常习惯加一。

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 21849
Vary: Cookie
Set-Cookie: session=.eJwVzU0KgzAQQOGrlJxAJ7oRuhstCjOBkjQkm0Jb6k_Mpl0oEe9eu3nL723ivn4_b1Ft4vQQlaDkVsYuKku5R5N5dJLAjwpNQXAd2DaRk5N-okxhDU73JWsHhK-R9DN3qc-Unidvm5FtnfvoJMe2pEtbuNRKj33G0QDD4UxUcDqKYWHoIuMQGeqFdRcYTEnJlJz6RenbrHAOnOZweIf1_4Wz2PcfgJo9Kw.FjDniw.TXVnUCHPXktAHdm1-eFu9_vkXHI; HttpOnly; Path=/
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 19 Oct 2022 01:42:35 GMT
```

这是返回的包。又是python啊，找了一会ssti，没有。格局小了，怎么能一看到python就觉得它有ssti漏洞呢？然而别的我也确实不会了，来个[wp](https://blog.csdn.net/weixin_44604541/article/details/109147735)。什么竟然还能这样？flask有个关于debug模式的[漏洞](https://blog.cfyqy.com/article/805da219.html),如果开了debug模式，我们就可以强行制造bug，触发debug界面。旧版flask可以直接利用这个debug界面的交互shell执行代码，新版则要用pin码认证。这样是不是就很安全了呢？并没有，pin码是根据算法生成的，有固定值。算法需要6个变量。

```
username 启动这个Flask的用户
modname 一般默认flask.app
getattr(app, '__name__', getattr(app.__class__, '__name__')) 一般默认flask.app为Flask
getattr(mod, '__file__', None)为flask目录下的一个app.py的绝对路径,可在爆错页面看到
str(uuid.getnode()) 则是网卡mac地址的十进制表达式
get_machine_id() 系统id
```

一般情况下获取这些值有些困难。

uaername 可以从/etc/passwd或者/proc/self/environ环境变量中读取

getattr(mod, '__file\__', None) flask目录下的一个app.py的绝对路径,这个值可以在报错页面看到。但有个坑，python3是app.py，python2中是app.pyc

网卡地址 读取这两个地址：/sys/class/net/eth0/address 或者 /sys/class/net/ens33/address

machine_id()
linux读取这三个文件 /proc/self/cgroup、/etc/machine-id、/proc/sys/kernel/random/boot_id
windows读取注册表中的HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography

2020.1.5对machine_id()进行了更新 get_machine_id unique for podman

https://github.com/pallets/werkzeug/commit/617309a7c317ae1ade428de48f5bc4a906c2950f

修改前是依序读取/proc/self/cgroup、/etc/machine-id、/proc/sys/kernel/random/boot_id三个文件，只要读取到一个文件的内容，立马返回值。
修改后是从/etc/machine-id、/proc/sys/kernel/random/boot_id中读到一个值后立即break，然后和/proc/self/cgroup中的id值拼接。

假如有个路径穿越的话一切都不是问题了。非常幸运的是，真的有。

```html
<link href="/asserts/css/bootstrap.min.css" rel="stylesheet">
<link href="/asserts/css/jumbotron-narrow.css" rel="stylesheet">
```

看这行很常见的引用bootstrap的代码，这个路径是不是和平时不一样？下面那行引用另一个css文件也是通过这个路径来的。虽然有可能设计时就是把这两个文件放asserts下了，不过测试一下有没有路径穿越也不难。

- /asserts/../../../../../../etc/passwd

我是在bp发的，直接发应该也行，不过最好编码一下。发现密码文件出来了，我们猜对了。倒是可以尝试把需要的文件读取出来构造pin码拿一个快乐shell，或者当个赌怪，一般flag在哪？根目录或者网站根目录下，名字一般叫flag，flag.txt或者php题是flag.php。最后发现flag.txt直接成功。

- /asserts/../../../../../../flag.txt

得到flag后去看了眼官方wp，我去好复杂，毕竟9分题。但是设计失误导致使用非预期解就变成了一道赌怪题。

### Flag
- cyberpeace{022a3e01165c771f4dfb7996d8183771}