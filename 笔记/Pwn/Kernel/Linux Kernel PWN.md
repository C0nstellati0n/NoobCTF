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