# Reverse技巧

## IDA使用

终于能用ida了，我等这一天已经等了几个月了。现在就是个纯纯ida萌新，完全不知道怎么用，故记录一下任何在做题时了解到的技巧。

1. f5键显示当前函数的伪代码。如果f5用不了，鼠标点进汇编代码窗口再tab也是可以的。假如当前已经是伪代码状态那tab键就能看到汇编代码。
2. g键是跳转任意地址的快捷键。
3. 伪代码内部双击变量可以查看其在栈上的位置。
4. 进入函数伪代码界面，点击函数名（会出现黄色背景自动选中函数名），然后按x可以找到该函数在其他函数中的引用。或者点击函数名右键->Jump to xref也是可以的。函数中的变量名也可以用这种方式找引用。
5. 点进一个函数，无论是汇编还是伪代码状态下，都可以在窗口底部看见当前函数的地址。
6. 选中一个数字类型数据再右键，可以选择数据显示的进制或者方式（比如10进制，16进制等）。
7. 菜单栏View->Open subviews可以打开很多有用的窗口，比如字符串，16进制等。
8. 右键变量可以重命名变量。
9. 想要提取数据，例如byte_array时，可以先双击变量进入data段，再右键变量名选择Jump in a new hex window,选中要复制的内容，shift+e就能提取了。我一般是选择hex string（spaced），粘贴到python里再split成数组。
10. 遇到想要改名的函数时，右键函数名->Rename global item。想改变量名也差不多，都是右键，点Rename就行了。
11. 选中一行代码，右键->Edit comment可以添加注释。或者选中一行代码后直接按`/`键。
12. ida中的数字有时候会带类型后缀。比如10h表示16进制的0x10，0i64表示int_64下的0。做题时注意区分，很容易把16进制看漏导致数据出现问题。
13. 在字符串窗口看见一个字符串并想找其引用时，先双击字符串，就会进入到另一个窗口，可以在字符串右侧看见DATA XREF。最后双击DATA XREF显示的函数名即可。

## Reverse技巧

1. 地址差值混淆。特征：程序先是取了两个地址a和b的差值，如c=a-b。程序后面又b+c取值。此时就要意识到现在取的是a的值。
2. 逆向时多在代码旁写注释，非常有助于分析逻辑。不要觉得多此一举或者懒得写，这个方法可以让小白更有头绪，大佬分析更快。
3. c++逆向中，接收输入和输出函数名可能不明显，但我们无需分析函数本身。接收输入认准`std::cin`,打印内容认准`std::cout`，特别是`std::cin`，跟它在一次出现的变量极有可能是用户输入，是逆向的主要目标。
4. 逆向要善于看整体。虽然说逆向真的就是字面意思——反着来，但反的是整体而不是机械式地倒着来。比如异或一般是一个for循环里面`^`，整个for循环周围的变量算作一个整体，也就是一个步骤。一个加密算法也是一个步骤，等等。如果是先加密算法再异或，那逆向的时候肯定是异或再加密算法，不难看出重点是区分异或和加密算法以及种种操作。区分后再着手细节，比如单个算法怎么逆。
5. 连着的变量可能会有间接引用。比如for循环中利用地址引用一个数组或类似数组的变量，而那个变量明显又没有那么长。这时候for循环中取到的值可能会有相邻的变量。比如(下面是个伪python代码）：

```
v30=array[5]
v31=x
v32=x
for i in range(7):
    v30[i]=xxx
```

示例中v30长度为5，然而for循环却取了7个元素。这时相邻的元素v31和v32就会被取到。ida中可能出现这种间接取变量的变量名都是挨着的，31，32，33或者别的一串数字。

6. xxtea加密算法识别。以下给出反编译得到的xxtea加密算法内容(c++)，其他的题反编译后看到类似结构的可以直接套用xxtea解密脚本。

```c++
_BYTE *__fastcall xxteaEncrypt(__int64 a1, unsigned __int64 a2, unsigned __int8 *a3, unsigned __int64 *a4)

{

  unsigned __int64 *v4; // r13

  unsigned __int64 v8; // rdi

  size_t v9; // rcx

  _DWORD *v10; // rax

  _DWORD *v11; // r15

  unsigned __int64 v12; // r14

  unsigned __int64 v13; // rdi

  unsigned __int64 i; // r9

  int v15; // edx

  _DWORD *v16; // r8

  char v17; // cl

  _DWORD *v18; // r12

  int v19; // ecx

  int v20; // eax

  int v21; // ecx

  int v22; // eax

  int v23; // ecx

  int v24; // eax

  int v25; // ecx

  int v26; // eax

  unsigned int v27; // ebp

  __int64 v28; // rcx

  unsigned int v29; // er10

  unsigned int v30; // eax

  __int64 v31; // r9

  unsigned int *v32; // rbx

  __int64 v33; // r11

  _DWORD *v34; // rax

  __int64 v35; // rsi

  __int64 v36; // r14

  char v37; // r13

  unsigned int v38; // er8

  __int64 v39; // rcx

  unsigned __int64 v40; // rbx

  size_t v41; // rcx

  _BYTE *v42; // rax

  _BYTE *v43; // rsi

  _BYTE *result; // rax

  char v45; // [rsp+20h] [rbp-58h]

  __int64 v46; // [rsp+28h] [rbp-50h]

  unsigned __int64 v47; // [rsp+30h] [rbp-48h]

  unsigned int v48; // [rsp+88h] [rbp+10h]

  unsigned __int64 *v49; // [rsp+98h] [rbp+20h]



  v49 = a4;

  v4 = a4;

  if ( !a2 )

    return 0i64;

  v8 = a2 >> 2;

  if ( (a2 & 3) != 0 )

    v8 = (a2 >> 2) + 1;

  v9 = v8 + 1;

  if ( v8 == -1i64 )

    v9 = -1i64;

  v10 = calloc(v9, 4ui64);

  v11 = v10;

  if ( !v10 )

    return 0i64;

  v12 = v8 + 1;

  v10[v8] = a2;

  v13 = 0i64;

  v47 = v12;

  for ( i = 0i64; i < a2; *v16 |= v15 << (8 * v17) )

  {

    v15 = *(unsigned __int8 *)(i + a1);

    v16 = &v10[i >> 2];

    v17 = i++ & 3;

  }

  v18 = calloc(4ui64, 4ui64);

  if ( v18 )

  {

    v19 = a3[7] << 8;

    v20 = a3[6];

    *v18 |= *a3 | ((a3[1] | (*((unsigned __int16 *)a3 + 1) << 8)) << 8);

    v21 = a3[4] | ((a3[5] | ((v20 | v19) << 8)) << 8);

    v22 = a3[10];

    v18[1] |= v21;

    v23 = a3[8] | ((a3[9] | ((v22 | (a3[11] << 8)) << 8)) << 8);

    v24 = a3[14];

    v18[2] |= v23;

    v25 = a3[13] | ((v24 | (a3[15] << 8)) << 8);

    v26 = a3[12];

    v27 = 0;

    v18[3] |= v26 | (v25 << 8);

    v28 = (unsigned int)(v12 - 1);

    v29 = v11[v28];

    v30 = 0x34 / (unsigned int)v12 + 6;

    v31 = v28;

    v45 = v12 - 1;

    v46 = v28;

    if ( (_DWORD)v12 != 1 && 0x34 / (unsigned int)v12 != -6 )

    {

      do

      {

        v32 = v11 + 1;

        v27 -= 1640531527;

        v48 = v30 - 1;

        v33 = 0i64;

        v34 = v11;

        v35 = (v27 >> 2) & 3;

        v36 = v31;

        v37 = v28;

        do

        {

          v38 = *v32++;

          ++v34;

          v39 = v35 ^ v33++ & 3;

          *(v34 - 1) += ((v27 ^ v38) + (v29 ^ v18[v39])) ^ (((16 * v29) ^ (v38 >> 3)) + ((v29 >> 5) ^ (4 * v38)));

          v29 = *(v34 - 1);

          --v36;

        }

        while ( v36 );

        v31 = v46;

        LOBYTE(v28) = v45;

        v30 = v48;

        v11[v46] += ((v27 ^ *v11) + (v29 ^ v18[v35 ^ v37 & 3])) ^ (((4 * *v11) ^ (v29 >> 5)) + ((*v11 >> 3) ^ (16 * v29)));

        v29 = v11[v46];

      }

      while ( v48 );

      v12 = v47;

      v4 = v49;

    }

    v40 = 4 * v12;

    v41 = 4 * v12 + 1;

    if ( 4 * v12 == -1i64 )

      v41 = -1i64;

    v42 = malloc(v41);

    v43 = v42;

    if ( v40 )

    {

      do

      {

        v42[v13] = v11[v13 >> 2] >> (8 * (v13 & 3));

        ++v13;

      }

      while ( v13 < v40 );

    }

    v42[4 * v12] = 0;

    *v4 = v40;

    free(v11);

    free(v18);

    result = v43;

  }

  else

  {

    free(v11);

    result = 0i64;

  }

  return result;

}
```

特征为一堆位操作。附xxtea python实现,[来源](https://www.cnblogs.com/DirWang/p/12198526.html)。

```python
import struct

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


def encrypt(str, key):
    if str == '': return str
    v = _str2long(str, True)
    k = _str2long(key.ljust(16, b"\0"), False)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    sum = 0
    q = 6 + 52 // (n + 1)
    while q > 0:
        sum = (sum + _DELTA) & 0xffffffff
        e = sum >> 2 & 3
        for p in  range(n):
            y = v[p + 1]
            v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
            z = v[p]
        y = v[0]
        v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff
        z = v[n]
        q -= 1
    return _long2str(v, False)


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
    return _long2str(v, True)
```

6. 识别base64编码。如果你在一个看起来很复杂的函数中发现引用了这样的字符串:`A-Za-z0-9+/=`，即全大写小写字母加数字和+/=这三个符号，注意可能是base64编码，无需逆向，找个解码网站就好了。
7. 识别迷宫题地图大小。因为迷宫题的地图有可能是一个平铺开的字符串，而运行时走的迷宫却是二维，这时判断迷宫是怎样摆的很重要。例题[maze](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/5%E7%BA%A7/Reverse/maze.md)中一段代码如下：

```c
if (s__*******_*_****_*_****_*_***_*#_*_00601060[(long)(int)local_28 * 8 + (long)local_28._4_4_]
        == '#') {
      __s = "Congratulations!";
      goto LAB_00400810;
    }
```

注意到`local_28 * 8`。很多正方形的迷宫题都是这个套路，先找到终点，然后看乘以了什么数字。这里是8，因此迷宫为8*8。