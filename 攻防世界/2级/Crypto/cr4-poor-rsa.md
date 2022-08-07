# cr4-poor-rsa

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=ac088cec-5373-4ffb-9e8a-ffc540735ffe_2)

这道题是很典型的rsa攻击方法之一——n值过小。

- ### RSA基础
- > 在RSA的加密过程中，常见地有n，p，q，e，d五个字母，它们分别指代了：
- > n:p和q的乘积
- > p:一个随机选择的大质数
- > q:也是一个大质数，但是要和p互质
- > e:一个整数，满足1<e<r
- > d:是e关于r的模反元素（如果存在）

好像又蹦出来了几个新名词，一起解释了：
- > r:即为φ(n),其值等于(p-1)*(q-a)
- > φ(n):小于或等于n的正整数中与n互质的数的数目
- > 模反元素:也称模倒数或者模逆元。定义为如果两个正整数a和b互质，那么一定可以找到整数c，使得 ac-1 被b整除，或者说ac被b除的余数是1。此时c就叫做a对模数b的“模反元素”

- ### 加密与解密
- > m为明文，c为密文
- > 加密：m^e ≡ c (mod n)$
- > 解密：c^d ≡ m (mod n)$
- > (n,e)是公钥，(n,d)是私钥

小白只需要记住结果就行了，“为什么”会在你做越来越多题后逐渐理解。当然，如果你拥有良好的数学基础，完全可以现在就去查询RSA的根本原理和证明。

那么看看上面的定义，为什么p和q一定要是大质数呢？这是因为RSA的安全性和p，q的大小密切相关。从上面不难看出解密与私钥的d息息相关，但是我们目前只知道公钥，该如何找到d呢？根据d的定义，我们在已经知道e的情况下还要找到r,但是r现在也不知道，所以根据r的定义，我们又要去找p-1和q-1的值。结果现在p和q也不知道，只有个n。那还能咋办，n等于p乘q，那就分解呗，现在计算机计算能力那么强大了，不至于找不到个分解结果……吧？

还真找不到。目前没有一种快速的算法可以将一个很大的数字分解成两个质数。我们又回到了“大数”这个定义上。到这里我们可以看看附件是什么了。

- ### flag.b64 
- > Ni45iH4UnXSttNuf0Oy80+G5J7tm8sBJuDNN7qfTIdEKJow4siF2cpSbP/qIWDjSi+w=

- ### key.pub
- -----BEGIN PUBLIC KEY-----
- ME0wDQYJKoZIhvcNAQEBBQADPAAwOQIyUqmeJJ7nzzwMv5Y6AJZhdyvJzfbh4/v8
- bkSgel4PiURXqfgcOuEyrFaD01soulwyQkMCAwEAAQ==
- -----END PUBLIC KEY-----

flag应该经过了base64加密，问题不大，但是这个公钥怎么看起来这么短？可以用python的Crypto第三方库来读取这个公钥。

```python
from Crypto.PublicKey import RSA
with open("你的公钥文件地址") as f:
    key=f.read()
pub_key=RSA.import_key(key)
print(f"n: {pub_key.n} , e: {pub_key.e}")
```

- ### 输出
- > n: 833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019,e: 65537

这对人类来说是个大数字，但是对于计算机来说，就是小菜一碟。前面说一定要“大数”的原因就是这个。像这样的数字我们完全可以直接暴力破解，无需担心不合理用时。可以用这个[网站](http://www.factordb.com/index.php?)来强行分解数字。

把得到的结果放进我们的解密脚本中。

```python
from Crypto.PublicKey import RSA
from base64 import b64decode
n=833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019
p=863653476616376575308866344984576466644942572246900013156919
e=65537
with open("你的flag.b64地址") as f:
    ciphertext=b64decode(f.read())
with open("你要存储的被b64解密后的文件的地址",'wb') as f:
    f.write(ciphertext)
q=n//p
toitent=(q-1)*(p-1)     #r
d=pow(e,-1,toitent)     #求模逆元素
component=(n,e,d)
rsa=RSA.construct(component)
with open("你要存储的私钥地址",'wb') as f:
    f.write(rsa.export_key())
```

网上很多writeup都是使用rsa模块来完成生成私钥的操作。但是我没有rsa库，所以这里就用Crypto的RSA库了。

- ### RSA.construct()
- > 接收一个元组作为参数，元组顺序依次为n，e，d。返回结果为根据参数所生成的私钥。可以使用export_key()方法来获得所生成的私钥。

最后就可以用openssl来解密了。

- > openssl pkeyutl -decrypt -in flag.b64 -inkey privateKey -out flag.txt

- ### Flag
- > ALEXCTF{SMALL_PRIMES_ARE_BAD}