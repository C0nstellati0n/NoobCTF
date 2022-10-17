# Windows_Reverse2

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f02bfcf0-bba1-4b23-8081-6371f173b078_2)

这题不知道为啥有两个版本的wp，一个超级复杂，一个5行代码不到。

拖进ghidra，一看就有壳。我还是没有下载脱壳工具，于是网上找了[wp](https://www.cnblogs.com/DirWang/p/12347399.html)的代码。

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char Dest; // [esp+8h] [ebp-C04h]
  char v5; // [esp+9h] [ebp-C03h]
  char myinput; // [esp+408h] [ebp-804h]
  char Dst; // [esp+409h] [ebp-803h]
  char tg; // [esp+808h] [ebp-404h]
  char v9; // [esp+809h] [ebp-403h]

  myinput = 0;
  memset(&Dst, 0, 0x3FFu);
  tg = 0;
  memset(&v9, 0, 0x3FFu);
  printf("input code:");
  scanf("%s", &myinput);
  if ( !firstcheck_4011F0(&myinput) )
  {
    printf("invalid input\n");
    exit(0);
  }
  maincheck_401240(&myinput, &tg);
  Dest = 0;
  memset(&v5, 0, 0x3FFu);
  sprintf(&Dest, "DDCTF{%s}", &tg);             
  if ( !strcmp(&Dest, "DDCTF{reverse+}") )
    printf("You've got it !!! %s\n", &Dest);
  else
    printf("Something wrong. Try again...\n");
  return 0;
}
```

很明显有几个函数来检查输入是否正确。都看一遍。

```c
char __usercall firstcheck_4011F0@<al>(const char *myinput@<esi>)
{
  signed int lens; // eax
  signed int v2; // edx
  int v3; // ecx
  char v4; // al

  lens = strlen(myinput);
  v2 = lens;
  if ( lens && lens % 2 != 1 )                  // 2的倍数位
  {
    v3 = 0;
    if ( lens <= 0 )
      return 1;
    while ( 1 )
    {
      v4 = myinput[v3];
      if ( (v4 < '0' || v4 > '9') && (v4 < 'A' || v4 > 'F') )// 0-9 A-F
        break;
      if ( ++v3 >= v2 )
        return 1;
    }
  }
  return 0;
}
```

myinput的长度需要是2的倍数，且字符控制在0-9和A-F之间。这个函数挺简单的，下一个。

```c
int __usercall maincheck_401240@<eax>(const char *myinput@<esi>, char *tg)
{
  signed int lens; // edi
  signed int i; // edx
  char t_; // bl
  char c; // al
  char v6; // al
  unsigned int v7; // ecx
  char t; // [esp+Bh] [ebp-405h]
  char v10; // [esp+Ch] [ebp-404h]
  char Dst; // [esp+Dh] [ebp-403h]

  lens = strlen(myinput);
  v10 = 0;
  memset(&Dst, 0, 0x3FFu);
  i = 0;
  if ( lens > 0 )//下面主要进行输入的转换，将输入的字符串按字面值存储，'0'-->0  ‘A’-->0x10  
  {
    t_ = t;
    do
    {
      c = myinput[i];
      if ( (unsigned __int8)(myinput[i] - '0') > 9u )
      {
        if ( (unsigned __int8)(c - 'A') <= 5u )
          t = c - '7';
      }
      else
      {
        t = myinput[i] - '0';
      }
      v6 = myinput[i + 1];
      if ( (unsigned __int8)(myinput[i + 1] - '0') > 9u )
      {
        if ( (unsigned __int8)(v6 - 'A') <= 5u )
          t_ = v6 - 55;
      }
      else
      {
        t_ = myinput[i + 1] - '0';
      }
      v7 = (unsigned int)i >> 1;
      i += 2;
      *(&v10 + v7) = t_ | 16 * t;
    }
    while ( i < lens );
  }
  return base64_encode_401000(lens / 2, tg);
}
```

一个do-while循环，每次取出输入的一个字符，转成int。如果输入在0-9之内，保留原值(不过这个原值不完全等于之前的了）；否则减去55(ord('7')=55)。然后取第二位，做相同操作。我没看懂这是在干啥，查了大佬wp：

- 可以看到，第一个do/while循环是将每两位用户输入处理成其对应的16进制数值，例如用户输入AD，则结果等于('A'-55) * 0x10 + 'D'-55 = 0xAD，因为A的ASCII为0x65，因此A减去55等于10，相当于是将其变为16进制中A的值，这是需要思考和理解的一点。

我看了一下，还真是，比如print(ord('1')-ord('0'))这个代码结果是1，数字的1。乘上0x10是因为A在“十位”（拿十进制类比的，我也不知道改怎么说）。举个例子，一个数字52，知道个位和十位数字是2和5，那表达这个数字就是5*10+2，高位乘以进率。不过题目中是以位运算来表示的，我真的不懂位运算。下次可以尝试自己放个值实验一下，靠输出猜测作用。

```c
int __cdecl base64_encode_401000(int size, void *tg)
{
  char *v2; // ecx
  int v3; // ebp
  char *v4; // edi
  signed int v5; // esi
  unsigned __int8 v6; // bl
  signed int v7; // esi
  int v8; // edi
  int v9; // edi
  size_t v10; // esi
  void *v11; // edi
  const void *v12; // eax
  unsigned __int8 Dst; // [esp+14h] [ebp-38h]
  unsigned __int8 v15; // [esp+15h] [ebp-37h]
  unsigned __int8 v16; // [esp+16h] [ebp-36h]
  char v17; // [esp+18h] [ebp-34h]
  char v18; // [esp+19h] [ebp-33h]
  char v19; // [esp+1Ah] [ebp-32h]
  char i; // [esp+1Bh] [ebp-31h]
  void *v21; // [esp+1Ch] [ebp-30h]
  char v22; // [esp+20h] [ebp-2Ch]
  void *Src; // [esp+24h] [ebp-28h]
  size_t Size; // [esp+34h] [ebp-18h]
  unsigned int v25; // [esp+38h] [ebp-14h]
  int v26; // [esp+48h] [ebp-4h]

  v3 = size;
  v4 = v2;
  v21 = tg;
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string<char,std::char_traits<char>,std::allocator<char>>(&v22);
  v5 = 0;
  v26 = 0;
  if ( size )
  {
    do
    {
      *(&Dst + v5) = *v4;
      v6 = v15;
      ++v5;
      --v3;
      ++v4;
      if ( v5 == 3 )
      {
        v17 = Dst >> 2;
        v18 = (v15 >> 4) + 16 * (Dst & 3);
        v19 = (v16 >> 6) + 4 * (v15 & 0xF);
        i = v16 & 0x3F;
        v7 = 0;
        do
          std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(
            &v22,
            (unsigned __int8)(a745230189[(unsigned __int8)*(&v17 + v7++)] ^ 0x76));// ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
        while ( v7 < 4 );
        v5 = 0;
      }
    }
    while ( v3 );
    if ( v5 )
    {
      if ( v5 < 3 )
      {
        memset(&Dst + v5, 0, 3 - v5);
        v6 = v15;
      }
      v18 = (v6 >> 4) + 16 * (Dst & 3);
      v17 = Dst >> 2;
      v19 = (v16 >> 6) + 4 * (v6 & 0xF);
      v8 = 0;
      for ( i = v16 & 0x3F; v8 < v5 + 1; ++v8 )
        std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(
          &v22,
          (unsigned __int8)(a745230189[(unsigned __int8)*(&v17 + v8)] ^ 0x76));
      if ( v5 < 3 )
      {
        v9 = 3 - v5;
        do
        {
          std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(&v22, '=');
          --v9;
        }
        while ( v9 );
      }
    }
  }
  v10 = Size;
  v11 = v21;
  memset(v21, 0, Size + 1);
  v12 = Src;
  if ( v25 < 0x10 )
    v12 = &Src;
  memcpy(v11, v12, v10);
  v26 = -1;
  return std::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string<char,std::char_traits<char>,std::allocator<char>>();
}
```

这个函数很复杂，但是看到熟悉的base64编码表，直接不管了，就当他是个base64加密。那全部操作很简单了，myinput经过各种函数后变为tg，tg需要等于reverse+，那我们反过来，base64decode reverse+，然后转为hex编码。

```python
import base64
s='reverse+'
print(base64.b64decode(s))
```

- b'\xad\xeb\xde\xae\xc7\xbe'

不知道python3怎么转hex编码，不过这样flag也出来了。

- ### Flag
  > flag{ADEBDEAEC7BE}