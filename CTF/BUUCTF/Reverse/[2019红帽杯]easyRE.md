# [2019红帽杯]easyRE

[题目地址](https://buuoj.cn/challenges#[2019%E7%BA%A2%E5%B8%BD%E6%9D%AF]easyRE)

心甘情愿掉进出题人挖的坑里。

strings界面交叉引用找到了main。

```c
__int64 Main()

{

  __int64 result; // rax

  int i; // [rsp+Ch] [rbp-114h]

  __int64 v2; // [rsp+10h] [rbp-110h]

  __int64 v3; // [rsp+18h] [rbp-108h]

  __int64 v4; // [rsp+20h] [rbp-100h]

  __int64 v5; // [rsp+28h] [rbp-F8h]

  __int64 v6; // [rsp+30h] [rbp-F0h]

  __int64 v7; // [rsp+38h] [rbp-E8h]

  __int64 v8; // [rsp+40h] [rbp-E0h]

  __int64 v9; // [rsp+48h] [rbp-D8h]

  __int64 v10; // [rsp+50h] [rbp-D0h]

  __int64 v11; // [rsp+58h] [rbp-C8h]

  char v12[13]; // [rsp+60h] [rbp-C0h] BYREF

  char v13[4]; // [rsp+6Dh] [rbp-B3h] BYREF

  char v14[19]; // [rsp+71h] [rbp-AFh] BYREF

  char input[32]; // [rsp+90h] [rbp-90h] BYREF

  int v16; // [rsp+B0h] [rbp-70h]

  char v17; // [rsp+B4h] [rbp-6Ch]

  char v18[72]; // [rsp+C0h] [rbp-60h] BYREF

  unsigned __int64 v19; // [rsp+108h] [rbp-18h]



  v19 = __readfsqword(0x28u);

  qmemcpy(v12, "Iodl>Qnb(ocy", 12);

  v12[12] = 127;

  qmemcpy(v13, "y.i", 3);

  v13[3] = 127;

  qmemcpy(v14, "d`3w}wek9{iy=~yL@EC", sizeof(v14));

  memset(input, 0, sizeof(input));

  v16 = 0;

  v17 = 0;

  read(0LL, input, 37LL);

  v17 = 0;

  if ( strlen(input) == 36 )

  {

    for ( i = 0; i < (unsigned __int64)strlen(input); ++i )

    {

      if ( (unsigned __int8)(input[i] ^ i) != v12[i] )

      {

        result = 4294967294LL;

        goto LABEL_13;

      }

    }

    printf("continue!");

    memset(v18, 0, 0x40uLL);

    v18[64] = 0;

    read(0LL, v18, 64LL);

    v18[39] = 0;

    if ( strlen(v18) == 39 )

    {

      v2 = Base64Encode(v18);

      v3 = Base64Encode(v2);

      v4 = Base64Encode(v3);

      v5 = Base64Encode(v4);

      v6 = Base64Encode(v5);

      v7 = Base64Encode(v6);

      v8 = Base64Encode(v7);

      v9 = Base64Encode(v8);

      v10 = Base64Encode(v9);

      v11 = Base64Encode(v10);

      if ( !(unsigned int)strcmp(v11, off_6CC090) )

      {

        printf("You found me!!!");

        printf("bye bye~");

      }

      result = 0LL;

    }

    else

    {

      result = 4294967293LL;

    }

  }

  else

  {

    result = 0xFFFFFFFFLL;

  }

LABEL_13:

  if ( __readfsqword(0x28u) != v19 )

    sub_444020();

  return result;

}
```

此题的符号表被完全打乱，只能根据经验和函数内部实现自己猜测着改名。一开始就有一个很明显的异或加密，不过要注意v12，v13和v14是连在一起的，从`strlen(input) == 36`能推测这点。以及`v12[12] = 127;`和`v13[3] = 127;`也要加在异或的字符串中。

```python
data="Iodl>Qnb(ocy\x7fy.i\x7fd`3w}wek9{iy=~yL@EC"
for i in range(len(data)):
    print(chr(ord(data[i])^i),end='')
```

被骗了，输出不是flag，只是告诉了我们flag的格式。继续往下看，把输入读入到v18中，一堆base64encode后与`off_6CC090`比较。找到`off_6CC090`，在线解密，然后得到`https://bbs.pediy.com/thread-254172.htm`。这是告诉我又被坑了？行吧，下面还有啥？没东西了啊？陷入僵局。

双击点进`off_6CC090`，能发现周围还有一些奇怪的字符。继续查找交叉引用，发现新天地。

```c
unsigned __int64 sub_400D35()
{
  unsigned __int64 result; // rax
  unsigned int v1; // [rsp+Ch] [rbp-24h]
  int i; // [rsp+10h] [rbp-20h]
  int j; // [rsp+14h] [rbp-1Ch]
  unsigned int v4; // [rsp+24h] [rbp-Ch]
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  v1 = sub_43FD20(0LL) - qword_6CEE38;
  for ( i = 0; i <= 1233; ++i )
  {
    sub_40F790(v1);
    sub_40FE60();
    sub_40FE60();
    v1 = sub_40FE60() ^ 0x98765432;
  }
  v4 = v1;
  if ( ((unsigned __int8)v1 ^ byte_6CC0A0[0]) == 'f' && (HIBYTE(v4) ^ (unsigned __int8)byte_6CC0A3) == 'g' )
  {
    for ( j = 0; j <= 24; ++j )
      sub_410E90(byte_6CC0A0[j] ^ *((_BYTE *)&v4 + j % 4));
  }
  result = __readfsqword(0x28u) ^ v5;
  if ( result )
    sub_444020();
  return result;
}
```

然而我看了半天没看出来逻辑，虽然也是简单的异或逻辑，`byte_6CC0A0`已知，但是v4是什么呢？无奈去看[wp](https://blog.nowcoder.net/n/f210b150f8874d729efe9040d14d6288)，好吧果然还是要猜。

刚刚那个异或得到的结果说flag前4位是flag，不是废话，因为这里出现了f和g的比较。v4就是v1，`if ( ((unsigned __int8)v1 ^ byte_6CC0A0[0]) == 'f' && (HIBYTE(v4) ^ (unsigned __int8)byte_6CC0A3) == 'g' )`比较了v1的低位和v4的高位（里面的HIBYTE，因为小端存储所以g在高位）与已知内容的异或后的结果。既然v4的高位直接是g了，不妨猜测整个v4的长度就为4，是flag与`byte_6CC0A0`前4位异或的值。接下来for语句中让`byte_6CC0A0`每一位分别与v4循环异或。

```python
data="40 35 20 56 5D 18 22 45 17 2F 24 6E 62 3C 27 54 48 6C 24 6E 72 3C 32 45 5B 00 00 00 00 00 00 00".split(" ")
s='flag'
v4=[]
for i in range(4):
    v4.append(int(data[i],16)^ord(s[i]))
for i in range(25):
    print(chr(int(data[i],16)^v4[i%len(v4)]),end='')
```

最后查找引用能发现`sub_400D35`在fini_array中被调用。忘了，除了init_array（是叫这个吗，有点忘了，总之也是某个array），看来fini_array也能藏东西。

## Flag
- flag{Act1ve_Defen5e_Test}