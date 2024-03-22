# Crypto笔记

## RSA
- 得到d和c，p和q为相邻质数。例题：[[NCTF2019]babyRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BNCTF2019%5DbabyRSA.md)
- 光滑数分解+威尔逊定理使用。例题1：[smooth](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/smooth.md)，例题2:[[RoarCTF2019]babyRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BRoarCTF2019%5DbabyRSA.md)
- 共模攻击。适用于相同明文用同样的n却用不同的e加密时。注意两个不同的e需要互质。[例题1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Crypto/best_rsa.md)搭配使用Crypto库读取公钥，[例题2](https://blog.csdn.net/weixin_44017838/article/details/104886290)搭配解密结果是ascii的情况。

```python
from Crypto.Util.number import *
from gmpy2 import invert
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def decrypt(e1,e2,n,c1,c2):
    _,s1,s2=egcd(e1,e2)
    if s1<0:
        s1 = -s1
        c1 = invert(c1, n)
    elif s2<0:
        s2 = -s2
        c2 = invert(c2, n)
    m = pow(c1,s1,n)*pow(c2,s2,n) % n
    return long_to_bytes(m)
n=0
c1=0
c2=0
print(decrypt(1697,599,n,c1,c2).decode())
```

- lcm问题+e与phi不互质（gcd较小）。例题：[[NPUCTF2020]EzRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BNPUCTF2020%5DEzRSA.md)
- dp泄露。例题：[0rsa0](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/0rsa0.md)
- sagemath解二元方程组+e，d泄露后分解n。例题:[[MRCTF2020]Easy_RSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BMRCTF2020%5DEasy_RSA.md)
```py
P_n = 
P_F_n =
var("p q")
eq1=P_n==p*q
eq2=P_F_n==(p-1)*(q-1)
solve([eq1,eq2],p,q)
```
- rsa衍生算法：[Rabin](https://co5mos.github.io/2018/09/14/rsa-rabin/)。[原理](https://zhuanlan.zhihu.com/p/533927542)及脚本：

```python
import libnum

p = 49123
q = 10663
c = 162853095
n = p*q
c_p = pow(c,(p+1)//4,p)
c_q = pow(c,(q+1)//4,q)
a = libnum.invmod(p,q)
b = libnum.invmod(q,p)
x = (b*q*c_p+a*p*c_q)%n
y = (b*q*c_p-a*p*c_q)%n

print(bin(x%n))
print(bin((-x)%n))
print(bin(y%n))
print(bin((-y)%n))
```

rabin算法可以解出来4个明文，一般末尾会有类似校验码的东西，帮助分辨哪个是真正的明文。[来源](https://www.jianshu.com/p/00a35ebd36fb)。
- 当模数n过大， $m^e$ 次方没有n大时，就可以直接对c开e次方。例题:[[INSHack2017]rsa16m](https://blog.csdn.net/zippo1234/article/details/109268561)。
- e和phi不互素+中国剩余定理解决多组c和n问题。例题1:[Weird_E_Revenge](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/Weird_E_Revenge.md)。例题2:[[De1CTF2019]babyrsa](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BDe1CTF2019%5Dbabyrsa.md)。[simpleRSA](https://blog.csdn.net/weixin_52640415/article/details/127817186)
  - 如果给出两组n，c和e，且两组数据的phi和e gcd一致，解法与Weird_E_Revenge大致相同。
```python
from Crypto.Util.number import *
import gmpy2
from sympy.ntheory.modular import crt
e1 = 0
p1 = 0
q1 = 0
c1 = 0
n1 = p1 * q1
e2 = 0
p2 = 0
q2 = 0
c2 = 0
n2 = p2 * q2
p = p1
phi1 = (p - 1) * (q1 - 1)
phi2 = (p - 1) * (q2 - 1)
b = gmpy2.gcd(e1, phi1)
a1 = e1 // b
a2 = e2 // b
bd1 = gmpy2.invert(a1, phi1)
bd2 = gmpy2.invert(a2, phi2)
mb1 = pow(c1, bd1, n1)
mb2 = pow(c2, bd2, n2)
c3 = mb1 * mb2 % p
c2 = mb2 % q2
c1 = mb1 % q1
res = crt([q1, q2, p],[c1, c2, c3])[0]
n = q1 * q2
f = (q1 - 1) * (q2 - 1)
m = res % n
d2 = gmpy2.invert(7, f)
m = pow(m, d2, n)
msg = gmpy2.iroot(m, 2)[0]
print(long_to_bytes(msg).decode())
```
- e非常大，相应的d就会很小。低解密指数攻击（wiener attack）。例题:[[羊城杯 2020]RRRRRRRSA](../../CTF/BUUCTF/Crypto/[羊城杯%202020]RRRRRRRSA.md)
```python
import gmpy2
from Crypto.Util.number import long_to_bytes
def continuedFra(x, y):
    cF = []
    while y:
        cF += [x // y]
        x, y = y, x % y
    return cF
def Simplify(ctnf):
    numerator = 0
    denominator = 1
    for x in ctnf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return (numerator, denominator)
def calculateFrac(x, y):
    cF = continuedFra(x, y)
    cF = list(map(Simplify, (cF[0:i] for i in range(1, len(cF)))))
    return cF
def solve_pq(a, b, c):
    par = gmpy2.isqrt(b * b - 4 * a * c)
    return (-b + par) // (2 * a), (-b - par) // (2 * a)
def wienerAttack(e, n):
    for (d, k) in calculateFrac(e, n):
        if k == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        p, q = solve_pq(1, n - phi + 1, n)
        if p * q == n:
            return abs(int(p)), abs(int(q))
    print('[!]not found!')
e = 0
n = 0
c = 0
p, q = wienerAttack(e, n)
print('[+]Found!')
print('[-]p =', p)
print('[-]q =', q)
d = gmpy2.invert(e, (p-1)*(q-1))
flag = long_to_bytes(pow(c,d,n))
print (flag)
```
- 多项式下的RSA(PolynomialRing)。例题:[[watevrCTF 2019]Swedish RSA](../../CTF/BUUCTF/Crypto/[watevrCTF%202019]Swedish%20RSA.md)
- e与phi不互质且gcd很大，使用AMM开根法+CRT。例题:[[NCTF2019]easyRSA](https://blog.soreatu.com/posts/intended-solution-to-crypto-problems-in-nctf-2019/#easyrsa909pt-2solvers)。附AMM算法（sagemath）：

```python
import time
import random
def AMM(o, r, q):
    start = time.time()
    print('\n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q-1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r**(t-1) * s)
    b = o ^ (r*alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r^(t-1-i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c^r)^j
        h = h * c^j
        c = c^r
    result = o^alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result
```

- p和q相邻或接近，使用费马分解法。

```python
import gmpy2
def Fermat(num):
    x = gmpy2.iroot(num,2)[0]
    if x*x < num:
        x += 1
    while(True):
        y2 = x*x - num
        y = gmpy2.iroot(y2,2)[0]
        if y*y == y2:
            break
        x += 1
    return [x+y, x-y]
```

- 低加密指数（e为3等较小数）攻击。

```python
from Crypto.Util.number import *
from gmpy2 import iroot
def smallEattack(c, e, n):
    for i in range(10 ** 10):
        res = iroot(n * i + c, e)
        if res[1]:
            print(long_to_bytes(res[0]))
            break
```

- Franklin-Reiter相关信息攻击巧解给出d，phi密文，m非常大，e很小的题目。例题:[d-phi-enc](../../CTF/HackTM%20CTF/Crypto/d-phi-enc.md)
- 获得d和n后可用Cryptodome库获取p和q。

```python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from pwn import xor
n = 0
e = 65537
d = 0
ciphertext =
p = RSA.construct((n, e, d)).p
q = n//p
key = xor(long_to_bytes(p), long_to_bytes(q)) #pwn的xor函数无需两个字符串相同长度
plaintext = xor(bytes.fromhex(ciphertext), key).decode()
print(plaintext)
```

- 根据d和e构造出n:[Calculating RSA Public Modulus from Private Exponent and Public Exponent](https://crypto.stackexchange.com/questions/81615/calculating-rsa-public-modulus-from-private-exponent-and-public-exponent)。更详细的方法：https://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the
- [已知d分解n](https://crypto.stackexchange.com/questions/6361/is-sharing-the-modulus-for-multiple-rsa-key-pairs-secure)。
```python
import random
import math
from Crypto.Util.number import long_to_bytes
c = 0
n = 0
d = 0
e = 0x10001
def remove_even(n):
    if n == 0:
        return (0, 0)
    r = n
    t = 0
    while (r & 1) == 0:
        t = t + 1
        r = r >> 1
    return (r, t)
def get_root_one(x, k, N):
    (r, t) = remove_even(k)
    oldi = None
    i = pow(x, r, N)
    while i != 1:
        oldi = i
        i = (i*i) % N
    if oldi == N-1:
        return None 
    return oldi
def factor_rsa(e, d, N):
    k = e*d - 1
    y = None
    while not y:
        x = random.randrange(2, N)
        y = get_root_one(x, k, N)
    p = math.gcd(y-1, N)
    q = N // p
    return (p, q)
p, q = factor_rsa(e, d, n)
print(p, q)
assert p * q == n
m = pow(c, d, n)
flag = p - m
print(long_to_bytes(flag))
```
已知phi分解n也是这个考点。本身已知e和d分解n就是为了凑phi的倍数，现在如果有phi直接分解即可。[factorize_me!](../../CTF/moectf/2023/Crypto/factorize_me!.md)。更好的脚本（给定n和phi直接返回n的全部因子，无论n是多少个质数的乘积）： https://github.com/XDSEC/MoeCTF_2023/blob/main/WriteUps/Orac1e/Crypto_Writeup.md#factorize_me

- p高位泄露（coppersmith），可直接根据泄露的高位p，n和e求出p。需使用sagemath运行。

```python
n = 0
p4=0 #泄露的高位
e = 0x10001
pbits = 1024 #完整p的位数
kbits = 128 #要爆破（求解）的位数（不是已泄露的位数，为pbits-已泄露位数）
PR.<x> = PolynomialRing(Zmod(n))
f = x + p4
roots = f.small_roots(X=2^kbits, beta=0.4)
if roots:        
    p = p4+int(roots[0])
    print ("n=", n)   
    print ("p=", p)
    print ("q=", n/p)
```

coppersmith算法的作用是求解根较小的同余式方程。已知p高位攻击其实是求这么一个方程的根： $p_{high}+x=0\mod p$ 。特殊地，如果大小得当，可以在不知道模只知道模的倍数前提下，求解方程。即解 $p_{high}+x=0\mod n$ 。
- coppersmith(m高位泄露,已知明文高位)。假设加密了消息 m，如下：

$C\equiv m^e\mod N$

并且我们假设我们知道消息 m的很大的一部分 m0，即 m=m0+x，但是我们不知道 x。那么我们就有可能通过coppersmith恢复消息。这里我们不知道的 x其实就是多项式的根，需要满足 Coppersmith 的约束。当 e足够小，且部分明文泄露时，可以采用Coppersmith单变量模等式的攻击，如下：

$c=m^e\mod n=(mbar+x_0)^e\mod n$

其中 mbar=(m>>kbits)<<kbits
```python
def phase2(high_m, n, c):
    R.<x> = PolynomialRing(Zmod(n), implementation='NTL')
    m = high_m + x
    M = m((m^3 - c).small_roots()[0])
    print(hex(int(M))[2:])

n = 
c = 
high_m = 

phase2(high_m, n, c)
```
```py
c = 
n = 
e = 
K.<x> = PolynomialRing(Zmod(n))
secret_len =  #原m的长度,有时候需要猜测
known_high = #已知的m高位
polynomial = (x + 2^(secret_len)*(known_high))^e - c
polynomial = polynomial.monic()
roots = polynomial.small_roots(X=2^secret_len)
print(roots)
```
有时候可以尝试用`\x00`尝试提高已知明文，然后用small_roots开根。[Small Inscription](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#small-inscription)。这题的e是3，flag长度小于30。方程确实是我理解的那个方程，就是补`\x00`才能解出来可能是因为这样small_root要求的根相对比较小，而且不会影响出来的结果。
```py
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
ct=
N=
R.<x> = PolynomialRing(Zmod(N))
prefix=b'' #已知的明文部分
for i in range(30):
    m1 = bytes_to_long(prefix+b'\x00'*i)
    poly= (m1+x)**3 - ct
    root=poly.small_roots()
    if root:
        print(long_to_bytes(m1+int(root[0])))
```
- coppersmith's short-pad attack& Related Message Attack(Franklin-Reiter，相关信息攻击)
```python
import binascii
def attack(c1, c2 e):
    PR.<x>=PolynomialRing(Zmod(n))
    a=
    b=
    c=
    d=
    g1 = (a*x+b)^e - c1
    g2 = (c*x+d)^e - c2

    def gcd(g1, g2):
        while g2:
            g1, g2 = g2, g1 % g2
        return g1.monic()
    return -gcd(g1, g2)[0]
c1 =
c2 =
e =
m1 = attack(c1, c2 e)
print(binascii.unhexlify("%x" % int(m1)))
```
相关信息攻击的关键点在于找出两条信息具有线性关系的方程。通常方程形如 $((a\*m)+b)^e\mod n$ 和 $((c\*m)+d)^e\mod n$ ，也是脚本中需要自己填写的a，b，c和d值的由来。[unusualrsa2](https://4xwi11.github.io/posts/80806ae5/#unusualrsa2)
- 给出p+q（(p-2)(q-2)一个作用）和n时，构造多项式即可获取p或q。

$f(x)=(x-p)(x-q)$<br>
$f(x)=x^2-(p+q)x+pq$<br>
$f(x)=x^2-(p+q)x+n$<Br>
$p,q=\frac{s\pm\sqrt{s^2-4n}}{2}$

```python
from gmpy2 import isqrt
from Crypto.Util.number import long_to_bytes
n=0
s = 0 #s为p+q
c=0
discrim = s**2 - 4*n
assert isqrt(discrim)
test = int(isqrt(discrim))
test_p = (s + test) // 2
if n % test_p != 0:
    test_p = (s - test) // 2
p = test_p
q = n // p
assert p * q == n
e = 0x10001
l = (p-1)*(q-1)
d = pow(e, -1, l)
m = pow(c, d, n)
print(long_to_bytes(m))
```
- rsa要求明文不能大于n。如果明文大于n了，解密的结果是m-k\*n。此时要么按照正常方式求出m后不断加上n的倍数尝试爆破，要么尝试获取多组密文解密后用crt还原完整明文。例题:[Search-3](https://hackmd.io/9_WE-HinSYqFQyKubluRuw?view#Search-3---470---Hard)
  - 爆破做法也是有技巧的，参考[rsa-is-broken](https://github.com/BCACTF/bcactf-4.0/tree/main/rsa-is-broken).大部分flag的结尾均为`}`,那么flag模256一定为125(`ord('}')`)。那么可以从模256=125的m出发开始爆破，每次加上n*256而不是1。至于为什么是256，个人猜测是因为0-255代表了所有可能的字符。同一道题还有以下脚本:
  ```py
    from Crypto.Util.number import *
    import math

    # Given
    p = 892582974910679288224965877067
    q = 809674535888980601722190167357
    n = p * q
    e = 65537
    d = pow(e, -1, math.lcm(p-1, q-1))
    c = 36750775360709769054416477187492778112181529855266342655304
    newm = pow(c, d, n)

    flag_len = 35   # Figured out experimentally lol

    minimum_byte_string = b'bcactf{' + b',' * (flag_len - 6)

    multiple = bytes_to_long(minimum_byte_string) // n              # Minimum multiple of N added to get `bcactf{`
    while (newm + n * multiple) & 0xFF != ord("}"): multiple += 1      # Increment until it will end with `}`

    start = multiple    # Minimum multiple of N starting with `bcactf{` and ending with `}`
    end = 2 ** 100      # Really big number that doesn't matter
    step = 256          # 256 is coprime to N, so v + i * N (mod 256) has a period of 256


    for i in range(start, end, 256):
        # Test byte string
        byte_str = long_to_bytes(newm + n * i)

        # Stop once we're past the `bcactf{` part
        if not byte_str.startswith(b'bcactf{'):
            break

        # If the whole byte string is in-flag-range ASCII, print and exit
        if all(0x2C < byte < 0x7f for byte in byte_str):
            print(byte_str)
            break
    ```   
- 基于多项式的RSA。在有限域上选取两个不可约多项式 g(p),g(q)，g(n)=g(p)⋅g(q)。计算出 g(n)的欧拉函数 φ(g(n))=φ。再选取一个整数 e作为公钥，e与 φ是互素的，那么对于明文 g(m)，加密过程为 $g(m)^e$ ≡g(c)(mod g(n))。解密则计算私钥 d满足 ed≡1(mod φ)，则 $g(c)^d$ ≡ $(g(m)^e)^d$ ≡ $g(m)^{ed}$ ≡ $g(m)^{φ+1}$ (mod g(n))。同样考虑 g(n)与 g(m)互素，欧拉定理对于多项式亦成立。得到 $g(m)^{φ+1}$ ≡g(m)(mod g(n))，所以 $g(c)^d$ ≡g(m)(mod g(n))。即整数上的rsa可以推广到多项式上。对于不可约多项式 g(x)，φ(g(x))= $p^n−1$ 。p为 GF(p)的模，n为该多项式最高项次数。[unusualrsa3](https://lazzzaro.github.io/2020/09/01/other-CTFshow%E4%BE%9B%E9%A2%98-unusualrsa%E7%B3%BB%E5%88%97/index.html#unusualrsa3)
```python
#sage
p = 
R.<x> = PolynomialRing(GF(p))
N = 
S.<x> = R.quotient(N)
c = 
P, Q = N.factor() #尝试直接分解出p和q
P, Q = P[0], Q[0]
phi = (p**P.degree()-1)*(p**Q.degree()-1)
e = 0x10001
d = inverse_mod(e, phi)
m = c^d
m = "".join([chr(c) for c in m.list()])
print(m)
```
补充一篇多项式RSA的[论文](https://www.whdl.org/sites/default/files/resource/academic/Freed-RSA%2520Encryption%2520Using%2520Polynomial%2520Rings-HP.pdf) 
- 程序允许输入任意数字（除了程序使用的e），跟phi计算模逆后返回。此时有下面几种方法恢复明文：
  - 输入程序使用的e的负数：-e。程序返回的结果直接就是-d，加个符号转为d就能直接解密
  - 发送-1，这样程序返回的就是phi-1。加上1得到真正的phi即可解密
  - 使用公式:`phi = (e * d - 1) // gcd(e - 1, d - 1)`
  - 向程序发送多个e，获取多个d。让 $x_i=d_i\*e_i$ ,那么对于每个 $x_i$ ,有某个k满足 $x_i\equiv 1\mod phi\Leftrightarrow x-1\equiv phi\*k$ 。于是取所有 $x_i-1$ 的gcd可能得到phi。注意不是每一次都一定成功。
  - 另外提一点，似乎利用phi的倍数求出的d不会影响解密。
- 低加密指数广播攻击（[Hastad's broadcast attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#H%C3%A5stad's_broadcast_attack)）使用相同的e加密相同的m至少e次，即可用CRT还原 $m^e$ 。攻击者可以通过开e次方获取m。这种攻击方式下的e很小，例如3.
```py
from sympy.ntheory.modular import crt
from gmpy2 import iroot
e=3
n1=
n2=
n3=
c1=
c2=
c3=
flag_cubed=crt([n1,n2,n3],[c1,c2,c3])[0]
flag=iroot(flag_cubed,3)
print(bytes.fromhex(hex(flag[0])[2:]))
```
- [unusualrsa4](https://lazzzaro.github.io/2020/09/01/other-CTFshow%E4%BE%9B%E9%A2%98-unusualrsa%E7%B3%BB%E5%88%97/index.html#unusualrsa4).已知q对p的模逆元(`inverse(q,p)`)，d，c和e，求m。
```py
from Crypto.Util.number import *
inv=
d=
c=
e=65537
for i in range(1,e):
    kphi=e*d-1
    if kphi%i==0:
        phi=kphi//i
        x=1+inv*phi-inv
        mod1=pow(3,phi,x)-1
        mod2=pow(5,phi,x)-1
        p=GCD(mod1,mod2)
        if p.bit_length()==1024:
            q=inverse(inv,p)
            print(long_to_bytes(pow(c,d,p*q)))
            break
```
- [superstitious](https://github.com/BCACTF/bcactf-4.0/tree/main/superstitious):分解特殊的n。若 $n=pq=(a^m+r_p)(b^m+r_q)$ ，则有更快速的方式分解n。参考论文： https://einspem.upm.edu.my/journal/fullpaper/vol13saugust/8.pdf ，具体实现方式在第7页。
- [Boneh-Durfee Attack](https://cryptohack.gitbook.io/cryptobook/untitled/low-private-component-attacks/boneh-durfee-attack):当d < $N^{0.292}$ 时，可利用该攻击方法恢复d
- [Sus](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Sus):分解n=p\*q\*r,其中 $q=p^2+p+1$
- [Wasteful](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Wasteful):给出`sz=2048;e_fast = getPrime(sz // 2);e_slow = e_fast + getPrime(sz // 3) * phi`,和2048位的公钥n，利用coppersmith获取p
- [S_H](https://sovietbeast-writeups.gitbook.io/writeups/ctfs/fetch-the-flag-2023/cryptography/s_h)
    - 尝试恢复部分被遮挡的SSH RSA private key。主要是要了解rsa private key的格式，确认没被遮挡的部分属于密钥的哪一部分。比如这题没被遮挡的部分为部分dq，完整dp和完整q。所以这题其实是“利用dp和e恢复p”
- [Missing Bits](https://meashiri.github.io/ctf-writeups/posts/202311-glacierctf/#missing-bits)
    - ASN.1 DER格式私钥分析： https://www.cem.me/20141221-cert-binaries.html
- [ARISAI](https://github.com/4n86rakam1/writeup/tree/main/GlacierCTF_2023/intro/ARISAI)
    - 多素数rsa+利用crt加快解密过程
- [Mayday Mayday](https://hackmd.io/@Giapppp/rJrKDLm8a),[官方wp](https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/crypto/%5BMedium%5D%20Mayday%20Mayday)
    - dp和dq均泄露一部分后（MSB）分解n。LSB的题型见[grhkm's babyrsa](https://gist.github.com/maple3142/96b790553050b6bed5571694c2e764c0)
- [N-less RSA](https://github.com/rixinsc/ctf-writeups/blob/master/wgmy2023.md#n-less-rsa)
    - 已知phi，e和c，获取m
- [easy-rsa](https://github.com/C0d3-Bre4k3rs/PingCTF2023-writeups/tree/main/easy-rsa)
    - 获知`q&p`和`q&(p<<1)`后分解n。或者说，在得知p和q的随机个bit后尝试恢复p和q：[Random known bits of p and q](https://eprint.iacr.org/2020/1506.pdf#page=23)。这题Z3可解
    - 又遇到了类似考点的题：[Shibs](https://kanzya.github.io/posts/MAPNACTF/)。这题wp作者用了多线程（python multiprocessing）配合z3。个人做这道题时倒是用了easy-rsa里的方法: https://gist.github.com/C0nstellati0n/cf6ae2c5e0e9fe1ecb532d257a56e101#shibs 。我发现这种类型的题只需要找到题目里p和q的bit之间的关系,结合backtrack的思想即可解出。p和q之间的关系用于backtrack设置bit及检查是否返回的条件。注意backtrack设置完bit并递归完后一定要取消刚才设置的bit
- [L4ugh](https://berliangabriel.github.io/post/0xl4ugh-ctf-2024/)
    - 利用LLL实现[Common Private Exponent](https://www.ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf)攻击。特征为多组公钥共享一个私钥。这种攻击比较简短的解释： https://connor-mccartney.github.io/cryptography/rsa/L4ugh-0xl4ughCTF-2024
    - AES翻转bit攻击（控制iv）
- [Baby RSA](https://writeup.gldanoob.dev/bitsctf/)
    - 矩阵上的RSA。参考 https://www.gcsu.edu/sites/files/page-assets/node-808/attachments/pangia.pdf 第9页的3.3案例
## Sagemath

感觉了解sagemath的api很重要啊，那今天就专门开个部分用于记录例题和使用的函数。

- https://github.com/Neobeo/CrewCTF2023/blob/main/crypto_writeups.ipynb
    - 实数域上的rsa。这里的p，q等数可能是分数
    - [factor_trial_division(m, limit='LONG_MAX')](https://doc.sagemath.org/html/en/reference/rings_standard/sage/rings/factorint.html#sage.rings.factorint.factor_trial_division):拿所有小于等于limit的质数尝试去除m，并给出不完整的分解结果
    - [nearby_rational(max_error=None, max_denominator=None)](https://doc.sagemath.org/html/en/reference/rings_numerical/sage/rings/real_mpfr.html#sage.rings.real_mpfr.RealNumber.nearby_rational)：必须指定max_error和max_denominator中的一个。若指定max_error，则返回[self-max_error .. self+max_error]最简的分数。若指定max_denominator，则返回最接近self的分数且分母不超过max_denominator
        - 此题 $n=\frac{p}{q}$ ,所以还可以利用连分数得到p和q：`continued_fraction(n).convergents()`。似乎效果类似nearby_rational？
- https://mitsu1119.github.io/blog/p/zer0pts-ctf-2023-writeup-english/#crypto-102pts-easy_factoring-95-solves
    - 当 $N=p^2+q^2$ 时，可以借助[高斯整数](https://zh.wikipedia.org/zh-cn/%E9%AB%98%E6%96%AF%E6%95%B4%E6%95%B8)分解N。 $N=p^2+q^2=(p+qi)(p-qi)$ ，说明满足这一条件的整数p和q存在于N的高斯整数分解中（以p+qi的形式）。不过使用sagemath的factor会将其分解为高斯素数，所以尝试分解出来的高斯素数的所有combinations即可恢复p和q
    - 还可以用sympy的diop_quadratic方法： https://connor-mccartney.github.io/cryptography/other/easy-factoring-zer0pts-CTF-2023
    - `ZZ[I](N)`表示将整数N转为高斯整数.ZZ[I]为高斯整数环
    - 也可以使用[divisors](https://doc.sagemath.org/html/en/constructions/number_theory.html#divisors)，直接给出所有因子。这种方法恢复p和q就不用爆破组合了，p和q就在里面，直接遍历因子列表然后isPrime判断即可
    - sagemath自带的[two_squares](https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.two_squares)确实可以很快把N写成两个平方的和，但是好像不一定是素数
- [Non-Quadratic Residues](https://github.com/rwandi-ctf/ctf-writeups/blob/main/amateursctf2023/non-quadratic%20residues.md)
    - 有这样一个式子： $c\equiv x^a\mod b$ ,其中a，b（质数）和c均已知。若a较小（如此题a=210），那么可以尝试用sagemath的[nth_root](https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod.html#sage.rings.finite_rings.integer_mod.IntegerMod_abstract.nth_root)开出x。
        ```py
        #感觉使用情况和效果都和上面提过的amm差不多
        GF(b)(c).nth_root(a,all=True)
        ```
- [Tan](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Tan)
    - $tan(m).n(1024)=t,arctan(t)+k\pi\approx m$ ,接下来可以用LLL尝试恢复准确的m。或者参考 https://math.stackexchange.com/questions/2160925/find-an-integer-a-such-that-a-sqrt2-has-a-given-decimal-part/2161019#2161019
        - [n](https://doc.sagemath.org/html/en/reference/misc/sage/misc/functional.html)
        - [LLL](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.LLL)
- [Noisier CRC](https://imp.ress.me/blog/2023-08-28/sekaictf-2023#noisier-crc)
    - [irreducible_element](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_ring.html#sage.rings.polynomial.polynomial_ring.PolynomialRing_dense_finite_field.irreducible_element):获取环上指定degree的不可约元素
    - [right_kernel](https://doc.sagemath.org/html/en/prep/Quickstarts/Linear-Algebra.html)
    - [basis](https://doc.sagemath.org/html/en/constructions/linear_algebra.html)
- [sqrt](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/crp/sqrt):计算Permutations(256)中某个元素的平方根。注意一个元素的平方根可能有很多个
    - [to_cycles](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/permutation.html#sage.combinat.permutation.Permutation.to_cycles)
    - [sage.combinat.permutation.from_cycles](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/permutation.html#sage.combinat.permutation.from_cycles)
- [Zombie Rolled](https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/crypto/%5BHard%5D%20Zombie%20Rolled)。这题啥都有，包含RSA，ECC还有lattice。暂记一些能看出来的知识点
    - 利用椭圆曲线上的rational point求解丢番图方程。参考 https://www.quora.com/How-do-you-find-the-positive-integer-solutions-to-frac-x-y+z-+-frac-y-z+x-+-frac-z-x+y-4
    - 利用Groebner basis求解方程组
- [GLNQ](https://kanzya.github.io/posts/MAPNACTF/#glnq-crypto-13-solve)
    - 计算矩阵上的离散对数。若矩阵的阶为光滑数，就可以用pohlig-hellman配合sagemath解出

## Lattice(格)

是的我需要一个格题分类。虽然我根本就不懂什么是格

- 攻击与格有关的密码的工具： https://github.com/josephsurin/lattice-based-cryptanalysis
- [LCG to the power of n!](https://github.com/SuperBeetleGamer/Crypto-Writeups/blob/main/LITCTF%202023/lcg%20to%20the%20power%20of%20n!.md)
    - 格（lattice）中的Closest Vector Problem（CVP）
    - [IntegerLattice](https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.IntegerLattice)
    - Babai_closest_vector算法实现
- [Geometry Hash](https://connor-mccartney.github.io/cryptography/other/Geometry-Hash-Balsn-CTF-2023)。这题的格构造与三角形的Centroid，Circumcenter和Incenter有关
- [Hohoho 2 Continue](https://mechfrog88.github.io/wargames-2023#hohoho-2-continue)
    - LCG。这题要求预测一个LCG的值，LCG的各个参数都知道，但要预测的项未知（不知道要预测第几个输出）。初始的x可以随意输入，但必须包含一个固定短语。做的时候傻了，后来发现可以找一个包含短语的x，并让其满足 $x=(ax+b)\mod n$ 即可。找的时候使用LLL（从wp里似乎摸到一点格的门道了，但是先不记，还有地方不懂，不想误导未来的自己）。类似的题目（也用了格，还有不错的介绍）：[Onelinecrypto](https://nush.app/blog/2023/06/21/see-tf-2023/)
- [any% ssg](https://hackmd.io/@lamchcl/SJIdwQb3a#cryptoany-ssg)
    - 利用LLL爆破类似minecraft的生成地图seed。参考官方[wp](https://github.com/AVDestroyer/CTF-Writeups/tree/main/lactf2024/any-percent-ssg)和wp里提到的视频[系列](https://www.youtube.com/playlist?list=PLke4P_1UHlmB8sB1oGdcea4SeBH0yZy5B) （另外这也是个不错的格入门视频），这题的知识点更准确地说，应该是“找到LCG的初始seed，使接下来的12个连续输出满足 $min\leq seed_i\leq max$ 的不等式“
    - 其他脚本： https://gist.github.com/TheBlupper/0b3cb0b7402c46e3d374a7244bd9e5cd

## Elliptic Curves(ECC,椭圆曲线)

是的我需要一个椭圆曲线题分类。我对这玩意的了解比格还少，只是记录下来方便未来的我复习(相信后人的智慧)
- [Isogenies](https://hackmd.io/_D7hNf_wQ7qq0PArYPWjSQ)
    - 3-torsion point
    - isogeny
    - montgomery coefficients
    - j-invariants
    - [Modular polynomials](https://math.mit.edu/~drew/ClassicalModPolys.html)
    - [Division polynomials](https://en.wikipedia.org/wiki/Division_polynomials)
    - [Resultant](https://en.wikipedia.org/wiki/Resultant)
- [yaonet](https://7rocky.github.io/en/ctf/other/dicectf/yaonet/)
    - OpenSSH格式ECDSA私钥恢复。给出损坏的私钥文件，文件内部包含缺少5个字节（3个前缀字节2个尾字节）私钥d，尝试恢复d并构造原本的私钥文件。利用Baby-step Giant-step算法及Meet-in-the-middle思想。难点在于当缺失的字节不连续时如何构造公式并从两端入手
    - 其他wp： https://connor-mccartney.github.io/cryptography/ecc/yaonet-DiceCTF-2024
- [not-suspicious-agency](https://www.youtube.com/watch?v=8Cbz1e3motE)
    - [Dual_EC_DRBG](https://en.wikipedia.org/wiki/Dual_EC_DRBG)（基于椭圆曲线的随机数生成器,有时候题目名称/描述会和NSA有关系）的[后门利用](https://crypto.stackexchange.com/questions/10417/explaining-weakness-of-dual-ec-drbg-to-wider-audience)。类似题目： https://github.com/cscosu/ctf-writeups/tree/master/2021/utctf/Sleeves
    - 如何在椭圆曲线下求乘法逆元：`inverse(a,E.order())`
- [budget bag](https://connor-mccartney.github.io/cryptography/ecc/budget-bag-LACTF-2024)
    - 通过曲线上的两个点恢复参数a和b
    - 带有elliptic cusp（a和b均为0）的椭圆曲线上的离散对数比较好求，参考 https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp
    - 利用离散对数将曲线上点的加法转换为线性方程（wp里说是背包问题，我菜到看不出来）。假设有一些已知的点，各个点的系数未知，整体加起来为曲线上的另一个点S。可以取已知的点中任意一个点作“生成点G”，那么剩下的点一定是G的倍数（具体多少倍求离散对数可得）。求G对于S的离散对数（不确定这样表达有没有问题，求S是G的多少倍），那么之前求的G相对于已知点集里各个点的离散对数结果与G对S的离散对数构成模曲线质数p的方程（各个离散对数结果记为 $d_i$ ,G对S的离散对数记为D那么 $d_ix+d_{i+1}y+...=D\mod p$ 。解这种模某个数的线性方程的脚本参考wp）
## Z3使用

开一个新的合集，用于记录那些和z3有关的crypto题目。但是优先级较低，记录在这里的题不能包含上面的RSA，格等内容（除非两者都有）

- [rps-casino](https://7rocky.github.io/en/ctf/other/dicectf/rps-casino/)
    - LFSR的另类实现（选取异或的bit时使用位移，一次更新4轮，输出4个bit）,以及其对应的z3实现
    - 模运算通常会破坏线性。例如本题输出的4bit的数字会模3，导致只能用z3强行解初始state
    - 其他wp： https://github.com/quasar098/ctf-writeups/tree/main/dicectf-2024/rps-casino 。bitvec不知为何无法使用，便用bool类型代替

## 其他

1. Crypto库根据已有信息构建私钥并解密

如果给出的是flag.enc和public.key这种形式的题目，平时的方法可能会解出乱码，需要利用私钥文件来解密。
```python
from Crypto.PublicKey import RSA
import gmpy2
import base64
from Crypto.Util.number import *
from Crypto.Cipher import PKCS1_OAEP
p=0
q=0
n=p*q
e=65537
phi=(p-1)*(q-1)
d=gmpy2.invert(e,phi)
with open("flag.enc",'rb') as f:
    c_bytes=f.read()
rsa_components=(n,e,int(d),p,q)
arsa=RSA.construct(rsa_components)
rsakey=RSA.importKey(arsa.exportKey())
rsakey=PKCS1_OAEP.new(rsakey)
decrypted=rsakey.decrypt(c_bytes)
print(decrypted)
```

3. python Crypto库读取公钥
```python
from Crypto.PublicKey import RSA
key1=RSA.importKey(open('public1.pub').read())
print(f"n={key1.n}\ne={key1.e}")
```
4. 离散对数问题（Discrete Logarithm ProblemDLP）。一般的对数 $a^b=c$ ，求得b可以直接用 $log_a(c)$ 。但是在加上模运算的情况下就要使用离散对数了。 $a^b=c\mod d$ ，使用sympy的离散对数函数。

```python
m = 0
c = 0
n=0
from Crypto.Util.number import *
import sympy
x=sympy.discrete_log(n,c,m)  #参数顺序：sympy.discrete_log(模数，结果，底数)
print(long_to_bytes(x))
```
也可用[网站](https://www.alpertron.com.ar/DILOG.HTM)计算. https://github.com/hollowcrust/TJCTF-2023/blob/main/crypto.md#2-ezdlp

或者sagemath脚本。
```py
#g^x = s mod p, find x
g =
s =
p =
Fp = IntegerModRing(p) 
g_modp = Fp(g) 
s_modp = Fp(s)
x = discrete_log(s_modp, g_modp)
print(x)
```

5. 海明码（汉明码）问题。例题：[H■m■i■g](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Misc/H%E2%96%A0m%E2%96%A0i%E2%96%A0g.md)。今天又遇见一道题：[鸡藕椒盐味](https://buuoj.cn/challenges#%E9%B8%A1%E8%97%95%E6%A4%92%E7%9B%90%E5%91%B3)，也是海明码，没想到直接用当时写的脚本就能出答案。
```python
import hashlib
def hamming_correct(bitblock):
    result=''
    for t in range(4):
        bits=[bit for i,bit in enumerate(bitblock) if i&(1<<t)]
        if bits.count(1)%2==0:
            result+='0'
        else:
            result+='1'
    return int(result[::-1],2)
code=[1,1,0,0,1,0,1,0,0,0,0,0]
wrong_pos=hamming_correct(code)
code[wrong_pos]=int(not code[wrong_pos])
c=''.join([str(i) for i in code])
md=hashlib.md5()
md.update(c.encode("utf8"))
flag = md.hexdigest()
print(flag)                   
```
以及其他人的脚本：[PARtly bintastic](https://github.com/Cryptonite-MIT/niteCTF-2023/tree/main/crypto/partly_bintastic)
6. rsa题目时要看清楚密文即证书的格式。有些题密文和n等信息会以文件的形式给出，有可能是bytes形式，可以直接long_to_bytes，但也有可能是base64编码后的形式。解密前注意这些细节，能省去很多怀疑人生的时间。
7. polybius方阵密码爆破。常见的方阵密码用数字1，2，3，4，5表示，不过任何5个元素都能表示polybius密文，比如aeiou。这里有个思维惯性，可能会下意识认为方阵排列形式就是aeiou，但可能并不是这样，aioue也不是不行。不同的排列组合会影响解密的结果。故需要爆破，利用下面的脚本：

```python
import itertools
s="aeoiu"
ciper="ouauuuoooeeaaiaeauieuooeeiea"
sumresult=[]
numsumresult=[]
for i in itertools.permutations(s,5):#找出所有全排列
    sumresult.append("".join(i))
for i in sumresult:
    temp=""
    for j in ciper:
        temp+=str(i.index(j)+1)
    numsumresult.append(temp)
for i in numsumresult:
    flag=""
    for j in range(0, len(i),2):
        xx=(int(i[j])-1)*5+int(i[j+1])+96
        if xx>ord('i'):
            xx+=1
        flag+=chr(xx)
    print(flag)
```

来源:[[BJDCTF2020]Polybius](https://blog.csdn.net/m0_52727862/article/details/119043003)

8. 猪圈密码+动物密码。例题:[[NPUCTF2020]Classical Cipher](https://blog.csdn.net/m0_52727862/article/details/119043219)
9. [四方密码](https://zh.wikipedia.org/zh-my/%E5%9B%9B%E6%96%B9%E5%AF%86%E7%A2%BC)，可用[网站](http://www.metools.info/code/four-square244.html)进行解密。例题:[四面八方](https://blog.csdn.net/LingDIHong/article/details/112684896)
10. 伪代码题。题目会给出伪代码文件，要求写出其任意代码实现。如：

```
get buf unsign s[256]
get buf t[256]
we have key:whoami
we have flag:????????????????????????????????

for i:0 to 256
    set s[i]:i

for i:0 to 256
    set t[i]:key[(i)mod(key.lenth)]

for i:0 to 256
    set j:(j+s[i]+t[i])mod(256) //前面从来没有出现过j，没出现过的实现时默认设为0
        swap:s[i],s[j]
//下面这段开始执行前要把i和j都归0，python里面for循环影响计数变量后会影响外面的
for m:0 to 38
    set i:(i + 1)mod(256)
    set j:(j + S[i])mod(256)
    swap:s[i],s[j]
    set x:(s[i] + (s[j]mod(256))mod(256))
    set flag[m]:flag[m]^s[x]

fprint flagx to file
```

这种题一般来说不难，重点是要注意把变量清0。此题脚本：

```python
s=[]
t=[]
key="whoami"
with open('file.txt','rb') as f:
    cipher=f.read()
for i in range(256):
    s.append(i)
for i in range(256):
    t.append(ord(key[i%len(key)]))
j=0
for i in range(256):
    j=(j+s[i]+t[i])%256
    s[i],s[j]=s[j],s[i]
i=j=0
for m in range(38):
    i=(i+1)%256
    j=(j+s[i])%256
    s[i],s[j]=s[j],s[i]
    x=(s[i]+(s[j]%256))%256
    print(chr(cipher[m]^s[x]),end='')
```

11. python解密aes。题目:[[ACTF新生赛2020]crypto-aes](https://buuoj.cn/challenges#[ACTF%E6%96%B0%E7%94%9F%E8%B5%9B2020]crypto-aes)

```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
enc_flag=b'\x8c-\xcd\xde\xa7\xe9\x7f.b\x8aKs\xf1\xba\xc75\xc4d\x13\x07\xac\xa4&\xd6\x91\xfe\xf3\x14\x10|\xf8p'
output=91144196586662942563895769614300232343026691029427747065707381728622849079757
key=long_to_bytes(output)[:16]*2
iv=long_to_bytes(bytes_to_long(long_to_bytes(output)[16:])^bytes_to_long(key[16:]))
aes = AES.new(key,AES.MODE_CBC,iv)
flag = aes.decrypt(enc_flag)
print(flag)
```

12. Many Time pad攻击（利用空格异或其他字符会转大小写的特性）。例题:[不止一次](../../CTF/moectf/2022/Crypto/不止一次.md)
13. 希尔密码（hill）。例题:[[UTCTF2020]hill](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BUTCTF2020%5Dhill.md)
14. 秘密共享（Secret sharing）的Asmuth-Bloom方案。例题:[[AFCTF2018]花开藏宝地](../../CTF/BUUCTF/Crypto/[AFCTF2018]花开藏宝地.md)
15. ecc（椭圆曲线加密算法）入门。[链接](https://www.pediy.com/kssd/pediy06/pediy6014.htm)。
16. 伏羲六十四卦解密脚本。

[来源及题目](https://blog.csdn.net/weixin_44110537/article/details/107494966)

```python
s='升随临损巽睽颐萃小过讼艮颐小过震蛊屯未济中孚艮困恒晋升损蛊萃蛊未济巽解艮贲未济观豫损蛊晋噬嗑晋旅解大畜困未济随蒙升解睽未济井困未济旅萃未济震蒙未济师涣归妹大有'
dic={'坤': '000000', '剥': '000001', '比': '000010', '观': '000011', '豫': '000100', '晋': '000101', '萃': '000110', '否': '000111', '谦': '001000', '艮': '001001', '蹇': '001010', '渐': '001011', '小过': '001100', '旅': '001101', '咸': '001110', '遁': '001111', '师': '010000', '蒙': '010001', '坎': '010010', '涣': '010011', '解': '010100', '未济': '010101', '困': '010110', '讼': '010111', '升': '011000', '蛊': '011001', '井': '011010', '巽': '011011', '恒': '011100', '鼎': '011101', '大过': '011110', '姤': '011111', '复': '100000', '颐': '100001', '屯': '100010', '益': '100011', '震': '100100', '噬嗑': '100101', '随': '100110', '无妄': '100111', '明夷': '101000', '贲': '101001', '既济': '101010', '家人': '101011', '丰': '101100', '离': '101101', '革': '101110', '同人': '101111', '临': '110000', '损': '110001', '节': '110010', '中孚': '110011', '归妹': '110100', '睽': '110101', '兑': '110110', '履': '110111', '泰': '111000', '大畜': '111001', '需': '111010', '小畜': '111011', '大壮': '111100', '大有': '111101', '夬': '111110', '乾': '111111'}
li=[]
k=0
for i in range(len(s)):
    if k ==1:
        k=0
        continue
    try:
        li.append(dic[s[i]])
    except:
        t=''
        t=t+s[i]+s[i+1]
        li.append(dic[t])
        k=1
ss=''.join(li)
res=''
for i in range(0,len(ss),8):
    res+=chr(eval('0b'+ss[i:i+8]))
print(res)
```

17.  [梅森旋转算法](https://liam.page/2018/01/12/Mersenne-twister/)（Mersenne Twister Algorithm，简称 MT）相关[考点](https://badmonkey.site/archives/mt19937.html)。
18.  python的随机数（如random.getrandbits()）基于梅森旋转算法MT。MT19937能做到生成 1≤k≤623 个32位均匀分布的随机数，如果我们获取了624个，解下来的随机数就能用[randCrack](https://github.com/tna0y/Python-random-module-cracker)预测了。例题:[[GKCTF 2021]Random](https://blog.csdn.net/m0_57291352/article/details/119655082)
19.  Many time pad攻击（利用[汉明距离](https://baike.baidu.com/item/%E6%B1%89%E6%98%8E%E8%B7%9D%E7%A6%BB/475174)。

[题目及来源](https://codeleading.com/article/68135872581/)

```python
import string
from binascii import unhexlify
from itertools import *


def bxor(a, b):  # xor two byte strings of different lengths
    if len(a) > len(b):
        return bytes([x ^ y for x, y in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for x, y in zip(a, b[:len(a)])])


def hamming_distance(b1, b2):
    differing_bits = 0
    for byte in bxor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits


def break_single_key_xor(text):
    key = 0
    possible_space = 0
    max_possible = 0
    letters = string.ascii_letters.encode('ascii')
    for a in range(0, len(text)):
        maxpossible = 0
        for b in range(0, len(text)):
            if (a == b):
                continue
            c = text[a] ^ text[b]
            if c not in letters and c != 0:
                continue
            maxpossible += 1
        if maxpossible > max_possible:
            max_possible = maxpossible
            possible_space = a
    key = text[possible_space] ^ 0x20
    return chr(key)


salt = "WeAreDe1taTeam"
si = cycle(salt)
b = unhexlify(
    b'hex')
plain = ''.join([hex(ord(c) ^ ord(next(si)))[2:].zfill(2) for c in b.decode()])
b = unhexlify(plain)
print(plain)

normalized_distances = []

for KEYSIZE in range(2, 40):
    n = len(b) // KEYSIZE
    list_b = []
    for i in range(n - 1):
        list_b.append(b[i * KEYSIZE: (i + 1) * KEYSIZE])

    normalized_distance = 0
    for i in range(len(list_b) - 1):
        normalized_distance += hamming_distance(list_b[i], list_b[i + 1])
    normalized_distance = float(normalized_distance) / (KEYSIZE * (len(list_b) - 1))

    normalized_distances.append(
        (KEYSIZE, normalized_distance)
    )
normalized_distances = sorted(normalized_distances, key=lambda x: x[1])
print(normalized_distances)

for KEYSIZE, _ in normalized_distances[:5]:
    block_bytes = [[] for _ in range(KEYSIZE)]
    for i, byte in enumerate(b):
        block_bytes[i % KEYSIZE].append(byte)
    keys = ''
    try:
        for bbytes in block_bytes:
            keys += break_single_key_xor(bbytes)
        key = bytearray(keys * len(b), "utf-8")
        plaintext = bxor(b, key)
        print("keysize:", KEYSIZE)
        print("key is:", keys)
        s = bytes.decode(plaintext)
        print(s)
    except Exception:
        continue
```

21. 通过分析重合指数破解类似维吉尼亚的密码。

[题目及来源](https://blog.csdn.net/weixin_44110537/article/details/107947158)

```python
#重合指数的应用:
import gmpy2
c=open('cipher','r').read()
best_index=0.065
sum=0
dic_index={'a': 0.08167,'b': 0.01492,'c': 0.02782,'d':0.04253,'e': 0.12702,'f':0.02228,'g': 0.02015,'h':0.06094,'i':0.06966,'j':0.00153,'k':0.00772,'l':0.04025,'m':0.02406,'n':0.06749,'o':0.07507,'p':0.01929,'q':0.00095,'r':0.05987,'s':0.06327,'t':0.09056,'u':0.02758,'v':0.00978,'w':0.02360,'x':0.00150,'y':0.01974,'z':0.00074}
def index_of_coincidence(s):
    '''
    计算字符串的重合指数(所有字母出现频率的平方和)
    :param s: 给定字符串
    :return: 重合指数
    '''
    alpha='abcdefghijklmnopqrstuvwxyz'#给定字母表
    freq={}#统计字母频率(frequency)
    for i in alpha:
        freq[i]=0
    #先全部初始化为0
    for i in s:
        freq[i]=freq[i]+1
    #统计频率
    index=0
    for i in alpha:
        index = index + (freq[i] * (freq[i] - 1)) / (len(s) * (len(s) - 1))
    return index
def index_of_coincidence_m(s):
    '''
    计算明文s中的各字母的频率与英文字母中的频率的吻合程度.
    :param s:明文s
    :return:吻合程度
    '''
    alpha = 'abcdefghijklmnopqrstuvwxyz'  # 给定字母表
    freq = {}  # 统计字母频率(frequency)
    for i in alpha:
        freq[i] = 0
    # 先全部初始化为0
    for i in s:
        freq[i] = freq[i] + 1
    # 统计频率
    index = 0
    for i in alpha:
        index = index + freq[i] / len(s) * dic_index[i]
    return index
def get_cycle(c):
    '''
    求出最符合统计学的m,n的最小公共周期,方法为通过爆破足够大的周期样本,观察成倍出现的周期.
    计算方法为解出每一个子密文段的重合指数和然后求平均值 再与最佳重合指数相减 误差在0.01以内.
    :param c: 密文
    :return: 公共周期列表
    '''
    cycle=[]
    for i in range(1,100):
        average_index=0#平均重合指数初始化为0
        for j in range(i):
            s = ''.join(c[j+i*x] for x in range(0,len(c)//i))
            index=index_of_coincidence(s)
            average_index+=index
        average_index=average_index/i-best_index
        if abs(average_index)<0.01:
            cycle.append(i)
    return cycle
cycle=get_cycle(c)
print(cycle)#[6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96]

#通过计算得到cycle都是6的倍数,因此cycle最小很有可能为6

cycle=6

#开始爆破keys

def decrypt(c,i,j):
    '''
    通过i,j解出与之相对应的密文段
    :param c: 密文段
    :param i:与明文相乘的key
    :param j: 位移j(维吉尼亚密码)
    :return: 明文段
    '''
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    m=''
    for x in c:
        m+=alpha[((alpha.index(x)-j)*gmpy2.invert(i,26))%26]
    return m
def get_key(c):
    '''
    得到某一密文段的单个字符key i j
    方法为暴力枚举所有的可能性,找到最符合统计学规律的 i,j 即该密文段的重合指数与最佳重合指数误差小于0.01
    :param c: 密文段
    :return: i,j
    '''
    for i in range(26):
        if  gmpy2.gcd(i,26)!=1:#i对26的逆元不只一个,造成明文不唯一,因此不符合条件.
            continue
        for j in range(26):
            m=decrypt(c,i,j)
            index=index_of_coincidence_m(m)
            if abs(index-0.065)<0.01:
                return (i,j)
def get_all_key(s,cycle):
    '''
    得到一个周期内的所有的密文段的key
    :param s: 原密文
    :param cycle: 周期
    :return: 无
    '''
    for i in range(cycle):
        temps=''.join([s[i+x*cycle] for x in range(0,len(s)//cycle)])
        print(get_key(temps))
get_all_key(c,6)
# (19, 10)
# (7, 9)
# (23, 3)
# (19, 24)
# (7, 14)
# (23, 15)
#此时我们大致可以推测出:keya=[19,7,23],keyb=[10,9,3,24,14,15],因此根据题目给的式子,我们就可以还原出明文了.
plaintext=''
keya=[19,7,23]
keyb=[10,9,3,24,14,15]
len_a=len(keya)
len_b=len(keyb)
alpha='abcdefghijklmnopqrstuvwxyz'
for i in range(len(c)):
    plaintext+=alpha[((alpha.index(c[i])-keyb[i%len_b])*gmpy2.invert(keya[i%len_a],26))%26]
print(plaintext)
```
22. lfsr爆破mask。例题:[LittLe_FSR](../../CTF/moectf/2022/Crypto/LittLe_FSR.md)
23. [Schmidt-Samoa 密码体系](https://www.ruanx.net/schmidt-samoa/)。
24. 求斐波那契数列大数取模值可利用[皮萨诺周期](https://blog.csdn.net/caozhk/article/details/53407845)。例题:[[INSHack2019]Crunchy](https://www.bilibili.com/read/cv13950329)
25. [希尔密码](https://hstar.me/2020/08/hill-cipher-study/)（hill cipher，线性替换密码）。例题：[hill-hard](../../CTF/LA%20CTF/Crypto/hill-hard.md)
26. [subgroup confinement attack on Diffie-Hellman](https://crypto.stackexchange.com/questions/27584/small-subgroup-confinement-attack-on-diffie-hellman)。链接证明里涉及的[定理](/笔记/Crypto/%E6%8A%BD%E8%B1%A1%E4%BB%A3%E6%95%B0/%E6%8A%BD%E8%B1%A1%E4%BB%A3%E6%95%B0%EF%BC%881-29%EF%BC%89.md).

[例题及来源](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/crypto/Compromised/writeup.md)

```python
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad


p = "prime"
g = 65537
prime_fac = ["factors"]
w = prime_fac[1]
k = (p-1)//w
ct = bytes.fromhex('0123456789abcdef')
iv = ct[:AES.block_size]
ct = ct[AES.block_size:]

# generator for subgroup
sub_gen = pow(g, k, p)
m = 1
while m <= w:
    key = pow(sub_gen, m, p)
    key = sha256(long_to_bytes(key)).digest()
    print('Key:', key.hex(), end='\r')
    aes = AES.new(key, AES.MODE_CBC, iv)
    try:
        flag = aes.decrypt(ct)
        flag = unpad(flag, AES.block_size).decode()
        if flag.startswith('p_ctf{'):
            break
    except ValueError:
        pass
    finally:
        m += 1

print('Key:', key.hex())
print('Flag:', flag)
```

27. md5算法的[特性](https://en.wikipedia.org/wiki/MD5#Collision_vulnerabilities)：

```
if h(a) = h(b),
then h(a||c) = h(b||c)
where, a, b and c are strings and || is concatenation
```

例题：[Broken Hash](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/crypto/BrokenHash/writeup.md)

28. [CustomAESed](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/crypto/customAESed/writeup.md)
- AES的[CTR模式](https://wumansgy.github.io/2018/11/03/AES%E7%9A%84CTR%E6%A8%A1%E5%BC%8F%E5%8A%A0%E5%AF%86%E8%A7%A3%E5%AF%86%E8%AF%A6%E8%A7%A3/)的模拟加密与解密。

```python
#解密
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import unpad
from hashlib import sha256

ct = "ciphertext"
iv = ct[:12]
ct = ct[12:]
block_size = AES.block_size
ctr = Counter.new(nbits=32, prefix=iv[:8], suffix=iv[8:], initial_value=1)
key = sha256("128bit_secretkey".encode()).digest()
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
pt = cipher.decrypt(ct)
pt = unpad(pt, block_size)
print(pt.decode())
```

- 汉明码（[hamming code](https://en.wikipedia.org/wiki/Hamming_code#General_algorithm)）的加密与解密

```python
from Crypto.Util.number import *
from math import log2

# pt is same as in above code
bin_text = pt.decode()
txt_len = len(bin_text)
decoded_text = ''
parity_bits = ''
n_parity_bits = int(log2(txt_len))+1
for x in range(n_parity_bits):
    parity_bit = 0
    for bit in range(1, txt_len+1):
        if bit & (2**x) == 2**x:
            parity_bit ^= int(bin_text[bit-1])
    parity_bits = str(parity_bit) + parity_bits
err_pos = int(parity_bits, 2)
if err_pos != 0:
    err_bit = '1' if bin_text[err_pos-1]=='0' else '0'
    bin_text = bin_text[:err_pos-1] + err_bit + bin_text[err_pos:]
x = 0
for bit in range(1, txt_len+1):
    if bit == (2**x):
        x += 1
        continue
    decoded_text += bin_text[bit-1]
decoded_text = long_to_bytes(int(decoded_text, 2))
print(decoded_text.decode())
```

- 获取AES的[GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode)模式下的GMAC（Galois Message Authentication Code）。使用GCM的AES加密即可获得GMAC。

```python
from Crypto.Cipher import AES
from Crypto.Util.number import *
from hashlib import sha256
from base64 import b64encode

key = sha256("128bit_secretkey".encode()).digest()
iv = ""
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

# decoded_text is obtained in the above code
ct, tag = cipher.encrypt_and_digest(decoded_text)
encoded_tag = b64encode(tag)
print(encoded_tag.decode())
```

29. [Blocks and Boxes](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/crypto/Blocks_and_Boxes/writeup.md)
- propagating cipher block chaining（[PCBC](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Propagating_cipher_block_chaining_(PCBC))）
- Caesar's box cipher(特征是密文的长度为平方数)
30. AES侧信道攻击（power trace analysis）。使用相同密钥加密不同已知明文，通过测量CPU的能源消耗推断出密钥（已知密文也可以）。下面为一些相关链接。
- [Breaking AES with side channel analysis](https://www.youtube.com/watch?v=whhM_P7xMMU)
- [DPA & CPA applied on AES Attack](https://yan1x0s.medium.com/side-channel-attacks-part-2-dpa-cpa-applied-on-aes-attack-66baa356f03f)
- [CPA的python实现](https://teamrocketist.github.io/2018/11/14/Crypto-SquareCtf-2018-C4-leaky-power/)。

如果题目给出16进制的明文和列表形式的trace，就可以直接用下面的脚本：

```python
import numpy as np
textins=[]
traces=[]
num_trace=339
for i in range(num_trace):
    path=f"traces/trace{i}.txt"
    with open(path) as f:
        d=f.read().split('\n')
        plain=bytes.fromhex(d[0])
        textins.append(plain)
        traces.append(eval(d[1]))
HW = [bin(n).count("1") for n in range(0,256)]

sbox=(
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16)

def intermediate(pt, keyguess):
    return sbox[pt ^ keyguess]

traces = np.array(traces)
pt = textins
bestguess = []
if bestguess == []:

    numtraces = np.shape(traces)[0]-1
    numpoint = np.shape(traces)[1]

    bestguess = [0]*16
    for bnum in range(0, 16):
        cpaoutput = [0]*256
        maxcpa = [0]*256
        for kguess in range(0, 256):
            #Initialize arrays & variables to zero
            sumnum = np.zeros(numpoint)
            sumden1 = np.zeros(numpoint)
            sumden2 = np.zeros(numpoint)

            hyp = np.zeros(numtraces)
            for tnum in range(0, numtraces):
                hyp[tnum] = HW[intermediate(pt[tnum][bnum], kguess)]


            #Mean of hypothesis
            meanh = np.mean(hyp, dtype=np.float64)

            #Mean of all points in trace
            meant = np.mean(traces, axis=0, dtype=np.float64)

            #For each trace, do the following
            for tnum in range(0, numtraces):
                hdiff = (hyp[tnum] - meanh)
                tdiff = traces[tnum,:] - meant

                sumnum = sumnum + (hdiff*tdiff)
                sumden1 = sumden1 + hdiff*hdiff 
                sumden2 = sumden2 + tdiff*tdiff

            cpaoutput[kguess] = sumnum / np.sqrt( sumden1 * sumden2 )
            maxcpa[kguess] = max(abs(cpaoutput[kguess]))


        bestguess[bnum] = np.argmax(maxcpa)

    key = ''
    for b in bestguess: 
        key += "%02x"%b
    print("Best Key Guess: %s" % key)
```
31. [Classic Game Theory](http://itsvipul.com/writeups/Trellix_Hax_2023/GameTheory.html)
- MD5函数的默认初始状态如下：

```
A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476
```

如果使用的初始状态不同，md5的结果也会不同。可以通过修改[脚本](https://github.com/Utkarsh87/md5-hashing/blob/master/md5.py)里的初始值来获取自定义的md5函数。
- 彩虹表攻击（rainbow table attack）。本质上还是爆破出哈希值的全部可能性后查表。
32. [DSA](https://github.com/xalanq/jarvisoj-solutions/blob/master/crypto/DSA.md)
- DSA签名算法[介绍](https://ctf-wiki.org/crypto/signature/dsa/#k_1)
- 随机密钥k共享攻击脚本：

```python
from Crypto.PublicKey import DSA
from Crypto.Util.asn1 import DerSequence
from Crypto.Hash import SHA1
import gmpy2

pubkey_file = 'dsa_public.pem'
file_1 = ['./packet3/message3', './packet3/sign3.bin']
file_2 = ['./packet4/message4', './packet4/sign4.bin']

pubkey = DSA.import_key(open(pubkey_file, 'r').read())

y = pubkey.y
g = pubkey.g
p = pubkey.p
q = pubkey.q

print('y =', y)
print('g =', g)
print('p =', p)
print('q =', q)

def get_rs(signature):
    der_seq = DerSequence().decode(signature, strict=True)
    return int(der_seq[0]), int(der_seq[1])

hm1 = int(SHA1.new(open(file_1[0], 'rb').read()).hexdigest(), 16)
hm2 = int(SHA1.new(open(file_2[0], 'rb').read()).hexdigest(), 16)
r, s1 = get_rs(open(file_1[1], 'rb').read())
_, s2 = get_rs(open(file_2[1], 'rb').read())

print('r =', r)
print('hm1 =', hm1)
print('s1 =', s1)
print('hm2 =', hm1)
print('s2 =', s2)

print('cracking')

ds = s2 - s1
dhm = hm2 - hm1
k = gmpy2.mul(dhm, gmpy2.invert(ds, q))
k = gmpy2.f_mod(k, q)
tmp = gmpy2.mul(k, s1) - hm1
x = tmp * gmpy2.invert(r, q)
x = gmpy2.f_mod(x, q)
print('x =', x)
```
33. 进制转换。

- base47（已知编码表）解码
```python
from Crypto.Util.number import long_to_bytes
def base47(cipher,dic):
    print(long_to_bytes(sum([dic.index(cipher[i]) * (len(dic) ** (len(cipher) - i - 1)) for i in range(len(cipher))])))
```
- base4爆破解码
```python
import itertools
from Crypto.Util.number import *
s=''
t = []
for k in itertools.permutations('0123'):
    m = ''
    for i in s:
        if i == t[0]:
            m += k[0]
        elif i == t[1]:
            m += k[1]
        elif i == t[2]:
            m += k[2]
        elif i == t[3]:
            m += k[3]
    m = long_to_bytes(int(m, 4))
    if b'flag' in m:
        print(m)
        break
```
- base64爆破解码
  - 根据base64的原理，base64是一种把二进制值变成文本数据的方式。在输入是文本的情况下，3个原始字符对应的就是4个base64编码后的字符。所以可以对编码后的base64字符4个4个的进行爆破，只要还原出来的3个原始字符在可见字符范围内即可。出来的结果需要手动重组。
```python
import base64
import itertools
x=""
def check_4(base64_part):
    _temp=[]
    results=[]
    for i in range(4):
        if base64_part[i].isalpha():
            _temp.append((base64_part[i].upper(),base64_part[i].lower()))
        else:
            _temp.append((base64_part[i],base64_part[i]))
    n=map(tuple, itertools.product(_temp[0],_temp[1],_temp[2],_temp[3]))
    for i in set(n):
        s='%s%s%s%s'%i
        try:
            result=base64.b64decode(s.encode()).decode()
            if result.isprintable():
                results.append(result)
        except:
            pass
    return(results)
l=[]
for i in range(int(len(x)/4)):
    l.append(check_4(x[i*4:i*4+4]))
for i in l:
    print(i)
```

34. [shamir秘密共享](https://blog.sagiri.tech/index.php/archives/55/)（secret sharing）[解密脚本](https://github.com/adviksinghania/shamir-secret-sharing/blob/main/shamir_secret_galois.py)。以下是简略版，仅保留原脚本的解密功能。

```python
class ShamirSecret:
    def __init__(self) -> None:
        pass
    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm."""
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y

        return last_x, last_y

    def galois_div(self, num, den, p):
        """
        Division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse.

        Inverse of an integer can be found using the Extended Euclidean Algorithm.
        (Note: inverse of A is B such that A*B % p == 1)

        Compute num / den modulo prime p

        To explain what this means, the return value will be such that the
        following is true: den * galois_div(num, den, p) % p == num

        Parameters
        ----------
        num: int
            Numerator
        den: int
            Denominator
        p: int
            Prime Number

        """
        inv, _ = self.extended_gcd(den, p)
        return num * inv

    def reconstruct(self, rand_shares, prime) -> int:
        """
        Reconstruct the secret with random shares and a prime.

        Parameters
        ----------
        rand_shares: tuple
            Containing pairwise tuples of random shares.
        prime: int
            The prime number for the galois field.

        Returns
        -------
        sigma: int
            The reconstructed secret

        Example
        -------
        >>> s.reconstruct(s.random_shares(), s.prime)
        1234

        """
        l = len(rand_shares)  # length: number of random shares
        x_s = tuple(map(lambda x: x[0], rand_shares))  # x values of shares
        y_s = tuple(map(lambda x: x[1], rand_shares))  # y values of shares

        def PI(vars):  # product of inputs (PI)
            acc = 1
            for v in vars:
                acc *= v

            return acc

        nume = tuple()
        deno = tuple()
        for j in range(l):
            nume += (PI(x_s[m] for m in range(l) if m != j), )
            deno += (PI(x_s[m] - x_s[j] for m in range(l) if m != j), )

        den = PI(deno)
        num = sum(self.galois_div(nume[i] * den * y_s[i] % prime, deno[i], prime) for i in range(l))
        sigma = (self.galois_div(num, den, prime) + prime) % prime

        return sigma
s = ShamirSecret()
shares=[]
prime=0
print('\nReconstructed Secret:', s.reconstruct(shares,prime))
```
35. 以下的java aes加密是最基础的默认情况，只设置了key：

```java
SecretKeySpec secretKeySpec = new SecretKeySpec(KEY.getBytes(), "AES");
Cipher cipher = Cipher.getInstance("AES");
cipher.init(1, secretKeySpec);
return Base64.getEncoder().encodeToString(cipher.doFinal(str.getBytes()));
```

那么默认IV为`00000000000000000000000000000`，模式为`AES/ECB/PKCS5Padding`

36. [SCAlloped_potatoes](https://hackmd.io/9_WE-HinSYqFQyKubluRuw?view#SCAlloped_potatoes---484---Medium)
- rsa side-channel attack：通过分析power trace恢复私钥。如果用matplotlib将powertrace的波形图绘制出来，会发现波形图的起伏对应私钥的各个字节（需要放大才能看到）。大概约10个数据为一组，高峰为1，中间值为0。
```python
power = eval(open("data.txt").read())

from matplotlib import pyplot as plt
plt.plot(power)
plt.show()

byt = []
msg = ""
for i in range(len(power)):
    if power[i] < 125: # low voltage seperator
        if byt:
            chunks = [] # condense groups of 10
            for j in range(0, len(byt), 10):
                chunks.append(sum(byt[j:j+10]) / 10)
            
            # walk chunks
            j = 0
            byt = "0"
            while j < len(chunks):
                if j < len(chunks) - 1 and chunks[j] < 175 and chunks[j + 1] > 175:
                    byt += "1"
                    j += 2
                else:
                    byt += "0"
                    j += 1
            msg += chr(int(byt, 2))
            byt = []
    else:
        byt.append(power[i]) 
print(msg)
```
37. [scherbius-machine](https://meashiri.github.io/ctf-writeups/posts/202312-pingctf/#scherbius-machine)
- enigma爆破。在知道大部分解密参数后可以尝试爆破完整参数
- https://gist.github.com/C0nstellati0n/cf6ae2c5e0e9fe1ecb532d257a56e101#scherbius-machine
38. [quoted-printable](http://web.chacuo.net/charsetquotedprintable)编码。如果flag包含中文，cyberchef可能解密出乱码，用给的网站链接并把字符集选为utf8即可。
39. 当铺密码。
```python
s ='田由中人工大王夫井羊'
code=""
code = code.split(" ")
w = ''
for i in code:
    k=""
    for j in i:
       k+=str(s.index(j))
    w+=chr(int(k))
print(w)
```

40. [[NPUCTF2020]Mersenne twister](https://blog.csdn.net/weixin_44110537/article/details/108436309)
- 梅森旋转算法（Mersenne twister,mt73991伪随机）的爆破。若攻击者能获取624个寄存器状态，可以直接逆向。若不足则需要[爆破](https://liam.page/2018/01/12/Mersenne-twister/) 。
41. [PRNG](https://github.com/tamuctf/tamuctf-2023/tree/master/crypto/prng)
- 针对[linear congruential generator](https://en.wikipedia.org/wiki/Linear_congruential_generator)（LCG）的预测攻击：给出prng的前十个数字（种子未知）。找出接下来的10个数字。使用[脚本](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/lcg/parameter_recovery.py)恢复初始参数，或者直接交互：
```python
#https://ctftime.org/writeup/12046
from pwn import *
class Rand:
    def __init__(self, seed,m,a,c):
        self.m = m
        self.a = a
        self.c = c
        self.seed = seed
        if seed % 2 == 0: # initial state must be odd
            self.seed += 1

    def rand(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

r = remote("", 443)
r.recvline()

numbers = [int(r.recvline().rstrip()) for _ in range(10)]

from functools import reduce
from math import gcd

def egcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modinv for {} does not exist'.format(a))
    return x % m

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)

m, a, c = crack_unknown_modulus(numbers)
rand = Rand(numbers[-1], m, a, c)

for i in range(10):
    r.sendline(str(rand.rand()))
r.interactive()
```
- 类似题目：
    - [LCG](https://github.com/google/google-ctf/tree/master/2023/quals/crypto-lcg).这题只用了6个。详细解析文章： http://www.reteam.org/papers/e59.pdf
    - [Thermopolium](https://meashiri.github.io/ctf-writeups/posts/202307-odysseyctf/#thermopolium),脚本来自 https://tailcall.net/posts/cracking-rngs-lcgs/ 。发现5个竟然也可以（有人说理论上4个就够了）
    - [LCG](https://flocto.github.io/writeups/2023/deadsecctf/lcg-writeup/).无法求逆元时的特殊情况。如果想求 $x=a*b^{-1}\mod n$ 且 g=gcd(a,gcd(b,n)), can divide a,b,n by g and then take the inverse
42. 多种密码的python攻击脚本：https://github.com/jameslyons/python_cryptanalysis 。其中一个脚本可用于攻击变种维吉尼亚密码。
```python
from chall_patched import Vigenot as Vigenere
from itertools import permutations
from math import log10

ctext = 
ctext = ctext.upper()


# from https://github.com/jameslyons/python_cryptanalysis/blob/master/ngram_score.py
class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in open(ngramfile):
            key,count = line.split(sep) 
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score

# https://github.com/jameslyons/python_cryptanalysis/blob/master/quadgrams.txt
qgram = ngram_score('quadgrams.txt')
# https://github.com/jameslyons/python_cryptanalysis/blob/master/trigrams.txt
trigram = ngram_score('trigrams.txt')


# from https://github.com/jameslyons/python_cryptanalysis/blob/master/break_vigenere.py
# keep a list of the N best things we have seen, discard anything else
class nbest(object):
    def __init__(self, N=1000):
        self.store = []
        self.N = N

    def add(self, item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]

    def __getitem__(self, k):
        return self.store[k]

    def __len__(self):
        return len(self.store)


# init
N = 100
for KLEN in range(3, 20):
    rec = nbest(N)

    for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 3):
        key = ''.join(i) + 'A' * (KLEN - len(i))
        pt = Vigenere(key).decipher(ctext)
        score = 0
        for j in range(0, len(ctext), KLEN):
            score += trigram.score(pt[j:j + 3])
        rec.add((score, ''.join(i), pt[:30]))

    next_rec = nbest(N)
    for i in range(0, KLEN - 3):
        for k in range(N):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key = rec[k][1] + c
                fullkey = key + 'A' * (KLEN - len(key))
                pt = Vigenere(fullkey).decipher(ctext)
                score = 0
                for j in range(0, len(ctext), KLEN):
                    score += qgram.score(pt[j:j + len(key)])
                next_rec.add((score, key, pt[:30]))
        rec = next_rec
        next_rec = nbest(N)
    bestkey = rec[0][1]
    pt = Vigenere(bestkey).decipher(ctext)
    bestscore = qgram.score(pt)
    for i in range(N):
        pt = Vigenere(rec[i][1]).decipher(ctext)
        score = qgram.score(pt)
        if score > bestscore:
            bestkey = rec[i][1]
            bestscore = score
    print(next_rec.store)
    print(bestscore, 'Vigenere, klen', KLEN, ':"' + bestkey.lower() + '",', Vigenere(bestkey).decipher(ctext).lower())
```
其中chall_patched为题目的变种维吉尼亚密码的解密实现。[Vigenot](https://github.com/tamuctf/tamuctf-2023/tree/master/crypto/vigenot)

43. AES-128省去mix_columns步骤时的攻击。mix_columns帮助AES打乱明文与密文之间的联系。如果省去这一步，会导致改动明文的1个字节也仅会改动密文的一个字节，那么就能通过与服务器交互获取每个位置明文对应的密文，从而破解密文。
```python
from pwn import *
import binascii

HOST = 
PORT = 

characters = string.ascii_letters + string.digits
# array for knowning where to unshift all the bytes after the operations
#注意改动一位明文对应着改动的密文不在同一个位置。下表记录了两者之间的对应关系，如改动1索引处的明文会导致索引9处的密文改变
unshift = [0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 5, 14, 7]

r = remote(HOST, PORT)

r.recvuntil(b'flag:\n')
ctxt = r.recvline().decode().strip()
print("Here's the challenge to decrypt: %s" % ctxt)

# create blocks of each alphanumeric character to encrypt
ptxt = ""
for letter in characters:
	ptxt += letter * 16 
ptxt = binascii.hexlify(ptxt.encode())

# send the plaintext and receive the encrypted version
r.recvuntil(b'hex:')
r.sendline(ptxt)
r.recvuntil(b'blocks:\n')
enc = r.recvline().decode().strip()

decrypted = [''] * 16
response = ""
for i in range(len(ctxt) // 2):
	byte_c = ctxt[2 * i : 2 * (i+1)]

	if i == 16:
		response = "".join(decrypted)
		
	char_ind = i % 16
	
	# iterate through all letters and check to find the matching one
	for j in range(len(characters)):
		index = 32 * j + 2 * char_ind
		byte_e = enc[index : index + 2]

		# if we have a match add the character to the right spot
		if byte_e == byte_c:
			decrypted[unshift[char_ind]] = characters[j]

response += "".join(decrypted)
print("Decrypted version: %s" % response)
r.recvuntil(b'answer?')
r.sendline(response.encode())
r.recvuntil(b'flag:\n')
flag = r.recvline().decode().strip()

r.close()

print("The flag is: %s" % flag)
```
[Shmooving](https://github.com/tamuctf/tamuctf-2023/tree/master/crypto/shmooving)

44. AES-128 ECB省去sub_bytes步骤时的攻击。S_BOX是AES中唯一不是线性的步骤，因此移去这一步等于可以用某个线性方程解出明文。此时AES就像仿射密码，可以用c=Ap+k表示（参考这篇[帖子](https://crypto.stackexchange.com/questions/20228/consequences-of-aes-without-any-one-of-its-operations)）。其中p是明文，c是密文，A需要自行计算。通过将征程AES移除add_round_key步骤然后加密128个输入，每个输入只有一位是1，其余是0。于是出来的128个密文就是A矩阵的列。接着用已知明文/密文对获取K，就能解出p了。完整脚本与例题:[Shmooving 2](https://github.com/tamuctf/tamuctf-2023/tree/master/crypto/shmooving-2)

45. [Shmooving 3](https://github.com/tamuctf/tamuctf-2023/tree/master/crypto/shmooving-3)
- 仅一轮的AES-128-ECB并省去mix_columns步骤。相关参考链接：
  - [One round of AES-128(有mix_columns)](https://crypto.stackexchange.com/questions/80743/one-round-of-aes-128)
  - [Low Data Complexity Attacks on AES](https://eprint.iacr.org/2010/633.pdf)
  - [The Effects of the Omission of Last Round's MixColumns on AES](https://www.sciencedirect.com/science/article/pii/S0020019010000335)
  - [On the security of inclusion or omission of MixColumns in AES cipher](https://www.semanticscholar.org/paper/On-the-security-of-inclusion-or-omission-of-in-AES-AlMarashda-Alsalami/e13e7d71861290e218b57307a09dda040978375f)
46. [DSA签名算法](https://ctf-wiki.org/en/crypto/signature/dsa/)需要在每次签名时使用不同的明文或不同的公钥。如果一直使用相同的公钥签名相同的明文，仅让私钥x随机变化，会导致攻击者获取多个签名后相互减，并取gcd即可获取的明文。[DSA?](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/cry/dsa)
47. [SHA256-CTR](https://github.com/AVDestroyer/CTF-Writeups/blob/main/sdctf2023/sha256-ctr.md)
- 使用sha256作为AES-CTR模式下counter的加密函数：有出现[hash length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack)的风险（很多hash类函数都有这个漏洞，包括md5）
  - hash length extension attack简述：已知Hash(message1)和message1的长度（无需确切知道message1的内容），且可控制接下来的message2。那么就能获得Hash(message1||message2)的值，其中||表示拼接两条信息。
  - 注意实施攻击时需要有特殊的padding。当计算Hash(secret)时，需要将secret的长度pad成56字节的倍数，接着再在后面加上8字节。遵循以下规则：
    - 先在secret后加上字节`\x80`
    - 然后使用`\x00`将secret的长度pad成56字节的倍数
    - 最后将secret的bit的长度（不包括添加的`\x80`和`\x00`）以大端转为长度为8bytes。例如32字节的secret就是256 bit长，转为byte就是`(256).to_bytes(8,'big')=\x00\x00\x00\x00\x00\x00\x01\x00`
  - 实现脚本：https://github.com/stephenbradshaw/hlextend .使用方法如下：
```py
sha = hlextend.new('sha256')
new_meta = sha.extend(b'content', b'known', length, hash)
#已知SHA256(secret)的结果hash，想要在secret+known的后面添上content并在secret的值未知的情况下获取SHA256(secret+known+content)，length为secret的长度。运行函数可得到一串值value，SHA256(secret+value)=SHA256(secret+known+content)
#脚本里有解释，另一道类似的例题：https://github.com/TJCSec/tjctf-2023-challenges/tree/main/crypto/drm-1
```
- 小端里的拼接字节技巧。假设有counter的计数为0x12345678，小端存储结果为0x78 0x56 0x34 0x12。如果想在0x12后面填上任意字节但是counter的值未知，可以用以下公式计算：`byte*(1 << (numBytes*8))`。byte表示想拼接的字节，numBytes表示counter的字节长度，或者想要位移的字节数（想在多少字节后面拼接）。例如想在刚刚counter后添加0x9a，加上`0x9a*(1 << (4*8))`即可。
- 如何用python subprocess.run配合hlextend与oracle交互：[forgeme](https://github.com/An00bRektn/CTF/tree/main/live_events/nahamcon_23/crypto_forgeme)
- 其他学习资源：
    - https://www.youtube.com/watch?v=6QQ4kgDWQ9w
    - https://www.synopsys.com/blogs/software-security/forging-sha-1-mac-using-length-extension-attack-python/
    - [ForgeMe 1](https://github.com/mohnad-0b/programming/tree/main/CTF/NahamConCTF_2023%20Crypto/FrogeMe%201):使用工具[HashPump](https://github.com/bwall/HashPump)
    - https://notateamserver.xyz/nahamcon-2023-crypto/#forgeme-1-and-2 :使用[hash_extender](https://github.com/iagox86/hash_extender)
48. [Forcing a file’s CRC to any value](https://www.nayuki.io/page/forcing-a-files-crc-to-any-value):该脚本可以将一个文件的crc改为任意值，通过在指定偏移处插入构造的字节（这些字节不一定可见）。用法：`python3 forcecrc32.py FileName ByteOffset NewCrc32Value`,表示将FileName对应文件的内容改为NewCrc32Value，构造用的字节插入在ByteOffset偏移处。
49. [Uniform](https://github.com/HeroCTF/HeroCTF_v5/tree/main/Crypto/Uniform)
- Mersenne Twister随机数预测。题目给出来自`random.uniform(0, 2**32-1)`的624个数字，要求预测第625个数字。注意由于uniform的输出是float，不能直接套用接收int的预测器。改动的脚本使用z3，已经在wp里了。
- uniform函数内部实现：`uniform(a, b)=a + (b - a)*random.random()`,那么可以经过简单的数学运算恢复random.random。有了random.random，就能恢复a>>5和b>>6了（下面给出的另一个版本脚本看得更清楚）。这两个数就是要提交进untwister的数。
```python
from pwn import *
from z3 import *
from random import Random
from itertools import count
from time import time
import logging

SYMBOLIC_COUNTER = count()

def r_float(n1, n2):
    """ https://github.com/deut-erium/RNGeesus
        get the two 32-bit random generated numbers to get 1 float number in the range of [0,1]
    """
    a = n1>>5
    b = n2>>6
    # 2**53 = 9007199254740992.0
    # 2**26 = 67108864
    return (a*67108864.0+b)*(1.0/9007199254740992.0)

def float_to_2_randnumber(f):
    """ do the reverse here of r_float function above
        converting float number back to the 2 random number (before bit shift)
    """
    n = int(f * 9007199254740992.0)
    return n // 67108864, n % 67108864

class Untwister:
    """ https://github.com/icemonster/symbolic_mersenne_cracker/blob/main/main.py
    """
    def __init__(self):
        name = next(SYMBOLIC_COUNTER)
        self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
        self.index = 0
        self.solver = Solver()

    #This particular method was adapted from https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
    def symbolic_untamper(self, solver, y):
        name = next(SYMBOLIC_COUNTER)

        y1 = BitVec(f'y1_{name}', 32)
        y2 = BitVec(f'y2_{name}' , 32)
        y3 = BitVec(f'y3_{name}', 32)
        y4 = BitVec(f'y4_{name}', 32)

        equations = [
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18))
        ]

        solver.add(equations)
        return y1

    def symbolic_twist(self, MT, n=624, upper_mask=0x80000000, lower_mask=0x7FFFFFFF, a=0x9908B0DF, m=397):
        '''
            This method models MT19937 function as a Z3 program
        '''
        MT = [i for i in MT] #Just a shallow copy of the state

        for i in range(n):
            x = (MT[i] & upper_mask) + (MT[(i+1) % n] & lower_mask)
            xA = LShR(x, 1)
            xB = If(x & 1 == 0, xA, xA ^ a) #Possible Z3 optimization here by declaring auxiliary symbolic variables
            MT[i] = MT[(i + m) % n] ^ xB

        return MT

    def get_symbolic(self, guess):
        name = next(SYMBOLIC_COUNTER)
        ERROR = 'Must pass a string like "?1100???1001000??0?100?10??10010" where ? represents an unknown bit'

        assert type(guess) == str, ERROR
        assert all(map(lambda x: x in '01?', guess)), ERROR
        assert len(guess) <= 32, "One 32-bit number at a time please"
        guess = guess.zfill(32)

        self.symbolic_guess = BitVec(f'symbolic_guess_{name}', 32)
        guess = guess[::-1]

        for i, bit in enumerate(guess):
            if bit != '?':
                self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

        return self.symbolic_guess


    def submit(self, guess):
        '''
            You need 624 numbers to completely clone the state.
                You can input less than that though and this will give you the best guess for the state
        '''
        if self.index >= 624:
            name = next(SYMBOLIC_COUNTER)
            next_mt = self.symbolic_twist(self.MT)
            self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
            for i in range(624):
                self.solver.add(self.MT[i] == next_mt[i])
            self.index = 0

        symbolic_guess = self.get_symbolic(guess)
        symbolic_guess = self.symbolic_untamper(self.solver, symbolic_guess)
        self.solver.add(self.MT[self.index] == symbolic_guess)
        self.index += 1

    def get_random(self):
        '''
            This will give you a random.Random() instance with the cloned state.
        '''
        #logger.debug('Solving...')
        start = time()
        self.solver.check()
        model = self.solver.model()
        end = time()
        #logger.debug(f'Solved! (in {round(end-start,3)}s)')

        #Compute best guess for state
        state = list(map(lambda x: model[x].as_long(), self.MT))
        result_state = (3, tuple(state+[self.index]), None)
        r = Random()
        r.setstate(result_state)
        return r


ut = Untwister()
io = remote('static-01.heroctf.fr', 9000)
context.log_level = 'DEBUG'

for i in range(624):
    a = float(io.recvline().strip().decode())
    # uniform(a, b) is calculated by a + (b-a) * rand_number, rand_number is in [0,1]
    # https://github.com/python/cpython/blob/main/Lib/random.py
    # now a = 0, b = 2 ** 32 - 1
    n1, n2 = float_to_2_randnumber(a / (2**32-1))
    ut.submit((bin(n1)[2:]).rjust(27, '0') + '?????')
    ut.submit((bin(n2)[2:]).rjust(26, '0') + '??????')

r1 = ut.get_random()
nn1 = r1.getrandbits(32)
nn2 = r1.getrandbits(32)
ans = r_float(nn1, nn2) * (2**32 - 1)
```
50. [Deseret Alphabet](https://www.2deseret.com/):形如`𐐒𐐀 𐐎𐐌 𐐏𐐅 𐐝𐐀 𐐓𐐀 𐐇𐐙 𐐔𐐇𐐝𐐀𐐡𐐇𐐓 𐐣𐐀𐐤𐐞 𐐐𐐊𐐤𐐆 𐐒`
51. [squishy](https://meashiri.github.io/ctf-writeups/posts/202305-tjctf/)
- 不安全的rsa签名。rsa签名为 $m^d\mod n$ ，但签名用的公钥和私钥不能与加密时用的一样，或是签名时不要直接使用明文，先用某种哈希函数求其hash值再签名。当攻击者已知m和签名使用的公钥时，就能在私钥未知的情况下利用交互获取m的签名
    - 选取 $m_1\not ={m}$ ,利用交互获取其签名 $s_1=m_1^d\mod n$
    - 计算 $m_2=m\*m_1^{-1}$ ,获取其签名 $s_2=m_2^d\mod n=(m\*m_1^{-1})^d\mod n$
    - 计算 $s=s_1\*s_2=(m_1\*m\*m_1^{-1})^d\mod n=m^d\mod n$ ，即为m的签名
52. [spring](https://medium.com/@laithxl_79681/hsctf-2023-spring-challenge-823d78d41fc2)
- java(java.util.Random)随机数预测工具[ReplicatedRandom](https://github.com/fta2012/ReplicatedRandom/tree/master)使用。获取两个int随机数（nextInt()）或一个double（nextDouble()）或一个long（nextLong()）的情况下即可预测接下来所有由Random输出的随机数。提交long数字时记得在数字后加个`L`,表示是long。
- python版本的预测java long随机数输出的脚本：https://github.com/Cr4ckC4t/crack-java-prng/blob/main/crack-nextLong.py .参考wp2:https://kos0ng.gitbook.io/ctfs/ctfs/write-up/2023/hsctf/cryptography#spring-48-solves
53. [e](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/crypto/e)
- coppersmith:m高位泄露。此题完整m的位数未知，需要爆破。wp里的脚本比一般的coppersmith实现复杂，参考：https://www.cryptologie.net/article/222/implementation-of-coppersmith-attack-rsa-attack-using-lattice-reductions/
- 其他wp：https://pseudoleon.github.io/tjctf-23/#cryptoe
54. [keysmith](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/crypto/keysmith)
- 给出m和 $c\equiv m^e\mod n$ ，在加密时使用的公钥(n,e)未知的情况下构建另一组公钥 $(n_1,e_1)$ （可与原公钥相同），使得 $c=\equiv m^{e_1}\mod n_1$ 且 $m\equiv c^{d_1}\mod n_1$ 。 https://crypto.stackexchange.com/questions/8902/given-a-message-and-signature-find-a-public-key-that-makes-the-signature-valid 。大致步骤如下（根据wp里的脚本改动）：
    - 选取p和q，p-1和q-1均为光滑数且p（p-1的分解结果）与q（q-1的分解结果）都是m的二次剩余。选取的p和q应该满足 $m\equiv c^{d_p}\mod p,m\equiv c^{d_q}\mod q$
    - 利用离散对数找到上一步提到的 $d_p$ 和 $d_q$ 。应存在d满足 $d\equiv d_p\mod p-1,e\equiv d_q\mod q-1$ 。那么利用crt即可恢复这样的d。
    - `(p-1)*(q-1)`即为phi，`p*q`即为n，d对phi求逆元即为e。公钥+私钥生成完成。
- 其他wp：https://pseudoleon.github.io/tjctf-23/#cryptokeysmith
55. [AdventurersKnapsack](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#adventurers-knapsack),[wp2](https://meashiri.github.io/ctf-writeups/posts/202306-dantectf/#adventurers-knapsack)
- 背包加密问题（knapsack）的攻击：
  - [Lenstra–Lenstra–Lovász (LLL) lattice basis reduction](https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm)
  - [Low Density attack on low-density knapsacks](https://static.aminer.org/pdf/PDF/000/119/853/solving_low_density_knapsacks.pdf)
- low density attack: For a given set of positive integers $A = \{a_1,..., a_n\} (a_i\not ={a_j})$ and a given positive integer s, determining whether there exists a subset of A with its sum being s, or finding a vector $e = (e_1, . . . , e_n) ∈ \{0, 1\}^n$ satisfying $Σ_{i=1}^n a_i·e_i = s$ , is called the subset sum problem (or the knapsack problem), and is known as an NP-hard problem in general. Low-density attack is a method which works effectively against subset sum problems with low density. The density of the subset sum problem d is defined by $d=\frac{n}{log_2[max(pubk)]}$ 。pubk是背包加密的公钥，或者说上面指定的集合A。max(pubk)=max( $a_i$ )。有以下两种针对此种情况的方法：
  - Lagarias and Odlyzko (LO) algorithm (works on d < 0.6463)
  - [Coster, Joux, LaMacchia, Odlyzko, Schnorr, and Stern (CJLOSS)](https://www.di.ens.fr/~fouque/ens-rennes/sac-LLL.pdf) algorithm(works on d < 0.9408)。创建一个`M*M`的单位矩阵（M为公钥长度+1），其矩阵的最后一行换为0.5，最后一列除最后一项填写N\*公钥(N大于公钥长度的平方根)，而最后一项填上密文。然后使用LLL算法进行格基规约。结果矩阵中的一个向量就是明文的bit。
  - [脚本](https://github.com/hyunsikjeong/LLL)
  ```py
    from Cryptodome.Util.number import *
    ct=
    pubk=

    def rotate(l):
        return [l[-1]]+l[:-1]

    # one of the papers describing the attack (there are many), "Bi, Jingguo, Xianmeng Meng, and Lidong Han. "Cryptanalysis of two knapsack public-key cryptosystems." Cryptology ePrint Archive (2009)."

    base = [1]+[0]*179
    M=[]
    N=15 # >sqrt(180)，大于公钥长度平方根

    # creating lattice matrix
    for i in range(180):
        M.append(base+[N*pubk[i]])
        base=rotate(base)
    M.append([0.5]*180+[N*ct])

    B=matrix(QQ,M).LLL()
    for row in B:
        if all(abs(k) == 0.5 for k in row[:-1]):
            sol = row
    sol = ''.join(['0' if j==1/2 else '1' for j in sol[:-5]])
    print(long_to_bytes(int(sol,2)))
  ```
- 似乎不同密度的knapsack构造矩阵进行格基规约时，构造的矩阵内部的数字不同，而且会影响结果。例如[knapsack](/CTF/moectf/Crypto/knapsack.md)这题的方法放在这题就解不出来。
56. [Casino](https://kos0ng.gitbook.io/ctfs/ctfs/write-up/2023/hsctf/cryptography#casino-101-solves)
- AES CTR已知明文翻转bit攻击(AES CTR bitflipping)。假设明文有n字节且已知，那么获取其密文后可以将密文修改成指定结果，使其解密时输出想要的明文。只需将密文与明文和期望输出明文异或即可（字节的位置不能错）
```py
pt='abc'
expect='def'
ct=AES.Encrypt("CTR",pt,key,nonce)
ct[0]^='a'^'d'
ct[1]^='b'^'e'
ct[2]^='c'^'f'
print(AES.Decrypt("CTR",ct,key,nonce))
#def
```
- python可用科学计数法用较少的字节数表示大数。如`1e9`.或者`float("nan")`，也是三字节。
57. [signature-i](https://github.com/BCACTF/bcactf-4.0/tree/main/signature-i)
- rsa签名伪造：[Bleichenbacher's RSA signature forgery based on implementation error](https://mailarchive.ietf.org/arch/msg/openpgp/5rnE9ZRN1AokBVj3VqblGlP63QE/). 此攻击基于PKCS-1 padding的错误实现+e为3。
  - PKCS-1 padding格式如下：`00 01 FF FF FF ... FF 00  ASN.1  HASH`，在按照正常RSA解出m后移走前面的padding即可获取hash。假如不检查hash后是否有多余字节就直接比对，如：`00 01 FF FF ... FF 00  ASN.1  HASH  GARBAGE`，那么攻击者就能构造一个立方数，其立方根即为构造的signature。
58. [signature-ii](https://github.com/BCACTF/bcactf-4.0/tree/main/signature-ii)
- 椭圆曲线签名（elliptic curve digital signature，ecc）算法及验签：https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
- 签名参数k共用攻击：签名算法里的k应该是随机且每次签名都不同的。若相同，攻击者在获取两对签名(r,s)和(r,s')以及其对应的明文后即可获取第三个使用相同k的签名(r,s'')所对应的明文。操作如下：
  - $k=\frac{m-m'}{s-s'}$
  - $d_A=\frac{sk-m}{r}$ ( $d_A$ 为私钥)
  - $s''\*k=m''+rd_A$
  - $m=s''\*k-rd_A$
59. [winterfactory](https://github.com/MathVerg/WriteUp/tree/master/GPN2023/winterfactory)
- [Winternitz One-Time Signature](https://junhaideng.github.io/2021/12/24/cryptography/signature/wots/) scheme介绍。
  - 该签名scheme签名m的过程简述如下：
    - 使用某种哈希函数H获得H(m)，并选择数字w。接着将H(m)分成多块 ( $b_i$ )，每份 $log_2(w)$ bits。然后将每份 $b_i$ 转换为 $log_2(w)$ bit长度的unsigned整数，称为 $v_i$ 。计算校验和： $c=\sum_i(w-v_i)$ ,将其拼接到b后。
    - 对每份 $b_i$ 都选择一个随机数 $p_i$ ，作为私钥。私钥的大小等同于之前选择的hash函数的输出大小。
    - 将每个私钥 $p_i$ hash w次，得到的结果 $P_i$ 即为公钥。( $P_i = H^{(w)}(p_i)$ )
    - 最后将每个私钥 $p_i$ hash $v_i$ 次： $s_i=H^{v_i}(p_i)$ 。 $s_i$ 拼接在一起即为签名结果。
  - 验签步骤：
    - 提供签名 $s_i$ ，将签名hash $w-v_i$ 次。若提供的签名正确，结果应等于公钥 $P_i$ 。 $H^{w-v_i}(s_i)=H^{w-v_i}(H^{v_i}(p_i))=H^w(p_i)=P_i$
- 此题介绍了一种当私钥被使用多次的攻击。不过局限性较大，签名结果checksum的一半被泄露，且事先已获取一组明文与其签名。
60. [number-lock](https://github.com/MathVerg/WriteUp/tree/master/GPN2023/number-lock)
- Differential Fault Attack (DFA) on [AES](https://zhuanlan.zhihu.com/p/78913397)（128）
  - 相关文章（原理）和工具：
    - https://blog.quarkslab.com/differential-fault-analysis-on-white-box-aes-implementations.html
    - https://github.com/Vozec/AES-DFA
  - 题目特征点
    - 允许攻击者在AES的某一轮加密处修改plain state为未知随机字节（fault）
    - 允许交互。攻击者输入明文，服务器返回对应的密文
    - 加密时的密钥固定。目标为利用有限的交互次数+fault破解使用的密钥
61. [signed_jeopardy](https://notateamserver.xyz/nahamcon-2023-crypto/#signed-jeopardy)
- ECDSA（椭圆曲线，ecc） nonce（k值）重用（reuse）导致的[签名伪造](https://billatnapier.medium.com/ecdsa-weakness-where-nonces-are-reused-2be63856a01a)。感觉和58条[signature-ii](https://github.com/BCACTF/bcactf-4.0/tree/main/signature-ii)类似，不过这题有不同的脚本
    - 继续补充看到的其他脚本：[Double-Whammy](https://mindflayer02-ctf-sec-notes.gitbook.io/mindflayer02-bisher-mohammads-ctf-writeups/nitectf-23/double-whammy)
    - 自动工具： https://github.com/Hungary23/ecc_cryptanalysis/
62. [Just One More](https://notateamserver.xyz/nahamcon-2023-crypto/#just-one-more)
- 利用矩阵与阶梯形矩阵解线性方程组。sagemath里构造出矩阵后，可用Matrix.rref()获取阶梯形矩阵。注意如果矩阵的阶数和未知数的数量不一样的话，结果的阶梯形矩阵会有差别。详情见wp。
- 也可用sympy linsolve： https://github.com/nzec/ctf-notes/tree/master/NahamCon23/Just%20One%20More
63. [RSA Outro](https://notateamserver.xyz/nahamcon-2023-crypto/#rsa-outro)
- 使用sympy解方程。
```py
from sympy import *
var('q')
solutions = solve(2*q*(q-1)-phi, q) #这里的方程结果为0，即 2*q*(q-1)-phi==0
q = solutions[1]
```
64. [order](https://github.com/hsncsclub/hsctf-10-challenges/tree/main/crypto/order)
- 数论寻找元素的阶（order， $a^x\equiv 1\mod p$ ,满足该条件最小的x）
    - 通过phi的因子来找（欧拉定理告诉我们 $a^{phi}\equiv 1\mod p$ ,于是phi可能为阶的倍数）：https://kos0ng.gitbook.io/ctfs/ctfs/write-up/2023/hsctf/cryptography#order-46-solves
    ```py
    from sympy.ntheory import *
    from Crypto.Util.number import long_to_bytes
    M = 
    sus = 
    a = 
    # sus**(t+1) == 1 (mod M)
    # note gcd(sus, M) = 1
    # order of sus (mod M) divides totient(M)
    # let's try determining the order
    order = -1
    for i in divisors(totient(M)):
        if pow(sus, i, M) == 1:
            order = i
            break
    print(order)
    # also, t == flag^-1 * a (mod M), and in particular t < M
    # order of sus (mod M) divides t+1, so just test multiples of order - 1 less than M
    # WOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # flag == a * t^-1 (mod M)
    for t in range(order-1, M, order):
        flag_long = a * pow(t, -1, M) % M
        flag_bytes = long_to_bytes(flag_long)
        if flag_bytes.startswith(b"flag{"):
            print(flag_bytes.decode())
            break
    ```
65. [Cursved](https://github.com/google/google-ctf/tree/master/2023/crypto-cursved)
- Schnorr signature scheme(基于ecc，椭圆曲线)。关于这种电子签名法，详细解析参考： https://www.btcstudy.org/2021/11/20/introduction-to-schnorr-signatures-by-suredbits/ ，单纯讲定义的简洁版： https://www.cnblogs.com/lsgxeva/p/12021636.html 。关于椭圆曲线本身再补充两个链接：
    - https://hackernoon.com/what-is-the-math-behind-elliptic-curve-cryptography-f61b25253da3
    - https://zhuanlan.zhihu.com/p/36326221
- [Pell conics over finite fields](https://arxiv.org/abs/2203.05290)：the points can form two different types of groups, depending on whether d is a square or a non-square in k, respectively。若d是模p的二次剩余，就有以下同构： $C(k)\simeq k^{\*}.C(k)\rightarrow k^{\*}(x,y)\mapsto x+sy$ ,where we fix a square root s of d in k. Hence, instead of solving a generically hard DLP over the Pell conic group law, we can solve it over $k^{\*}$ instead. 个人认为的关键点：ecc的安全性基于离散对数的计算难度，但如果像上面这样有Pell conic的存在且d是模p的二次剩余，就能将原本要计算的k域转为 $k^{\*}$ ,计算就能简单一点，从而破解私钥了。使用[cado-nfs](https://cado-nfs.gitlabpages.inria.fr/)计算。参考： https://discord.com/channels/984515980766109716/1120323829303083079/1122884985007898654
```py
p = 
D = 
F = GF(p)
dd = F(D).sqrt()

G = GX, GY = F(2), F(1)
assert GX^2 - D*GY^2 == 1
PUB = (F(), F())

φ = lambda x, y: (x - dd*y, x + dd*y)
ψ = lambda u, v: ((u + v)/2, (v - u)/(2*dd))

uG = φ(*G)[0]
uP = φ(*PUB)[0]
ell = ZZ(p//2)
assert is_prime(ell)
print(f"G: {uG^2}\nP: {uP^2}")
cadologG = 
cadologP = 
dlog1 = ZZ(GF(ell)(cadologP) / (cadologG))
dlog2 = ZZ(discrete_log_rho(uP^ell, uG^ell, operation='*', ord=2))
dlog = CRT(ZZ(dlog1), ZZ(dlog2), p//2, 2)
print(f"PRIVATE = {dlog}")
print(uG^dlog == uP)
#cadologG 和 cadologP计算方法： ./cado-nfs.py -dlp target=<value_G>,<value_P> ell=<p//2> <p>
```
66. [mhk2](https://github.com/google/google-ctf/tree/master/2023/crypto-mhk2)，[wp](https://mystiz.hk/posts/2023/2023-06-26-google-ctf-mhk2/)
- 修改版MHK2 cryptosystem攻击。此题与完整MHK2 cryptosystem实现方式的不同点在于：In MHK2 cryptosystem, the prime numbers $p_1$ and $p_2$ are randomly generated such that $\frac{p_i}{2}$ < $\sum _js_{ij}$ < $p_i$ . This is not our case – we fix it to $p_i=\sum _js_{ij}+2$ 。所以这道题提供的解法无法破解标准的MHK2 cryptosystem。
67. [myTLS](https://github.com/google/google-ctf/tree/master/2023/crypto-mytls)
- [Key Compromise Impersonation attacks (KCI)](https://www.cryptologie.net/article/372/key-compromise-impersonation-attacks-kci/):当攻击者可以获取client或server的private key后，即可实施中间人攻击，篡改加密的通信。根据不同的实现，篡改的方式不同。wp里列出了一种方式。
68. [ZIP](https://github.com/google/google-ctf/tree/master/2023/crypto-ziphard)
- 微型ZIP archiver python实现，或者也能称为PKZIP Stream Cipher。这种密码有[ZIP 明文攻击](https://flandre-scarlet.moe/blog/1685/)，可用[bkcrack](https://github.com/kimci86/bkcrack/tree/master)工具进行攻击。该工具要求至少知道12个字节的明文以及其对应密文（或者说明文对应密文的偏移），其中至少有8个字节是连续的。此题知道的12字节分布在两个不同的文件，前8个已知字节在flag.txt里，而另外5个在另一个文件。不过根据明文攻击的原理，前8个字节才是真正用于破解密钥的，后面的字节只是为了验证得到的密钥是否正确。所以可以将工具自行patch以下，参照wp里的做法。
- python里，若将字符串以`utf-8-sig`编码，除了字符串正常UTF-8编码，还会在结果前面加上Unicode byte order marker。Utf-8里这个marker为`ef bb bf`
- C语言爆破CRC脚本
69. [Three-Time Pad](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/crypto/three_time),[wp](https://github.com/daffainfo/ctf-writeup/tree/main/UIUCTF%202023/Three-Time%20Pad)
- 同样的密钥用于加密多个消息且密文已知，可直接用wp里的脚本恢复明文+key。不过这题其实没那么麻烦，只是记录一下脚本：https://github.com/Jwomers/many-time-pad-attack/tree/master ,即使密文长度不一样也可以用
70. [Morphing Time](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/crypto/morphing),[wp](https://tsumiiiiiiii.github.io/uiu-crypto/#morphing-time)
- [Elgamal Cryptosystem](https://en.wikipedia.org/wiki/ElGamal_encryption)：homomorphic under multiplication。
- 利用[tonelli shanks algorithm](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm)解方程 $x^2\equiv a\mod p$
71. [At Home](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/crypto/at_home),[wp](https://github.com/P3qch/ctfs/tree/main/uiuctf2023/at_home)
- wp提供了一种利用z3求解 $ax\equiv b\mod p$ 的方法
72. [Crack The Safe](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/crypto/crack_the_safe),[wp](https://bronson113.github.io/2023/07/03/uiuctf-2023-writeups.html#crack-the-safe)
- Pohlig-Hellman discrete log Attack:对于离散对数 $g^x\equiv k\mod p$ （p为质数），若p-1（群的阶）为光滑数且最大的那个因子较小，则计算x的代价将降为那个最大的因子。需要使用[cado-nfs](https://github.com/cado-nfs/cado-nfs)（[gitlab](https://gitlab.inria.fr/cado-nfs/cado-nfs)）计算模不同因子下的指数后再用crt组合出原本的x。
- 另一种解法 https://github.com/Norske-Nokkelsnikere/writeups/tree/main/2023/uiuctf-2023/crack_the_safe 利用AES 128bit key的特点爆破出了key（cado-nfs无法安装，故只能利用sagemath算出前几个因子相关的对数，最后一个最大的算不出来）
    - 类似做法： https://pseudoleon.github.io/uiuctf-23/ 。两者都有Pohlig-Hellman的sagemath实现
73. [Group Projection](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/crypto/group_projection),[wp](https://github.com/ctfguy/My_CTF_Writeups/blob/main/UIUCTF%202023/Crypto/Group%20Project%20and%20Projection/solution.md)
- [Small subgroup confinement attack on Diffie-Hellman](https://crypto.stackexchange.com/questions/27584/small-subgroup-confinement-attack-on-diffie-hellman)
74. [Derik](https://github.com/AKSLEGION/Crypto-Writeups/tree/master/Crypto_CTF_2023/Derik)
- 对于不定方程 $x^3+y^3+z^3=nxyz$ ,0 < n < 81的已知解： http://matwbn.icm.edu.pl/ksiazki/aa/aa73/aa7331.pdf ，（<= 197）: https://mathoverflow.net/questions/384565/status-of-x3y3z3-6xyz
- 根据 https://zhuanlan.zhihu.com/p/642698403 ， 方程 $x^3+y^3+z^3=nxyz$ ，或者说三次齐次方程（cubic homogeneous equation），都与椭圆曲线等价（也不是说完全一样，两者之间有同态关系(不太确定是不是同态，birational isomorphism？)）。a homogeneous cubic in three variables with rational coefficients利用sagemath的[EllipticCurve_from_cubic](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/constructor.html#sage.schemes.elliptic_curves.constructor.EllipticCurve_from_cubic)即可做转换
```py
R.<x,y,z> = QQ[]
cubic = x^3 + y^3 + z^3 - 73 * x * y * z #三次齐次方程
P = [1,-1,0] #三次齐次方程的非零解，在上述方程所构成的curve C上defining a projective point
E = EllipticCurve_from_cubic(cubic, P, morphism=False) #当morphism=False，返回C在birational isomorphism映射后的Weierstrass elliptic curve（E）像
f = EllipticCurve_from_cubic(cubic, P, morphism=True) #若等于True，直接返回C到E的birational isomorphism
finv = f.inverse() #获取f的逆映射。既然f是从cubic curve到elliptic curve，这个就是从elliptic curve到cubic curve
R = E.gens()[0] #获取E上的生成元
PP = f(P)
print(finv(R)) #打印生成元映射到cubic curve的点
```
75. [TPSD](https://meashiri.github.io/ctf-writeups/posts/202307-cryptoctf/#tpsd)
- 求解不定方程（丢番图方程，diophantane equation） $x^3+y^3+z^3=1$ 的任意bit长度解。这个方程的解一定满足 $(9a^4)^3+(3a-9a^4)^3+(1-9a^3)^3=1$ (或者 $(9a^4)^3+(-3a-9a^4)^3+(1+9a^3)^3$ ，来源 https://github.com/AKSLEGION/Crypto-Writeups/tree/master/Crypto_CTF_2023/TPSD),且只有最后一个数字可能是质数。插入不同的a值即可获取不同的解。
    - 论文：https://www.ams.org/journals/mcom/2007-76-259/S0025-5718-07-01947-3/S0025-5718-07-01947-3.pdf
    - wiki： https://en.wikipedia.org/wiki/Sums_of_three_cubes
76. [Blobfish](https://meashiri.github.io/ctf-writeups/posts/202307-cryptoctf/#blobfish)
- 使用[bkcrack](https://github.com/kimci86/bkcrack)实施zip明文攻击爆破加密zip密码。此题zip内部的文件为png（Image.new('RGB', (800, 50))），因为png的前16个字节已知且固定，故可以实施明文攻击。
    - https://zhuanlan.zhihu.com/p/643106267 ：似乎前33（0x21）个都是一样的
77. [Bertrand](https://github.com/abhishekg999/CTFWriteups/tree/main/CryptoCTF/Bertrand)
- [Hilbert curve](https://en.wikipedia.org/wiki/Hilbert_curve):一种连续分形空间填充曲线，一条无限长的曲线可完全填充有限的二维空间。利用它可以将一个任意数字独特地映射到一个2d点（单射，可逆）
78. [ASlv1](https://github.com/AKSLEGION/Crypto-Writeups/tree/master/Crypto_CTF_2023/ASIv1)
- 模上的矩阵与向量相乘。其实就是正常的矩阵操作然后把每个结果模制定的数就好了。对于Ax=b其中x和b都是向量，A是矩阵的方程，可以用sagemath自带的solve_right来解决(估计类似的xA=b就用solve_left)。wp里的解法尝试将矩阵行规约（elementary row reduction operation），应该是solve_right的本质。不过solve_right要考虑矩阵是否满秩和线性系统的复杂度，参考 https://zhuanlan.zhihu.com/p/643106267 和 https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#asiv1
79. [Trex](https://github.com/AKSLEGION/Crypto-Writeups/tree/master/Crypto_CTF_2023/Trex)
- 求解不定方程 $x^2 + y^2 - xy = a * z^3$ ， $z = 3a,y = 6a^2,x = -b/2 = y/2 = 3a^2$ 。这类方程的思路是可以把整个方程本身看作普通的基于x的一元二次方程，然后根据求根公式的判别式 $b^2=4ac$ ，我们可以让提供的x，y和z满足这一条件（根一样会比较简单），然后基于这一条件推出x，y和z与a的关系。
80. [Roldy](https://github.com/AKSLEGION/Crypto-Writeups/tree/master/Crypto_CTF_2023/Roldy)
- python pyope模块实现了order-preserving encryption，意味着如果a < b 那么 enc(a) < enc(b)，即加密函数单调递增。在给出密文和oracle后，可利用binary search解密密文。前提是oracle满足以下条件：
    - oracle拥有无限次交互机会
    - oracle会返回用户输入的任意明文的密文
    - 明文按照单个字符一个一个加密
81. [Barak](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#barak),[wp](https://zhuanlan.zhihu.com/p/642698403)
- 曲线方程 $x^3+y^3+c=dxy$ 同样可以利用sagemath里三次齐次方程转椭圆曲线的函数[EllipticCurve_from_cubic](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/constructor.html#sage.schemes.elliptic_curves.constructor.EllipticCurve_from_cubic)转椭圆曲线，只需引入一个变量z来把它变成齐次式 $x^3+y^3+cz^3=dxyz$ ，当z=1时即为原方程。映射完成后原曲线方程上的离散对数问题Q=mP就可以在椭圆曲线上用discrete_log完成。
    - 这个曲线方程其实是椭圆曲线的[Hessian形式](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Hessian_form_of_an_elliptic_curve),通过代数运算可以直接代回成Weierstrass形式。 https://ctfnote.leg.bzh/pad/s/SL4mIXF3b
- sagemath里面可以检查曲线方程是什么类型的曲线
```py
x,y=ZZ['x,y'].gens()
eq=
Curve(eq).genus()
#若输出1，说明曲线方程是椭圆曲线。可以去 https://www.hyperelliptic.org/EFD/ 查看它是椭圆曲线的什么形式
```
- 在椭圆曲线中，若Q=mP（over GF(p)）且m小于P的阶小于p，那么离散对数求出m后不一定是原来的m，真正的m类似模运算，为x+n|P|
82. [Risk](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#risk)
- [A New Attack on Special-Structured RSA Primes](https://einspem.upm.edu.my/journal/fullpaper/vol13saugust/8.pdf): 当RSA的p和q有特殊结构时，可以对其实施攻击。 $p=a^m+r,q=b^m+s$ . $n=pq=(a^m+r)(b^m+s)=a^mb^m+sa^m+rb^m+rs\equiv sa^m+rb^m+e(\mod a^mb^m)$
- 如果已知两个数m和n的乘积与和，可构造 $f(x)=(x-m)(x-n)$ ，即一元二次方程，然后求根，两个根即为m和n。
- RSA当e与phi不互素时，对p和q分别对c开e次根，然后利用crt组合出原本的m。在[NCTF2019]easyRSA那里提过，包括wp，这里再提供几种不同的做法
    - https://zhuanlan.zhihu.com/p/642698403 ：开根+crt的不同脚本
83. [Keymoted](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#keymoted)
- Z/nZ上ECC类似RSA的加密。思路与正常RSA差不多，必要的一步也是分解n,然后求逆元。
```py
Z = Zmod(n)
E = EllipticCurve(Z, [a, b]) #定义椭圆曲线
C = E(encx, ency) #C=me，encx和ency是结果密文C的x和y坐标
Ep = EllipticCurve(GF(p), [a, b]) #定义p和q下的椭圆曲线
Eq = EllipticCurve(GF(q), [a, b])
od = Ep.order() * Eq.order() #获取phi
d = pow(e, -1, od)
M = d * C
print(long_to_bytes(int(M.xy()[0])))
```
或者参考 https://zhuanlan.zhihu.com/p/643176962 ，在p和q下分别求离散对数，然后crt。

84. [Big](https://zhuanlan.zhihu.com/p/643355092)
- [Cocks IBE scheme](https://en.wikipedia.org/wiki/Cocks_IBE_scheme)：基于二次剩余（quadratic residuosity）的加密方式
- [韦达定理](https://baike.baidu.com/item/%E9%9F%A6%E8%BE%BE%E5%AE%9A%E7%90%86/105027)+sagemath利用kronecker求二次剩余
- n=pq，当q=int(str(p)[::-1])时，可以快速分解n
- 其他wp
    - https://hackmd.io/@taiyaki/BJbEomuF2#Big-169-pts-23-solves-Hard
    - https://shiho-elliptic.tumblr.com/post/722391959624433664/crypto-ctf-2023-writeup-en
85. [Marjan](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#marjan),[wp](https://zhuanlan.zhihu.com/p/643355092)
- 基于ECC的类似ecdsa的签名算法。当k较小时，可以转化为NHP问题然后利用格和格基规约（如LLL）来解
- 验签算法实现时要考虑签名参数的非平凡性，否则攻击者可能可以将某个参数置为0然后消除方程的未知数。
86. [Shevid](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#shevid)
- [Supersingular isogeny key exchange(SIDH)](https://en.wikipedia.org/wiki/Supersingular_isogeny_key_exchange)（论文介绍： https://eprint.iacr.org/2019/1321.pdf ）破解： https://eprint.iacr.org/2022/975 。针对该加密的Castryck-Decru攻击脚本： https://github.com/GiacomoPope/Castryck-Decru-SageMath
    - 其他wp（用作脚本使用参考）
        - https://zhuanlan.zhihu.com/p/643416297
        - https://shiho-elliptic.tumblr.com/post/722391959624433664/crypto-ctf-2023-writeup-en
87. [Byeween](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#byeween)
- 给定随机椭圆曲线E和E上一点Q，找到所有满足 $2P=Q,P\in E$ 的P。使用sagemath的division_points。
    ```py
    E = EllipticCurve()
    Q = E(x,y,z)
    for x in Q.division_points(2):
        print(",".join(map(str, x.xy())))
    #配合sage_eval和coefficient： https://shiho-elliptic.tumblr.com/post/722391959624433664/crypto-ctf-2023-writeup-en
    ```
    - 构造方程解法： https://zhuanlan.zhihu.com/p/643355092
88. ecc上的[Smart's Attack](https://ariana1729.github.io/2021/05/31/SmartAttack.html)。当一个椭圆曲线additive transfer（anomalous curve）时，则可以进行Smart's Attack，能够在线性时间内解决ecc上的dlp问题。
 - additive transfer指the order of the elliptic curve group is equal to the order of the underlying prime field. 感觉用sagemath里的api比较好解释：
```py
Ep = EllipticCurve(GF(p), [a, b]) #p-1: the order of the underlying prime field. 要是p不是质数的话可能会是别的数，质数的话就是p-1
Ep.order() #曲线加法群的阶（the order of the elliptic curve group）
```
- 攻击脚本：https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/smart_attack.py
- 可以在这里查看什么样的曲线容易受到transfer相关的攻击： https://safecurves.cr.yp.to/transfer.html
- 关于如何判断曲线是否anomalous以及另一个版本的smart attack脚本，可以参考[这题](https://github.com/sahuang/my-ctf-challenges/tree/main/vsctf-2023/crypto_ecc-fantasy)的生成函数。感觉特征应该是`E.trace_of_frobenius() == 1`
89. [rsalcg2](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/crypto/rsalcg2),[wp](https://hackmd.io/@keymoon/S100q2xch)
- [half GCD(hgcd)算法](https://www.cnblogs.com/whx1003/p/16217087.html)在特殊情况下的加速。hgcd用于计算多项式的gcd，比欧几里得算法要快。
90. [The Vault 2](https://github.com/rwandi-ctf/ctf-writeups/blob/main/amateursctf2023/the%20vault%202.md)
- 三个立方和方程以及四个立方和方程的参数化
    - https://en.wikipedia.org/wiki/Sum_of_four_cubes_problem
    - https://www.alpertron.com.ar/FCUBES.HTM
    - https://github.com/aparker314159/ctf-writeups/blob/main/AmateursCTF2023/the-vault-2.md
91. [Weak Primes](https://github.com/rwandi-ctf/ctf-writeups/blob/main/amateursctf2023/weak%20primes.md)
- coppersmith补充
    - The coppersmith method uses lattice reduction to find small integer solutions to a polynomial modulo a factor of n that is $\geq n^{\beta}$
    - Setting $\beta\approx 0.5$ and $f(x)=2^{2047}+x$ , it will find an integer solution to x such that $2^{2047}+x\equiv 0\mod m$ where m|n, $m\geq n^{\beta}$ (the smaller the difference between m and $n^{\beta}$ the better)
92. [Non-Quadratic Residues](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/crypto/non-quadratic-residues),[wp](https://github.com/GabrieleDellepere/writeups/blob/main/AmateursCTF/non-quadratic-residue-writeup.md)
- amm开根法应用的特殊情况。假如有 $x^a\equiv b\mod c$ 其中a，b和c已知，amm开根法可用于恢复x。若a可分解，可以参照wp里的做法，分别开分解后的质数次根。如`a=2*3*5*7`，就在模c的基础上开2次根，然后开出的结果拿去开3次根，结果再拿去开5次根……一直到恢复x
    - 指数较小的甚至直接用sagemath构造多项式就能开出来
    ```py
    P.<x> = PolynomialRing(Zmod(b))
    pol=x^a-c
    roots=pol.roots()
    ```
93. [gcd-query](https://enscribe.dev/blog/actf-2023/gcd-query/)
- $x\equiv -n\mod gcd(x+n,m)$
94. [flatcrypt](https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-09-14-CSAW-CTF-Quals/README.md#100-crypto--flatcrypt)
- [CRIME](https://en.wikipedia.org/wiki/CRIME) oracle攻击。攻击条件：
    1. 可输入内容与服务器进行交互
    2. 输入的内容被拼接到flag后并返回压缩的内容。压缩方式诸如gzip，zlib等都可以
    - 原理（以zlib举例）：当压缩的内容有重复部分时,压缩内容的长度会比没有重复部分的短。可利用这点猜测出之前的内容是什么
    ```py
    import zlib
    print(len(zlib.compress(b"good_secret"))) #19
    print(len(zlib.compress(b"good_secret" + b"good"))) #21
    print(len(zlib.compress(b"good_secret" + b"baad"))) #23
    ```
    脚本： https://github.com/mpgn/CRIME-poc/tree/master
95. [signer](https://meashiri.github.io/ctf-writeups/posts/202307-imaginaryctf/#signer)
- crc32无法防止collsion，也无法防止数据被篡改。在给定一个crc32值后，可以利用[工具](https://github.com/theonlypwner/crc32)逆向算法，获取该crc32值对应的字符串
96. [MCTEENX](https://xhacka.github.io/posts/writeup/2023/07/29/MCTEENX/)
- 利用bkcrack爆破ZipCrypto Store： https://www.anter.dev/posts/plaintext-attack-zipcrypto/
- 利用CyberChef爆破异或密码的key（cribdrag）
97. [Fermentation](https://xa21.netlify.app/blog/tfcctf-2023/Fermentation/)
- [aes cbc翻转字节攻击](http://www.f0und.icu/article/28.html)。可以在不知道key和iv的情况下，通过修改密文实现解密出来的明文为攻击者期望的内容
98. [Polypoint](https://maxniederman.com/posts/ctf/lit-2023/polypoint/)
- 线性方程组缺少一个完全未知的方程的解法。之前见过缺少一个方程组的线性系统，但是那个未知的方程解已知。这题完全不知道。当线性系统缺少方程时，方程组有解且有无数个解，这时就需要通过设置解的范围来确定唯一的的解。wp作者使用的软件为Mathematica
```
Encoded = Import["encoded.csv"]; //导入文件
X = Encoded[[All, 1]];
Y = Encoded[[All, 2]]; //将文件中第二列全部内容存入Y
V = Function[x, Power[x, Range[0, 10]]]; //构造一个函数，参数为x，返回x 0-10幂次组成的数列
M = V /@ X; //将函数作用于X中的每一元素
p = {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11};
SolutionBounds = Cuboid[ //构造一个解的范围。根据wp，p1的下限是0，上限是2^(78 * 8)；其余的下限是10^11，上限是10^12
        Join[{0}, Table[10^11, 10]],
        Join[{2^(78 * 8)}, Table[10^12, 10]]
    ];
Solution = Solve[M.p == Y &&  p ∈ SolutionBounds, p, Integers]
Flag = First[p1 /. Solution]
Print[ByteArrayToString[ByteArray[IntegerDigits[Flag, 2^8]]]]
```
- 某些情况下可以用z3： https://nolliv22.com/writeups/lit%20ctf%202023/polypoint
99. [The Door to the Xord](https://demo.hedgedoc.org/s/aCKUEfByW)
- 获取MT19937连续的624个32-bit输出后，即可预测接下来的随机数。参考 https://www.schutzwerk.com/en/blog/attacking-a-rng/ ，工具： https://github.com/anneouyang/MT19937 。因为其state有19968 bit，624个32 bit就是624×32=19968
- mt19937是线性的，就算只能获取32-bit输出与一个固定未知值的异或结果，仍然也是线性的。只需要在z3里实现mt19937即可
- 如果不能获取32 bit输出而是其n倍bit，可以将n倍bit转为32 bit。因为其输出是倒着拼接的
```py
import random
random.seed(0)
print([hex(random.getrandbits(32)) for _ in range(8)])
random.seed(0)
print(hex(random.getrandbits(256)))
#['0xd82c07cd', '0x629f6fbe', '0xc2094cac', '0xe3e70682', '0x6baa9455', '0xa5d2f34', '0x42485e3a', '0xf728b4fa']
#0xf728b4fa42485e3a0a5d2f346baa9455e3e70682c2094cac629f6fbed82c07cd
```
100. [are YOU smarter than Joseph-Louis Lagrange????](https://github.com/programmeruser2/ctf-solutions/tree/main/litctf/2023/lagrange)
- 使用[wolfram](https://www.wolframalpha.com/)解方程+Lagrange Interpolation。当知道任意数量的点后，Lagrange Interpolation可用于给出满足所有输出点的一个函数方程
101. [E(Z/C)LCG](https://meashiri.github.io/ctf-writeups/posts/202308-litctf/#cryptoezclcg)
- 椭圆曲线（ecc）的参数恢复。Weierstrass形式的椭圆曲线方程为 $y^2=x^3+ax+b$ ，若已知曲线上任意两个点，就能恢复a和b。 https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/parameter_recovery.py
- 注意当g=ax，其中x是椭圆曲线上的点，a是常数的话，已知g，a求x要用离散对数（还是要根据定义来，这里的乘法不是常规意义上的乘法，是椭圆曲线自己定义的）
102. [All in One](https://meashiri.github.io/ctf-writeups/posts/202308-cybergonctf/#all-in-one)
- 维吉尼亚密码（Vigenere）decoder。这个decoder的字符集较广而且区分大小写，网上常见的decoder都解不出来
103. [CryptoGRAPHy 1](https://ctfnote.leg.bzh/pad/s/Z_QKPfErn)
- Graph Encryption Scheme(GES)。似乎和给定两点后图表内连接两点的最短路径有关系。属于对称加密，因为已知key后就能直接解密服务器提供的最短路径
104. [CryptoGRAPHy 2](https://ctfnote.leg.bzh/pad/s/dZNZbd-9e)
- 只要有足够的query次数和泄露的token，可以从加密后的最短路径构造出single-destination shortest path (SDSP) tree。具体操作为query每个（除destination本身）node到destination的最短路径，然后建立token到node的映射即可
105. [Noisy CRC](https://ctfnote.leg.bzh/pad/s/haum5HonP)
- CRC16的本质是在二进制多项式域(`GF(2)[x]`)上的除法。给定要求CRC的key p(x)和生成多项式q(x),CRC16算法会做一个多项式长除法，返回 $p(x)\*x^{16}$ 除以q(x)的余数。如果可以控制q(x)，就能在获取多个CRC值后利用CRT恢复p(x)
- 特别地，如果CRC值被混在其他随机值内，可以选择 $x^6$ 的倍数作为多项式。这样其余数一定也是 $x^6$ 的倍数，而随机值是倍数的可能性很小
- 另一个[wp](https://7rocky.github.io/en/ctf/other/sekai-ctf/noisy-crc/)用dfs来爆破正确的crc值组合
- 还有个[wp](https://imp.ress.me/blog/2023-08-28/sekaictf-2023#noisy-crc)利用composite moduli的性质。假设有多组 $f_i(x)=g(x)\*h_i(x)$ ，那么求 $res=s(x)\mod g(x)\*h_i(x)$ ，每组的res模g(x)的结果应该是一样的（要求g(x)不可约）
106. [cryptoGRAPHy 3](https://7rocky.github.io/en/ctf/other/sekai-ctf/cryptography-1-2-3/#cryptography-3)
- tree isomorphism, which defines a one-to-one relation between the nodes of two trees. python的etworkx模块提供了tree_isomorphism函数来找到同构
- 这篇wp里还有cryptoGRAPHy 1和2更详细的解释
107. [RandSubWare](https://imp.ress.me/blog/2023-08-28/sekaictf-2023#randsubware)
- 针对[代换-置换网络(Substitution–permutation network)](https://en.wikipedia.org/wiki/Substitution%E2%80%93permutation_network)的[差分攻击(differential attack)](https://ioactive.com/differential-cryptanalysis-for-dummies/)。差分攻击简述就是分析明文与密文之间的差距（差距的定义不同密码，不同，可以是异或的值，也可以是别的东西），然后爆破密钥，哪个密钥最符合之前得到的差距，哪个就可能是最可能的密钥。选择明文+爆破攻击
- 可用差分攻击的特征：
    - SPN密码轮数较少（例如5轮）。small number of rounds means that differences in ciphertext are poorly diffused
    - 对于好的SPN密码，明文中1 bit的更改应导致输出中一半的bit更改。如果这个值较低（如0.4），大概率有问题
- 出题人的自动化模块，利用z3: https://github.com/deut-erium/auto-cryptanalysis
108. [Diffecientwo](https://imp.ress.me/blog/2023-08-28/sekaictf-2023#diffecientwo)
- 利用z3找到[布隆过滤器(bloom filter)](https://zhuanlan.zhihu.com/p/43263751)的碰撞（collision）。布隆过滤器的实现一般会使用murmurhash3（`import mmh3`）
- https://www.josephkirwin.com/2018/04/07/z3-hash-inversions/ 。用这里面的代码硬找所要求hash的明文也是可以的，就是时间比较长。这篇里面还提到了一个z3使用tips： https://www.josephkirwin.com/2017/11/16/constraint-solver-tips/
- 注意脚本内使用了z3.LShR而不是单纯的`>>`。z3中的整数默认是有符号的，不这么做可能会得到unsat
109. [Lottery](https://meashiri.github.io/ctf-writeups/posts/202309-csaw/#lottery)
- 一个ticket可以从1-70中选6个不同的数字，开奖时越多数字匹配就能得到越多奖。多少个ticket才能保证一定盈利？利用fano planes构造特殊数字组即可。参考 https://www.youtube.com/watch?v=zYkmIxS4ksA 。解法不唯一
110. [Linear Aggressor](https://muuu.net/2023-09-18/)
- [linear regression model](https://en.wikipedia.org/wiki/Linear_regression)
111. [Blocky Noncense](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/crypto/blocky%20noncense)
- ECDSA中nonce的选取应该完全随机。如果使用了cubic congruential generator，会导致所有nonce之间都有一定的关系，可通过related nonce attack获取私钥（对于cubic congruential generator来说需要6个签名）。论文： https://eprint.iacr.org/2023/305.pdf
112. [Circles](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/crypto/circles)
- [Moser's Circles pattern](https://3blue1brown.substack.com/p/revisiting-mosers-circle-problem)。该序列以`1, 2, 4, 8, 16`开头，看起来像2的n次方，但后续则与2的n次方渐行渐远
113. [arc3](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/crp/arc3)
- RC4攻击。与[普通RC4](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E7%AC%94%E8%AE%B0/Tools/%E5%B7%A5%E5%85%B7%E8%84%9A%E6%9C%AC.md#rc4%E5%8A%A0%E5%AF%86%E8%84%9A%E6%9C%AC)不同的是，这里的RC4更像个RNG，S盒为打乱顺序的0-255数字序列，i和j均为随机一个索引，每次输出`S[(S[i] + S[j]) % 256]`。明文的前1000个字节已知，尝试爆破200000轮运行后的RC4的输出序列
114. [random](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/crp/random)
- 64位机器上的C#默认使用`xoshiro256**`作为其PRNG。此题提供了在获取i到i+2000(共2000个输出)个`rng.Next(256)`后如何获取第i-1个`rng.Next(256)`的输出
115. [SSS](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/crp/sss)
- 利用largrange polynomial计算多项式在某一点上的值
- [Fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform)（FFT）以及inverse FFT. FFT is equivalent to evaluating the polynomial at every power of the root of unity used; the inverse FFT (normal FFT using an inverted root of unity) is equivalent to interpolating the polynomial
- Bluestein's algorithm
- 为了理解这题去看了傅里叶分析的介绍： https://zhuanlan.zhihu.com/p/19763358 ，还是啥也不懂
116. [Electronical](https://github.com/D13David/ctf-writeups/tree/main/buckeyectf23/crypto/electronical)
- aes ecb padding oracle attack. 特征是有oracle接收任意输入，拼接上flag后返回整体的加密结果。其他可用脚本： https://gist.github.com/C0nstellati0n/cf6ae2c5e0e9fe1ecb532d257a56e101
117. [Real Smooth](https://github.com/nass15456/CTFs/blob/main/BuckeyeCTF/Real%20Smooth.md)
- chacha20 key/nonce reuse+明文攻击。chacha20的算法比较复杂，但是可以简易地理解成“对于明文中的每个字节，生成一个对应的密钥字节与其异或”。不同的key/nonce组合会生成不同的密钥字节（与key不同），因此重用一对key/nonce就成了many time pad。假如已知一对明文和密文，就能异或两者得到完整的密钥字节，进而解码其余密文
118. [coding](https://github.com/cscosu/buckeyectf-2023-public/tree/master/crypto-coding)
- [arithmetic coding](https://www.nayuki.io/page/reference-arithmetic-coding)
119. [Jack’s Worst Trials](https://berliangabriel.github.io/post/tcp1p-ctf-2023/)
- 当python网站使用`jwt.decode()`而没有指定具体使用的算法时，代表可能可以用公钥伪造JWT，然后用HS256算法验证。参考CVE-2017-11424，enables symmetric/asymmetric key confusion attacks against users using the PKCS1 PEM encoded public keys。利用工具 https://github.com/silentsignal/rsa_sign2n 可从两个jwt中计算公钥，然后伪造jwt
120. [Final Consensus](https://berliangabriel.github.io/post/tcp1p-ctf-2023/)
- Meet in the Middle attack(MITM),常用于double encryption scheme：
```
c1=encrypt(k1,plaintext)
c2=encrypt(k2,c1)
```
如果直接爆破k1和k2，时间复杂度为key space of k1\*key space of k2。但是可以把两者拆开，分别计算encrypt(k1,plaintext)和decrypt(k2,c2)。若两者结果匹配，我们就找到了(k1,k2)，时间复杂度要少上不少
121. [Strong Primes](https://blog.bithole.dev/blogposts/ctf-writeups/udctf-strong-primes/)
- python Crypto.Util里的getStrongPrime函数所生成的质数保证p-1里有一个因子是较大的质数。这并不意味着完全安全，因为那个较大的质数减去1仍然可能有很多很小的因子。故基于strongPrime的Diffie–Hellman协议仍然有机率可以使用Pohlig–Hellman算法求得离散对数
122. [Keyshare](https://github.com/eylau-ucsd/ctf-sols/tree/main/LakeCTF/KeyShare)
- ECC invalid curve attack。题目的oracle允许用户输入任意公钥（一个点的x和y坐标），并返回私钥（一个数）乘上公钥的结果。若oracle没有检查用户输入的点是否在程序自己定义的曲线上，即可使用invalid curve attack。攻击者可通过修改服务器上曲线的参数B来生成自己的曲线A，使离散对数在曲线A上的计算更加容易。曲线A的阶可以被分解成若干个小质数，在阶为小质数上的曲线计算离散对数要容易许多。获取多个小质数曲线的离散对数结果后可用CRT恢复原本大曲线上的离散对数。注意这些小质数的乘积要大于原本的大质数，若小于则有多个解，在可接受范围内一个一个试即可。对于这题,`b = 5432486176130386246309866246117127606417222221223493595694`非常光滑，只用一个就能恢复密钥
- 获取私钥k后，根据kP计算P只需乘上k在曲线上的逆元即可
123. [shuffled-aes](https://github.com/LosFuzzys/GlacierCTF2023_writeups/tree/main/crypto/shuffled-aes)
- 如果先执行10轮的SubBytes, AddRoundKey再执行10轮的ShiftRows, MixColumns, AddRoundKey，AES就不再安全了。因为后10轮的操作完全线性可逆，前10轮的操作可以通过请求多组明文密文对搭建对照表格
124. 当使用AES-CTR时，不要用同样的key-nonce pair加密多个明文。见 https://cedricvanrompay.gitlab.io/cryptopals/challenges/19-and-20.html 。因为CTR模式是用明文异或nonce的AES密文得到结果，如果多个明文用同一个nonce，结果就等于many time pad了。此时任意两个密文相异或等同于对应的两个明文异或；如果能猜测到其中一个明文，便能解码另一个明文
125. [MSS](https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/crypto/%5BEasy%5D%20MSS)
- [Mignotte Secret Sharing](https://en.wikipedia.org/wiki/Secret_sharing_using_the_Chinese_remainder_theorem#Mignotte_threshold_secret_sharing_scheme)。一种利用CRT的秘密共享方式
126. [Knapsack](https://meashiri.github.io/ctf-writeups/posts/202312-backdoorctf/#knapsack)
- 当density of the matrix太高时，LLL无法解决这类knapsack问题。不过要是本身供选择的数字集合中的数字较少，可以考虑使用MITM攻击。除了subset sum，subset product也可以用MITM攻击，原理差不多，见subset product题型的[wp](https://tsumiiiiiiii.github.io/fh_crypto/#primes-festival)。设ans为要求的subset sum，将数字集合分为两半，在前一半尝试所有组合的可能性，并用一个字典记录值（记做s1，为key）和对应所使用的数字（为value）。然后尝试后一半所有组合的可能性，记为s2。计算ans-s2，若该键在字典里存在，即找到了目标
- 其他方法：若density只是稍微高了一点，可以随机选择几个数字，将其替换为subset sum里绝对不可能出现的数字。此时矩阵density下降，就能直接使用LLL了；或者爆破几个数字，拿剩下的数字构造density较小的矩阵。或者换种方式用LLL，再或者用BKZ方法: https://gist.github.com/C0nstellati0n/cf6ae2c5e0e9fe1ecb532d257a56e101#knapsack
    - 有“BKZ可以解出某些LLL解不出来的题”的说法。以下是aparker314159的解释：BKZ is better at finding the shortest vectors than LLL, but it takes longer to run. You can change the BKZ block size parameter to adjust the tradeoff (higher block size means slower but more likely to find shortest vector; LLL is BKZ with block size 2)
    - https://connor-mccartney.github.io/cryptography/other/BackdoorCTF-2023-writeups#knapsack :硬要使用LLL在特殊情况下也是可以的（这篇wp继续加深我对格和LLL的理解）
127. [Drunk](https://meashiri.github.io/ctf-writeups/posts/202312-backdoorctf/#drunk)
- [Fernet](https://zweilosec.gitbook.io/hackers-rest/os-agnostic/cryptography-and-encryption#fernet)对称加密密码。其key和cipher均与base64相似
128. [Curvy_Curves](https://connor-mccartney.github.io/cryptography/other/BackdoorCTF-2023-writeups#curvy_curves)
- William's p+1 factorisation
- 题目文件在[这里](https://tsumiiiiiiii.github.io/bdoorctf/#curvy-curves)可以找到。感觉像ECC上的RSA，同样是分解n后求逆元
129. [Accessible Sesamum Indicum](https://pshegger.github.io/posts/irisctf-2024/#accessible-sesamum-indicum)
- de Bruijn sequence([德布鲁因序列](https://halfrost.com/go_s2_de_bruijn/))。该序列满足任何其期望长度的substring都不会重复（例如期望长度为4，该字符串内任意一个长度为4的substring都不会重复。不同期望长度的德布鲁因序列的构造不同）。可用pwntools的cyclic_gen获取序列
130. [Integral Communication](https://nightxade.github.io/ctf-writeups/writeups/2024/Iris-CTF-2024/crypto/integral-communication.html)
- AES CBC翻转字节攻击。修改第i个块的解密结果后，第i-1块会解密出乱码。基本这种方式只能改一块，因为上一块的解密结果未知。除非以某种方式得知了修改当前块后上一块的解密结果（如题目特殊的oracle）。如修改第二块会影响第一块的解密结果，这时如果也想修改第一块，就要获取其被影响后的解密结果，然后改IV
- 更详细的解析wp： https://amateurs.team/writeups/IrisCTF-2024/integral-communication
131. [manykey](https://connor-mccartney.github.io/cryptography/ecc/manykey-IrisCTF-2024)
- ECDSA私钥伪造。给出一条明文及其签名和对应的公钥，构造一个可通过验证的私钥。验签公式如下： $(\frac{h}{s}\*G+\frac{r}{s}\*Q).x\equiv r\mod n$ 。r和s是签名的一部分，h是要验证的消息hash，G是选择的curve generator，Q是私钥指数d乘上G的结果。补充链接： https://toadstyle.org/cryptopals/61.txt
132. [Burrows–Wheeler Transform](https://www.dcode.fr/burrows-wheeler-transform):密文长得很像栅栏
133. [Music Sheet Cipher](https://www.dcode.fr/music-sheet-cipher):密文类似五线谱里的音符
134. [export-grade-cipher](https://github.com/UofTCTF/uoftctf-2024-chals-public/tree/master/Cryptography/export-grade-cipher)
- wp参考 https://kanzya.github.io/posts/UofTCTF/ 和 https://hackmd.io/@Wrth/UofTCTF-2024-EGC 。据出题人所说，此题为 https://web.archive.org/web/20000302000206/http://www.dvd-copy.com/news/cryptanalysis_of_contents_scrambling_system.htm 里提到的一种经典攻击，专门针对数据打乱类型的密码（Contents Scrambling System）
135. [What Next II](https://github.com/rhaeyx/ctf/tree/main/mapnactf/what-next-2)
- [randcrack](https://github.com/tna0y/Python-random-module-cracker)通过输入32bit的随机数来预测MT19937。如果获取的是256bit的数字(`getrandbits(256)`)，可以用[Extend MT19937 Predictor](https://github.com/NonupleBroken/ExtendMT19937Predictor)直接预测，无需手动将其分解为多个32bit随机数
- 这篇[wp](https://nolliv22.com/writeups/mapna%20ctf%202023/what-next-2)使用randcrack
136. [adapt](https://mystiz.hk/posts/2024/2024-02-03-tetctf-adapt/)
- immutable AVL tree：[cosmos/iavl](https://github.com/cosmos/iavl) （v0.19.7）下的proof伪造。可通过构造特殊node获取一个假的proof，用于证明某个特定的node在tree中不存在（但实际存在）
137. [winter](https://7rocky.github.io/en/ctf/other/dicectf/winter/)
- Winternitz One-Time Signature (WOTS)签名伪造。这是一个单次签名算法，一个私钥只能签名一条信息。若同时签两条，攻击者可以通过第一条消息的签名伪造第二条消息的签名。只需构造一个字符串，使该字符串的sha256输出的每一个字节都大于等于第一条消息的sha256输出的相应字节即可。相似考点在59条winterfactory时就已见过，实际做题时也想到了这个做法，但是没找到符合要求的两条消息……wp作者的做法更聪明，与其随机生成两条消息并比对它们的hash，不如设定一个阈值，让第一条消息的hash值的每个字节都大于这个阈值，而第二条消息的hash值的每个字节都小于这个阈值。或者使用c++爆破hash脚本： https://gist.github.com/C0nstellati0n/cf6ae2c5e0e9fe1ecb532d257a56e101#winter
- 其他wp： https://sylvainpelissier.gitlab.io/posts/2024-02-04-dicectf-winter/ 。利用已知的bitcoin hash加快爆破。这类有特殊性质的hash还可以在 https://beneri.se/hashgame/ 找到
138. [RSA-GCD](https://nolliv22.com/writeups/0xl4ugh%20ctf%202024/rsagcd)
- [modular binomial](https://www.ctfrecipes.com/cryptography/general-knowledge/maths/modular-arithmetic/modular-binomial)的运用
134. [Combinatorial Conundrum](https://github.com/Pamdi8888/My_CTF_Chals/tree/main/Combinatorial%20Conundrum)
- 假如要求满足`sum(x1+...+xN) = R`解的数量，其中0<=x<=R，公式为(N+R-1) 选 (R)；若Li<=x<=R，则：”subtract Li from each limit and also subtract sum(Li) from R, then apply the same formula“
- dp解法： https://writeup.gldanoob.dev/bitsctf/
135. [selamat pagi](https://sheeptester.github.io/longer-tweets/lactf/#cryptoselamat-pagi)
- 针对印度尼西亚语（Indonesian）的字母替换密码的分析及破解。可用工具： https://www.dcode.fr/monoalphabetic-substitution 。其他wp： https://docs.google.com/document/d/19YJiUPCGInwjKSYJaAApLTyc43-Ck_P11GqYTdXIQRI
- 利用wordlist的工具： https://github.com/JorianWoltjer/SubSolver
136. [prove it!](https://tsumiiiiiiii.github.io/lacrypto/)
- zero-knowledge proof:zk-snarks。不过这题其实和零知识证明没啥关系，主要还是利用离散对数和多项式解出目标