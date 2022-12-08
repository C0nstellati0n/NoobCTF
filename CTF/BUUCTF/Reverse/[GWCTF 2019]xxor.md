# [GWCTF 2019]xxor

[题目地址](https://buuoj.cn/challenges#[GWCTF%202019]xxor)

看了半天才告诉我不是tea？

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  int i; // [rsp+8h] [rbp-68h]
  int j; // [rsp+Ch] [rbp-64h]
  __int64 v6[6]; // [rsp+10h] [rbp-60h] BYREF
  __int64 v7[6]; // [rsp+40h] [rbp-30h] BYREF

  v7[5] = __readfsqword(0x28u);
  puts("Let us play a game?");
  puts("you have six chances to input");
  puts("Come on!");
  v6[0] = 0LL;
  v6[1] = 0LL;
  v6[2] = 0LL;
  v6[3] = 0LL;
  v6[4] = 0LL;
  for ( i = 0; i <= 5; ++i )
  {
    printf("%s", "input: ");
    __isoc99_scanf("%d", (char *)v6 + 4 * i);
  }
  v7[0] = 0LL;
  v7[1] = 0LL;
  v7[2] = 0LL;
  v7[3] = 0LL;
  v7[4] = 0LL;
  for ( j = 0; j <= 2; ++j )
  {
    dword_601078 = v6[j];
    dword_60107C = HIDWORD(v6[j]);  //看起来取的是一个东西，实际上是两个值。dword_601078是低位，dword_60107C是高位，它们是不同的值。
    sub_400686((unsigned int *)&dword_601078, dword_601060);  //这里只传了一个进去，不过注意传的是地址，可以获取到相邻的dword_60107C
    LODWORD(v7[j]) = dword_601078;
    HIDWORD(v7[j]) = dword_60107C;
  }
  if ( (unsigned int)sub_400770(v7) != 1 )
  {
    puts("NO NO NO~ ");
    exit(0);
  }
  puts("Congratulation!\n");
  puts("You seccess half\n");
  puts("Do not forget to change input to hex and combine~\n");
  puts("ByeBye");
  return 0LL;
}
```

main函数获取输入，加密过程都是在`sub_400686`中完成的。

```c
__int64 __fastcall sub_400686(unsigned int *a1, _DWORD *a2)
{
  __int64 result; // rax
  unsigned int v3; // [rsp+1Ch] [rbp-24h]
  unsigned int v4; // [rsp+20h] [rbp-20h]
  int v5; // [rsp+24h] [rbp-1Ch]
  unsigned int i; // [rsp+28h] [rbp-18h]

  v3 = *a1;
  v4 = a1[1];
  v5 = 0;
  for ( i = 0; i <= 63; ++i )
  {
    v5 += 1166789954;  //v5每次加这么多，逆向时就要从其64倍开始逆，然后每次-=这么多
    v3 += (v4 + v5 + 11) ^ ((v4 << 6) + *a2) ^ ((v4 >> 9) + a2[1]) ^ 0x20;    //逆向这段这么看。不要理后面那段烦人的逻辑，就看成v3+=x。逆向肯定就是v3-=x了。第二步再判断当时加密时用的是什么值，参与加密的值是v4，且是原值。*a2代表a2[0]，那逆向先找到v4的原值直接套进去就行了
    v4 += (v3 + v5 + 20) ^ ((v3 << 6) + a2[2]) ^ ((v3 >> 9) + a2[3]) ^ 0x10;  //这段同理，只不过参与v4加密的是v3的加密值。告诉我们要从v4逆起，逆出来v4的原值后就能找到v3的原值了
  }
  *a1 = v3;
  result = v4;
  a1[1] = v4;
  return result;
}
```

最后当然还有个比较函数。

```c
__int64 __fastcall sub_400770(_DWORD *a1)
{
  __int64 result; // rax

  if ( a1[2] - a1[3] == 0x84A236FFLL
    && a1[3] + a1[4] == 0xFA6CB703LL
    && a1[2] - a1[4] == 0x42D731A8LL
    && *a1 == 0xDF48EF7E
    && a1[5] == 0x84F30420
    && a1[1] == 0x20CAACF4 )
  {
    puts("good!");
    result = 1LL;
  }
  else
  {
    puts("Wrong!");
    result = 0LL;
  }
  return result;
}
```

函数不多，不过检查函数要用z3跑一下看看值。

```python
from z3 import *
a0, a1, a2, a3, a4, a5 = Ints('a0 a1 a2 a3 a4 a5')
s = Solver()
s.add(a2 - a3 == 0x84A236FF)
s.add(a3 + a4 == 0xFA6CB703)
s.add(a2 - a4 == 0x42D731A8)
s.add(a0 == 0xDF48EF7E)
s.add(a5 == 0x84F30420)
s.add(a1 == 0x20CAACF4)
if s.check() == sat:
    print(s.model())
```

根据[wp](https://blog.csdn.net/m0_71081503/article/details/125743375)所说，如果程序内用的是无类型数，z3求解时最好转成16进制。因为两者会计算出不一样的结果，16进制算出来正确的概率较高。接着就能逆向加密算法了。我看整个算法特征很像tea，就没细想直接用了之前的脚本，结果解密出一堆妖魔鬼怪。之后发现并不是，不过逆向思路很像。

```c
#include <stdio.h>
int main()
{
    int a1[6] = { 3746099070,550153460,3774025685,1548802262,2652626477,2230518816 };  //z3解出来的
    unsigned int a2[4] = { 2,2,3,4 };   //查看main的调用可以知道a2是dword_601060，这是里面的值
    unsigned int v3;
    unsigned int v4;
    int v5;
    for (unsigned int j = 0; j < 5; j += 2)   //正好循环3次，每次能取出2个
    {
        v3 = a1[j];   //取出第一个
        v4 = a1[j + 1];   //取出第二个
        v5 = 1166789954 * 64;   //从64倍开始
        for (unsigned int i = 0; i < 64; i++)
        {
            v4 -= (v3 + v5 + 20) ^ ((v3 << 6) + a2[2]) ^ ((v3 >> 9) + a2[3]) ^ 0x10;  //就跟上面一模一样，根本不用考虑那么多
            v3 -= (v4 + v5 + 11) ^ ((v4 << 6) + *a2) ^ ((v4 >> 9) + a2[1]) ^ 0x20;
            v5 -= 1166789954;  //减去固定值
        }
        a1[j] = v3;
        a1[j + 1] = v4;
    }//小端序
    for (unsigned int i = 0; i < 6; i++)
        printf("%c%c%c", *((char*)&a1[i] + 2), *((char*)&a1[i] + 1), *(char*)&a1[i]);  //按小端序输出
}
```

这个脚本很有意思的地方在于这些值放进c语言编译器里是会提示溢出的，然而溢出后也能算出来正确的值。

## Flag
> flag{re_is_great!}