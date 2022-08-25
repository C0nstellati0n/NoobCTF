# SM

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=2cdc51a8-5213-402e-bafa-34d2f9e8a285_2)

我的数学没救了。

附件是个python脚本加上ef，ps和r这三个不知道是啥的文件。分析一下代码。

```python
from Crypto.Util.number import getPrime,long_to_bytes,bytes_to_long
from Crypto.Cipher import AES
import hashlib
from random import randint
def gen512num():
    order=[]
    while len(order)!=512:
        tmp=randint(1,512)
        if tmp not in order:
            order.append(tmp)
    ps=[]
    for i in range(512):
        p=getPrime(512-order[i]+10)
        pre=bin(p)[2:][0:(512-order[i])]+"1"
        ps.append(int(pre+"0"*(512-len(pre)),2))
    return ps
def run():
    choose=getPrime(512)
    ps=gen512num()
    print "gen over"
    bchoose=bin(choose)[2:]
    r=0
    bchoose = "0"*(512-len(bchoose))+bchoose
    for i in range(512):
        if bchoose[i]=='1':
            r=r^ps[i]
    flag=open("flag","r").read()
    key=long_to_bytes(int(hashlib.md5(long_to_bytes(choose)).hexdigest(),16))
    aes_obj = AES.new(key, AES.MODE_ECB)
    ef=aes_obj.encrypt(flag).encode("base64")
    open("r", "w").write(str(r))
    open("ef","w").write(ef)
    gg=""
    for p in ps:
        gg+=str(p)+"\n"
    open("ps","w").write(gg)
run()
```

先搞清楚那三个文件是啥。根据“ef=aes_obj.encrypt(flag).encode("base64")”可以得到ef为被aes加密后再进行base64编码的flag。ps来自于gen512num方法，r来自于一连串异或操作。

想解密flag就要知道aes的key，而key是choose的md5值的16进制。那我们的目标应该就是找到choose了。choose是一个用getPrime方法得到的512位质数，不太可能找到，但是下面还有个bchoose，是choose的二进制。接着为了让bchoose的长度为512，在右边添上了未知数目的0。开始奇怪了，继续往下看。

```python
for i in range(512):
    if bchoose[i]=='1':
        r=r^ps[i]
```

这个操作相当于遍历bchoose，如果某一位为1，就把r的值设为r与ps对应索引的异或。r最开始为0。去看看生成ps的函数。

```python
def gen512num():
    order=[]
    while len(order)!=512:
        tmp=randint(1,512)
        if tmp not in order:
            order.append(tmp)
    ps=[]
    for i in range(512):
        p=getPrime(512-order[i]+10)
        pre=bin(p)[2:][0:(512-order[i])]+"1"
        ps.append(int(pre+"0"*(512-len(pre)),2))
    return ps
```

首先随机生成1-512的数字，数字不重复且顺序未知。ps中的每一项由以下操作得来：

1.生成 512-order[i]+10 位数的的质数<br>
2.pre为p的二进制，截取512-order[i] 的长度，然后在最后一位补1。<br>
3.pre补上末尾 512-len(pre) 长度的0，然后将整个二进制数字转为10进制的int。

第一步不重要，重点在第二第三步出现的特征。可以看出来ps中的每一项末尾都有不同长度的0，且不会重复，连续的0的前面一位必定是1。如果你数学好或者是身经百战的老师傅，应该早就感觉到什么东西了。但是我两者都不是，所以从基础复习一下。

- ### 异或
  > 同为0，异为1

现在我们有最后一次运算后的r和全部的ps。并不是所有的ps都与r进行异或，判断当前ps是否要与r进行异或的条件是bchoose当前位是否为1。所有的ps紧跟末尾一串0的1位置都不一样，如果当前ps与r进行了异或，那么r在ps的1那一位一定是1，否则就是0。我竟然花了很久才意识到这一点，还是看了别人的[答案](https://www.cnblogs.com/coming1890/p/13547193.html)后才知道的。

```python
from Crypto.Util.number import getPrime,long_to_bytes,bytes_to_long
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
with open("/Users/constellation/Desktop/r",'r') as f:
    r=int(f.read())
with open("/Users/constellation/Desktop/ps",'r') as f:
    ps=[int(i) for i in f.read().split('\n')[:-1]]
pbits=[bin(x).rfind('1')-2 for x in ps]
bc=['0']*512
for le in range(512):
    ind=pbits.index(511-le)
    tt=bin(r)[2:].rjust(512,'0')[511-le]
    if tt=='1':
        bc[ind]='1'
        r^=ps[ind]
key=int(''.join(bc),2)
with open('/Users/constellation/Desktop/ef','rb') as f:
    ef=b64decode(f.read())
    key=long_to_bytes(int(md5(long_to_bytes(key)).hexdigest(),16))
    aes_obj = AES.new(key, AES.MODE_ECB)
    print(aes_obj.decrypt(ef))
```

pbits=[bin(x).rfind('1')-2 for x in ps]找到每个ps从右往左数的第一个1的位置，-2是因为bin方法转换会有个0b前缀。ind=pbits.index(511-le) 找到bc对应的索引，511是因为上面的 512-order[i]+10 最短10，最长511，范围就是511（也许吧，这是我能想到最合理的解释了，我也不懂啊），这是为了让ps与r的操作逆向执行。tt=bin(r)[2:].rjust(512,'0')[511-le] 找到r在对应位置的数字，是1代表bc对应位置也是1，然后异或，进入下一步。

for循环结束后我们就得到了key。现在就可以解密了。

- ### Flag
  > flag{shemir_alotof_in_wctf_fun!}

