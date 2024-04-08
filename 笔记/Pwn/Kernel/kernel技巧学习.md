# kernel技巧学习

我爱挖坑（heap：你不看看我吗？），但我不填。

## [Overwriting modprobe_path](https://lkmidas.github.io/posts/20210223-linux-kernel-pwn-modprobe/)

modprobe在install或者uninstall新模块进linux kernel时会被执行。其路径默认为/sbin/modprobe。可通过以下命令获得其路径：
```sh
cat /proc/sys/kernel/modprobe
```
kernel里也有个名为modprobe_path的全局symbol记录其路径。这个symbol位于可写的内存页，可通过/proc/kallsyms获取其地址（kaslr情况下地址每次都不一样）
```sh
cat /proc/kallsyms | grep modprobe_path
```
当我们执行一个未知类型的文件时，该程序会被调用。更准确地说，如果我们对一个系统未知的文件头（file signature，magic header）调用execve()，最终会调用到modprobe
1. do_execve()
2. do_execveat_common()
3. bprm_execve()
4. exec_binprm()
5. search_binary_handler()
6. request_module()
7. call_modprobe()

长话短说，modprobe_path存储的路径所指向的文件会在system尝试调用未知文件类型的文件时被调用。当我们获取到任意地址写时，把modprobe_path覆盖成我们自己写的getshell脚本，然后执行一个未知类型的文件即可获取root权限的rce（rce内容为shell脚本里的内容）。

这个技巧的前置条件：
1. 已知modprobe_path的地址
2. 已知kpti_trampoline的地址（覆盖modprobe_path后返回userland）
3. 拥有任意地址写

modprobe_path和kpti_trampoline均不受FG-KASLR影响。

在大部分linux系统中，/tmp文件夹无论任何user都可以自由读写。因此可以把shell脚本放到这下面。

总结利用手法：
1. 构造ropchain，覆盖modprobe_path（文件名转成小端hex直接放进ropchain即可）并调用kpti_trampoline返回userland的getshell函数
2. getshell函数中用system准备shell脚本（应该提前准备好也行）+未知文件并执行未知文件
```c
system("echo '#!/bin/sh\ncp /dev/sda /tmp/flag\nchmod 777 /tmp/flag' > /tmp/x");
system("chmod +x /tmp/x");
system("echo -ne '\\xff\\xff\\xff\\xff' > /tmp/dummy");
system("chmod +x /tmp/dummy");
system("/tmp/dummy");
system("cat /tmp/flag");
```
完整exp：https://lkmidas.github.io/posts/20210223-linux-kernel-pwn-modprobe/modprobe.c

## [Cross-Cache attack](https://xz.aliyun.com/t/12898)

Cross-Cache attack个人其实没找到明确定义，只在标题的文章中看见作者提了一嘴。大概是：说每个结构体/object都有对应的slab管理器，而kernel中常用的攻击手法——堆喷——目标是让kernel中的某一个重要结构体与我们能控制的内存重合（是吧？）。那要是题目中所有结构体所在的slab里没有可以利用的重要结构体，就寄了？并没有。在这篇[文章](https://brieflyx.me/2020/heap/linux-kernel-slab-101/)中可以看到slab在内存中以页为单位存在。如果我们free某个内存页中所有的结构体，使整个内存页完全空闲，kernel就会回收这个内存页。这时我们分配一个重要结构体，kernel就会把刚才那个回收的内存页用做这个结构体所在的slab。至此我们成功让某个内存页出现在了两个slab中，即“cross”

找到了，详细解析在这： https://ruia-ruia.github.io/2022/08/05/CVE-2022-29582-io-uring/#crossing-the-cache-boundary

## [pipe-primitive](https://github.com/veritas501/pipe-primitive)
利用pipe_buffer结构体实现任意文件写。参考 https://kaligulaarmblessed.github.io/post/palindromatic-biosctf2024/ 的DirtyPipe章节。说是pipe_buffer结构体里有个PIPE_BUF_FLAG_CAN_MERGE标志。当某些文件内容被写入pipe_buffer且长度不足以填满一个page时，其内容会被添加到已经存在的page（ring中上一个pipe_buffer的page。至于ring是什么，这里截一段原文：`The actual pipe_buffer object that is allocated is actually a ring of pipe_buffer structs. Initially the object is empty, when its written to for the first time, a pipe_buffer is added to the ring.`）而不是新分配一个，前提是这些pipe_buffer设置了PIPE_BUF_FLAG_CAN_MERGE标志。从pipe读取数据不会取消设置标志

内核里还有个splice函数，可以从两个文件描述符中转移数据。所以我们可以splice一个文件，如`/etc/passwd`，这时会在ring里新增一个pipe_buffer。然后用诸如UAF的方法尝试泄漏这个新增的pipe_buffer，紧接着构造一个假的pipe_buffer，同时设置PIPE_BUF_FLAG_CAN_MERGE标志。然后往这个pipe_buffer里写东西，就会被添加到ring中上一个pipe_buffer的page，即刚才打开的/etc/passwd。这段参考了 https://blog.bi0s.in/2024/02/26/Pwn/bi0sCTF24-palindromatic/