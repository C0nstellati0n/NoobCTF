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