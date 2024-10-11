# ezlegendre

```py
from sympy import *
from Crypto.Util.number import *
p = 303597842163255391032954159827039706827
c=
flag=""
for i in c:
        if legendre_symbol(i,p)==-1:
                flag+='0'
        else:
                flag+='1'
print(long_to_bytes(int(flag,2)))
```
看了flag才知道到底是为啥……看到题目名称就想到legendre符号，再稍微实验一下就知道答案了