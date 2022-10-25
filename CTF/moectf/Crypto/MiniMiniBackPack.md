# MiniMiniBackPack

怎么加题了啊？数学差生看到Crypto连续加4道直接傻眼。

这题看题目和脚本就能立刻想到是[背包加密](https://www.ruanx.net/lattice-2/)。这篇文章里详细地介绍了背包加密，而且易懂，推荐阅读，看完了这道题直接秒杀。

```python
from gmpy2 import *
from Crypto.Util.number import *
import random
from FLAG import flag

def gen_key(size):
    s = 1000
    key = []
    for _ in range(size):
        a = random.randint(s + 1, 2 * s)
        assert a > sum(key)
        key.append(a)
        s += a
    return key

m = bytes_to_long(flag)
L = len(bin(m)[2:])
key = gen_key(L)
c = 0

for i in range(L):
    c += key[i]**(m&1)
    print(key[i]**(m&1))
    m >>= 1

print(key)
print(c)
```

简述一下背包加密的流程。假设有一个背包，重量为c。你有一堆重量不等的物品，这堆物品按特定顺序放在一个叫key的篮子里。现在要求你从篮子里挑n个物品，让这些物品放在背包里后重量等于c。问你该如何选择物品？篮子中被选中的物品标为1，没被选中的物品标为0。这就是背包密码的解密，可以知道在没有其他条件的情况下，是很难找到正好n个物品匹配重量c的。

加密也很简单。首先把物品按顺序放到篮子里，然后把要加密的明文转为2进制。0位表示不拿对应的物品，1位表示拿对应的物品，把1位处的物品的重量加起来得到c，也就是密文。

现在题目给出了篮子和c，怎么找明文？如果key这个篮子里的物品真的随机摆放，解密会很痛苦，至少不会像现在这么简单。但gen_key函数中有个重要的提示：assert a > sum(key)。a是第n次的物品重量，说明第n次的单个物品重量药大于从n-1到1次的所有物品的重量之和。这回篮子可不是普通的篮子了，叫超级递增序列。有了这个条件解密就非常简单了。

拿上面那篇文章的例子。有个篮子$M=(3,11,24,50,115)$，密文$S=142$。$142>115$，因此加密时一定拿了115这个物品，因为115比前面所有物品的总和还要大，如果不拿这个物品，而把前面的物品全部装上，那么此时的重量一定小于115，从而小于142。由此可得142这个重量重一定包含115。把115移除，还剩27的重量。$27<50$说明肯定没拿50，还剩下$(3,11,24)$。这不就是和第一次一样的情况吗？重复以上步骤，便可得到明文。

题目还有一个和普通背包加密不一样的地方。for循环中c += key[i]**(m&1)将key的每一位将m的每一位作为指数进行乘方，而不是相乘。这导致就算m当前位是0，没有拿当前位的物品，背包还是加上了1的重量，因为任何数的0次方都是1。不过没啥影响，我尝试把1减掉,得到的flag最后一位不对，反而是正常解密完全对了。

脚本中的attachment.txt删除了最后一行的密文，因为密文比较短直接复制过来就好了。

```python
from Crypto.Util.number import long_to_bytes
c=2396891354790728703114360139080949406724802115971958909288237002299944566663978116795388053104330363637753770349706301118152757502162
with open("attachment.txt",'r') as f:
    key=f.read().split(',')
    for i in range(len(key)):
        key[i]=int(key[i].strip().replace(']','').replace('[',''))
answer=[]
for k in key.__reversed__():
    if c>k:
        answer.append('1')
        c-=k
    else:
        answer.append('0')
        #c-=1
result=int(''.join(answer),2)
print(long_to_bytes(result))
```

- ### Flag
  > moectf{Co#gRa7u1at1o^s_yOu_c6n_d3c0de_1t}