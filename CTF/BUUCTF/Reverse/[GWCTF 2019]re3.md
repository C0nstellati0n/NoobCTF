# [GWCTF 2019]re3

[题目地址](https://buuoj.cn/challenges#[GWCTF%202019]re3)

第一次使用idc脚本。

下面的程序都是经过idc处理后的内容了，把函数解密后逻辑分析着不难，只要能分辨出这是个AES加密算法。日常先看main函数。

```c
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  int i; // [rsp+8h] [rbp-48h]
  char s[40]; // [rsp+20h] [rbp-30h] BYREF
  unsigned __int64 v5; // [rsp+48h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  __isoc99_scanf("%39s", s);
  if ( (unsigned int)strlen(s) != 32 )
  {
    puts("Wrong!");
    exit(0);
  }
  mprotect(&dword_400000, 0xF000uLL, 7);
  for ( i = 0; i <= 223; ++i )
    *((_BYTE *)sub_402219 + i) ^= 0x99u;
  sub_40207B(&unk_603170);
  sub_402219(s);
  JUMPOUT(0x4021F5LL);
}
```

又出现了for循环改函数字节。原本的程序被加密了，运行前才解密出来，防逆向。点进` `还发现函数也不让动态调试dump出原文件。都是只能防老实人和菜狗的防御（啊我就是），看[wp](https://www.cnblogs.com/Mayfly-nymph/p/12829168.html)了解到了ida自带的[idc脚本](https://blog.csdn.net/CharlesGodX/article/details/84866365)。

首先去到`sub_402219`的text段，选中这里全部的数据，按D转为数据形式。这步很重要，少了后面就会莫名其妙反编译不出来伪代码。然后打开菜单栏->File->Script command(shift+F2)，运行下面的代码：

```c
#include <idc.idc>

static main()
{
    //auto关键字定义变量
    auto addr = 0x402219;
    auto i;
    for(i = 0; i <= 223; ++i){
        PatchByte(addr+i,Byte(addr+i)^0x99);
    }
}
```

代码运行完毕没有提示，别按多了。再次查看`sub_402219`处的数据就会发现变了，继续选中那些数据，右键->Analyze selected area->Force，现在这些数据就应该被反编译出来了。选中反编译完成后的内容，p键制作函数。此时就能看见函数的伪代码了。

```c
__int64 __fastcall sub_402219(__int64 a1)
{
  unsigned int v2; // [rsp+18h] [rbp-D8h]
  int i; // [rsp+1Ch] [rbp-D4h]
  char v4[200]; // [rsp+20h] [rbp-D0h] BYREF
  unsigned __int64 v5; // [rsp+E8h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  sub_400A71(v4, &unk_603170);
  sub_40196E(v4, a1);
  sub_40196E(v4, a1 + 16);
  v2 = 1;
  for ( i = 0; i <= 31; ++i )
  {
    if ( *(_BYTE *)(i + a1) != byte_6030A0[i] )
      v2 = 0;
  }
  return v2;
}
```

`sub_400A71`和`sub_40196E`函数都是AES加密算法，(特征为第一个函数生成轮密钥，后面调用相同的函数分别加密一个内容的低16位和高16位）。`unk_603170`是密钥。接下来的for循环中比对加密结果是否与`byte_6030A0`一致，那么`byte_6030A0`就是密文。AES知道密文和密钥就能解密出原文了，不过密钥是什么呢？回到main函数，发现`unk_603170`还在`sub_40207B`出现过，是其参数。

```c
unsigned __int64 __fastcall sub_40207B(__int64 a1)
{
  char v2[16]; // [rsp+10h] [rbp-50h] BYREF
  __int64 v3; // [rsp+20h] [rbp-40h] BYREF
  __int64 v4; // [rsp+30h] [rbp-30h] BYREF
  __int64 v5; // [rsp+40h] [rbp-20h] BYREF
  unsigned __int64 v6; // [rsp+58h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  sub_401CF9(&unk_603120, 64LL, v2);
  sub_401CF9(&unk_603100, 20LL, &v3);
  sub_401CF9(&unk_6030C0, 53LL, &v4);
  sub_401CF9(&dword_4025C0, 256LL, &v5);
  sub_401CF9(v2, 64LL, a1);
  return __readfsqword(0x28u) ^ v6;
}
```

这个函数具体干什么就不用细看了，只需要判断其是否引用了输入。发现没有，那就可以直接动调出来，无需逆向。动调得到是`BC0AADC0147C5ECCE0B140BC9C51D52B46B2B9434DE5324BAD7FB4B39CDB4B5B`。使用python进行解密([来源](https://blog.csdn.net/weixin_52369224/article/details/121255693))。

```python
from Crypto.Cipher import AES
from Crypto.Util.number import *
key = long_to_bytes(0xcb8d493521b47a4cc1ae7e62229266ce) #密钥
mi = long_to_bytes(0xbc0aadc0147c5ecce0b140bc9c51d52b46b2b9434de5324bad7fb4b39cdb4b5b) #密文
lun = AES.new(key, mode=AES.MODE_ECB)
flag = lun.decrypt(mi)
print(flag)
```

## Flag
> flag{924a9ab2163d390410d0a1f670}