# halo

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c114f5b0-23d4-4e3a-b2f5-9d8e430dd049_2)

这题绷不住了，真的太离谱了。

附件内容如下（是的这次我要把附件放出来，才能凸显离谱之处）

- aWdxNDs0NDFSOzFpa1I1MWliT09w

base家族在向我招手。base64解码后得到一串用途不明显的字符串，

- igq4;441R;1ikR51ibOOp

在我印象中，没啥密码长这样吧？非要说跟凯撒那种移位密码也行，可是移到什么程度算是flag？看wp发现要按位异或。emmm……有点猜的感觉了。爆破异或的值还是很简单的。

```python
from base64 import b64decode
data=list(b64decode("aWdxNDs0NDFSOzFpa1I1MWliT09w"))
for i in range(100):
    candidate=''
    for j in data:
        candidate+=chr(j^i)
    print(candidate)
```

一堆结果里只有一个全字母数字，没有其他乱七八糟的玩意。

- jdr78772Q82jhQ62jaLLs

python3里面b64decode是个已经被ord的数组，所以直接异或就行了。但是为什么不对？我真的百思不得其解，只能去看官方wp了。wp如下：

```python
import string
from base64 import *
b=b64decode("aWdxNDs1NDFSOzFpa1I1MWliT08w")
data=list(b)
for k in range(0,200):
    key="“
    for i in range(len(data)):
        key+=chr(ord(data[i])^k)
    print (key)
```

这里需要用ord，注意和上面区分，不是咱们的逻辑差不多啊，哪里错了？后面一个一个字符比对才发现是末尾是08w，而不是附件给的09w。不是这谁想得到啊？出题出错了吧？如果题真的就这么设计的我一巴掌打死出题人。所以正确脚本如下：

```python
from base64 import b64decode
data=list(b64decode("aWdxNDs0NDFSOzFpa1I1MWliT08w"))
for i in range(100):
    candidate=''
    for j in data:
        candidate+=chr(j^i)
    print(candidate)
```

从来没有这么无语过。

- ### Flag
  > flag{jdr78672Q82jhQ62jaLL3}