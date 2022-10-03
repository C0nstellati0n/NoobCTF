# special-rsa

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=bf642291-4175-4a1e-af48-a40710fb56a8_2)

至少我从不会做后连wp都看不懂进步到了只有不会做了。

又是rsa。很多时候rsa题目包含很多不只是rsa的考点。

```python
import os, sys
from key import k, random_r
import msgpack

N = 23927411014020695772934916764953661641310148480977056645255098192491740356525240675906285700516357578929940114553700976167969964364149615226568689224228028461686617293534115788779955597877965044570493457567420874741357186596425753667455266870402154552439899664446413632716747644854897551940777512522044907132864905644212655387223302410896871080751768224091760934209917984213585513510597619708797688705876805464880105797829380326559399723048092175492203894468752718008631464599810632513162129223356467602508095356584405555329096159917957389834381018137378015593755767450675441331998683799788355179363368220408879117131L

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    assert g == 1
    return x % m

def pad_even(x):
    return ('', '0')[len(x)%2] + x

def encrypt(ms, k):
    out = [] 
    for i in range(0, len(ms), 256):
        m = ms[i:i+256]
        m = int(m.encode('hex'), 16)
        r = random_r()
        r_s = pad_even(format(r, 'x')).decode('hex')
        assert m < N
        c = (pow(k, r, N) * m) % N
        c_s = pad_even(format(c, 'x')).decode('hex')
        out.append((r_s, c_s))
    return msgpack.packb(out)

def decrypt(c, k):
    out = ''
    for r_s, c_s in msgpack.unpackb(c):
        r = int(r_s.encode('hex'), 16)
        c = int(c_s.encode('hex'), 16)
        k_inv = modinv(k, N)
        out += pad_even(format(pow(k_inv, r, N) * c % N, 'x')).decode('hex')
    return out

if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1] not in ('enc', 'dec'):
        print 'usage: %s enc|dec input.file output.file' % sys.argv[0]
        sys.exit()

    with open(sys.argv[3], 'w') as f:
        if sys.argv[1] == 'enc':
            f.write(encrypt(open(sys.argv[2]).read(), k))
        elif sys.argv[1] == 'dec':
            f.write(decrypt(open(sys.argv[2]).read(), k))
```

看起来有点复杂，实际上这比一些5，6分的crypto题还好理解，只不过不看[wp](https://gist.github.com/elliptic-shiho/489804cd675ed11d7adb)之前有点难想到。附件还有一段明文和密文，叫它们m1和c1好了。

encrypt函数中，把ms按255的长度分成几份，每份用c = (pow(k, r, N) * m) % N这行代码加密，加密后的结果填充一下放进密文列表。具体怎么解密不用管，看解密要什么就行了。从decrypt函数中不难发现要密文和k。k暂时不知道，那么这道题的目标是找k。涉及到k的只有上面提到了那行加密代码了。快乐数学时间。

$c_1\equiv k_1^{r_1}*m_1\mod N$<br>$c_2\equiv k_2^{r_2}*m_2\mod N$

pow里面的mod n似乎不重要，不影响最终结果。这一写出来不就熟悉了吗？同余方程啊，不过把两个k的r次方看作一个整体，暂时找不出来真正的k。解也很简单，假如m和n互质的话，直接找逆元就行了。

$k_1^{r_1}=c_1*m_1^{-1}\mod N$<br>$k_2^{r_2}=c_2*m_2^{-1}\mod N$

但是我们不要次方的k，我们要k本身。这时候就要egcd登场了。正好题目脚本也给了egcd函数，egcd($r_1,r_2$)函数的三个返回值g，a，b中a，b满足$a * r_1 + b * r_2 = 1$。奇妙代数时刻。

$(k^{r_1})^a * (k^{r_2})^b = k^{(a*{r_1} + b*{r_2})} = k^1 = k$

妙啊，太妙啦！不过不知道wp说的msgpack库在哪，几个r都是从那里找的。可能给少东西了吧，所以没有脚本ᶘ ᵒᴥᵒᶅ

- ### Flag
  > BCTF{q0000000000b3333333333-ju57-w0n-pwn20wn!!!!!!!!!!!!}