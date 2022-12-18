# [GUET-CTF2019]number_game

[题目地址](https://buuoj.cn/challenges#[GUET-CTF2019]number_game)

动调真的很重要。

```c
unsigned __int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 v4; // [rsp+8h] [rbp-38h]
  __int64 input; // [rsp+10h] [rbp-30h] BYREF
  __int16 v6; // [rsp+18h] [rbp-28h]
  __int64 v7; // [rsp+20h] [rbp-20h] BYREF
  __int16 v8; // [rsp+28h] [rbp-18h]
  char v9; // [rsp+2Ah] [rbp-16h]
  unsigned __int64 v10; // [rsp+38h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  input = 0LL;
  v6 = 0;
  v7 = 0LL;
  v8 = 0;
  v9 = 0;
  __isoc99_scanf("%s", &input);
  if ( (unsigned int)sub_4006D6((const char *)&input) )
  {
    v4 = sub_400758(&input, 0LL, 10LL);
    sub_400807(v4, &v7);
    v9 = 0;
    sub_400881(&v7);
    if ( (unsigned int)sub_400917() )
    {
      puts("TQL!");
      printf("flag{");
      printf("%s", (const char *)&input);
      puts("}");
    }
    else
    {
      puts("your are cxk!!");
    }
  }
  return __readfsqword(0x28u) ^ v10;
}
```

第一个函数`sub_4006D6`仅仅是判断输入是否在范围内。

```c
__int64 __fastcall sub_4006D6(const char *a1)
{
  __int64 result; // rax
  int i; // [rsp+1Ch] [rbp-4h]

  if ( strlen(a1) == 10 )
  {
    for ( i = 0; i <= 9; ++i )
    {
      if ( a1[i] > 52 || a1[i] <= 47 )          // 输入字符只能是0，1，2，3，4
        goto LABEL_2;
    }
    result = 1LL;
  }
  else
  {
LABEL_2:
    puts("Wrong!");
    result = 0LL;
  }
  return result;
}
```

接下来两个函数我看不懂但大受震撼。

```c
_QWORD *__fastcall sub_400758(__int64 a1, int a2, unsigned int a3)
{
  char v5; // [rsp+1Fh] [rbp-11h]
  _QWORD *v6; // [rsp+28h] [rbp-8h]
                                                // a1=input
                                                // a2=0
                                                // a3=10
  v5 = *(_BYTE *)(a2 + a1);
  if ( v5 == 32 || v5 == 10 || a2 >= (int)a3 )
    return 0LL;
  v6 = malloc(0x18uLL);
  *(_BYTE *)v6 = v5;
  v6[1] = sub_400758(a1, (unsigned int)(2 * a2 + 1), a3);
  v6[2] = sub_400758(a1, (unsigned int)(2 * (a2 + 1)), a3);
  return v6;
}
```

```c
__int64 __fastcall sub_400807(__int64 a1, __int64 a2)
{
  __int64 result; // rax

  result = a1;
  if ( a1 )
  {
    sub_400807(*(_QWORD *)(a1 + 8), a2);
    *(_BYTE *)(a2 + dword_601080++) = *(_BYTE *)a1;
    result = sub_400807(*(_QWORD *)(a1 + 16), a2);
  }
  return result;
}
```

看到`sub_400758`时本来还想着分析的，结果发现是个递归，完球，我不知道怎么逆向递归。看大佬的[wp](https://blog.csdn.net/qq_39542714/article/details/106834921)才知道是个二叉树，两个函数分别是一个二叉树的先序遍历和中序遍历，对字符数组中的下标进行排序。`sub_400758`函数将输入构造为先序遍历的二叉树，然后`sub_400807`将输入变换为中序遍历。接下来一个函数就是把中序遍历的结果填入数组。

```c
__int64 __fastcall sub_400881(char *a1)
{
  __int64 result; // rax

  byte_601062 = *a1;
  byte_601067 = a1[1];
  byte_601069 = a1[2];
  byte_60106B = a1[3];
  byte_60106E = a1[4];
  byte_60106F = a1[5];
  byte_601071 = a1[6];
  byte_601072 = a1[7];
  byte_601076 = a1[8];
  result = (unsigned __int8)a1[9];
  byte_601077 = a1[9];
  return result;
}
```

最后自然就是验证对不对了。

```c
__int64 sub_400917()
{
  unsigned int v1; // [rsp+0h] [rbp-10h]
  int i; // [rsp+4h] [rbp-Ch]
  int j; // [rsp+8h] [rbp-8h]
  int k; // [rsp+Ch] [rbp-4h]

  v1 = 1;
  for ( i = 0; i <= 4; ++i )
  {
    for ( j = 0; j <= 4; ++j )
    {
      for ( k = j + 1; k <= 4; ++k )
      {
        if ( *((_BYTE *)&unk_601060 + 5 * i + j) == *((_BYTE *)&unk_601060 + 5 * i + k) )
          v1 = 0;
        if ( *((_BYTE *)&unk_601060 + 5 * j + i) == *((_BYTE *)&unk_601060 + 5 * k + i) )
          v1 = 0;
      }
    }
  }
  return v1;
}
```

这是一个很明显的5\*5数据遍历逻辑（特征就是两个for循环嵌套，两个for循环的循环变量小于等于几就是几乘几）。但是k的加入让人一眼看上去不知道在比较什么，不过从最简单的情况开始，然后进入k的循环脑算就能知道在干啥了。当i=j=0，k=1时，第一个if语句比较索引0处是否等于索引1处；第二个if语句比较索引0处是否等于索引5处。当i=j=0，k=2时，第一个if语句比较索引0处是否等于索引2处；第二个if语句比较索引0处是否等于索引10处。结合这是个5\*5的数据，能看出是在判断某个位置的数据是否等于其所在行或者所在列的任何一个数据。数独的规则。把` `的数据用5\*5打印出来看看是啥。

```python
data='31 34 23 32 33 33 30 23 31 23 30 23 32 33 23 23 33 23 23 30 34 32 23 23 31'.split(' ')
for i in range(len(data)):
    if i%5==0:
        print()
    print(chr(int(data[i],16)),end='')
```

```
14#23
30#1#
0#23#
#3##0
42##1
```

#位置就是留着给我们填数独的了。得亏这还是个弱化版数独，可以用爆破的方式得到（刚才的wp），自己填也不是特别难，数字是`0,4,2,1,4,2,1,4,3,0`。问题在于，填好答案后，二叉树的变换那里怎么搞呢？怎么让我们填入的答案在经过二叉树变换后是正确的答案？一种方法是自己把先序遍历函数抄下来，参数输入0和10，查看其遍历后画出二叉树，再自己根据画出的二叉树得出中序遍历。第二种方法则是利用动调，比如这篇[wp](https://blog.csdn.net/Palmer9/article/details/104613420)，最开始输入就输入0123456789，然后patch掉最开始检查输入的函数，并在中序遍历函数那里下个断点，直接获取遍历结果。这里获取到的结果`7,3,8,1,9,4,0,5,2,6`是答案索引的对应关系，比如原来在索引0的要放到索引7去，原来在索引1的要放到索引3去。之后就能对照着获取flag了。

```python
data=[7,3,8,1,9,4,0,5,2,6]
answer='0421421430'
flag=[0]*10
for i in range(len(answer)):
    flag[data[i]]=answer[i]
    print(''.join(flag))
```

## Flag
> flag{1134240024}
