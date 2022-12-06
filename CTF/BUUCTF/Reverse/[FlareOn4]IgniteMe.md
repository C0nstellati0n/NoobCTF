# [FlareOn4]IgniteMe

[题目地址](https://buuoj.cn/challenges#[FlareOn4]IgniteMe)

这题完全就是学怎么用ida动调。

```c
void __noreturn start()
{
  DWORD NumberOfBytesWritten; // [esp+0h] [ebp-4h] BYREF

  NumberOfBytesWritten = 0;
  hFile = GetStdHandle(0xFFFFFFF6);
  dword_403074 = GetStdHandle(0xFFFFFFF5);
  WriteFile(dword_403074, aG1v3M3T3hFl4g, 0x13u, &NumberOfBytesWritten, 0);
  sub_4010F0();
  if ( sub_401050() )
    WriteFile(dword_403074, aG00dJ0b, 0xAu, &NumberOfBytesWritten, 0);
  else
    WriteFile(dword_403074, aN0tT00H0tRWe7r, 0x24u, &NumberOfBytesWritten, 0);
  ExitProcess(0);
}
```

明显`sub_401050()`是检查函数，进去看看。

```c
int sub_401050()
{
  int v1; // [esp+0h] [ebp-Ch]
  int i; // [esp+4h] [ebp-8h]
  unsigned int j; // [esp+4h] [ebp-8h]
  char v4; // [esp+Bh] [ebp-1h]

  v1 = sub_401020((int)byte_403078);
  v4 = sub_401000();
  for ( i = v1 - 1; i >= 0; --i )
  {
    byte_403180[i] = v4 ^ byte_403078[i];
    v4 = byte_403078[i];
  }
  for ( j = 0; j < 0x27; ++j )
  {
    if ( byte_403180[j] != (unsigned __int8)byte_403000[j] )
      return 0;
  }
  return 1;
}
```

这题虽然哪个是输入不明显，但是我们能直接分析出来。最后一个for循环是比较，`byte_403000`前面没引用且有默认值，一定是期望结果。那`byte_403180`一定是加密结果，最后剩下的`byte_403078`只能是输入。程序整体加密逻辑不难，问题是v4的生成有点迷。

```c
__int16 sub_401000()
{
  return (unsigned __int16)__ROL4__(-2147024896, 4) >> 1;
}
```

来吧动调。菜单栏->Debugger->Select debugger->Local Windows debugger，当然配置好了选别的也行。然后断点下在` `的第10行，正好是for循环那里。Debugger->Start process开启调试进程。确认进来后F9或者Debugger->Continue process。如果遇见`xxx:Software breakpoint exception`，不要理它，直接勾上Don't display，然后ok。继续f9，如果刚刚遇见那个弹窗，现在大概率会再弹出个Exception handling。选择`No(discard)`，一切正常。此时应该会弹出程序的对话窗口，但是输入提示还没有打印出来。重复刚才f9的操作，弹窗就选no，直到对话窗口出现输入flag的提示。随便输点东西后回车。

注意可能不会显示碰到断点，也就是程序没有弹出来下了断点的函数。不过程序还是会一步一步走的，只需要人工注意下`IDA View-EIP`执行到哪一步了，如果到了断点就`菜单栏->Debugger->Debugger windows->Locals`打开当前程序的本地变量，会发现v4是`\x04`，转成数字就是4。成功获取到v4值。终止程序只需要在菜单栏下方找到一个蓝边白底的小方块，点击就行了。

```python
arr2 = [0x0D,0x26,0x49,0x45,0x2A,0x17,0x78,0x44,0x2B,0x6C,0x5D,0x5E,0x45,0x12,0x2F,0x17,
0x2B,0x44,0x6F,0x6E,0x56,0x09,0x5F,0x45,0x47,0x73,0x26,0x0A,0x0D,0x13,0x17,0x48,
0x42,0x01,0x40,0x4D,0x0C,0x02,0x69]

arr1 = []
v4 = 4
for i in range(len(arr2)-1,-1,-1):
    arr1.append(arr2[i] ^ v4)
    v4 = arr1[-1]
print ('flag{'+''.join([chr(x) for x in arr1[::-1]])+'}')
```

## Flag
> flag{R_y0u_H0t_3n0ugH_t0_1gn1t3@flare-on.com}