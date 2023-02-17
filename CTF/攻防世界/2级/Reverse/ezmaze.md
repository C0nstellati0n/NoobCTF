# ezmaze

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=8254ba70-6bfd-11ed-ab28-000c29bc20bf&task_category_id=4)

看看main。

```c
__int64 __fastcall main()
{
  _main();
  printf("Welcome to the maze game. Try to get out of the maze and get the flag.\n");
  initmap();
  text_55("%s", Input);
  if ( check(Input) )
    printf("Congratulations on coming out of the maze! The flag is 'flag{your input}'\n");
  else
    printf("What a pity. You're still trapped in the maze :(\n");
  system("pause");
  return 0i64;
}
```

内部调用了check，这才是关键函数。

```c
bool __fastcall check(char *ch_0)
{
  int v2; // eax
  char *v3; // rcx
  unsigned int x; // er8
  unsigned int y; // edx
  char *v6; // r11
  char v7; // al

  v2 = strlen(ch_0);
  if ( v2 > 0 )
  {
    v3 = ch_0;
    x = 0;
    y = 0;
    v6 = &ch_0[v2 - 1 + 1];
    while ( 1 )
    {
      v7 = *v3;
      if ( *v3 == 's' )
      {
        ++y;
      }
      else if ( v7 > 's' )
      {
        if ( v7 != 'w' )
          return 0;
        --y;
      }
      else if ( v7 == 'a' )
      {
        --x;
      }
      else
      {
        if ( v7 != 'd' )
          return 0;
        ++x;
      }
      if ( !realmap[10 * y + x] || y > 9 || x > 9 )
        break;
      if ( v6 == ++v3 )
        return x == 9 && y == 9;
    }
  }
  return 0;
}
```

迷宫题关键点在于：

1. 找到迷宫地图，确定其排版
2. 确定指令代表的操作，确定起点和终点

这两点搞清楚了就没什么难的了（基本的迷宫题）。对于第一点，我们发现check中明显有个realmap，点进去发现是空的。按x找交叉引用，发现是在initmap中初始化的。跟我们的输入没关系的函数统统不看，直接动调取map。用ida在调用initmap后双击realmap，shift+e就能提取内容了。

至于排版，我们发现取realmap索引时是`10*y+x`。这里我重命名过变量，不过只要记住，和某个数字相乘的一定是y，加上的一定是x。同时if语句要求x和y都不能大于9，说明地图宽10（索引从0开始）。写个脚本打印出地图。

```python
d='01 00 00 00 01 00 00 01 00 00 01 01 01 00 00 00 00 01 01 01 00 00 01 00 00 01 01 01 00 01 01 01 01 01 01 01 00 00 00 01 01 00 01 00 00 00 00 01 01 01 01 00 01 01 00 00 01 01 00 00 01 00 00 01 00 00 01 00 00 00 01 01 01 00 00 00 01 01 01 00 01 00 00 00 00 00 01 00 00 00 01 01 01 01 00 00 01 01 01 01'.split(' ')
print(d[0][1:],end='')
for i in range(1,len(d)):
    print(d[i][1:],end='')
    if i%10==9:
        print()
```

```
1000100100
1110000111
0010011101
1111110001
1010000111
1011001100
1001001000
1110001110
1000001000
1111001111
```

y和x的初始值都是0，说明起点就在(0,0)。`return x==9 && y==9`，说明终点在(9,9)。指令操作都很明确，正常的wasd。那手动走一下迷宫就好了。

## Flag
> flag{sddssdddwddwddsssaasassssddd}