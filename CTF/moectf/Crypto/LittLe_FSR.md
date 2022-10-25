# LittLe_FSR

脚本小子的噩梦到来了：没有现成答案。

看到一篇[文章](https://www.anquanke.com/post/id/184828)，想看看这道题能不能用同样的方法，正好缺个笔记本。

```python
from Crypto.Util.number import *
from gmpy2 import *
from secret import FLAG, key
import string
import random

assert FLAG[:7] == b'moectf{'
assert FLAG[-1:]== b'}'
table = string.ascii_letters+string.digits+string.punctuation
for _ in range(50-len(FLAG)):
    FLAG += random.choice(table).encode()
assert len(FLAG) == 50
assert len(key) == 5

class LFSR:
    def __init__(self):
        self.data = list(map(int,list(bin(bytes_to_long(FLAG))[2:].rjust(400,'0'))))
        for _ in range(2022):
            self.cycle()

    def cycle(self):
        bit = self.data[0]
        new = 0
        for i in key:
            new ^= self.data[i]
        self.data = self.data[1:] + [new]
        return bit

ILOVEMOECTF = LFSR()
for _ in range(2022):
    print(ILOVEMOECTF.cycle(), end='')
```

目前已知的信息：FLAG正常格式，长度50，key长度为5，每一位可能是0-9。FLAG在加密前被转为了2进制，且右边用0填充至400的长度。没别的了，cycle函数应该对应lfsr中的反馈函数。每次cycle都会输出第0位的bit，整体最后再拼接new，new等于data在未知的key位进行异或的结果。但是new只有可能是0或1，因为在给的附件中并没有发现其他数字的身影且data只有0和1。

然后就没思路了。做了个实验，发现最后那个for循环输出的内容前400个和第一次加密内容一致。

```python
from Crypto.Util.number import *
import string
import random
table = string.ascii_letters+string.digits+string.punctuation
FLAG=b'moectf{'
for _ in range(49-len(FLAG)):
    FLAG += random.choice(table).encode()
FLAG+=b'}'
key=b'38298'
class LFSR:
    def __init__(self):
        self.data = list(map(int,list(bin(bytes_to_long(FLAG))[2:].rjust(400,'0'))))
        print(''.join([str(i) for i in self.data]))
        for _ in range(2022):
            self.cycle()
    def cycle(self):
        bit = self.data[0]
        new = 0
        for i in key:
            print(i)
            new ^= self.data[i]
        self.data = self.data[1:] + [new]
        return bit
ILOVEMOECTF = LFSR()
print(''.join([str(i) for i in ILOVEMOECTF.data]))
times=1
for _ in range(2022):
    times+=1
    print(ILOVEMOECTF.cycle(), end='')
    if times>400:
        print()
        times=1
```

这题只知道一次加密的输出肯定是得不到什么东西的，不然循环这么多次就没意义了。这题第一个棘手的地方在于不知道key。另外通过实验打印出i的值，发现key不一定是数字，因为byte截取出来的内容会被转成ascii值。还不止，我发现这个i的值竟然不是固定的，总是会诡异地多出个0或1。这下彻底不会了。

我！做！出！来！了！用了整整1个多星期，中途脚本写错了卡了好几天，都想放弃了。这题不需要上面提到的那篇文章的办法，要[这里](https://www.ruanx.net/babylfsr/)的。这题关于lfsr的实现看似有些不一样，实际上效果完全和下面的脚本一样。

```python
class lfsr():
    def __init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output
```

其中mask是key，length是400。有一点不一样的是，这个lfsr的实现是直接吐出加密后的bit，给的lfsr的实现是先吐出init的bit。问题不大，慢了一个周期而已。现在就是要找出key，然后倒推过程（太痛苦了我倒推的时候看错了一个东西怎么搞都不对）。求key还挺简单的，把 lfsr 的状态一行一行地写在矩阵上，形成的矩阵记为M. 把 lsfr 每次所生成的结果也拼成一个向量，记为 T。把掩码向量记为v，那么得到下一个bit的过程等同于M点乘v，M*v=T。想要找v还不简单，$v=T*M^{-1}$。唯一的条件是矩阵要是方矩阵，也就是n*n，因为状态向量有400位，对应的mask也要400位，想确定mask全部的400位就要400个方程。400个方程对应400个值，故想靠这种方法找到mask至少要800位。

题目给了我们2022位啊，这不是绰绰有余？结果当我们兴冲冲地输入脚本时，报错了！为什么？查看报错信息，“矩阵秩不足”。当时我愣了一下，想到是不是不能选前800位？我又选了800-1600位，好家伙还是不足。经测试，矩阵的秩无论选哪800位，都卡在了390这个数字上。题有问题？怎么可能呢，当时已经有解出的人了，只能是我有问题。回忆之前学习的关于线性代数的内容，秩是什么？

- 矩阵的秩（rank）等于矩阵的行简化阶梯形的主列的数量。

虽然我不清楚行简化阶梯形是什么，但我依稀记得主列简单来看就是一列除了一个是1其他都是0的列。单位矩阵就是标准例子。那矩阵就是缺了10个主列呗，这么少我直接爆破不就行了？反正主列非常好构造。T向量对应那一行的值也爆破，只有0和1两种可能，不难。改编一下大佬的sagemath脚本。

```python
import itertools
def test(padding):
    s = [int(x) for x in '0001010100110101100111100111000001010000011111100101110001100010011111110001011101110001101011101001010001100010100101011011101100100100111100100001100101101010100010011001010011001100111000101011100010101011101101101110111100111101001010010011101111110011100011010010001000100000001110010001011110011001101110011110111110110111000011011000010001110101011110011110101001101111101000110001101001110100000001100100110010010110111001011000000101010011111010100001001100010111111110001001001001010111101110001101000101110110011100101101110010000000100010100100001001101010101100001011101000101111010010111001100010100000000000001110010011111100010011010000110000111111000001111111001011101011101111011110010010000110100001110011110111001110100111101001011110110110101110001100111110100011011110']
    test=[0]*400
    index=390
    M = matrix(GF(2), 400, 400)
    T = vector(GF(2), 400)

    for i in range(390):
        M[i] = s[i : i + 400]
        T[i] = s[i+400]
    for i in range(400):
        last_rank=M.rank()
        test[i]=1
        M[index]=test
        if M.rank()>last_rank:
            T[index]=padding[index-390]
            index+=1
            if M.rank()==400:
                break
        test[i]=0
    try:
        mask = M.inverse() * T
        mask=''.join(map(str, (mask)))
        if mask.count('1')==5:
            print(mask)
    except:
        return
for x in itertools.product([0, 1], repeat = 10):
    test(list(x))
```

key的长度为5，由此得出mask中1的数量也是5,可以用这个条件筛选mask。（写的时候跑了一下，不知道为什么很慢，当时做的时候是很快的，还有可能跑出不出来。奇了怪了，多跑几次就变快直接出答案了。）得到mask为：

```python
mask=0b0000000010000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000
```

接下来要倒推回去。我是从这篇[文章](https://www.anquanke.com/post/id/181811)得到灵感的，同时也误导了我。能发现这篇文章里提到的lfsr也跟上面那个一样，那破解办法可以一起用。事实证明我想得太简单了，这题mask第一个1的位置出现在第9位，意味着我们要从第9位开始爆破。这是不是意味着时间变长了？一次爆破9位的时间比一次爆破1位的时间差了可不是一点半点。实际上我们完全可以用一次爆破1位的方法，前8为都填0，第9位爆破，因为前8位在当前状态下完全不重要，不会影响下一个bit的输出。大家看之前给的几篇文章应该就能懂了，我总结了一下：mask从第n位开始是1就从第n位开始爆破，n位之前全填0。

过程理解了步骤就很好写了，除了索引有点烦。

```python
from Crypto.Util.number import long_to_bytes
with open("attachment.txt") as f:
    _init=f.read()[:400]
mask=0b0000000010000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000
class lfsr():
    def __init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output
temp=[]
index=0
def check(plaintext,expected):
    global mask
    t=lfsr(int(plaintext,2),mask,400)
    return str(t.next())==expected

for i in range(2000):
    index+=1
    if index<393:
        answer=_init[-(index+8)]
        plaintext='0'*9+''.join(temp)+_init[:-(index+8)]
    else:
        answer=temp[-(index-392)]
        plaintext='0'*9+''.join(temp[:-(index-392)])
    if check(plaintext,answer):
        temp=['0']+temp
    else:
        temp=['1']+temp
    if index==400:
        index=0
        _init=''.join(temp)
        temp.clear()
for i in range(22):
    answer=_init[-(index+8)]
    plaintext='0'*9+''.join(temp)+_init[:-(index+8)]
    if check(plaintext,answer):
        temp=['0']+temp
    else:
        temp=['1']+temp
flag=''.join(temp)+_init[:-22]
print(long_to_bytes(int(flag,2)))
```

两个脚本都写的很垃圾，请不要在意。每次plaintext的构造都是8位无用填充0+爆破bit（这里也填0就把它和填充位放一起了）+已爆破出来的bits+当前初始状态前几个bits。已爆破出来的bits+当前初始状态前几个bits永远等于311。当index为393时，现在的初始状态已经到底了，就从temp开始取bit。2022不是400的倍数，那就先2000，再22，flag是temp的全部bit共22位+初始状态的400-22个bit（我不会告诉你我连400-22都懒得算）。脚本结果的前几个字母不见了，不是问题，flag前缀我们早就知道了。

- ### Flag
  > moectf{Bru!e_@r_so1^e_A_sy3teM_0f_eq&aT10n3?}