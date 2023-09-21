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