# ez_cbc

看看附件。

```python
from Crypto.Util.number import *
import random
from secret import flag

IV = bytes_to_long(b'cbc!') 
K = random.randrange(1,1<<30)
assert flag[:7] == b'moectf{'
assert flag[-1:] == b'}'

block_length = 4
flag = flag + ((block_length - len(flag) % block_length) % block_length) * b'\x00'
plain_block = [flag[block_length * i: block_length * (i + 1)] for i in range(len(flag) // block_length)]

c = []
c0 = (IV ^ bytes_to_long(plain_block[0])) ^ K
c.append(c0)
for i in range(len(plain_block)-1):
    c.append(c[i] ^ bytes_to_long(plain_block[i+1]) ^ K)

print(c)

'''
[748044282, 2053864743, 734492413, 675117672, 1691099828, 1729574447, 1691102180, 657669994, 1741780405, 842228028, 1909206003, 1797919307]
'''
```

cbc，但是没有key。key是一个随机数，不可能被我们猜到，至于能不能推算出来我也不知道。理一下逻辑。

```python
flag = flag + ((block_length - len(flag) % block_length) % block_length) * b'\x00'
```

len(flag) % block_length 求出flag最后不足block_length的部分的长度。block_length - len(flag) % block_length 求出flag在最后需要的补位长度。有点难描述，我画个图（其实是我自己把自己绕晕了）

- xxxx xxx 是明文，len(flag) % block_length 表达式结果为3
- block_length - len(flag) % block_length=4-3=1
- (block_length - len(flag) % block_length) % block_length=1%3=1

至于为啥最后还要% block_length这点我不太理解，(block_length - len(flag) % block_length) 表达式的值怎么都应该小于等于block_length才对。算了我的数学不配质疑脚本。总之这段就是用\x00对齐长度，方便加密，不能再探讨了，再探讨我就不会了。

```python
plain_block = [flag[block_length * i: block_length * (i + 1)] for i in range(len(flag) // block_length)]
```

按照block_length的长度将flag分为len(flag) // block_length)这么多块。这应该就是明文块了。

重点来了，加密逻辑。

```python
c = []
c0 = (IV ^ bytes_to_long(plain_block[0])) ^ K
c.append(c0)
```

初始化密文块，密文块的每一块由IV异或明文块异或K而成。目前不知道K看起来没有突破点。继续。

```python
for i in range(len(plain_block)-1):
    c.append(c[i] ^ bytes_to_long(plain_block[i+1]) ^ K)
```

把当前密文块异或明文块的下一块再异或K。你这K有毛病啊，你刚刚不是异或过了吗，怎么又来了？把整个式子简化一下。

- c1=c0^m1^k,c0=IV^m0^k,c1=IV^m0^k^m1^k,c1=IV^m0^m1

不知道能不能这么写，但我觉得两次异或k后应该等于没有异或……吧？这么看下来c1=m0^m1，因为IV已知所以可以当作没有。m0我们知道是固定的flag前缀，现在试一下看看能不能解密。

第二块逆向出来了，但是剩下的全是乱码。我就知道没那么简单,还没推算c2呢。

- c2=c1^m2^k,c1=IV^m0^m1,? (IV^m0^m1^m2^k)

问题来了，c1被解密后是没有k的，意味着k不会被抵消。就算代入IV^m0^k^m1^k，那也有3个k，还是无法取消。推c3看看。

- c3=c2^m3^k,c2=c1^m2^k=IV^m0^m1^m2^k,c3=IV^m0^m1^m2^k^m3^k,c3=IV^m0^m1^m2^m3,c3=m2^m3

还是像之前一样，把已知项取消。可以发现c3的结构和c1很像，但这次我们既不知道m2也不知道m3。同时判断可能有这样一个规律：第n（n为偶数，偶数是因为我们省略了第0个密文块）个密文块等于第n-1个明文块异或第n个明文块。

线索到这就断了。再往下推还有用吗？

- c4=c3^m4^k=m2^m3^m4^k=m4^k

没用。

- c5=c4^m5^k=m2^m3^m4^k^m5^k=m5^k

还可以将当前密文块与前一个密文块异或，得到cn=mn^k。没用，除了能帮我们把解不出来的题变得更加解不出来。

不对啊，c2是不是还可以这么写？

- c2=c1^m2^k=c0^m1^k^m2^k=c0^m1^m2

这不就又抵消了吗？多写一点看看整体规律。

- c3=c2^m3^k=c1^m2^k^m3^k=c1^m2^m3
<br>c4=c3^m4^k=c2^m3^k^m4^k=c2^m3^m4

cn=c(n-2)^m(n-1)^mn可能是规律，则mn=cn^(c(n-2)^m(n-1))。括号是必须项，异或逆向时多打大括号，把需要求的项单独放出来，其余全部括号括起来。比如把c(n-2)^m(n-1)^m看成a^b就能很简单看出来谁异或谁了。c0和c1除外，c1=IV^m0^m1，c0的明文我们已经知道了。研究解密脚本。

出了出了！这题可以，不是特别难但是也不像入门题一样看都不用看就出来了，留给我这样的萌新思考余地。最重要是没有脑洞（misc我说的就是你）。当然对大佬们来说就是小菜一碟了。

```python
from Crypto.Util.number import *
IV = bytes_to_long(b'cbc!')
cipher=[748044282, 2053864743, 734492413, 675117672, 1691099828, 1729574447, 1691102180, 657669994, 1741780405, 842228028, 1909206003, 1797919307]
flag=[1836016995,1952873317]
for i in range(2,len(cipher)):
    flag_part=cipher[i]^(cipher[i-2]^flag[i-1])
    flag.append(flag_part)
flag_str=b''
for i in flag:
    flag_str+=long_to_bytes(i)
print(flag_str)
```

脚本中flag的第二项是第一次推出来的，和其他的规律不一样就没有放在一起。

- ### Flag
  > moectf{es72b!a5-njad!@-#!@$sad-6bysgwy-1adsw8}

