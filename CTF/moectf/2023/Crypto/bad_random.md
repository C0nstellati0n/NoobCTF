# bad_random

题目是基于`(a*m)+c mod n`的随机数生成器(名字叫lcg)。这类生成器不安全，获取至少4个数字（听别人说的，不太确定。总之这题给了9个肯定够了）即可破解生成器的参数从而预测接下来的输出。
```py
from functools import reduce
from math import gcd
from pwn import *
from itertools import product
from string import ascii_letters
from hashlib import md5
#lcg crack部分来自 https://github.com/google/google-ctf/blob/master/2023/crypto-lcg/src/solve_challenge.py
def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment
def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * pow(states[1] - states[0], -1, modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)
def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)
def crack(key,md5hash):
    code = ''
    strlist = product(ascii_letters, repeat=4) #不要用permutations
    for i in strlist:
        code = ''.join(i)
        temp=code.encode()+key
        encinfo = md5(temp).hexdigest().encode()
        if encinfo == md5hash:
            return code
class LCG:
    def __init__(self,m,a,c,x):
        self.m = m
        self.a = a
        self.c = c
        self.x = x
    def __call__(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x
p=remote("localhost",57259)
p.recvuntil("md5(XXXX+")
last_letters=p.recvuntil(")",drop=True)
p.recvuntil("== ")
expected_hash=p.recvline(keepends=False)
p.sendlineafter(": ",crack(last_letters,expected_hash))
vals=[]
for i in range(9):
    p.sendlineafter("times: ",'1')
    p.recvuntil("The right number is ")
    vals.append(int(p.recvline(keepends=False)))
modulus, multiplier, increment = crack_unknown_modulus(vals)
lcg=LCG(modulus,multiplier,increment,vals[-1])
p.sendlineafter("times: ",str(lcg()))
print(p.recvall())
```
有时候会因为破解时找不到逆元而报错，多运行几次就好了