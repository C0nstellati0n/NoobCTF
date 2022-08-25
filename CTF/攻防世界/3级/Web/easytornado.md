# easytornado

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c458642a-8cd8-42fd-8750-f4343020a408_2)

场景打开是由几个非常简陋的页面组成的。

- /flag.txt<br>/welcome.txt<br>/hints.txt

flag.txt里面告诉了我们flag的位置。

- /flag.txt<br>flag in /fllllllllllllag

welcome.txt里面只有一个单词。

- /welcome.txt<br>render

hints.txt似乎告诉了我们某种格式。

- /hints.txt<br>md5(cookie_secret+md5(filename))

filename我们已经知道了，问题是这个cookie_secret是啥？查看当前网页的cookie发现并不是普通的cookie。不过既然题目提到了tornado，那就搜一下是啥。

- ### Tornado
- > 一种 Web 服务器软件的开源版本。Tornado 和主流Web 服务器框架（包括大多数 Python 的框架）有着明显的区别：它是非阻塞式服务器，而且速度相当快。

看来是一种网页模版。模版大家都很熟悉这个词了，模版注入也是web常考项之一。随便捣鼓一下页面，发现在filehash不正确的情况下会出现错误页面。

- http://61.147.171.105:54410/error?msg=Error

get传参，条件反射改一下传的东西看看有没有回显。结果发现有，离模版注入又近了一步。{{}}是Tornado的表达式，可以是任意的Python表达式, 包括函数调用。所以尝试在里传一些内容进行测试。

- http://61.147.171.105:54410/error?msg={{datetime}}

在Tornado的前端页面模板中，datetime是指向python中datetime这个模块，Tornado提供了一些对象别名来快速访问对象，可以参考Tornado官方文档。

根据输出结果判断有模版注入。查阅文档后发现目标cookie_secret在Application对象settings属性中。不过这里没法直接调用self.application.settings，还要想别的办法。

- RequestHandler.settings
- > Application.reverse_url 的别名。

找到了个别名，但是RequestHandler.settings好像也不能被直接调用……不过还有个handler，指向的处理当前这个页面的RequestHandler对象。所以当我们调用handler.settings是就等同于调用self.application.settings。开始构造payload。

- http://61.147.171.105:54410/error?msg={{handler.settings}}

- {'autoreload': True, 'compiled_template_cache': False, 'cookie_secret': '5c519b0f-beb1-438f-893a-e571a1853dd7'}

拿到cookie_secret了。接下来就根据hint.txt的内容构造filehash了。将cookie_secret的值拼上filename的md5值，再把得到的结果再次md5加密，得到的结果就是filehash了。注意这里加密的是/fllllllllllllag。

- http://61.147.171.105:54410/file?filename=/fllllllllllllag&filehash=326c027165a51c4271522c4e70bb261e

- ### Flag
- > flag{3f39aea39db345769397ae895edb9c70}
