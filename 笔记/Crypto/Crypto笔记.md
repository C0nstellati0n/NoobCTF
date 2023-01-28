# Crypto笔记

## RSA
- 得到d和c，p和q为相邻质数。例题：[[NCTF2019]babyRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BNCTF2019%5DbabyRSA.md)
- 光滑数分解+威尔逊定理使用。例题1：[smooth](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/smooth.md)，例题2:[[RoarCTF2019]babyRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BRoarCTF2019%5DbabyRSA.md)
- 共模攻击。适用于相同明文用同样的n却用不同的e加密时。注意两个不同的e需要互质。[例题1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Crypto/best_rsa.md)搭配使用Crypto库读取公钥，[例题2](https://blog.csdn.net/weixin_44017838/article/details/104886290)搭配解密结果是ascii的情况。例题2脚本：

```python
from gmpy2 import invert
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
n=6266565720726907265997241358331585417095726146341989755538017122981360742813498401533594757088796536341941659691259323065631249
e1=773
e2=839
c1=3453520592723443935451151545245025864232388871721682326408915024349804062041976702364728660682912396903968193981131553111537349
c2=5672818026816293344070119332536629619457163570036305296869053532293105379690793386019065754465292867769521736414170803238309535
_,s1,s2=egcd(e1,e2)
if s1<0:
	s1 = -s1
	c1 = invert(c1, n)
elif s2<0:
	s2 = -s2
	c2 = invert(c2, n)
m = str(pow(c1,s1,n)*pow(c2,s2,n) % n)
i=0
while i<len(m):
  if m[i]=='1':
    print(chr(int(m[i:i+3])),end='')
    i+=3
  else:
    print(chr(int(m[i:i+2])),end='')
    i+=2
```

为了整体好用，给出函数版本：

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
n=785095419718268286866508214304816985447077293766819398728046411166917810820484759314291028976498223661229395009474063173705162627037610993539617751905443039278227583504604808251931083818909467613277587874545761074364427549966555519371913859875313577282243053150056274667798049694695703660313532933165449312949725581708965417273055582216295994587600975970124811496270080896977076946000102701030260990598181466447208054713391526313700681341093922240317428173599031624125155188216489476825606191521182034969120343287691181300399683515414809262700457525876691808180257730351707673660380698973884642306898810000633684878715402823143549139850732982897459698089649561190746850698130299458080255582312696873149210028240898137822888492559957665067936573356367589784593119016624072433872744537432005911668494455733330689385141214653091888017782049043434862620306783436169856564175929871100669913438980899219579329897753233450934770193915434791427728636586218049874617231705308003720066269312729135764175698611068808404054125581540114956463603240222497919384691718744014002554201602395969312999994159599536026359879060218056496345745457493919771337601177449899066579857630036350871090452649830775029695488575574985078428560054253180863725364147
with open("HUB1",'r') as f:
    c1=f.read().split('\n')[3:]
with open("HUB2",'r') as f:
    c2=f.read().split('\n')[3:]
with open("result.txt",'w') as f:
    for i,j in enumerate(c1):
        f.write(decrypt(1697,599,n,int(j),int(c2[i])).decode())
```

- lcm问题+e与toitent不互质（gcd较小）。例题：[[NPUCTF2020]EzRSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BNPUCTF2020%5DEzRSA.md)
- dp泄露。例题：[0rsa0](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/0rsa0.md)
- sagemath解二元方程组+e，d泄露后分解n。例题:[[MRCTF2020]Easy_RSA](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BMRCTF2020%5DEasy_RSA.md)
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
- e和phi不互素+中国剩余定理解决多组c和n问题。例题1:[Weird_E_Revenge](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/Weird_E_Revenge.md)。例题2:[[De1CTF2019]babyrsa](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Crypto/%5BDe1CTF2019%5Dbabyrsa.md)
- 低解密指数攻击（wiener attack）。例题:[[羊城杯 2020]RRRRRRRSA](../../CTF/BUUCTF/Crypto/[羊城杯%202020]RRRRRRRSA.md)
- 多项式下的RSA(PolynomialRing)。例题:[[watevrCTF 2019]Swedish RSA](../../CTF/BUUCTF/Crypto/[watevrCTF%202019]Swedish%20RSA.md)
- e与phi不互质且gcd很大，使用AMM开根法+CRT。例题:[[NCTF2019]easyRSA](https://blog.soreatu.com/posts/intended-solution-to-crypto-problems-in-nctf-2019/#easyrsa909pt-2solvers)
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

1. Crypto库根据已有信息构建私钥并解密

如果给出的是flag.enc和public.key这种形式的题目，平时的方法可能会解出乱码，需要利用私钥文件来解密。

```python
from Crypto.PublicKey import RSA
import gmpy2
import base64
from Crypto.Util.number import *
from Crypto.Cipher import PKCS1_OAEP
n=79832181757332818552764610761349592984614744432279135328398999801627880283610900361281249973175805069916210179560506497075132524902086881120372213626641879468491936860976686933630869673826972619938321951599146744807653301076026577949579618331502776303983485566046485431039541708467141408260220098592761245010678592347501894176269580510459729633673468068467144199744563731826362102608811033400887813754780282628099443490170016087838606998017490456601315802448567772411623826281747245660954245413781519794295336197555688543537992197142258053220453757666537840276416475602759374950715283890232230741542737319569819793988431443
e=65537
p=3133337
q=25478326064937419292200172136399497719081842914528228316455906211693118321971399936004729134841162974144246271486439695786036588117424611881955950996219646807378822278285638261582099108339438949573034101215141156156408742843820048066830863814362379885720395082318462850002901605689761876319151147352730090957556940842144299887394678743607766937828094478336401159449035878306853716216548374273462386508307367713112073004011383418967894930554067582453248981022011922883374442736848045920676341361871231787163441467533076890081721882179369168787287724769642665399992556052144845878600126283968890273067575342061776244939
phi=(p-1)*(q-1)
d=gmpy2.invert(e,phi)
text='GVd1d3viIXFfcHapEYuo5fAvIiUS83adrtMW/MgPwxVBSl46joFCQ1plcnlDGfL19K/3PvChV6n5QGohzfVyz2Z5GdTlaknxvHDUGf5HCukokyPwK/1EYU7NzrhGE7J5jPdi0Aj7xi/Odxy0hGMgpaBLd/nL3N8O6i9pc4Gg3O8soOlciBG/6/xdfN3SzSStMYIN8nfZZMSq3xDDvz4YB7TcTBh4ik4wYhuC77gmT+HWOv5gLTNQ3EkZs5N3EAopy11zHNYU80yv1jtFGcluNPyXYttU5qU33jcp0Wuznac+t+AZHeSQy5vk8DyWorSGMiS+J4KNqSVlDs12EqXEqqJ0uA=='
c_bytes = base64.b64decode(text)
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
4. 离散对数问题。一般的对数 $a^b=c$ ，求得b可以直接用 $log_a(c)$ 。但是在加上模运算的情况下就要使用离散对数了。 $a^b=c\mod d$ ，使用sympy的离散对数函数。

```python
""" #!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Util.number import *
import random

n = 2 ** 512
m = random.randint(2, n-1) | 1
c = pow(m, bytes_to_long(flag), n)
print 'm = ' + str(m)
print 'c = ' + str(c)

# m = 391190709124527428959489662565274039318305952172936859403855079581402770986890308469084735451207885386318986881041563704825943945069343345307381099559075
# c = 6665851394203214245856789450723658632520816791621796775909766895233000234023642878786025644953797995373211308485605397024123180085924117610802485972584499 """
m = 391190709124527428959489662565274039318305952172936859403855079581402770986890308469084735451207885386318986881041563704825943945069343345307381099559075
c = 6665851394203214245856789450723658632520816791621796775909766895233000234023642878786025644953797995373211308485605397024123180085924117610802485972584499
n=2**512
from Crypto.Util.number import *
import sympy
x=sympy.discrete_log(n,c,m)  #参数顺序：sympy.discrete_log(模数，结果，底数)
print(long_to_bytes(x))
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

12. Many Time pad攻击（利用空格异或其他字符会转大小写的特性）。例题:[不止一次](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Crypto/%E4%B8%8D%E6%AD%A2%E4%B8%80%E6%AC%A1.md)。
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
    b'49380d773440222d1b421b3060380c3f403c3844791b202651306721135b6229294a3c3222357e766b2f15561b35305e3c3b670e49382c295c6c170553577d3a2b791470406318315d753f03637f2b614a4f2e1c4f21027e227a4122757b446037786a7b0e37635024246d60136f7802543e4d36265c3e035a725c6322700d626b345d1d6464283a016f35714d434124281b607d315f66212d671428026a4f4f79657e34153f3467097e4e135f187a21767f02125b375563517a3742597b6c394e78742c4a725069606576777c314429264f6e330d7530453f22537f5e3034560d22146831456b1b72725f30676d0d5c71617d48753e26667e2f7a334c731c22630a242c7140457a42324629064441036c7e646208630e745531436b7c51743a36674c4f352a5575407b767a5c747176016c0676386e403a2b42356a727a04662b4446375f36265f3f124b724c6e346544706277641025063420016629225b43432428036f29341a2338627c47650b264c477c653a67043e6766152a485c7f33617264780656537e5468143f305f4537722352303c3d4379043d69797e6f3922527b24536e310d653d4c33696c635474637d0326516f745e610d773340306621105a7361654e3e392970687c2e335f3015677d4b3a724a4659767c2f5b7c16055a126820306c14315d6b59224a27311f747f336f4d5974321a22507b22705a226c6d446a37375761423a2b5c29247163046d7e47032244377508300751727126326f117f7a38670c2b23203d4f27046a5c5e1532601126292f577776606f0c6d0126474b2a73737a41316362146e581d7c1228717664091c')
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
c=open('/Users/constellation/Desktop/encrypted_message','r').read()
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

22. lfsr爆破mask。例题:[LittLe_FSR](../../CTF/moectf/Crypto/LittLe_FSR.md)
23. [Schmidt-Samoa 密码体系](https://www.ruanx.net/schmidt-samoa/)。