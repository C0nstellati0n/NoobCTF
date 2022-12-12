# [ACTF新生赛2020]Oruga

[题目地址](https://buuoj.cn/challenges#[ACTF%E6%96%B0%E7%94%9F%E8%B5%9B2020]Oruga)

新品种迷宫题get！

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 result; // rax
  int i; // [rsp+0h] [rbp-40h]
  char s1[6]; // [rsp+4h] [rbp-3Ch] BYREF
  char s2[6]; // [rsp+Ah] [rbp-36h] BYREF
  char s[40]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v8; // [rsp+38h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  memset(s, 0, 0x19uLL);
  printf("Tell me the flag:");
  scanf("%s", s);
  strcpy(s2, "actf{");
  for ( i = 0; i <= 4; ++i )
    s1[i] = s[i];
  s1[5] = 0;
  if ( !strcmp(s1, s2) )
  {
    if ( sub_78A((__int64)s) )
      printf("That's True Flag!");
    else
      printf("don't stop trying...");
    result = 0LL;
  }
  else
  {
    printf("Format false!");
    result = 0LL;
  }
  return result;
}
```

main函数检查了一个flag前缀，重点都在`sub_78A`里。

```c
_BOOL8 __fastcall sub_78A(__int64 a1)
{
  int v2; // [rsp+Ch] [rbp-Ch]
  int v3; // [rsp+10h] [rbp-8h]
  int v4; // [rsp+14h] [rbp-4h]

  v2 = 0;
  v3 = 5;
  v4 = 0;
  while ( byte_201020[v2] != '!' )
  {
    v2 -= v4;
    if ( *(_BYTE *)(v3 + a1) != 'W' || v4 == -16 )// 这里的判断有点奇怪，不过注意到if语句里用了“不等于某某数据”，那就应该看else里的内容
    {
      if ( *(_BYTE *)(v3 + a1) != 'E' || v4 == 1 )
      {
        if ( *(_BYTE *)(v3 + a1) != 'M' || v4 == 16 )
        {
          if ( *(_BYTE *)(v3 + a1) != 'J' || v4 == -1 )
            return 0LL;                         // 判断了4个数据，加上4个选项中两个两个一组。每组之间是相反的关系，这是迷宫题的特征之一
          v4 = -1;
        }
        else
        {
          v4 = 16;
        }
      }
      else
      {
        v4 = 1;
      }
    }
    else
    {
      v4 = -16;
    }
    ++v3;
    while ( !byte_201020[v2] )                  // 那么这就是迷宫地图了
    {
      if ( v4 == -1 && (v2 & 0xF) == 0 )        // 这里看了好久不知道在干啥，但是意识到是迷宫题时就能猜一下了。结合实验，0&0xf=0，16&0xf=0，32&0xf=0，这个是判断是否在地图最左侧。v4=-1代表往左走，整个判断的意思是“如果在地图最左侧，就不能往左走
        return 0LL;
      if ( v4 == 1 && v2 % 16 == 15 )           // 类似地，这个肯定就是判断在地图最右侧时不能往右走了
        return 0LL;
      if ( v4 == 16 && (unsigned int)(v2 - 240) <= 0xF )// 整个地图是16*16=256，如果当前在最后一行，256-240就会小于15。这里判断如果在最后一行，就不能往下走
        return 0LL;
      if ( v4 == -16 && (unsigned int)(v2 + 15) <= 0x1E )// 类似地，如果在第一行，就不能往上走
        return 0LL;
      v2 += v4;                                 // 加一个v4就向指定方向移动。因为放在了while循环了，就会一直向前移动，直到前方不是0，即有障碍物
    }
  }
  return *(_BYTE *)(v3 + a1) == '}';
}
```

迷宫题最重要的步骤恐怕就是确认迷宫地图长什么样了。有时候知道地图长什么样了以后，就算有些逻辑看不懂都能照着地图猜出来。比如这里，地图是直接摆好在hex里面的，打开ida自带的hex窗口查看变量就是了。或者可以直接跟这篇wp(https://blog.nowcoder.net/n/98e4ae74bb164256983440455ea7726d)一样，用更好看的方式打印出地图。照着地图就能自己走出迷宫了，比一般的难，搞懂了规则还是可以的。就是选好了一个方向后就会一直往哪个方向移动，直到撞到障碍物。

简单的迷宫题个人觉得遵循下面的步骤：

1. 找到地图。不是所有题都跟这题一样迷宫这么明显的，要根据程序的逻辑判断出来。这里碰巧hex view是16\*16，迷宫也是16\*16，才能直接看。如果不是就要自己推断了，通常程序里都有线索的。
2. 通常加的数值小的一对是左右，大的一对是上下。比如这题，有1，-1和16，-16这两组。明显后面的更大，控制上下。这里也可以当作推断迷宫地图的线索，因为走上下是加16和减16，说明地图宽是16。然后就能根据地图的总大小除出来长了。

## Flag
> flag{MEWEMEWJMEWJM}