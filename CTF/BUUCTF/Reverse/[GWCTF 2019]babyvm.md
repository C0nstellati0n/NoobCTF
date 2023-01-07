# [GWCTF 2019]babyvm

[题目地址](https://buuoj.cn/challenges#[GWCTF%202019]babyvm)

第一次遇到vm类型的题。

```c
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  __int64 v3[2]; // [rsp+10h] [rbp-10h] BYREF

  v3[1] = __readfsqword(0x28u);
  v3[0] = 0LL;
  puts("Please input something:");
  SetFunction((__int64)v3);
  run((__int64)v3);
  FakeCheck();
  puts("And the flag is GWHT{true flag}");
  exit(0);
}
```

这里给出的flag绝对是假的。根据这篇[文章](https://blog.csdn.net/weixin_43876357/article/details/108570305)，因为虚拟机是出题人自己实现的，会使用自定义机器码，所以必定有一个函数规定这些机器码对应什么操作。SetFunction正是这样一个函数。

```c
unsigned __int64 __fastcall SetFunction(__int64 a1)
{
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  *(_DWORD *)a1 = 0;
  *(_DWORD *)(a1 + 4) = 18;
  *(_DWORD *)(a1 + 8) = 0;
  *(_DWORD *)(a1 + 12) = 0;
  *(_QWORD *)(a1 + 16) = &optcode;
  *(_BYTE *)(a1 + 24) = 0xF1;                   // 0xF1对应mov，剩下的类似。先设置操作码再设置函数
  *(_QWORD *)(a1 + 32) = mov;
  *(_BYTE *)(a1 + 40) = 0xF2;
  *(_QWORD *)(a1 + 48) = xor;
  *(_BYTE *)(a1 + 56) = 0xF5;
  *(_QWORD *)(a1 + 64) = JudgeLength;
  *(_BYTE *)(a1 + 72) = 0xF4;
  *(_QWORD *)(a1 + 80) = nop;
  *(_BYTE *)(a1 + 88) = 0xF7;
  *(_QWORD *)(a1 + 96) = mul;
  *(_BYTE *)(a1 + 104) = 0xF8;
  *(_QWORD *)(a1 + 112) = swap;
  *(_BYTE *)(a1 + 120) = 0xF6;
  *(_QWORD *)(a1 + 128) = linearCalculation;
  res = malloc(0x512uLL);
  memset(res, 0, 0x512uLL);
  return __readfsqword(0x28u) ^ v2;
}
```

第一次做这种题的我哪里知道这是什么，看[wp](https://blog.csdn.net/m0_46296905/article/details/116374983)也没有讲怎么得到的对应关系。后来我想了一下，一是可以动调看，二是可以乱推理一番。操作码和函数的设置肯定是对应关系，无非是先操作码还是先函数的关系。如果是先函数，剩下的最上方的0xF1和最下方的linearCalculation怎么看都不像能配上对的关系，因此是先操作码先函数。把这些函数都看一遍。

```c
unsigned __int64 __fastcall mov(__int64 a1)
{
  int *v2; // [rsp+28h] [rbp-18h]
  unsigned __int64 v3; // [rsp+38h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  v2 = (int *)(*(_QWORD *)(a1 + 16) + 2LL);     // 这里v2结合下方的res+*v2，应该是索引的用处
  switch ( *(_BYTE *)(*(_QWORD *)(a1 + 16) + 1LL) )
  {
    case 0xE1:                                  // E1，E2等是寄存器，或者说是操作，对应怎么处理res，是放到a1的某个位置还是把a1的某个位置放进a1。res是内存，也是最终加密结果的存储地
      *(_DWORD *)a1 = *((char *)res + *v2);
      break;
    case 0xE2:
      *(_DWORD *)(a1 + 4) = *((char *)res + *v2);
      break;
    case 0xE3:
      *(_DWORD *)(a1 + 8) = *((char *)res + *v2);
      break;
    case 0xE4:
      *((_BYTE *)res + *v2) = *(_DWORD *)a1;
      break;
    case 0xE5:
      *(_DWORD *)(a1 + 12) = *((char *)res + *v2);
      break;
    case 0xE7:
      *((_BYTE *)res + *v2) = *(_DWORD *)(a1 + 4);
      break;
    default:
      break;
  }
  *(_QWORD *)(a1 + 16) += 6LL;
  return __readfsqword(0x28u) ^ v3;
}
```

mov和我们所理解的mov不一样，后面跟的两个操作数表示“怎么处理res”和“处理res的哪一个字符”。比如`F1 E1 1`表示“把res[1]存入a1。

```c
unsigned __int64 __fastcall xor(__int64 a1)
{
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  *(_DWORD *)a1 ^= *(_DWORD *)(a1 + 4);         // 两个操作数相差4
  ++*(_QWORD *)(a1 + 16);
  return __readfsqword(0x28u) ^ v2;
}
```

xor这里注意两个操作数相差4，并把结果存入第一个操作数。这个到时候结合操作码看会比较清楚。

```c
unsigned __int64 __fastcall JudgeLength(__int64 a1)
{
  const char *buf; // [rsp+10h] [rbp-10h]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  buf = (const char *)res;
  read(0, res, 0x20uLL);                        // 程序输入点，将input输入到res中
  dword_2022A4 = strlen(buf);
  if ( dword_2022A4 != 21 )
  {
    puts("WRONG!");
    exit(0);
  }
  ++*(_QWORD *)(a1 + 16);
  return __readfsqword(0x28u) ^ v3;
}
```

检查输入长度，同时也是获取输入的函数。

```c
unsigned __int64 __fastcall nop(__int64 a1)
{
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  ++*(_QWORD *)(a1 + 16);
  return __readfsqword(0x28u) ^ v2;
}
```

nop啥也不干，对应操作码F4。不过结合接下来的run函数，这个函数应该是ret的意思，总之虚拟机一旦读到这个指令就停止运行。

```c
unsigned __int64 __fastcall run(__int64 a1)
{
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  *(_QWORD *)(a1 + 16) = &optcode;
  while ( **(_BYTE **)(a1 + 16) != 0xF4 )
    sub_E6E(a1);
  return __readfsqword(0x28u) ^ v2;
}
```

run函数内部调用了的另一个函数才是实际执行运行的函数。不过我真看不懂它是怎么实现的。

```c
unsigned __int64 __fastcall sub_E6E(__int64 a1)
{
  int i; // [rsp+14h] [rbp-Ch]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  for ( i = 0; **(_BYTE **)(a1 + 16) != *(_BYTE *)(16 * (i + 1LL) + a1 + 8); ++i )
    ;
  (*(void (__fastcall **)(__int64))(16 * (i + 1LL) + a1 + 16))(a1);// 看不明白是怎么实现的，但肯定是通过操作码调用对应的函数
  return __readfsqword(0x28u) ^ v3;
}
```

FakeCheck是假的检查逻辑，就不看了。真正的还要看RealCheck。这个函数没找到引用，经典搞心态。

```c
unsigned __int64 RealCheck()
{
  int i; // [rsp+Ch] [rbp-14h]
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  for ( i = 0; dword_2022A4 - 1 > i; ++i )
  {
    if ( *((_BYTE *)res + i) != byte_202020[i] )
      exit(0);
  }
  return __readfsqword(0x28u) ^ v2;
}
```

现在就是把optcode里面的内容拿出来翻译了。wp里写的很详细，这里我截取一段困扰了我一会的地方。

```
	0xf1,0xe1,0x5,0x0,0x0,0x0,#r1 = flag[5] //E1寄存器是a1
	0xf1,0xe2,0x6,0x0,0x0,0x0,#r2 = flag[6] //E2寄存器是a1+4
	0xf2,#r1 = r1^r2 //f2是xor。在xor里面我们知道两个操作数相隔4，里面的实现就是*a1^=*(a1+4)，或许不仅两个操作数相隔4，两个操作数可能只能是e1和e2？
	0xf1,0xe4,0x5,0x0,0x0,0x0,#stack[5] = r1

	0xf1,0xe1,0x6,0x0,0x0,0x0,#r1 = flag[6]
	0xf1,0xe2,0x7,0x0,0x0,0x0,#r2 = flag[7]
	0xf1,0xe3,0x8,0x0,0x0,0x0,#r3 = flag[8]
	0xf1,0xe5,0xC,0x0,0x0,0x0,#r4 = flag[12]
	0xf6, #r1 = (3*r1+2*r2+r3) //再看linearCalculation里的运算。a1=(a1+8)+2*(a1+4)+3*a1，完全和这里一样。或许这些操作都是限定寄存器的。
	0xf7, #r1 = r1*r4
	0xf1,0xe4,0x6,0x0,0x0,0x0,#stack[6] = r1
```

然后跟着大佬将翻译出来的机器码对应的操作逆向就好了。加密逻辑非常简单，先异或再线性运算最后交换，那反过来先交换再线性运算最后异或就是答案了。

```python
from z3 import *
a=Real('a')
b=Real('b')
c=Real('c')

byte=[0x69, 0x45, 0x2A, 0x37, 0x09, 0x17, 0xC5, 0x0B, 0x5C, 0x72, 0x33, 0x76, 0x33, 0x21, 0x74, 0x31, 0x5F, 0x33, 0x73, 0x72,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]

temp=byte[15]
byte[15]=byte[17]
byte[17]=temp

temp=byte[14]
byte[14]=byte[18]
byte[18]=temp

temp=byte[13]
byte[13]=byte[19]
byte[19]=temp
solve((3*a+2*b+c)*0x33==0x6dc5,(3*b+2*c+0x72)*0x33==0x5b0b,(3*c+2*0x72+0x33)*0x33==0x705c)
#a = 118,b = 51,c = 95

byte[6] = 118
byte[7] = 51
byte[8] = 95

byte[5]^=(byte[6])
byte[4]^=(byte[5])
byte[3]^=(byte[4])
byte[2]^=(byte[3])
byte[1]^=(byte[2])
byte[0]^=(byte[1])

flag=''
for i in range(32):
	flag+=chr(byte[i])
print(flag)
```

## Flag
> flag{Y0u_hav3_r3v3rs3_1t!}