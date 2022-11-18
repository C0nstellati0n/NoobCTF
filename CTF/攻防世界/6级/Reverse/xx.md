# xx

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=db0bfa07-7d5f-4f8f-b19f-25d07a6ff4c8_2&task_category_id=4)

纸老虎也是老虎啊！

main函数多多少少有点吓人。

```c++
int __cdecl main(int argc, const char **argv, const char **envp)

{

  unsigned __int64 v3; // rbx

  __int64 inputLength; // rax

  __int128 *key; // rax

  __int64 code; // r11

  __int128 *v7; // r14

  int v8; // edi

  __int128 *ptr_key; // rsi

  char c; // r10

  int v11; // edx

  __int64 v12; // r8

  unsigned __int64 codeLength; // rcx

  __int64 v14; // rcx

  unsigned __int64 v15; // rax

  unsigned __int64 i; // rax

  _BYTE *encrypt_result; // rax

  size_t v18; // rsi

  _BYTE *encrypt_result2; // rbx

  _BYTE *result_str; // r9

  int v21; // er11

  char *v22; // r8

  __int64 v23; // rcx

  char v24; // al

  __int64 v25; // r9

  __int64 index; // rdx

  __int64 v27; // rax

  size_t Size; // [rsp+20h] [rbp-48h] BYREF

  __int128 v30; // [rsp+28h] [rbp-40h] BYREF

  int v31; // [rsp+38h] [rbp-30h]

  int v32; // [rsp+3Ch] [rbp-2Ch]

  int inputKey[4]; // [rsp+40h] [rbp-28h] BYREF

  int v34; // [rsp+50h] [rbp-18h]



  *(_OWORD *)inputKey = 0i64;

  v34 = 0;

  GetInput(std::cin, (__int64)argv, (__int64)inputKey);

  v3 = -1i64;

  inputLength = -1i64;

  do

    ++inputLength;

  while ( *((_BYTE *)inputKey + inputLength) );

  if ( inputLength != 19 )

  {

    PrintSth(std::cout, "error\n");

    _exit((int)inputKey);

  }

  key = (__int128 *)operator new(5ui64);        // 这里可能是new一个字符串类或者别的什么类似的用来装key的东西

  code = *(_QWORD *)&Code;

  v7 = key;

  v8 = 0;

  ptr_key = key;

  do

  {

    c = *((_BYTE *)ptr_key + (char *)inputKey - (char *)key);// 换个顺序看，ptr_key-key+input,ptr_key和key上面赋值来看是一样的，那么实际上仅是取input的每一位

    v11 = 0;

    *(_BYTE *)ptr_key = c;                      // 把input的前4位放入key中

    v12 = 0i64;

    codeLength = -1i64;

    do

      ++codeLength;

    while ( *(_BYTE *)(code + codeLength) );

    if ( codeLength )

    {

      do

      {

        if ( c == *(_BYTE *)(code + v12) )      // 如果我们输入的字符在code里的话，v11就不可能大于等于codeLength

          break;

        ++v11;

        ++v12;

      }

      while ( v11 < codeLength );

    }

    v14 = -1i64;

    do

      ++v14;

    while ( *(_BYTE *)(code + v14) );

    if ( v11 == v14 )                           // 因此这里的判断结合起来看就是我们输入的字符必须都在code里

      _exit(code);

    ptr_key = (__int128 *)((char *)ptr_key + 1);// 这里ptr_key自增1。现在结合最上面那个ptr_key-key+input看就很清楚了

  }

  while ( (char *)ptr_key - (char *)key < 4 );  // key长4位

  *((_BYTE *)key + 4) = 0;

  do

    ++v3;

  while ( *((_BYTE *)inputKey + v3) );

  v15 = 0i64;

  v30 = *v7;                                    // v7在上面的逻辑中没有改变，还是key的拷贝

  while ( *((_BYTE *)&v30 + v15) )

  {

    if ( !*((_BYTE *)&v30 + v15 + 1) )

    {

      ++v15;

      break;

    }

    if ( !*((_BYTE *)&v30 + v15 + 2) )

    {

      v15 += 2i64;

      break;

    }

    if ( !*((_BYTE *)&v30 + v15 + 3) )

    {

      v15 += 3i64;

      break;

    }

    v15 += 4i64;

    if ( v15 >= 0x10 )

      break;

  }

  for ( i = v15 + 1; i < 0x10; ++i )

    *((_BYTE *)&v30 + i) = 0;                   // 这里加上上面那个while循环都是在填充v30（还是key的拷贝）的末尾为0，一直到长度16

  encrypt_result = xxteaEncrypt((__int64)inputKey, v3, (unsigned __int8 *)&v30, &Size);

  v18 = Size;

  encrypt_result2 = encrypt_result;

  result_str = operator new(Size);

  v21 = 1;

  *result_str = encrypt_result2[2];

  v22 = result_str + 1;

  result_str[1] = *encrypt_result2;             // 一堆替换

  result_str[2] = encrypt_result2[3];

  result_str[3] = encrypt_result2[1];

  result_str[4] = encrypt_result2[6];

  result_str[5] = encrypt_result2[4];

  result_str[6] = encrypt_result2[7];

  result_str[7] = encrypt_result2[5];

  result_str[8] = encrypt_result2[10];

  result_str[9] = encrypt_result2[8];

  result_str[10] = encrypt_result2[11];

  result_str[11] = encrypt_result2[9];

  result_str[12] = encrypt_result2[14];

  result_str[13] = encrypt_result2[12];

  result_str[14] = encrypt_result2[15];

  result_str[15] = encrypt_result2[13];

  result_str[16] = encrypt_result2[18];

  result_str[17] = encrypt_result2[16];

  result_str[18] = encrypt_result2[19];

  result_str[19] = encrypt_result2[17];

  result_str[20] = encrypt_result2[22];

  result_str[21] = encrypt_result2[20];

  result_str[22] = encrypt_result2[23];
  // for的第一个字句和这个for循环干的事情一点关系也没有，仍然是上面替换的一部分。索引是v21，v18是整个字符串的长度
  for ( result_str[23] = encrypt_result2[21]; v21 < v18; ++v22 )// v21上面的初始赋值是1

  {

    v23 = 0i64;

    if ( v21 / 3 > 0 )

    {

      v24 = *v22;                               // v22=result_str+1。因为v22在自增且初始值为result_str[1]，粗略看为在遍历取result_str值。

      do

      {

        v24 ^= result_str[v23++];  // v23是while循环里的索引

        *v22 = v24;

      }

      while ( v23 < v21 / 3 ); // do-while执行次数取决于v21是3的多少倍。v23每次for循环开始时都设为0，异或完自增1。而v21只有是3的倍数时才会进入if分支，意味着v21/3最小是1，然后是2，3……这里代表循环v21/3次。

    }

    ++v21;

  }

  *(_QWORD *)&v30 = 0xC0953A7C6B40BCCEui64;

  v25 = result_str - (_BYTE *)&v30;             // 注意v25是result_str和v30地址的差值

  *((_QWORD *)&v30 + 1) = 0x3502F79120209BEFi64;

  index = 0i64;

  v31 = -939386845;

  v32 = -95004953;

  do

  {                                             // 遍历比较v30和result_str

    if ( *((_BYTE *)&v30 + index) != *((_BYTE *)&v30 + index + v25) )// 这里看整体，把v30+index看成简单的遍历操作。v30+index+v25其实是在遍历result_str，因为v25是result_str和v30地址的差值

      _exit(v8 * v8);

    ++v8;

    ++index;

  }

  while ( index < 24 );

  v27 = PrintSth(std::cout, "You win!");

  std::ostream::operator<<(v27, sub_1400017F0);

  return 0;

}
```

不过分析下来会发现逻辑并不是特别难逆向（问题是我不跟着[wp](https://www.cnblogs.com/DirWang/p/12198526.html)根本捋不清逻辑）。重要的东西已经写在注释里了，这里再捋一遍。

首先获取用户输入，将输入的前4位作为key，组成key的字符必须在code中，长4位。接着用0填充key到16位，进行xxtea加密。这里需要点进xxtea函数内部看一下，通过函数特征识别出xxtea加密算法，然后网上找个解密脚本就得了。这个函数内部十分复杂，然而识别出加密算法后就能直接套用脚本，逆向的难度骤减。接下来的一堆替换倒过来不难，眼力好就行。

最后的那个for循环异或有点混淆的成分。它干的事情倒也不难，我先把exp放出来，对着逆向再结合我写的注释就能理解了。

```python
import struct
from Crypto.Util.number import *
_DELTA = 0x9E3779B9


def _long2str(v, w):
    n = (len(v) - 1) << 2
    if w:
        m = v[-1]
        if (m < n - 3) or (m > n): return ''
        n = m
    s = struct.pack('<%iL' % len(v), *v)
    return s[0:n] if w else s


def _str2long(s, w):
    n = len(s)
    m = (4 - (n & 3) & 3) + n
    s = s.ljust(m, b"\0")
    v = list(struct.unpack('<%iL' % (m >> 2), s))
    if w: v.append(n)
    return v

def decrypt(str, key):
    if str == '': return str
    v = _str2long(str, False)
    k = _str2long(key.ljust(16, b"\0"), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    q = 6 + 52 // (n + 1)
    sum = (q * _DELTA) & 0xffffffff
    while (sum != 0):
        e = sum >> 2 & 3
        for p in range(n, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            y = v[p]
        z = v[n]
        v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
        y = v[0]
        sum = (sum - _DELTA) & 0xffffffff
    return _long2str(v,True)
tg=[0xCE, 0xBC, 0x40, 0x6B, 0x7C, 0x3A, 0x95, 0xC0, 0xEF, 0x9B, 0x20, 0x20, 0x91, 0xF7, 0x02, 0x35,
    0x23, 0x18, 0x02, 0xC8, 0xE7, 0x56, 0x56, 0xFA ]
order=[2,0,3,1,6,4,7,5,10,8,11,9,14,12,15,13,18,16,19,17,22,20,23,21]
flag=[0]*24
for i in range(23,-1,-1):
    for j in range(i//3):
        tg[i]^=tg[j]
print('逆异或操作后：'+' '.join(map(hex,tg)))
for i in range(24):
    flag[order[i]]=tg[i]
print('逆加密字符串替换后：'+' '.join(map(hex,flag)))
x=decrypt(bytes(flag),'flag'.encode())
print(x)
```

tg是v30，&v30+1，v31和v32（转hex后）的值，此处是一个相邻地址间接取值。因为是小端，所以要倒着读。order复原替换加密，最后就是xxtea解密了。

## Flag
> flag{CXX_and_++tea}