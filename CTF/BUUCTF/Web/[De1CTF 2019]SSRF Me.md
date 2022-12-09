# [De1CTF 2019]SSRF Me

[题目地址](https://buuoj.cn/challenges#[De1CTF%202019]SSRF%20Me)

非预期解直接把这道题拉低了好几个档次。

进入网站，一坨代码。因为注释无法利用网站美化，提前看[wp](https://blog.csdn.net/qq_42967398/article/details/103549258)获取源代码。

```python
#! /usr/bin/env python
#encoding=utf-8
from flask import Flask
from flask import request
import socket
import hashlib
import urllib
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('latin1')

app = Flask(__name__)

secert_key = os.urandom(16)


class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)
        if(not os.path.exists(self.sandbox)):          #SandBox For Remote_Addr
            os.mkdir(self.sandbox)

    def Exec(self):
        result = {}
        result['code'] = 500
        #检查签名
        if (self.checkSign()):
            if "scan" in self.action:  #传进来的action里要有scan
                tmpfile = open("./%s/result.txt" % self.sandbox, 'w')
                resp = scan(self.param) #获取param函数的值，那这个就传flag.txt
                if (resp == "Connection Timeout"):
                    result['data'] = resp
                else:
                    print resp
                    tmpfile.write(resp)
                    tmpfile.close()
                result['code'] = 200
            if "read" in self.action:  #传进来的action里要有read
                f = open("./%s/result.txt" % self.sandbox, 'r')
                result['code'] = 200
                result['data'] = f.read()  #这里面才存储着真正的flag，因此要求action里scan和read都有
            if result['code'] == 500:
                result['data'] = "Action Error"
        else:
            result['code'] = 500
            result['msg'] = "Sign Error"
        return result

    def checkSign(self):
        if (getSign(self.action, self.param) == self.sign):   #这里就是检查传入的md5值和算出来的一不一样
            return True
        else:
            return False

#/geneSign路径，可以get或者post传参
#generate Sign For Action Scan.
@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.unquote(request.args.get("param", ""))  #如果param参数不传，默认值就是空
    action = "scan" #action写死了
    return getSign(action, param) #返回md5值

#/geneSign路径，同样可以get或者post传参
@app.route('/De1ta',methods=['GET','POST'])
def challenge():
    action = urllib.unquote(request.cookies.get("action"))  #这个和sign都是通过cookie传值
    param = urllib.unquote(request.args.get("param", ""))   #这个get或post都行
    sign = urllib.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
    if(waf(param)):
        return "No Hacker!!!!"
    task = Task(action, param, sign, ip)
    return json.dumps(task.Exec()) #目标是让这里dump出flag.txt的内容
@app.route('/')
def index():
    return open("code.txt","r").read()

#上面用到的scan函数是自定义的，别和python自带的搞混了
def scan(param):
    socket.setdefaulttimeout(1)
    try:
        return urllib.urlopen(param).read()[:50]
    except:
        return "Connection Timeout"


#永远不要使用拼接来生成md5值。这里直接拼接全部参数的值生成md5，也是非预期解出现的根本原因
def getSign(action, param):
    return hashlib.md5(secert_key + param + action).hexdigest()


def md5(content):
    return hashlib.md5(content).hexdigest()


def waf(param):
    check=param.strip().lower()
    if check.startswith("gopher") or check.startswith("file"):
        return True
    else:
        return False


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
```

代码里分析了一波，如果我们在De1ta页面让各个参数的值为：

```
param=flag.txt
action=readscan
sign=？？？，应为secret_key+flag.txt+readscan
```

getSign函数生成签名时把secret_key放进去了，导致我们不能自己算出md5。然而geneSign拼接生成出大问题。虽然里面action固定是scan，但是param可控啊。而且getSign把action放到param后面了，可以利用一下。我们想要读取flag时action等于readscan，就在getSign时这么传：

```
param=flag.txtread
```

然后会生成`secret_key+flag.txtread+scan`的md5值。等一下，这不和De1ta里面需要的md5值一样吗？直接开干。

- http://6f229b7f-6c06-447f-9c45-2b16727fa4e4.node4.buuoj.cn:81/geneSign?param=flag.txt

获取到md5`8fb36efc6bdd64d73e4ff92d145f9abb`。这个值每个人都会不一样。现在去拿flag。

- http://6f229b7f-6c06-447f-9c45-2b16727fa4e4.node4.buuoj.cn:81/De1ta?param=flag.txt

cookie的添加用chrome控制台搞定。

```js
document.cookie="action=readscan";
document.cookie="sign=8fb36efc6bdd64d73e4ff92d145f9abb";
```

这题预期解是[MD5hash长度扩展攻击](https://joychou.org/web/hash-length-extension-attack.html)。

- 效果：预测md5(salt+message+padding+append)值
- 条件：以下内容需要提前得知
  > md5(salt+message)的值
  > message内容
  > salt+message长度

原理说难也不难，关键在于了解md5算法内部的实现。简单提一嘴，里面有4个magic number。这几个magic number与最终生成的md5值息息相关。比如`21232f297a57a5a743894a0e4a801fc3`这个md5值，算法内部生成完成的那一刻，4个magic number分别是：

```
A=0x292f2321
B=0xa7a5577a
C=0xe4a8943
D=0xc31f804a
```

换个端序拼在一起就是md5值了。另外一个重要的点，在于md5加密信息时会把原文分成若干个信息块，每块长64字节。不足64字节的就要padding。padding的规则是，在最末一个字节之后补充0x80，其余的部分填充为0x00，padding最后的8字节用来表示需要哈希的消息长度。一个块会更新一轮magic number，更新后的Magic number被用于计算下一个块的md5值。

现在我们知道了md5(salt+message)的值，就能推断出md5(salt+message)时的magic number。因为md5算法实现是公开的，直接把初始值设定为推断出来的magic number，然后加密自己的东西，不就能得到和正常md5加密一样的结果了吗？达成这点很简单，把要加的内容和原始值在一起做个padding，利用推断出来的magic number加密一轮，完成。

这里只是简单提了一下，具体还是要看文章。[这篇](http://blog.chinaunix.net/uid-27070210-id-3255947.html)讲的也很好。建议直接用工具：[hushpump](https://github.com/bwall/HashPump)。

## Flag
> flag{407ea613-9b44-4e39-9405-1d5d63bc7056}