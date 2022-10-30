# easy_Maze

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f86170b2-1fd8-4e90-9853-f15813522188_2)

越做逆向越觉得动态调试真的太重要了，我现在还没配好环境，寄。

运行一下，程序打印了一句话，然后要求输入内容。不是走迷宫吗，迷宫呢？开始逆向。

```c
undefined8 main(void)

{
  basic_ostream *this;
  long lVar1;
  undefined8 *puVar2;
  undefined8 map [26];
  undefined8 local_1a8 [26];
  int local_d8;
  undefined4 local_d4;
  undefined4 local_d0;
  undefined4 local_cc;
  undefined4 local_c8;
  undefined4 local_c4;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined4 local_b8;
  undefined4 local_b4;
  undefined4 local_b0;
  undefined4 local_ac;
  undefined4 local_a8;
  undefined4 local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  undefined4 local_88;
  undefined4 local_84;
  undefined4 local_80;
  undefined4 local_7c;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  
  local_d8 = 1;
  local_d4 = 1;
  local_d0 = 0xffffffff;
  local_cc = 1;
  local_c8 = 0xffffffff;
  local_c4 = 1;
  local_c0 = 0xffffffff;
  local_bc = 0;
  local_b8 = 0;
  local_b4 = 0;
  local_b0 = 0;
  local_ac = 1;
  local_a8 = 0xffffffff;
  local_a4 = 0;
  local_a0 = 0;
  local_9c = 1;
  local_98 = 0;
  local_94 = 0;
  local_90 = 1;
  local_8c = 0;
  local_88 = 0xffffffff;
  local_84 = 0xffffffff;
  local_80 = 0;
  local_7c = 1;
  local_78 = 0;
  local_74 = 1;
  local_70 = 0xffffffff;
  local_6c = 0;
  local_68 = 0xffffffff;
  local_64 = 0;
  local_60 = 0;
  local_5c = 0;
  local_58 = 0;
  local_54 = 0;
  local_50 = 1;
  local_4c = 0xffffffff;
  local_48 = 0xffffffff;
  local_44 = 1;
  local_40 = 0xffffffff;
  local_3c = 0;
  local_38 = 0xffffffff;
  local_34 = 2;
  local_30 = 1;
  local_2c = 0xffffffff;
  local_28 = 0;
  local_24 = 0;
  local_20 = 0xffffffff;
  local_1c = 1;
  local_18 = 0;
  puVar2 = local_1a8;
  for (lVar1 = 0x18; lVar1 != 0; lVar1 = lVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)puVar2 = 0;
  puVar2 = map;
  for (lVar1 = 0x18; lVar1 != 0; lVar1 = lVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)puVar2 = 0;
  Step_0(&local_d8,7,(int *)local_1a8);
  Step_1((int *)local_1a8,7,(int *)map);
  this = std::operator<<((basic_ostream *)__TMC_END__,"Please help me out!");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)this,
             (FuncDef487 *)PTR_endl<char,std_char_traits<char>>_00103fd0);
  Step_2((int *)map,7);
  system("pause");
  return 0;
}
```

我好疑惑这堆变量是什么玩意？先放一边。根据之前逆向c++的经验，最开始几个不明所以的for循环都是和逆向逻辑没关系的，不看就行了。发现打印的内容在Step_0和Step_1函数之后，说明前两个函数的逻辑无论重不重要，我们都没法控制，逆向要从能控制的函数开始，这里就是Step_2。

```c
/* Step_2(int (*) [7], int) */

undefined8 Step_2(int *param_1,int param_2)

{
  long lVar1;
  basic_ostream *pbVar2;
  undefined8 uVar3;
  char local_38 [35];
  char input;
  int local_14;
  int horizontal;
  int vertical;
  
  vertical = 0;
  horizontal = 0;
  local_14 = 0;
  do {
    while( true ) {
      while( true ) {
        if ((0x1d < local_14) || (param_1[(long)vertical * 7 + (long)horizontal] != 1)) {
          if ((vertical == 6) && (horizontal == 6)) {
            pbVar2 = std::operator<<((basic_ostream *)__TMC_END__,"Congratulations!");
            std::basic_ostream<char,std::char_traits<char>>::operator<<
                      ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                       (FuncDef487 *)PTR_endl<char,std_char_traits<char>>_00103fd0);
            output(local_38,local_14);
            uVar3 = 1;
          }
          else {
            pbVar2 = std::operator<<((basic_ostream *)__TMC_END__,"Oh no!,Please try again~~");
            std::basic_ostream<char,std::char_traits<char>>::operator<<
                      ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                       (FuncDef487 *)PTR_endl<char,std_char_traits<char>>_00103fd0);
            uVar3 = 0;
          }
          return uVar3;
        }
        std::operator>>((basic_istream *)std::cin,&input);
        lVar1 = (long)local_14;
        local_14 = local_14 + 1;
        local_38[lVar1] = input;
        if (input != 'd') break;
        horizontal = horizontal + 1;
      }
      if ('d' < input) break;
      if (input == 'a') {
        horizontal = horizontal + -1;
      }
      else {
LAB_001017bc:
        pbVar2 = std::operator<<((basic_ostream *)__TMC_END__,"include illegal words.");
        std::basic_ostream<char,std::char_traits<char>>::operator<<
                  ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                   (FuncDef487 *)PTR_endl<char,std_char_traits<char>>_00103fd0);
      }
    }
    if (input == 's') {
      vertical = vertical + 1;
    }
    else {
      if (input != 'w') goto LAB_001017bc;
      vertical = vertical + -1;
    }
  } while( true );
}
```

输入内容应该是wasd。作用就和打游戏一样，不用多想。关注重点if语句中的判断。

```c
if ((0x1d < local_14) || (param_1[(long)vertical * 7 + (long)horizontal] != 1))
```

local_14在下方。

```c
std::operator>>((basic_istream *)std::cin,&input);
        lVar1 = (long)local_14;
        local_14 = local_14 + 1;
        local_38[lVar1] = input;
```

每输入一个内容，local_14自增1，同时local_38[lVar1]=input。结合congratulations分支里的output函数看，两者都和flag有关系。

```c
/* output(char*, int) */

void output(char *param_1,int param_2)

{
  basic_ostream *this;
  int i;
  
  std::operator<<((basic_ostream *)__TMC_END__,"Thanks! Give you a flag: UNCTF{");
  for (i = 0; i < param_2; i = i + 1) {
    std::operator<<((basic_ostream *)__TMC_END__,param_1[i]);
  }
  this = std::operator<<((basic_ostream *)__TMC_END__,"}");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)this,
             (FuncDef487 *)PTR_endl<char,std_char_traits<char>>_00103fd0);
  return;
}
```

param_1即local_38，我们输入的指令，是flag内容；param_2即local_14，单纯就是长度。flag格式为UNCTF{}。结合最开始的if语句，我们一定要走0x1d步，且把每一步换算成索引取param_1的值都是1。这么看来param_1很有可能就是我们要找的地图，动态调试看看地图长什么样。把断点下在Step_2函数的开始，因为64位用寄存器传参，所以第一个参数在rdi里。

```
Breakpoint 4, 0x000055678253b703 in Step_2(int (*) [7], int) ()
(gdb) x/80dw $rdi
0x7ffd9153c5e0: 1       0       0       1
0x7ffd9153c5f0: 1       1       1       1
0x7ffd9153c600: 0       1       1       0
0x7ffd9153c610: 0       1       1       1
0x7ffd9153c620: 1       0       1       1
0x7ffd9153c630: 1       0       0       0
0x7ffd9153c640: 1       1       0       0
0x7ffd9153c650: 1       1       1       1
0x7ffd9153c660: 0       0       0       1
0x7ffd9153c670: 0       0       0       1
0x7ffd9153c680: 1       1       1       1
0x7ffd9153c690: 1       1       1       0
0x7ffd9153c6a0: 1       0       0       0
0x7ffd9153c6b0: -1      0       -1      0
0x7ffd9153c6c0: 1       2       0       1
0x7ffd9153c6d0: -1      0       -1      0
0x7ffd9153c6e0: -1      1       -1      1
0x7ffd9153c6f0: 1       1       0       0
0x7ffd9153c700: -1      1       0       0
0x7ffd9153c710: 0       0       -1      0
```

发现地图。检查用的w是双字，d是整数打印。我们要让每一步都走在1上，但是这个地图好像是条死路？因为我们把排版搞错了，地图的摆放应该是7\*7，从函数签名Step_2(int (\*) [7], int)看出。或者更简单的，跟[wp](https://blog.csdn.net/xiao__1bai/article/details/120012374)一样用ida，好看多了。

### Flag
> UNCTF{ssddwdwdddssaasasaaassddddwdds}