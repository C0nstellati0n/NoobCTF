# [GXYCTF2019]simple CPP

[题目地址](https://buuoj.cn/challenges#[GXYCTF2019]simple%20CPP)

一扯到内存操作字符串我就懵了。

这题搞清逻辑后看的就是眼力。main函数大大一个，不写注释记录进度很容易看晕。

```c++
int __cdecl main(int argc, const char **argv, const char **envp)
{
  bool v3; // si
  __int64 v4; // rax
  unsigned __int8 *v5; // rax
  unsigned __int8 *v6; // rbx
  int v7; // er10
  __int64 v8; // r11
  void **v9; // r9
  void **v10; // r8
  __int64 v11; // rdi
  __int64 v12; // r15
  __int64 v13; // r12
  __int64 v14; // rbp
  int v15; // ecx
  unsigned __int8 *v16; // rdx
  __int64 v17; // rdi
  __int64 *v18; // r14
  __int64 v19; // rbp
  __int64 v20; // r13
  __int64 *v21; // rdi
  __int64 v22; // r12
  __int64 v23; // r15
  __int64 v24; // rbp
  __int64 v25; // rdx
  __int64 v26; // rbp
  __int64 v27; // rbp
  __int64 v28; // r10
  __int64 v29; // rdi
  __int64 v30; // r8
  bool v31; // dl
  __int64 v32; // rax
  void **v33; // rdx
  const char *v34; // rax
  __int64 v35; // rax
  void *v36; // rcx
  __int64 v38; // [rsp+20h] [rbp-68h]
  void *input[2]; // [rsp+30h] [rbp-58h] BYREF
  unsigned __int64 v40; // [rsp+40h] [rbp-48h]
  unsigned __int64 v41; // [rsp+48h] [rbp-40h]

  v3 = 0;
  v40 = 0i64;
  v41 = 15i64;
  LOBYTE(input[0]) = 0;
  LODWORD(v4) = printf(std::cout, "I'm a first timer of Logic algebra , how about you?", envp);
  std::ostream::operator<<(v4, sub_140001B90);
  printf(std::cout, "Let's start our game,Please input your flag:");
  scanf(std::cin, input);
  std::ostream::operator<<(std::cout, sub_140001B90);
  if ( v40 - 5 > 0x19 )
  {
    LODWORD(v35) = printf(std::cout, "Wrong input ,no GXY{} in input words");
    std::ostream::operator<<(v35, sub_140001B90);
    goto LABEL_43;
  }
  v5 = (unsigned __int8 *)operator new(0x20ui64);
  v6 = v5;
  if ( v5 )
  {
    *(_QWORD *)v5 = 0i64;
    *((_QWORD *)v5 + 1) = 0i64;
    *((_QWORD *)v5 + 2) = 0i64;
    *((_QWORD *)v5 + 3) = 0i64;
  }
  else
  {
    v6 = 0i64;
  }
  v7 = 0;
  if ( v40 )
  {
    v8 = 0i64;
    do
    {
      v9 = input;
      if ( v41 >= 0x10 )
        v9 = (void **)input[0];
      v10 = &qword_140006048;
      if ( (unsigned __int64)qword_140006060 >= 0x10 )
        v10 = (void **)qword_140006048;
      v6[v8] = *((_BYTE *)v9 + v8) ^ *((_BYTE *)v10 + v7 % 27);// input->异或->v6
      ++v7;
      ++v8;
    }
    while ( v7 < v40 );
  }
  v11 = 0i64;
  v12 = 0i64;
  v13 = 0i64;
  v14 = 0i64;
  if ( (int)v40 > 30 )
    goto LABEL_27;
  v15 = 0;
  if ( (int)v40 <= 0 )
    goto LABEL_27;
  v16 = v6;                                     // input->v6->v16
  do
  {
    v17 = *v16 + v11;                           // v11这里并不是索引，而是上一次取出的字符移到高位的结果。*v16是当前字符，v17是结果
    ++v15;
    ++v16;                                      // v16代表了input的起始地址，每次都会自增，所以每次循环一顶会取出不一样的字符
    switch ( v15 )
    {
      case 8:                                   // 4个case对应分成4份
        v14 = v17;
        goto LABEL_23;
      case 16:
        v13 = v17;
        goto LABEL_23;
      case 24:
        v12 = v17;
LABEL_23:
        v17 = 0i64;                             // 清0
        break;
      case 32:
        printf(std::cout, "ERRO,out of range");
        exit(1);
    }
    v11 = v17 << 8;                             // 这里更新v11，把v17左移8位。64位里面一个字符就是8位，此举将之前v17内的字符移到高位，结合上面v17=*v16+v11，整个逻辑将输入转为数字，分为4份存入各变量个
  }                                             // 假设输入的两个字符转为数字分别为0x12和0x34。第一次取出0x12，v17=*v16+v11等同于v17=0x12+0。第二次取出0x34，如果直接0x12+0x34肯定不对，所以(0x12<<8)+0x34，这样的结果就是0x1234了
  while ( v15 < (int)v40 );
  if ( v14 )
  {
    v18 = (__int64 *)operator new(0x20ui64);
    *v18 = v14;                                 // 刚刚转换的结果统一存入v18数组
    v18[1] = v13;
    v18[2] = v12;
    v18[3] = v11;
    goto LABEL_28;
  }
LABEL_27:
  v18 = 0i64;
LABEL_28:
  v38 = v18[2];
  v19 = v18[1];
  v20 = *v18;
  v21 = (__int64 *)operator new(0x20ui64);
  if ( IsDebuggerPresent() )                    // 反调试，不过一个patch就弄掉了
  {
    printf(std::cout, "Hi , DO not debug me !");
    Sleep(0x7D0u);
    exit(0);
  }
  v22 = v19 & v20;                              // 这一段先不用急着分析，看下面有没有直接的比较可以得出v18数组的正确值
  *v21 = v19 & v20;
  v23 = v38 & ~v20;                             // v20=v18[0],v38=v18[2]
  v21[1] = v23;
  v24 = ~v19;
  v25 = v38 & v24;
  v21[2] = v38 & v24;
  v26 = v20 & v24;
  v21[3] = v26;
  if ( v23 != 1176889593874i64 )                // 不要漏了这个约束
  {
    v21[1] = 0i64;
    v23 = 0i64;
  }
  v27 = v23 | v22 | v25 | v26;
  v28 = v18[1];
  v29 = v18[2];
  v30 = v25 & *v18 | v29 & (v22 | v28 & ~*v18 | ~(v28 | *v18));
  v31 = 0;
  if ( v30 == 577031497978884115i64 )           // 一个约束
    v31 = v27 == 4483974544037412639i64;        // 这也是一个约束
  if ( (v27 ^ v18[3]) == 4483974543195470111i64 )// 这里有一个可供z3的约束
    v3 = v31;
  if ( (v23 | v22 | v28 & v29) == (~*v18 & v29 | 864693332579200012i64) && v3 )// 看起来可用z3约束求解，那么就要找约束，这里有一个
  {
    LODWORD(v32) = printf(std::cout, "Congratulations!flag is GXY{");
    v33 = input;
    if ( v41 >= 0x10 )
      v33 = (void **)input[0];
    v34 = (const char *)sub_140001FD0(v32, v33, v40);
    printf(v34, "}");
    j_j_free(v6);
  }
  else
  {
    printf(std::cout, "Wrong answer!try again");
    j_j_free(v6);
  }
LABEL_43:
  if ( v41 >= 0x10 )
  {
    v36 = input[0];
    if ( v41 + 1 >= 0x1000 )
    {
      v36 = (void *)*((_QWORD *)input[0] - 1);
      if ( (unsigned __int64)(input[0] - v36 - 8) > 0x1F )
        invalid_parameter_noinfo_noreturn();
    }
    j_j_free(v36);
  }
  return 0;
}
```

关于最开始那个把输入分为4份转为数字那里，做个简单的实验就清晰好懂了。以后看到这种不熟悉的真的是做实验最好，一目了然。

```python
a=0x12
b=0x34
print(hex(a+b)) #错误的方法
#0x46
print(hex((a<<8)+b)) #正确的方法
#0x1234
```

中间的逻辑确实是有点难分辨，几个变量互相赋值，最后if语句比较的是谁还得往上找。几个if并没有直接使用v18数组的值，需要我们自己仔细看逻辑转换为v18数组相关值。总之我是没看下去，跑去抄[wp](https://www.cnblogs.com/LLeaves/p/13522069.html)。

```python
# -*- coding:utf-8 -*-

from z3 import *

debug_str = "i_will_check_is_debug_or_not"
x,y,z,w=BitVecs('x y z w',64)

s=Solver()

s.add((~x)&z==1176889593874)
s.add(((z&~x)|(x&y)|(z&(~y))|(x&(~y)))^w==4483974543195470111)
s.add(((z&~y)&x|z&((x&y)|y&~x|~(y|x)))==577031497978884115)
s.add(((z&~x)|(x&y)|(z&~y)|(x&~y))==4483974544037412639)
s.add(((z&(~x)) | (x&y) | y & z) == (((~x)& z)|864693332579200012))

s.check()
m = s.model()
for i in m:
    print("%s = 0x%x"%(i,m[i].as_long()))
flag=""
li=[]
# 拼接
li.append(hex(m[x].as_long())[2:])
li.append(hex(m[y].as_long())[2:])
li.append(hex(m[z].as_long())[2:])
li.append(hex(m[w].as_long())[2:-2])
print(li)
```

这样就求出来了v18数组的值。距离真正的输入还差一个异或，异或值应该是`qword_140006048`，但是点进去发现是0。不可能，找找交叉引用，在这里找到了赋值（仅截取末尾的一段)。

```c++
LABEL_26:
    invalid_parameter_noinfo_noreturn();
  qword_140006058 = a3;
  v5 = &qword_140006048;
  if ( (unsigned __int64)qword_140006060 >= 0x10 )
    v5 = (void **)qword_140006048;
  memmove(v5, "i_will_check_is_debug_or_not", a3);// 这里将i_will_check_is_debug_or_not赋值给qword_140006048
  *((_BYTE *)v5 + a3) = 0;
  return &qword_140006048;
```

key是`i_will_check_is_debug_or_not`,可以解flag了。

```python
Dst = 'i_will_check_is_debug_or_noi_wil'
flag=[0x3E,0x3A,0x46,0x05,0x33,0x28,0x6F,0x0D,0x8C,0x00,0x8A,0x09,0x78,0x49,0x2C,0xAC,0x08,0x02,0x07,0x17,0x15,0x3E,0x30,0x13,0x32,0x31,0x06]
s=''
for i in range(len(flag)):
    s+=chr(ord(Dst[i]) ^ flag[i])
print(s)
```

解出来是乱码。这是因为就算我们有5个约束，出来的解仍然不唯一。这次约束求出来的可能不对，可以用while循环让z3一直输出，找到那个正确的值再异或就是flag。

## Flag
> flag{We1l_D0ne!P0or_algebra_am_i}