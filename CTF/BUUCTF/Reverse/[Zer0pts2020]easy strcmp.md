# [Zer0pts2020]easy strcmp

[题目地址](https://buuoj.cn/challenges#[Zer0pts2020]easy%20strcmp)

这算不算一个hook？

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  if ( a1 > 1 )
  {
    if ( !strcmp(a2[1], "zer0pts{********CENSORED********}") )
      puts("Correct!");
    else
      puts("Wrong!");
  }
  else
  {
    printf("Usage: %s <FLAG>\n", *a2);
  }
  return 0LL;
}
```

过于祥和，有猫腻！把左边函数栏的函数全看一遍，发现一个可疑的逻辑。

```c
__int64 __fastcall sub_6EA(__int64 a1, __int64 a2)
{
  int i; // [rsp+18h] [rbp-8h]
  int v4; // [rsp+18h] [rbp-8h]
  int j; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; *(_BYTE *)(i + a1); ++i )
    ;
  v4 = (i >> 3) + 1;
  for ( j = 0; j < v4; ++j )
    *(_QWORD *)(8 * j + a1) -= qword_201060[j]; // 觉得可疑是因为qword_20106有数据
  return strcmp(a1, a2);
}
```

然而`sub_6EA`的交叉引用竟然找不到，还好下面一个函数就是hook的逻辑。

```c
int (**sub_795())(const char *s1, const char *s2)
{
  int (**result)(const char *, const char *); // rax

  result = &strcmp;
  strcmp = (__int64 (__fastcall *)(_QWORD, _QWORD))&strcmp;
  off_201028 = sub_6EA;                         // off_201028是strcmp的got表，此举修改got表为sub_6EA，因此main函数调用strcmp时其实是在调用sub_6EA
  return result;
}
```

`sub_6EA`函数便是隐藏的比对逻辑了。我双击`qword_201060`发现是一些数字，便在hex window里拷贝下来，写出了下面的脚本：

```python
data='00 00 00 00 00 00 00 00 42 09 4A 49 35 43 0A 41 F0 19 E6 0B F5 F2 0E 0B 2B 28 35 4A 06 3A 0A 4F 00 00 00 00 00 00 00 00'.split(' ')
#data=data[::-1]
flag='zer0pts{********CENSORED********}'
for i in range(len(flag)):
    print(chr((ord(flag[i])+int(data[i],16))&0xff),end='')
```

挺疑惑的，其他的都行结果中间几个不行。无奈看了[wp](https://blog.csdn.net/m0_71081503/article/details/125938026)，和我的思路差不多，只不过我是一个一个字节复原，wp是按照原程序逻辑分成3段一起复原。注意ida里面hex window的数据不需要倒过来，但是这样合在一起很长的数据就是小端存储的，需要`[::-1]`倒过来。

```python
import binascii
str_1 = "********" #把flag平均分为3份，对应下面数字的三份
str_2 = "CENSORED"
str_3 = "********"
word_1 = [0x410A4335494A0942]
word_2 = [0x0B0EF2F50BE619F0]
word_3 = [0x4F0A3A064A35282B]
bin_1 = binascii.b2a_hex(str_1.encode('ascii')[::-1]) #将分为3份的flag转成byte再转为16进制并倒序
bin_2 = binascii.b2a_hex(str_2.encode('ascii')[::-1])
bin_3 = binascii.b2a_hex(str_3.encode('ascii')[::-1])
j_1 = binascii.a2b_hex(hex(int(bin_1, 16) + word_1[0])[2:])[::-1] #逆向逻辑，加回来再倒序成为正常端序输出
j_2 = binascii.a2b_hex(hex(int(bin_2, 16) + word_2[0])[2:])[::-1]
j_3 = binascii.a2b_hex(hex(int(bin_3, 16) + word_3[0])[2:])[::-1]
print(j_1 + j_2 + j_3)
```

[binascii.b2a_hex](https://docs.python.org/zh-cn/3.8/library/binascii.html)可参照此处。

## Flag
> flag{l3ts_m4k3_4_DETOUR_t0d4y}