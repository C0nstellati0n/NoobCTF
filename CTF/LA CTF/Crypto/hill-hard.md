# hill-hard

[题目](https://github.com/uclaacm/lactf-archive/tree/main/2023/crypto/hill-hard)

详细[wp](https://hackmd.io/@lamchcl/r1zQkbvpj#cryptohill-hard)甩我脸上我都看不懂。于是我自己再抄一遍，但愿抄的过程中能懂吧。

```python
#!/usr/local/bin/python3

import numpy as np

def det(M):
    # stolen from https://stackoverflow.com/a/66192895
    M = [[int(x) for x in row] for row in M] # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0: # swap with another row having nonzero i's elem
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return 0 # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
        prev = M[i][i]
    return sign * M[-1][-1]

n = 20
A = np.random.randint(0, 95, [n, n])
while np.gcd(det(A), 95) != 1:
    # ensures invertibility
    A = np.random.randint(0, 95, [n, n])

def stov(s):
    return np.array([ord(c)-32 for c in s])

def vtos(v):
    return ''.join([chr(v[i]+32) for i in range(n)])

def encrypt(s):
    return vtos(np.matmul(A, stov(s))%95)

fakeflag = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(13)]) + "}"
fakeflag2 = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(13)]) + "}"
assert(len(fakeflag) == n)
assert(len(fakeflag2) == n)
f = encrypt(fakeflag)
f2 = encrypt(fakeflag2)

def xorencrypt(s):
    v1 = stov(s)
    v2 = stov(fakeflag)
    v = np.bitwise_xor(v1, v2)
    return encrypt(vtos(v))

def giveflag():
    flag = open("flag.txt", "r").readline().strip()
    print("\nYour vision fades to black, and arcane symbols begin to swarm your mind. To others, it might seem like magic, but you can see what others cannot.")
    print(flag)
    exit(0)

def oracle(guess):
    print(xorencrypt(guess))

def trydecode():
    guess = input("\nEnter your guess: ")
    if len(guess) != 20:
        return 1
    for c in guess:
        if ord(c) < 32 or ord(c) >= 127:
            return 2
        if c == ' ':
            return 3
    
    oracle(guess)
    return 0

def guess(num):
    while (err := trydecode()) != 0:
        if err == 1:
            print("Your guess must be exactly 20 characters.")
        elif err == 2:
            print("Your guess must use only ASCII characters")
        elif err == 3:
            print("Sorry, spaces aren't allowed anymore.")
    
    print("You have", 13-num, "attempts left")

print("On the hill lies a stone. It reads:")
print(f)
print("\nA mysterious figure offers you 14 uses of an oracle:")
for i in range(14):
    guess(i)

print("\nThe figure vanishes, leaving only a vague message. Encrypt me:")
print(fakeflag2)
guess = input("\nEnter your guess: ")
if guess == f2:
    giveflag()
else:
    print("Nope.")
```

题目在[希尔密码](https://hstar.me/2020/08/hill-cipher-study/)的加密基础上增加了异或操作。开头会给出fakeflag的密文，然后我们可以在限制下与服务器交互14次，服务器会返回每次输入的密文。最后，如果我们能输入fakeflag2的正确密文，就能获得flag。题目的加密操作模了个95，那下面提到的运算都是基于模95的，除非特别指出。

让A为加密的矩阵，即密钥矩阵。因为flag格式已知，所以把里面的内容和格式分开比较方便。定义 $\vec{b}$ 为flag格式向量，里面的内容全为0。即`stov("lactf{"+" "*13+"}")`(根据stov函数的实现，空格的ord值转换为矩阵数字就是0)。然后让 $\vec{1}$ 为flag内容向量，即flag前6个字符和最后一个字符（flag格式）处为0，剩下的是1，正好和 $\vec{b}$ 相反。定义 $\vec{f}$ ，让 $\vec{f}$ 满足 $\vec{b}+\vec{f}$ 等于fakeflag的向量(`stov(fakeflag)`)。相应的，定义 $\vec{f_2}$ 满足 $\vec{b}+\vec{f_2}$ 等于fakeflag2的向量。

两个fakeflag都满足flag格式，因此 $\vec{f}$ 和 $\vec{f_2}$ 的前6个字符以及最后一个字符处都是0。另外一个值得注意的地方是，两个fakeflag的内容都为小写字母，因此 $\vec{f}$ 和 $\vec{f_2}$ 的非0项在[65,90]中（包含）。

原本的希尔密码加密是符合线性的。但这里的加密多了个异或操作。假如我们的输入是 $\vec{i}$ ，加密过程为 $(\vec{b}+\vec{f})\oplus\vec{i}$ 。在不知道fakeflag的值的情况下，异或破坏了原本的线性。有没有什么办法能移除异或？答案是有，还记得之前提到“ $\vec{f}$ 的非0项在[65,90]中”吗？65-90的二进制只有最后5位不同，假如我们小心地选输入的明文，是可以保留线性的。

让f为 $\vec{f}$ 的非0项。如果我们将f与32的倍数异或，后5位不会改变。因此 $f\oplus 32=f+32$ 。类似地， $f\oplus 64=f-64$ 。这意味着如果我们把输入 $\vec{i}$ 限制在32和64之间，就能保留加密时的线性。

上面是其中两种特殊的情况，另外两种没那么明显。如果我们将数字与31异或，最后5位会翻转。对于0-31内的x来说， $x+(x\oplus 31)=31$ ，或者说 $x\oplus 31=31-x$ ，同样去除了未知的异或，保留线性。类似地还有63，同样满足 $x\oplus 63=63-x$ 。对非0项f进行加密，得到： $f\oplus 31=((f-64)\oplus 31)+64=(31-(f-64))+64=159-f$ （这里不懂为啥会减个64，猜测是因为f的范围在65-90内，这里-64后保证f在31范围内，就能运用刚才提到的规律）。63则更好，有： $f\oplus 31=((f-64)\oplus 63)+64=(63-(f-64))+64=191-f$ 。191模95等于1，因此 $f\oplus 63=1-f$ ，简单易懂。

开始思考解题策略。14次输入，一次输入可获取20个加密信息（每次输入的guess长度为20），那14次只有280项，离密钥矩阵A的400项远着呢。节省一点，只获取矩阵A在非flag格式项上的列，即除前6列和最后一列外的列。那这样就只需要获取260项了，flag格式加密这个可以一次搞定，这样14次就能完成了。

介绍一些符号，方便后面使用。A'是一个除前6列和最后一列外都等同于A的矩阵，这是我们将用交互求出的矩阵。如果输入 $\vec{x}$ 在flag格式列都为0， $A'\vec{x}=A\vec{x}$ 。让 $E(\vec{i})=(\vec{b}+\vec{f})\oplus\vec{i}$ ，即异或操作。如果把输入 $\vec{i}$ 拆为 $\vec{b}$ 和 $\vec{x}$ 的和，其中 $\vec{x}$ 在flag格式列都为0；就有 $E(\vec{b}+\vec{x})=(\vec{b}+\vec{f})\oplus(\vec{b}+\vec{x})=(\vec{b}\oplus\vec{f})\oplus(\vec{b}\oplus\vec{x})=\vec{f}\oplus\vec{x}$ （因为两个 $\vec{b}$ 和 $\vec{f},\vec{x}$ 的互补性，加法操作在这里等于异或操作）。最后让 $\vec{x}[i]$ 为 $\vec{x}$ 的第i个元素，i从0开始。

第一次交互，我们输入 $\vec{b}+\vec{x}=\vec{b}+63\*\vec{1}$ ，加密结果为 $\vec{v}=A\*(E(\vec{b}+63\*\vec{1}))=A\*(\vec{f}\oplus(63\*\vec{1}))=A\*(\vec{1}-\vec{f})$ 。单纯这个玩意没用，我们需要让其配合后面的内容生成fakeflag2的加密结果。

剩下的13次交互，下标r从0开始，到12结束。发送 $\vec{b}+\vec{x_r}$ ，其中 $\vec{x_r}$ 等于 $64\*\vec{1}$ ，除了 $\vec{x_r}[6+r]$ 处等于32。经过转换得到 $\vec{e_r}=E(\vec{b}+\vec{x_r})=\vec{f}\oplus\vec{x_r}$ 。让 $\vec{d_r}=\vec{e_r}-\vec{f}$ ，就会得到 $\vec{d_r}[i]=(-64)\*\vec{1}[i]$ ，如果i不等于6+r；否则 $\vec{d_r}[i]=32$ 。这里 $\vec{e_r}$ 的每一项等于 $\vec{f}$ 的每一项减去64(除了6+r处)，即f-64。于是根据 $\vec{d_r}=\vec{e_r}-\vec{f}$ , $\vec{d_r}$ 的每一项应该为f-64-f(我不懂的地方来了，这样看不应该直接是-64吗，为什么还要乘flag内容向量 $\vec{1}[i]$ ?)。32的地方类似，只不过是f+32而不是f-64。最后的加密结果为 $A\*\vec{e_r}=A\*(\vec{d_r}+\vec{f})$ 。

到了处理阶段。还记得第一次交互得到的 $\vec{v}$ 吗？我们将13次交互的结果与它加起来，得到 $\vec{c_r}=A\*(\vec{d_r}+\vec{f})+A\*(\vec{1}-\vec{f})=A\*(\vec{d_r}+1)$ ，就是已知值的加密结果了。

接下来构造矩阵B，每一列r都是 $\vec{d_r}+1$ 的非零部分（除去flag格式），得到一个13\*13的矩阵（13次交互，flag内容长13，加密结果也长13）。接着构造矩阵C，每一列r等于 $\vec{c_r}$ ，就有20行13列。现在就能考虑找矩阵A'了。A'形如`[0 x 0]`，其中x为代表flag内容的13列。回顾 $\vec{c_r}$ 那里的关系，有XB=C。使用sagemath的solve_left函数，即可得到A'。

还不够，我们最终需要的是 $A\*(\vec{b}+\vec{f_2})$ 。服务器已经给出了fakeflag的密文，即 $A\*(\vec{b}+\vec{f})$ 。将其加上 $\vec{v}$ ,得到 $A\*(\vec{1}-\vec{f})+A\*(\vec{b}+\vec{f})=A\*(\vec{b}+\vec{1})$ 。加上 $A'\*(\vec{f_2}-\vec{1})$ ，得到 $A\*(\vec{b}+\vec{1})+A'\*(\vec{f_2}-\vec{1})=A\*(\vec{b}+\vec{f_2})$ ，完成。

```python
from pwn import *
def stov(s):
    return [int(c)-32 for c in s]
def vtos(v):
    return ''.join([chr(int(i)+32) for i in v])

C = []
B = []
with remote("lac.tf", 31141) as r:
	r.readline()
	f = vector(Zmod(95), stov(r.readline(False)))
	
	r.readuntil(b"Enter your guess: ")
	c = bytearray(b"lactf{_____________}")
	r.sendline(c)
	inv = vector(Zmod(95), stov(r.readline(False)))
	base = inv + f
	
	for i in range(13):
		r.readuntil(b"Enter your guess: ")
		c = bytearray(b"lactf{`````````````}")
		c[6+i] = 64
		b = vector(Zmod(95), [-63] * 13)
		b[i] = 33
		r.sendline(c)
		v = vector(Zmod(95), stov(r.readline(False)))
		C.append(v + inv)
		B.append(b)
	CC = matrix(Zmod(95), C).T
	BB = matrix(Zmod(95), B).T
	AA = BB.solve_left(CC)
	
	r.readuntil(b"Encrypt me:")
	r.readline()
	target = r.readline(False)[6:-1]
	t = vector(Zmod(95), [int(c)-32-1 for c in target])
	tt = base + (AA * t)
	r.sendline(vtos(tt).encode())
	r.interactive()
```

## Flag
> lactf{putting_the_linear_in_linear_algebra}