# maze

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=18e12857-0acc-421a-a784-b769b9ca7c6a_2)

我现在才知道reverse里[迷宫题](https://ctf-wiki.org/reverse/maze/maze/)居然是一类题型。

```c
undefined8 Main(void)

{
  char cVar1;
  char cVar2;
  int iVar3;
  uint current_instruction;
  size_t inputLength;
  ulong step;
  char *__s;
  undefined8 local_28;
  
  local_28 = 0;
  puts("Input flag:");
  scanf("%s",&input);
  inputLength = strlen(&input);
  if (((inputLength != 24) || (iVar3 = strncmp(&input,"nctf{",5), iVar3 != 0)) ||
     (cRam00000000006010d7 != '}')) {
FAIL:
    puts("Wrong flag!");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  inputLength = strlen(&input);
  step = 5;
  if (inputLength - 1 < 6) {
SUCCESS:
    if (s__*******_*_****_*_****_*_***_*#_*_00601060[(long)(int)local_28 * 8 + (long)local_28._4_4_]
        == '#') {
      __s = "Congratulations!";
      goto LAB_00400810;
    }
  }
  else {
    do {
      current_instruction = (uint)(char)(&input)[step];
      cVar1 = '\0';
      if ((int)current_instruction < L'O') {
        if ((current_instruction & 0xff) == L'.') {
          cVar1 = FUN_00400670(&local_28);
        }
        else if ((current_instruction & 0xff) == L'0') {
          cVar1 = FUN_00400680(&local_28);
        }
      }
      else if ((current_instruction & 0xff) == L'O') {
        cVar1 = FUN_00400650((long)&local_28 + 4);
      }
      else if ((current_instruction & 0xff) == L'o') {
        cVar1 = FUN_00400660((long)&local_28 + 4);
      }
      cVar2 = FUN_00400690(s__*******_*_****_*_****_*_***_*#_*_00601060,local_28._4_4_,
                           local_28 & 0xffffffff);
      if (cVar2 == '\0') goto FAIL;
      step = step + 1;
      inputLength = strlen(&input);
    } while (step < inputLength - 1);
    if (cVar1 != '\0') goto SUCCESS;
  }
  __s = "Wrong flag!";
LAB_00400810:
  puts(__s);
  return 0;
}
```

分析一下，flag格式是nctf{xxxxx}，长度为24。不知道cRam00000000006010d7是什么东西，我就当成input的一部分了。第一个if语句肯定进不去，到else的do-while循环。input的每个字符就是要走的方向，一共有.,0,O,o四种指令（出题人太阴间了这什么鬼指令）。现在就是找迷宫地图和每个指令对应的方向了，迷宫题标准思路。

我不是很能看懂几个决定方向的函数，但是我结合之前做的迷宫题发现了一个不知道是不是规律的规律。看这个语句：

```c
if (s__*******_*_****_*_****_*_***_*#_*_00601060[(long)(int)local_28 * 8 + (long)local_28._4_4_]
        == '#') {
      __s = "Congratulations!";
      goto LAB_00400810;
    }
```

第一个数组很明显就是迷宫地图字符，local_28应该是我们当前所在位置。local_28 * 8表示地图大小是8的倍数，很多时候是正方形8\*8，这还要结合实际地图字符来判断。同时是低位的local_28用于乘以8，高位的local_28._4_4_用于加，大概率说明低位是y坐标，高位是x坐标。这是将二维坐标转换为数组中索引的一个方法，比如我们当前的坐标是(5,2)，在我们之前的格子就是5\*8+2=42个，永远是y坐标乘上地图的宽+x坐标求出当前所在位置是地图内的第几个符号。这里判断我们所在的坐标对应的符号是不是#，#一定是目标。现在x和y判断出来了，看这些符号内部的函数。

```c
uint FUN_00400670(uint *param_1)

{
  uint uVar1;
  
  uVar1 = *param_1;
  *param_1 = uVar1 - 1;
  return uVar1 & 0xffffff00 | (uint)(0 < (int)uVar1);
}

uint FUN_00400680(uint *param_1)

{
  uint uVar1;
  
  uVar1 = *param_1 + 1;
  *param_1 = uVar1;
  return uVar1 & 0xffffff00 | (uint)((int)uVar1 < 8);
}
```

四个函数里有两个好像是重复的，第一个是.的，第二个是0的。里面param_1的变换表示在当前轴的正负变换，关键在参数的传入。FUN_00400670和FUN_00400680传的是低位，说明传低位的两个指令是y轴，另外两个自然是x轴了。

地图只有63个字符，在前面加一个空白格做起点。

```python
data="   *******   *  **** * ****  * ***  *#  *** *** ***     *********"
for i in range(1,len(data)):
    print(data[i],end='')
    if i%8==0:
        print()
```

最后看着地图走就完事了。

### Flag
> nctf{o0oo00O000oooo..OO}