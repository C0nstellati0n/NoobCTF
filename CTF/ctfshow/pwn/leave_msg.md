# leave_msg

[题目地址](https://ctf.show/challenges#leave_msg-3832)

新手杯给了官方wp，但是我还是想自己写一下，因为我是菜狗。

这题确实很简单，但是我被误导了,被自己菜出天际。

```c
undefined8 Main(void)

{
  undefined4 uVar1;
  int iVar2;
  long in_FS_OFFSET;
  undefined local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_38,0,0x20);
  FUN_004009fa();
  PrintTitle();
  puts("welcome to the first challenge!\nwhat you need to do it to tell me something about youself!"
      );
  puts("then enjoy the game!");
  while (iVar2 = Login(), iVar2 != 0) {
    PrintMenu();
    GetInput(local_38,2);
    uVar1 = _atoi(local_38);
    switch(uVar1) {
    default:
      puts("Illegal input");
      break;
    case 1:
      Create();
      break;
    case 2:
      Check();
      break;
    case 3:
      Delete();
      break;
    case 4:
      Modify();
      break;
    case 5:
      IsLogin = 0;
      IsAdmin = 0;
      break;
    case 6:
      ExitSystem();
      break;
    case 7:
      CheckLogInformation();
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

进来直接懵了，“新手”？“简单题”？哪有新手上来就菜单题，还是堆的？煞有介事分析了一波，没发现明显漏洞，懵了，直接做不动了，堆一直不懂。看了wp，……为什么我刷了这么久题还是菜狗的原因找到了。只有这个一个函数有用。

```c
void ExitSystem(void)

{
  long in_FS_OFFSET;
  undefined local_58 [32];
  char local_38 [40];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  memset(local_58,0,0x20);
  GetInput(local_58,0x20);
  sprintf(local_38,"echo %s",local_58);
  system(local_38);
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

还用多说吗，命令注入。本来local_58处是输入名字的，但是用snprntf拼接起来再放进system执行就有问题了。构造&& ls查看目录，发现flag名字就是flag，再登录一次使用&& cat flag直接得flag。这个故事告诉我们搜进入程序的第一件事是看看有没有system！看有没有system！看有没有system！不要先钻进一个函数里分析，每个都过一遍再仔细研究，不然可能会错过一个亿！

- ### Flag
  > ctfshow{b899abe5-28f4-4d32-8e05-a3d9e3304648}