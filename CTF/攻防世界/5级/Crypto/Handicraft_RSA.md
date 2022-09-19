# Handicraft_RSA

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=198c3589-ddb9-49d2-b6ee-99de91f744b2_2)

我大意了。

来吧rsa，反正我基本做不出来。

```python
#!/usr/bin/python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from secret import s, FLAG
def gen_prime(s):
    while True:
        r = getPrime(s)
        R = [r]
        t = int(5 * s / 2) + 1
        for i in range(0, t):
            R.append(r + getRandomRange(0, 4 * s ** 2))
        p = reduce(lambda a, b: a * b, R, 2) + 1
        if isPrime(p):
            if len(bin(p)[2:]) == 1024:
                return p
while True:
    p = gen_prime(s)
    q = gen_prime(s)
    n = p * q
    e = 65537
    d = inverse(e, (p-1)*(q-1))
    if len(bin(n)[2:]) == 2048:
        break
msg = FLAG
key = RSA.construct((long(n), long(e), long(d), long(p), long(p)))
for _ in xrange(s):
    enc = key.encrypt(msg, 0)[0]
    msg = enc
print key.publickey().exportKey()
print '-' * 76
print enc.encode('base64')
print '-' * 76
```

gen_prime函数非常有迷惑性，我看了半天都不知道它在干什么，也没发现漏洞点。直到我看了wp的第一行：“n可以直接被分解”。直接就能被分解那我想这么复杂干什么？看来以后不要盲目分析，先分解试试。把output.txt中的公钥部分复制出来保存成publickey.txt，用Crypto读取公钥，然后放到factordb在线分解。还没结束，加密脚本循环了s次，也就是把明文加密了s次，而s是未知的。好办，直接破解就行了。把output.txt删除公钥部分和分割线，保存。

```python
from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long,long_to_bytes,inverse
with open("publickey.txt") as f:
    key=f.read()
pub_key=RSA.import_key(key)
print(f"n: {pub_key.n} , e: {pub_key.e}")
p=139457081371053313087662621808811891689477698775602541222732432884929677435971504758581219546068100871560676389156360422970589688848020499752936702307974617390996217688749392344211044595211963580524376876607487048719085184308509979502505202804812382023512342185380439620200563119485952705668730322944000000001
q=155617827023249833340719354421664777126919280716316528121008762838820577123085292134385394346751341309377546683859340593439660968379640585296350265350950535158375685103003837903550191128377455111656903429282868722284520586387794090131818535032744071918282383650099890243578253423157468632973312000000000000001
e=65537
d=inverse(e,(p-1)*(q-1))
with open("output.txt") as f:
    msg=bytes_to_long(b64decode(f.read()))
for i in range(100):
    msg=pow(msg,d,p*q)
    if b'flag' in long_to_bytes(msg):
        print(long_to_bytes(msg))
        break
```

看了官方wp，发现原题要用pollard p-1，也就是分解smooth因数的。可能比赛结束后有人把分解结果上传到factordb了？

- ### Flag
  > ASIS{n0t_5O_e4sy___RSA___in_ASIS!!!}