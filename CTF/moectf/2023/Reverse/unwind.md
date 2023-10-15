# unwind

关键点在于后半部分的flag用tea加密了两次。用seh和故意引发的异常控制程序流，导致难以通过静态分析直接得到flag（前半部分可以，因为在main函数里就能看到，用ghidra甚至能看到伪代码）。后半部分的加密逻辑把全部函数翻一遍还是能找到的，但是一个关键点在于后半部分用tea加密了两次。如果直接靠蒙猜测只加密一次的话会陷入无限的自我怀疑（我怀疑了自己半个月）

https://reverseengineering.stackexchange.com/questions/18192/stepping-into-exception-handler 给了我解题思路。目前的问题是不知道程序经过seh修改程序流后到底怎么加密的。如果能调试器跟进看就好了。方法在于将断点下在`ntdll!ExecuteHandler2`的`call ecx`指令处，然后就能跟进看到接下来调用了什么函数了。根据调试结果，后半部分调用了tea两次。所以解密两次即可

下断点的时候我倒是没有搜到`ntdll!ExecuteHandler2`这个symbol，不过我直接x32dbg ctrl+f搜指令`call ecx`。这个指令程序里不多，当时搜出来4个，最后一个是要找的
```py
from ctypes import *
def decrypt(v, k):
    v0, v1 = c_uint32(v[0]), c_uint32(v[1])
    delta = -0x61c88647
    k0, k1, k2, k3 = k[0], k[1], k[2], k[3]
    total = c_uint32(delta * 32)
    for i in range(32):                       
        v1.value -= ((v0.value<<4) + k2) ^ (v0.value + total.value) ^ ((v0.value>>5) + k3) 
        v0.value -= ((v1.value<<4) + k0) ^ (v1.value + total.value) ^ ((v1.value>>5) + k1)  
        total.value -= delta
    return [v0.value, v1.value]
def process_cipher(c):
    cipher=[]
    part=[]
    for i in range(0,len(c),4):
        part.append(int(''.join(c[i:i+4][::-1]),16))
        if len(part)==2:
            cipher.append(part)
            part=[]
    return cipher
def tea_decrypt(cipher):
    ans=''
    for i in range(len(cipher)):
        res=decrypt(cipher[i],k[i])
        for j in range(2):
            for z in range(4):
                ans+=chr(res[j]&0xff)
                res[j]>>=8
    return ans
k=[]
c='5a e3 6b e4 06 87 02 4f 43 df cd c1 77 98 6b db 8f 38 43 99 e3 93 22 b5 23 fd b0 1c e5 e3 ee ce'.split()
key='44 58 33 39 30 36 00 00 00 00 00 00 00 00 00 00 64 6f 63 74 6f 72 33 00 00 00 00 00 00 00 00 00 46 55 58 31 41 4f 59 55 4e 00 00 00 00 00 00 00 52 33 76 65 72 69 65 72 00 00 00 00 00 00 00 00'.split()
cipher=process_cipher(c)
part=[]
for i in range(0,len(key),4):
    part.append(int(''.join(key[i:i+4][::-1]),16))
    if len(part)==4:
        k.append(part)
        part=[]
flag=''
flag+=tea_decrypt(cipher)
"""
#get c3
c2='2f 1d ad 2b a4 15 98 f9 d8 eb 25 fa 6b 21 b7 72 b9 03 33 2e d9 4c eb 7b f5 a7 48 f9 90 9d 38 fc'.split()
cipher=process_cipher(c2)
for i in range(len(cipher)):
    res=decrypt(cipher[i],k[i])
    for j in range(2):
        for z in range(4):
            print(f"{res[j]&0xff:02x}",end=' ')
            res[j]>>=8"""
c3='ca 76 19 6b 95 21 b7 b3 dd 8d b5 ad ae f2 02 24 5e 60 d7 f0 e9 38 7e 55 8a 22 de 27 3e 97 e8 aa'.split()
cipher=process_cipher(c3)
flag+=tea_decrypt(cipher)
print(flag)
```
所以我的静态分析能力约等于0