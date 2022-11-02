# asong

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=47ca6091-4ffa-4c21-8b09-d033eede51a5_2)

我逆向算法一把刷子都没有。

给了3个文件，难的逆向就喜欢联系上下文。that_girl是txt，里面写着同名歌曲的歌词；out是密文，那asong必定是要分析的对象了。

```c
undefined8 Main(void)

{
  void *pvVar1;
  void *input;
  
  pvVar1 = malloc(0xbc);
  input = malloc(0x50);
  Init();
  GetInput(input);
  CopyInput(input);
  FUN_00400aaa("that_girl",pvVar1);
  FUN_00400e54(input,pvVar1);
  return 0;
}
```

前三个函数没啥看的，不过CopyInput并不是完全拷贝，而是只复制flag格式中间的内容，QCTF{xxx}中的xxx。pvVar1在这些函数里都没有改变，看关键的两个函数。

```c
void FUN_00400aaa(char *that_girl,long param_2)

{
  int iVar1;
  ssize_t sVar2;
  int *piVar3;
  long in_FS_OFFSET;
  undefined local_15;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_14 = open(that_girl,0);
  while( true ) {
    sVar2 = read(local_14,&local_15,1);
    if (sVar2 != 1) break;
    iVar1 = FUN_00400936();
    piVar3 = (int *)(param_2 + (long)iVar1 * 4);
    *piVar3 = *piVar3 + 1;
  }
  close(local_14);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

local_14是打开的歌词文件，然后while循环每次读取文件的一个字节到local_15中。FUN_00400936根据参数的内容进行一些操作，操作本身倒不复杂。

```c
undefined * FUN_00400936(char param_1)

{
  undefined *puVar1;
  
  puVar1 = (&switchD_00400955::switchdataD_00401018)[(int)param_1 - 10U];
  switch((int)param_1 - 10U) {
  case 0:
    puVar1 = (undefined *)(ulong)((int)param_1 + 0x23);
    break;
  default:
    if ((param_1 < '0') || ('0' < param_1)) {
      if ((param_1 < 'A') || ('Z' < param_1)) {
        if (('`' < param_1) && (param_1 < '{')) {
          puVar1 = (undefined *)(ulong)((int)param_1 - 0x57);
        }
      }
      else {
        puVar1 = (undefined *)(ulong)((int)param_1 - 0x37);
      }
    }
    else {
      puVar1 = (undefined *)(ulong)((int)param_1 - 0x30);
    }
    break;
  case 0x16:
  case 0x17:
  case 0x18:
    puVar1 = (undefined *)(ulong)((int)param_1 + 10);
    break;
  case 0x1d:
    puVar1 = (undefined *)(ulong)((int)param_1 + 2);
    break;
  case 0x22:
    puVar1 = (undefined *)(ulong)((int)param_1 - 4);
    break;
  case 0x24:
    puVar1 = (undefined *)(ulong)((int)param_1 - 7);
    break;
  case 0x30:
  case 0x31:
    puVar1 = (undefined *)(ulong)((int)param_1 - 0x15);
    break;
  case 0x35:
    puVar1 = (undefined *)(ulong)((int)param_1 - 0x1b);
    break;
  case 0x55:
    puVar1 = (undefined *)(ulong)((int)param_1 - 0x31);
  }
  return puVar1;
}
```

唯一的问题是不知道传入了什么参数。提前看[wp](https://blog.csdn.net/wlz_lc_4/article/details/104888823)，对比发现参数是local_15。这种简单运算的加密一般逆向起来不难，看最后一个函数。

```c
void FUN_00400e54(char *param_1,long param_2)

{
  int iVar1;
  int iVar2;
  size_t sVar3;
  long in_FS_OFFSET;
  int i;
  undefined local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  sVar3 = strlen(param_1);
  iVar1 = (int)sVar3;
  for (i = 0; i < iVar1; i = i + 1) {
    iVar2 = FUN_00400936((int)param_1[i]);
    local_48[i] = (char)*(undefined4 *)(param_2 + (long)iVar2 * 4);
  }
  FUN_00400d33(local_48);
  FUN_00400db4(local_48,iVar1);
  WriteFile(local_48,&out,iVar1);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

FUN_00400936就是刚才看到switch函数，只用看下面两个就好了。

```c
void FUN_00400d33(undefined *param_1)

{
  undefined uVar1;
  int local_c;
  
  local_c = 0;
  uVar1 = *param_1;
  while (*(int *)(&DAT_006020a0 + (long)local_c * 4) != 0) {
    param_1[local_c] = param_1[*(int *)(&DAT_006020a0 + (long)local_c * 4)];
    local_c = *(int *)(&DAT_006020a0 + (long)local_c * 4);
  }
  param_1[local_c] = uVar1;
  return;
}
```

因为ghidra有几率在数组上识别错误，因此这里local_c*4的操作仅仅是遍历DAT_006020a0的每一个元素而已。

```c
void FUN_00400db4(byte *param_1,int param_2)

{
  byte bVar1;
  int local_c;
  
  bVar1 = *param_1;
  for (local_c = 0; local_c < param_2 + -1; local_c = local_c + 1) {
    param_1[local_c] = param_1[(long)local_c + 1] >> 5 | param_1[local_c] << 3;
  }
  param_1[local_c] = bVar1 >> 5 | param_1[local_c] << 3;
  return;
}
```

有亿点烦人的位运算，一直不懂是怎么逆向的。不过先不管，梳理程序流程才是重中之重。程序最开始获取输入，然后将输入的flag复制出中间的部分；第二步进入FUN_00400aaa，内部嵌套函数FUN_00400936会返回一个可逆向的值，这个值被用作param_2（main函数pvVar1）的索引，索引对应处自增1。注意此函数无需逆向，因为和输入没关系，结果是固定的，提前跑一下把对应关系记录下来就行了。第三步FUN_00400e54中第一个for循环和上一步作用相似，但这次需要逆向了，param_1是input。内部函数FUN_00400d33看起来不难，不过容易被绕晕。local_c作用等同于循环用的索引i，所以while循环的意思是param_1[i]=param_1[DAT_006020a0[i]]，i=DAT_006020a0[i]，条件为DAT_006020a0[i]!=0。最后的FUN_00400db4是位运算，local_c还是等于index i，param_1[i]=param_1[i+1]>>5|param_1[i]<<3，当前元素与下一个元素做位运算，大家肯定见过不知一次了。单纯位移运算的逆向很简单，>>的逆是<<，反之亦然；或不用管，照抄就是了。就是不知道for循环后的那行代码是什么意思，而且最后看wp脚本最后是要有个&0x7的，暂时不懂啥意思。

逆向就是字面意思，反着来。我们要先逆位运算，然后FUN_00400d33，然后FUN_00400e54中的for循环。位运算怎么逆已经说过了，FUN_00400d33怎么逆？总结我们已经有的，DAT_006020a0和改变后的param_1；local_c是索引，有却只有一半。关键在于还原加密完成后的状态，而索引并不是简单自增，所以现在我们还不知道加密完成那一刻的local_c是啥。这个简单，我们自己跑一下不就知道了？导出数组，然后执行一遍while循环的内容，得到真正的数组。这是给的wp的逆向思路，不过下面的[脚本](https://blog.csdn.net/qq_41071646/article/details/90043300)用了更简洁然而没那么好理解的逆法。

```python
#!/usr/bin/python3
# -*- coding:utf-8 -*-
s = [22, 0, 6, 2, 30, 24, 9, 1, 21, 7, 18, 10, 8, 12, 17, 23, 13, 4, 3, 14, 19, 11, 20, 16, 15, 5, 25, 36, 27, 28, 29, 37, 31, 32, 33, 26, 34, 35]
mapp={' ': 71, "'": 40, '_': 245, 'a': 104, 'c': 15, 'b': 30, 'e': 169, 'd': 29, 'g': 38, 'f': 19, 'i': 60, 'h': 67, 'k': 20, 'm': 28, 'l': 39, 'o': 165, 'n': 118, 'p': 26, 's': 51, 'r': 61, 'u': 45, 't': 133, 'w': 34, 'v': 7, 'y': 62}
def decypt():
    enc = open("out","rb").read()
    d0 = []
    temp = enc[len(enc)-1]& 0x7
    for i in range(len(enc)):
        d0.append((temp << 5) | (enc[i]) >> 3)
        temp = enc[i] & 0x7
 
    i = 37
    temp = d0[37]
    while s.index(i) != 37:
        d0[i] = d0[s.index(i)]
        i = s.index(i)
    d0[i] = temp
    flag = []
    for i in d0:
        flag.append(list(mapp.keys())[list(mapp.values()).index(i)])
    return "QCTF{%s}" % ''.join(flag)
print(decypt())
```

看了一个小时没搞懂中间FUN_00400d33怎么逆向的，最开始的i=37是哪里来的？不过mapp我知道，是提前根据switch那个函数做的映射表，可能这样更简单吧，因为你只用把原switch函数抄下来代入所有可能值运行，结果记录下来就能对应着逆向了。

### Flag
> QCTF{that_girl_saying_no_for_your_vindicate}