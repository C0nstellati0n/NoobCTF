# broken_hash

虽然代码有点不同，但是和去年的[ezhash](https://github.com/XDSEC/MoeCTF_2022/blob/main/Official_Writeup/Crypto/Moectf_CryptoWriteup.md#ezhash)一样的思路。去年我用的是非预期解z3直接冲，今年没试，反正我知道正确的解法了（byd二周目速通是吧？）

_block_hash的a，b，c和d做个交换即可拿到同样hash但不同的字符串
```py
from string import ascii_letters
from pwn import *
from itertools import product
from hashlib import md5
from base64 import b64decode,b64encode
p=remote("localhost",56675)
def bytes2blocks(data: bytes, block_size=16):
    if len(data) % block_size != 0:
        data += b"\x00" * (block_size - len(data) % block_size)
    return [
        int.from_bytes(data[i : i + block_size], "little")
        for i in range(0, len(data), block_size)
    ]
def blocks2bytes(blocks):
    res=b''
    for block in blocks:
        res+=block.to_bytes(16,'little')
    return res
def crack(key,md5hash):
    code = ''
    strlist = product(ascii_letters, repeat=4)
    for i in strlist:
        code = ''.join(i)
        temp=code.encode()+key
        encinfo = md5(temp).hexdigest().encode()
        if encinfo == md5hash:
            return code
p.recvuntil("md5(XXXX+")
last_letters=p.recvuntil(")",drop=True)
p.recvuntil("== ")
expected_hash=p.recvline(keepends=False)
p.sendlineafter(": ",crack(last_letters,expected_hash))
p.recvuntil("this is a random bytes: ")
problem=b64decode(p.recvline(keepends=False))
blocks=bytes2blocks(problem)
block_size=4
collision=blocks[block_size : block_size * 2]+blocks[block_size * 2 : block_size * 3]+blocks[block_size * 3 :]+blocks[:block_size]
p.sendlineafter("same hash: ",b64encode(blocks2bytes(collision)))
print(p.recvall())
```